from __future__ import annotations

import hmac
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = ROOT / "provider" / "backs_provider.py"
CATALOG = {"models": [{"model": name} for name in (
    "kimi-k3", "kimi-k2.7-code", "deepseek-v4-pro", "deepseek-v4-flash",
    "glm-5.3", "glm-5.3-flash", "qwen3.5", "nemotron-3-ultra",
    "minimax-m3", "minimax-m2.7", "mistral-large-3",
)]}


def fixture_env(home: Path) -> dict[str, str]:
    """Allowlist, not an inherited environment with a few keys removed."""
    return {
        "HOME": str(home),
        "PATH": str(Path(sys.executable).parent) + os.pathsep + os.defpath,
        "LANG": "C.UTF-8",
        "XDG_CONFIG_HOME": str(home / ".config"),
        "TMPDIR": str(home),
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
    }


class ProviderControlTest(unittest.TestCase):
    def run_provider(self, home: Path, action: str, *, catalog: dict | None = CATALOG,
                     cwd: Path = ROOT, extra_env: dict[str, str] | None = None
                     ) -> subprocess.CompletedProcess[str]:
        env = {**fixture_env(home), **(extra_env or {})}
        if catalog is not None:
            catalog_path = home / "catalog.json"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            env["BACKS_OLLAMA_CATALOG_FILE"] = str(catalog_path)
        return subprocess.run(
            [sys.executable, "-I", "-B", str(CONTROLLER), action],
            cwd=cwd, env=env, text=True, capture_output=True, check=False, timeout=20,
        )

    def assert_success(self, result: subprocess.CompletedProcess[str]) -> None:
        # Never include captured output in assertion messages: __key writes a secret.
        self.assertEqual(0, result.returncode, "Controller failed; output withheld")

    def test_ollama_switch_resolves_entire_lineup_from_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            path = home / ".claude" / "settings.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"env": {"KEEP_ME": "yes"}}))
            self.assert_success(self.run_provider(home, "ollama"))
            settings = json.loads(path.read_text())
            env = settings["env"]
            self.assertEqual("yes", env["KEEP_ME"])
            self.assertEqual("https://ollama.com", env["ANTHROPIC_BASE_URL"])
            self.assertEqual("kimi-k3", env["ANTHROPIC_MODEL"])
            self.assertEqual("deepseek-v4-pro", env["ANTHROPIC_DEFAULT_OPUS_MODEL"])
            self.assertEqual("kimi-k2.7-code", env["ANTHROPIC_DEFAULT_SONNET_MODEL"])
            self.assertEqual("glm-5.3-flash", env["ANTHROPIC_DEFAULT_HAIKU_MODEL"])
            self.assertNotIn("ANTHROPIC_AUTH_TOKEN", env)
            self.assertNotIn("ANTHROPIC_API_KEY", env)
            self.assertTrue(settings["apiKeyHelper"].endswith("/.local/bin/backs-ollama-key"))
            state = json.loads((home / ".config/backs-aios/provider-state.json").read_text())
            self.assertGreaterEqual(len(state["fallbacks"]["default"]), 5)
            self.assertIn("nemotron-3-ultra", state["fallbacks"]["default"])
            self.assertNotIn("OLLAMA_API_KEY", json.dumps(state))

    def test_role_fallback_activates_when_preferred_model_is_absent(self) -> None:
        catalog = {"models": [{"model": name} for name in
                               ("kimi-k2.7-code", "nemotron-3-ultra", "glm-5.3", "qwen3.5")]}
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            self.assert_success(self.run_provider(home, "ollama", catalog=catalog))
            state = json.loads((home / ".config/backs-aios/provider-state.json").read_text())
            self.assertEqual("nemotron-3-ultra", state["selected"]["opus"])
            self.assertIn(state["selected"]["default"], {m["model"] for m in catalog["models"]})

    def test_round_trip_restores_preexisting_claude_settings(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            path = home / ".claude/settings.json"
            path.parent.mkdir(parents=True)
            original = {"env": {"KEEP_ME": "yes", "ANTHROPIC_MODEL": "preexisting-user-model",
                                "ANTHROPIC_AUTH_TOKEN": "preexisting-token-placeholder"},
                        "apiKeyHelper": "/existing/helper", "permissions": {"allow": ["Read"]}}
            path.write_text(json.dumps(original))
            self.assert_success(self.run_provider(home, "ollama"))
            self.assert_success(self.run_provider(home, "claude"))
            self.assertTrue(original == json.loads(path.read_text()), "Settings not restored")

    def test_models_reports_pool_without_mutating_settings(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            result = self.run_provider(home, "models")
            self.assert_success(result)
            self.assertTrue("nemotron-3-ultra" in result.stdout)
            self.assertTrue("fallback:" in result.stdout)
            self.assertFalse((home / ".claude/settings.json").exists())

    def test_status_defaults_to_claude_without_touching_settings(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            result = self.run_provider(home, "status")
            self.assert_success(result)
            self.assertTrue("provider: claude" in result.stdout)
            self.assertFalse((home / ".claude/settings.json").exists())

    def test_internal_key_helper_reuses_backs_runtime_env(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            project = home / "fixture-project"
            core = project / "backend/core"
            core.mkdir(parents=True)
            (core / "__init__.py").write_text("")
            (core / "env_loader.py").write_text(
                "import os\n"
                "def load_runtime_env(*, override=False, repo_root=None):\n"
                "    p = repo_root / '.env'\n"
                "    for line in p.read_text().splitlines():\n"
                "        if '=' in line:\n"
                "            k, v = line.split('=', 1)\n"
                "            os.environ.setdefault(k.strip(), v.strip())\n"
                "    return [p]\n")
            (core / "env_utils.py").write_text(
                "import os\n"
                "def env_secret_text(name, default='', *, aliases=(), **kwargs):\n"
                "    for key in (name, *aliases):\n"
                "        value = os.getenv(key, '').strip()\n"
                "        if value:\n"
                "            return value\n"
                "    return default\n")
            (project / ".env").write_text("OLLAMA_API_KEY=test-runtime-key\n")
            result = self.run_provider(home, "__key", catalog=None, cwd=project,
                                       extra_env={"BACKS_PROJECT_ROOT": str(project)})
            self.assert_success(result)
            self.assertTrue(hmac.compare_digest(b"test-runtime-key", result.stdout.encode()),
                            "Fixture credential mismatch; values redacted")
            self.assertFalse((home / ".config/backs-aios/secrets").exists())

    def test_parent_credentials_and_project_do_not_enter_fixture_environment(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            poison = {name: "fixture-parent-value" for name in (
                "BACKS_PROJECT_ROOT", "CLOUD_OLLAMA_API_KEY", "OLLAMA_API_KEY",
                "LOCAL_OLLAMA_API_KEY", "OLLAMA_CLOUD_API_KEY", "OLLAMA_API_KEY_FILE",
                "CREDENTIALS_DIRECTORY", "PYTHONPATH", "ANTHROPIC_API_KEY",
                "BACKS_OLLAMA_CATALOG_FILE", "BACKS_PROVIDER_CONTROLLER")}
            with mock.patch.dict(os.environ, poison):
                self.assertFalse(set(poison).intersection(fixture_env(home)))
                self.test_internal_key_helper_reuses_backs_runtime_env()

    def test_invalid_action_is_rejected_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            path = home / ".claude/settings.json"
            path.parent.mkdir(parents=True)
            path.write_text('{"env":{"KEEP_ME":"yes"}}\n')
            before = path.read_bytes()
            result = self.run_provider(home, "bad-provider")
            self.assertEqual(2, result.returncode)
            self.assertTrue(before == path.read_bytes(), "Settings unexpectedly modified")


if __name__ == "__main__":
    unittest.main()
