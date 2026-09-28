from __future__ import annotations

import contextlib
import copy
import hmac
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = ROOT / "provider/backs_provider.py"


def fixture_env(home: Path) -> dict[str, str]:
    return {"HOME": str(home), "PATH": os.defpath, "LANG": "C.UTF-8",
            "TMPDIR": str(home), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"}


def fixture_project(path: Path) -> None:
    core = path / "backend/core"
    core.mkdir(parents=True)
    (core / "__init__.py").write_text("")
    (core / "env_loader.py").write_text(
        "import os\n"
        "def load_runtime_env(*, override=False, repo_root=None):\n"
        "    for file in (repo_root / 'backend/.env', repo_root / '.env'):\n"
        "        if file.is_file():\n"
        "            for line in file.read_text().splitlines():\n"
        "                if '=' in line:\n"
        "                    k, v = line.split('=', 1)\n"
        "                    os.environ.setdefault(k, v)\n")
    (core / "env_utils.py").write_text(
        "import os\n"
        "def env_secret_text(name, default='', *, aliases=(), **kwargs):\n"
        "    return next((os.environ[k] for k in (name, *aliases) if os.environ.get(k)), default)\n")
    (path / ".env").write_text("OLLAMA_API_KEY=fixture-only-key\n")


class ProviderControlTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.project = self.home / "project"
        fixture_project(self.project)
        env = fixture_env(self.home)
        env["BACKS_PROJECT_ROOT"] = str(self.project)
        patch = mock.patch.dict(os.environ, env, clear=True)
        patch.start()
        self.addCleanup(patch.stop)
        spec = importlib.util.spec_from_file_location("fixture_provider", CONTROLLER)
        self.p = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.p)
        self.profile = self.p.load_profile()
        self.catalog = sorted({m for row in self.profile["roles"].values() for m in row})
        self.selected, _ = self.p.resolve_lineup(self.profile, self.catalog)
        self.local_path = self.project / ".claude/settings.local.json"

    def patch_requests(self, fail=False):
        stack = contextlib.ExitStack()
        stack.enter_context(mock.patch.object(self.p, "helper_key", return_value="fixture-only-key"))
        stack.enter_context(mock.patch.object(self.p, "fetch_catalog", return_value=self.catalog))
        self.verify = stack.enter_context(mock.patch.object(self.p, "verify_messages",
            side_effect=self.p.ProviderError("Fixture auth failure") if fail else None))
        return stack

    def test_activation_neutralizes_stale_auth_in_both_settings_scopes(self):
        settings = {"env": {"KEEP": "yes", "ANTHROPIC_AUTH_TOKEN": "stale-placeholder"}, "hooks": {"kept": []}}
        state = {}
        self.local_path.parent.mkdir(parents=True)
        self.local_path.write_text(json.dumps({"env": {"CUSTOM": "yes", "ANTHROPIC_API_KEY": "stale-placeholder"}}))
        with self.patch_requests():
            self.p.activate_ollama(settings, state)
        for path in (self.p.CLAUDE_SETTINGS, self.local_path):
            value = json.loads(path.read_text())
            for key in ("ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN"):
                self.assertEqual("", value["env"][key])
            self.assertIn("backs-ollama-key", value["apiKeyHelper"])
            self.assertFalse("fixture-only-key" in path.read_text())
        self.assertTrue(settings["hooks"] == {"kept": []})
        self.assertEqual(len(self.catalog), state["catalog_size"])
        self.verify.assert_called_once()

    def test_401_preflight_leaves_all_settings_and_state_untouched(self):
        self.p.CLAUDE_SETTINGS.parent.mkdir()
        self.p.CLAUDE_SETTINGS.write_text('{"env":{"KEEP":"yes"}}\n')
        before = self.p.CLAUDE_SETTINGS.read_bytes()
        with self.patch_requests(fail=True), self.assertRaises(self.p.ProviderError):
            self.p.activate_ollama({"env": {"KEEP": "yes"}}, {})
        self.assertTrue(self.p.CLAUDE_SETTINGS.read_bytes() == before)
        self.assertFalse(self.p.STATE_FILE.exists())
        self.assertFalse(self.local_path.exists())

    def test_round_trip_restores_owned_keys_but_preserves_other_edits(self):
        settings = {"env": {"KEEP": "yes", "ANTHROPIC_AUTH_TOKEN": "prior-placeholder"}, "apiKeyHelper": "prior-helper"}
        original = copy.deepcopy(settings)
        state = {}
        self.local_path.parent.mkdir(parents=True)
        local_original = {"env": {"CUSTOM": "yes", "ANTHROPIC_BASE_URL": "prior-placeholder"}}
        self.local_path.write_text(json.dumps(local_original))
        credentials = self.home / ".claude/.credentials.json"
        credentials.parent.mkdir(exist_ok=True)
        credentials.write_text("fixture-oauth-must-not-change")
        with self.patch_requests():
            self.p.activate_ollama(settings, state)
        settings["new_preference"] = 5
        self.p.activate_claude(settings, state)
        original["new_preference"] = 5
        self.assertTrue(original == json.loads(self.p.CLAUDE_SETTINGS.read_text()))
        self.assertTrue(local_original == json.loads(self.local_path.read_text()))
        self.assertTrue(credentials.read_text() == "fixture-oauth-must-not-change")
        self.assertTrue((self.project / ".env").read_text() == "OLLAMA_API_KEY=fixture-only-key\n")

    def test_second_activation_does_not_replace_native_baseline(self):
        settings = {"env": {"KEEP": "yes"}}
        state = {}
        with self.patch_requests():
            self.p.activate_ollama(settings, state)
            before = copy.deepcopy(state["baseline"])
            self.p.activate_ollama(settings, state)
        self.assertTrue(before == state["baseline"])

    def test_old_baseline_does_not_delete_a_newer_unowned_key(self):
        settings = {"env": {"CLAUDE_CODE_OAUTH_TOKEN": "fixture-prior"}}
        self.p.restore_snapshot(settings, {"env": {}, "top": {}})
        self.assertTrue(settings["env"]["CLAUDE_CODE_OAUTH_TOKEN"] == "fixture-prior")

    def test_claude_without_baseline_does_not_delete_authentication(self):
        settings = {"env": {"ANTHROPIC_API_KEY": "prior-placeholder"}}
        original = copy.deepcopy(settings)
        self.p.activate_claude(settings, {})
        self.assertTrue(settings == original)

    def test_saved_project_is_found_without_a_shell_override(self):
        self.p.PROJECT_FILE.parent.mkdir(parents=True)
        self.p.PROJECT_FILE.write_text(str(self.project))
        with mock.patch.dict(os.environ, fixture_env(self.home), clear=True), mock.patch.object(Path, "cwd", return_value=self.home):
            self.assertEqual(self.project, self.p.find_backs_project_root())

    def test_bad_explicit_project_does_not_silently_load_other_keys(self):
        with mock.patch.dict(os.environ, {"BACKS_PROJECT_ROOT": str(self.home / "absent")}), self.assertRaises(self.p.ProviderError):
            self.p.find_backs_project_root()

    def test_http_401_body_and_credential_are_never_in_error_text(self):
        error = urllib.error.HTTPError("https://ollama.com/v1/messages", 401, "fixture-sensitive-text", {}, io.BytesIO(b"fixture-sensitive-text"))
        with mock.patch.object(self.p.urllib.request, "build_opener") as build:
            build.return_value.open.side_effect = error
            with self.assertRaises(self.p.ProviderError) as caught:
                self.p.request_json("https://ollama.com/v1/messages", "fixture-sensitive-text", {})
        self.assertNotIn("fixture-sensitive-text", str(caught.exception))
        self.assertIn("401", str(caught.exception))

    def test_messages_check_uses_post_messages_not_catalog(self):
        payload = {"type": "message", "role": "assistant", "content": [{"type": "text", "text": "OK"}]}
        with mock.patch.object(self.p, "request_json", return_value=payload) as request:
            self.p.verify_messages(self.profile, self.selected, "fixture-key")
        self.assertEqual(len(set(self.selected.values())), request.call_count)
        for call in request.call_args_list:
            self.assertTrue(call.args[0].endswith("/v1/messages"))
            self.assertFalse(call.args[2]["stream"])
            self.assertEqual(64, call.args[2]["max_tokens"])

    def test_empty_assistant_content_does_not_pass_inference_check(self):
        with mock.patch.object(self.p, "request_json", return_value={"type": "message", "role": "assistant", "content": []}), self.assertRaises(self.p.ProviderError):
            self.p.verify_messages(self.profile, self.selected, "fixture-key")

    def test_nonofficial_credential_destination_is_rejected(self):
        with mock.patch.dict(os.environ, {"BACKS_OLLAMA_BASE_URL": "https://example.invalid"}), self.assertRaises(self.p.ProviderError):
            self.p.endpoint(self.profile)

    def test_endpoint_with_embedded_credentials_is_rejected(self):
        with mock.patch.dict(os.environ, {"BACKS_OLLAMA_BASE_URL": "https://fixture:fixture@ollama.com"}), self.assertRaises(self.p.ProviderError):
            self.p.endpoint(self.profile)

    def test_cloud_policy_is_not_overridden(self):
        with mock.patch.dict(os.environ, {"CLAUDE_CODE_USE_VERTEX": "1"}), self.assertRaises(self.p.ProviderError):
            self.p.check_policy(self.project)

    def test_partial_config_write_failure_rolls_back_previous_writes(self):
        first, second = self.home / "first.json", self.home / "second.json"
        first.write_text('{"keep":1}')
        original = self.p.atomic_json_write
        def fail(path, payload, mode=0o600):
            if path == second:
                raise OSError("fixture-write-error")
            return original(path, payload, mode)
        with mock.patch.object(self.p, "atomic_json_write", side_effect=fail), self.assertRaises(OSError):
            self.p.commit_changes({first: {"changed": 2}, second: {"new": 3}})
        self.assertTrue(json.loads(first.read_text()) == {"keep": 1})
        self.assertFalse(second.exists())

    def test_fallbacks_are_resolved_from_available_catalog(self):
        available = ["kimi-k2.7-code", "nemotron-3-ultra", "glm-5.3", "qwen3.5"]
        selected, fallbacks = self.p.resolve_lineup(self.profile, available)
        self.assertTrue(set(selected.values()) <= set(available))
        self.assertEqual("nemotron-3-ultra", selected["opus"])

    def test_catalog_fixture_cannot_bypass_messages_preflight(self):
        with self.patch_requests():
            with mock.patch.dict(os.environ, {"BACKS_OLLAMA_CATALOG_FILE": "fixture"}):
                self.p.activate_ollama({}, {})
        self.verify.assert_called_once()


    def test_actual_http_request_carries_bearer_and_messages_payload(self):
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
        import threading
        seen = []
        class Handler(BaseHTTPRequestHandler):
            def do_POST(inner):
                body = json.loads(inner.rfile.read(int(inner.headers["Content-Length"])))
                seen.append((inner.path, inner.headers.get("Authorization"), inner.headers.get("X-Api-Key"), body))
                payload = json.dumps({"type": "message", "role": "assistant", "content": [{"type": "text", "text": "OK"}]}).encode()
                inner.send_response(200)
                inner.send_header("Content-Type", "application/json")
                inner.send_header("Content-Length", str(len(payload)))
                inner.end_headers()
                inner.wfile.write(payload)
            def log_message(inner, *args):
                pass
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            result = self.p.request_json(f"http://127.0.0.1:{server.server_port}/v1/messages", "fixture-only-key", {"model": "fixture-model"})
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
        self.assertEqual("assistant", result["role"])
        self.assertTrue(seen == [("/v1/messages", "Bearer fixture-only-key", "fixture-only-key", {"model": "fixture-model"})])

    def test_http_redirect_is_not_followed_with_a_credential(self):
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
        import threading
        seen = []
        class Handler(BaseHTTPRequestHandler):
            def do_GET(inner):
                seen.append(inner.path)
                inner.send_response(302)
                inner.send_header("Location", "/other")
                inner.end_headers()
            def log_message(inner, *args):
                pass
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with self.assertRaises(self.p.ProviderError):
                self.p.request_json(f"http://127.0.0.1:{server.server_port}/api/tags", "fixture-only-key")
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
        self.assertEqual(["/api/tags"], seen)

if __name__ == "__main__":
    unittest.main()
