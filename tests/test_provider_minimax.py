"""MiniMax provider contracts: real local HTTP, disk writes and installed launchers.

The local HTTP fixture is not a live MiniMax or Claude Code UI verification.
Production endpoint validation is tested separately; no fixture bypass ships.
"""
from __future__ import annotations

import contextlib
import copy
import hmac
import importlib.util
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest import mock

import test_provider_control as fixtures

ROOT = Path(__file__).resolve().parents[1]


@contextlib.contextmanager
def messages_server(mode="ok"):
    seen = []
    blocks = [
        {"type": "thinking", "thinking": "fixture reasoning", "signature": "fixture-signature"},
        {"type": "tool_use", "id": "fixture_tool_1", "name": "backs_provider_probe", "input": {"echo": "BACKS_OK"}},
    ]
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            seen.append({"path": self.path, "auth": self.headers.get("Authorization"), "body": body})
            if mode == "unauthorized":
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b"fixture-sensitive-error")
                return
            if body.get("stream"):
                events = [{"type": "message_start", "message": {
                    "type": "message", "role": "assistant", "model": body["model"], "content": []}}]
                events.extend([
                    {"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": ""}},
                    {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "fixture reasoning"}},
                    {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "fixture-signature"}},
                    {"type": "content_block_stop", "index": 0},
                    {"type": "content_block_start", "index": 1, "content_block": {
                        "type": "tool_use", "id": "fixture_tool_1", "name": "backs_provider_probe", "input": {}}},
                    {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": '{"echo":'}},
                    {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": '"BACKS_OK"}'}},
                    {"type": "content_block_stop", "index": 1},
                    {"type": "message_delta", "delta": {"stop_reason": "tool_use"}},
                    {"type": "message_stop"},
                ])
                if mode == "truncated":
                    events = events[:-1]
                elif mode == "error_event":
                    events = [{"type": "error", "error": {"message": "fixture-sensitive-error"}}]
                elif mode == "wrong_tool":
                    events[5]["content_block"]["name"] = "unexpected_probe"
                data = "".join("event: " + e["type"] + "\r\ndata: " + json.dumps(e) + "\r\n\r\n" for e in events).encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
            else:
                data = json.dumps({"type": "message", "role": "assistant", "model": body["model"],
                                   "stop_reason": "end_turn", "content": [{"type": "text", "text": "BACKS_OK" if mode != "wrong_result" else "incorrect"}]}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/anthropic", seen, blocks
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


class MiniMaxProviderTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.project = self.home / "project"
        fixtures.fixture_project(self.project)
        with (self.project / ".env").open("a") as out:
            out.write("MINIMAX_API_KEY=fixture-minimax-key\n")
        self.env = fixtures.fixture_env(self.home)
        self.env.update(BACKS_PROJECT_ROOT=str(self.project), BACKS_PROVIDER_PYTHON=sys.executable)
        patch = mock.patch.dict(os.environ, self.env, clear=True)
        patch.start()
        self.addCleanup(patch.stop)
        spec = importlib.util.spec_from_file_location("minimax_test_controller", ROOT / "provider/backs_provider.py")
        self.p = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.p)

    def install(self):
        result = subprocess.run(["bash", str(ROOT / "install-provider.sh"), str(self.project)],
                                env=self.env, cwd=self.home, capture_output=True, timeout=20)
        self.assertEqual(0, result.returncode, "fixture install failed; output withheld")

    def cli(self, *args):
        return subprocess.run([str(self.home / ".local/bin/backs-provider"), *args],
                              env=self.env, cwd=self.home, capture_output=True, timeout=20)

    def profile(self):
        return self.p.load_profile("minimax")

    def test_minimax_catalog_is_documented_not_an_ollama_network_request(self):
        profile = self.profile()
        with mock.patch.object(self.p, "request_json", side_effect=AssertionError("unexpected catalog request")):
            catalog = self.p.fetch_catalog(profile)
        self.assertIn("MiniMax-M3", catalog)
        self.assertIn("MiniMax-M2.7", catalog)

    def test_m3_is_selected_for_all_roles_not_accidentally_downgraded(self):
        profile = self.profile()
        selected, alternatives = self.p.resolve_lineup(profile, self.p.fetch_catalog(profile))
        self.assertEqual(set(self.p.ROLE_ENV), set(selected))
        self.assertEqual({"MiniMax-M3"}, set(selected.values()))
        self.assertTrue(all("MiniMax-M2.7" in row for row in alternatives.values()))

    def test_endpoint_allowlist_rejects_credential_and_redirect_destinations(self):
        profile = self.profile()
        for url in ("https://example.invalid/anthropic", "http://api.minimax.io/anthropic",
                    "https://api.minimax.io/other", "https://api.minimax.io/anthropic?key=fixture",
                    "https://fixture:@api.minimax.io/anthropic", "https://api.minimax.io:bad/anthropic",
                    "https://api.minimax.io.evil.invalid/anthropic"):
            with self.subTest(url=url), mock.patch.dict(os.environ, {"BACKS_MINIMAX_BASE_URL": url}):
                with self.assertRaises(self.p.ProviderError):
                    self.p.endpoint(profile)
        self.assertEqual("https://api.minimax.io/anthropic", self.p.endpoint(profile))

    def test_explicit_china_endpoint_is_supported(self):
        with mock.patch.dict(os.environ, {"BACKS_MINIMAX_BASE_URL": "https://api.minimax.cn/anthropic"}):
            self.assertEqual("https://api.minimax.cn/anthropic", self.p.endpoint(self.profile()))

    def test_installed_helpers_keep_provider_credentials_separate(self):
        self.install()
        for name, expected in (("backs-minimax-key", b"fixture-minimax-key"), ("backs-ollama-key", b"fixture-only-key")):
            result = subprocess.run([str(self.home / ".local/bin" / name)], env=fixtures.fixture_env(self.home),
                                    cwd=self.home, capture_output=True, timeout=20)
            self.assertEqual(0, result.returncode)
            self.assertTrue(hmac.compare_digest(expected, result.stdout), "fixture helper mismatch; values withheld")
            self.assertEqual(b"", result.stderr)

    def test_missing_minimax_key_never_falls_back_to_ollama(self):
        self.install()
        (self.project / ".env").write_text("OLLAMA_API_KEY=fixture-only-key\n")
        result = self.cli("minimax")
        self.assertNotEqual(0, result.returncode)
        self.assertNotIn(b"fixture-only-key", result.stdout + result.stderr)
        self.assertFalse(self.p.STATE_FILE.exists())
        self.assertFalse(self.p.CLAUDE_SETTINGS.exists())

    def test_cli_models_minimax_works_without_a_key_and_rejects_extra_arguments(self):
        self.install()
        (self.project / ".env").unlink()
        result = self.cli("models", "minimax")
        self.assertEqual(0, result.returncode)
        self.assertIn(b"MiniMax-M3", result.stdout)
        self.assertIn(b"documented", result.stdout.lower())
        for args in (("minimax", "unexpected"), ("models", "__key"), ("status", "minimax"), ("doctor", "minimax;echo")):
            self.assertEqual(2, self.cli(*args).returncode)

    def test_installed_skill_is_visible_in_both_cli_and_project_scopes(self):
        self.install()
        for skill in (self.home / ".claude/skills/provider/SKILL.md", self.project / ".claude/skills/provider/SKILL.md"):
            self.assertIn("minimax", skill.read_text())
            self.assertIn("doctor", skill.read_text())

    def test_real_http_stream_tool_result_and_full_assistant_preservation(self):
        self.install()
        profile = self.profile()
        selected, _ = self.p.resolve_lineup(profile, self.p.fetch_catalog(profile))
        with messages_server() as (base, seen, blocks), mock.patch.object(self.p, "endpoint", return_value=base):
            self.p.verify_messages(profile, selected, self.p.helper_key("minimax"))
        self.assertEqual(2, len(seen))
        self.assertTrue(all(row["path"] == "/anthropic/v1/messages" for row in seen))
        self.assertTrue(all(row["auth"] == "Bearer fixture-minimax-key" for row in seen))
        self.assertTrue(seen[0]["body"]["stream"])
        self.assertEqual("MiniMax-M3", seen[0]["body"]["model"])
        self.assertEqual(blocks, seen[1]["body"]["messages"][-2]["content"])
        self.assertEqual("fixture_tool_1", seen[1]["body"]["messages"][-1]["content"][0]["tool_use_id"])

    def test_failed_preflight_does_not_write_settings_or_state(self):
        self.install()
        self.p.CLAUDE_SETTINGS.parent.mkdir(parents=True, exist_ok=True)
        self.p.CLAUDE_SETTINGS.write_text('{"env":{"KEEP":"yes"}}\n')
        before = self.p.CLAUDE_SETTINGS.read_bytes()
        for mode in ("unauthorized", "truncated", "error_event", "wrong_tool", "wrong_result"):
            with self.subTest(mode=mode), messages_server(mode) as (base, _, _):
                with mock.patch.object(self.p, "endpoint", return_value=base), self.assertRaises(self.p.ProviderError) as caught:
                    self.p.activate_minimax({"env": {"KEEP": "yes"}}, {})
                self.assertNotIn("fixture-sensitive-error", str(caught.exception))
                self.assertEqual(before, self.p.CLAUDE_SETTINGS.read_bytes())
                self.assertFalse(self.p.STATE_FILE.exists())
                self.assertFalse((self.project / ".claude/settings.local.json").exists())

    def test_all_provider_round_trips_preserve_native_baselines_and_other_settings(self):
        self.install()
        local_path = self.project / ".claude/settings.local.json"
        local_path.parent.mkdir(parents=True, exist_ok=True)
        native = {"env": {"KEEP": "yes", "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "12345"},
                  "model": "native-placeholder", "apiKeyHelper": "native-helper", "hooks": {"kept": []}}
        local_native = {"env": {"CUSTOM": "yes"}, "model": "local-placeholder"}
        original_env = (self.project / ".env").read_bytes()
        oauth = self.home / ".claude/.credentials.json"
        oauth.parent.mkdir(parents=True, exist_ok=True)
        oauth.write_text("fixture-oauth-preserve")
        ollama = self.p.load_profile()
        catalog = sorted({m for row in ollama["roles"].values() for m in row})
        fetch = self.p.fetch_catalog
        for order in (("minimax", "ollama", "minimax"), ("ollama", "minimax", "ollama")):
            with self.subTest(order=order):
                settings, state = copy.deepcopy(native), {}
                local_path.write_text(json.dumps(local_native))
                with mock.patch.object(self.p, "verify_messages"), mock.patch.object(self.p, "fetch_catalog", side_effect=lambda p, key=None: fetch(p, key) if p.get("provider") == "minimax" else catalog):
                    for provider in order:
                        getattr(self.p, "activate_" + provider)(settings, state)
                        for path in (self.p.CLAUDE_SETTINGS, local_path):
                            value = json.loads(path.read_text())
                            self.assertIn("backs-" + provider + "-key", value["apiKeyHelper"])
                            self.assertNotIn("fixture-minimax-key", path.read_text())
                            self.assertNotIn("fixture-only-key", path.read_text())
                            self.assertEqual(value["env"]["ANTHROPIC_MODEL"], value["model"])
                        if provider == "minimax":
                            self.assertEqual("MiniMax-M3[1m]", settings["env"]["ANTHROPIC_MODEL"])
                            self.assertEqual("1000000", settings["env"]["CLAUDE_CODE_AUTO_COMPACT_WINDOW"])
                        else:
                            self.assertEqual("12345", settings["env"]["CLAUDE_CODE_AUTO_COMPACT_WINDOW"])
                settings["new_preference"] = 5
                self.p.activate_claude(settings, state)
                self.assertEqual(dict(native, new_preference=5), json.loads(self.p.CLAUDE_SETTINGS.read_text()))
                self.assertEqual(local_native, json.loads(local_path.read_text()))
                self.assertEqual(original_env, (self.project / ".env").read_bytes())
                self.assertEqual("fixture-oauth-preserve", oauth.read_text())

    def test_repeated_claude_restore_does_not_revert_later_user_edits(self):
        settings, state = {}, {"provider": "minimax", "baseline": self.p.snapshot({"model": "original"})}
        self.p.activate_claude(settings, state)
        settings["model"] = "user-edit"
        self.p.activate_claude(settings, state)
        self.assertEqual("user-edit", settings["model"])

    def test_repeated_activation_extends_old_project_snapshot_for_new_owned_keys(self):
        self.install()
        settings, state = {"model": "original"}, {}
        local = self.project / ".claude/settings.local.json"
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_text('{"model":"project-original"}')
        with mock.patch.object(self.p, "verify_messages"):
            self.p.activate_minimax(settings, state)
            for baseline in (state["baseline"], state["project_overlay"]["baseline"]):
                baseline["env"].pop("CLAUDE_CODE_AUTO_COMPACT_WINDOW", None)
            self.p.activate_minimax(settings, state)
        self.assertIn("CLAUDE_CODE_AUTO_COMPACT_WINDOW", state["project_overlay"]["baseline"]["env"])

    def test_status_identifies_saved_minimax_not_claude_transport(self):
        import io
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.p.status({}, {"provider": "minimax", "selected": {"default": "MiniMax-M3"}, "messages_preflight": "passed"})
        self.assertIn("MiniMax", output.getvalue())
        self.assertNotIn("prior Claude settings", output.getvalue())

    def test_models_without_provider_uses_saved_minimax(self):
        self.install()
        self.p.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.p.STATE_FILE.write_text('{"provider":"minimax"}')
        result = self.cli("models")
        self.assertEqual(0, result.returncode)
        self.assertIn(b"MiniMax-M3", result.stdout)


if __name__ == "__main__":
    unittest.main()
