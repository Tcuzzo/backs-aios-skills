from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = ROOT / "provider" / "backs_provider.py"

CATALOG = {
    "models": [
        {"model": "kimi-k3"},
        {"model": "kimi-k2.7-code"},
        {"model": "deepseek-v4-pro"},
        {"model": "deepseek-v4-flash"},
        {"model": "glm-5.3"},
        {"model": "glm-5.3-flash"},
        {"model": "qwen3.5"},
        {"model": "nemotron-3-ultra"},
        {"model": "minimax-m3"},
        {"model": "minimax-m2.7"},
        {"model": "mistral-large-3"},
    ]
}


class ProviderControlTest(unittest.TestCase):
    def run_provider(
        self,
        home: Path,
        action: str,
        *,
        catalog: dict | None = CATALOG,
        cwd: Path = ROOT,
        extra_env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        env = {**os.environ, "HOME": str(home), **(extra_env or {})}
        if catalog is not None:
            catalog_path = home / "catalog.json"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            env["BACKS_OLLAMA_CATALOG_FILE"] = str(catalog_path)
        return subprocess.run(
            ["python3", str(CONTROLLER), action],
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_ollama_switch_resolves_entire_lineup_from_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            settings_path = home / ".claude" / "settings.json"
            settings_path.parent.mkdir(parents=True)
            settings_path.write_text(json.dumps({"env": {"KEEP_ME": "yes"}}), encoding="utf-8")

            result = self.run_provider(home, "ollama")
            self.assertEqual(0, result.returncode, result.stderr)

            settings = json.loads(settings_path.read_text(encoding="utf-8"))
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

            state = json.loads((home / ".config" / "backs-aios" / "provider-state.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(state["fallbacks"]["default"]), 5)
            self.assertIn("nemotron-3-ultra", state["fallbacks"]["default"])
            self.assertNotIn("OLLAMA_API_KEY", json.dumps(state))

    def test_role_fallback_activates_when_preferred_model_is_absent(self) -> None:
        catalog = {
            "models": [
                {"model": "kimi-k2.7-code"},
                {"model": "nemotron-3-ultra"},
                {"model": "glm-5.3"},
                {"model": "qwen3.5"},
            ]
        }
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            result = self.run_provider(home, "ollama", catalog=catalog)
            self.assertEqual(0, result.returncode, result.stderr)
            state = json.loads((home / ".config" / "backs-aios" / "provider-state.json").read_text())
            self.assertEqual("nemotron-3-ultra", state["selected"]["opus"])
            self.assertIn(state["selected"]["default"], {m["model"] for m in catalog["models"]})

    def test_round_trip_restores_preexisting_claude_settings(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            settings_path = home / ".claude" / "settings.json"
            settings_path.parent.mkdir(parents=True)
            original = {
                "env": {
                    "KEEP_ME": "yes",
                    "ANTHROPIC_MODEL": "preexisting-user-model",
                    "ANTHROPIC_AUTH_TOKEN": "preexisting-token-placeholder",
                },
                "apiKeyHelper": "/existing/helper",
                "permissions": {"allow": ["Read"]},
            }
            settings_path.write_text(json.dumps(original), encoding="utf-8")

            first = self.run_provider(home, "ollama")
            self.assertEqual(0, first.returncode, first.stderr)
            second = self.run_provider(home, "claude")
            self.assertEqual(0, second.returncode, second.stderr)

            restored = json.loads(settings_path.read_text(encoding="utf-8"))
            self.assertEqual(original, restored)

    def test_models_reports_pool_without_mutating_settings(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            result = self.run_provider(home, "models")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("nemotron-3-ultra", result.stdout)
            self.assertIn("fallback:", result.stdout)
            self.assertFalse((home / ".claude" / "settings.json").exists())

    def test_status_defaults_to_claude_without_touching_settings(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            result = self.run_provider(home, "status")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("provider: claude", result.stdout)
            self.assertFalse((home / ".claude" / "settings.json").exists())

    def test_internal_key_helper_reuses_backs_runtime_env(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home, tempfile.TemporaryDirectory() as raw_project:
            home = Path(raw_home)
            project = Path(raw_project)
            core = project / "backend" / "core"
            core.mkdir(parents=True)
            (core / "__init__.py").write_text("", encoding="utf-8")
            (core / "env_loader.py").write_text(
                "import os\n"
                "def load_runtime_env(*, override=False, repo_root=None):\n"
                "    p = repo_root / '.env'\n"
                "    for line in p.read_text().splitlines():\n"
                "        if '=' in line:\n"
                "            k, v = line.split('=', 1)\n"
                "            os.environ.setdefault(k.strip(), v.strip())\n"
                "    return [p]\n",
                encoding="utf-8",
            )
            (core / "env_utils.py").write_text(
                "import os\n"
                "def env_secret_text(name, default='', *, aliases=(), **kwargs):\n"
                "    for key in (name, *aliases):\n"
                "        value = os.getenv(key, '').strip()\n"
                "        if value:\n"
                "            return value\n"
                "    return default\n",
                encoding="utf-8",
            )
            (project / ".env").write_text("OLLAMA_API_KEY=test-runtime-key\n", encoding="utf-8")

            result = self.run_provider(home, "__key", catalog=None, cwd=project)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("test-runtime-key", result.stdout)
            self.assertFalse((home / ".config" / "backs-aios" / "secrets").exists())

    def test_invalid_action_is_rejected_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as raw_home:
            home = Path(raw_home)
            settings_path = home / ".claude" / "settings.json"
            settings_path.parent.mkdir(parents=True)
            settings_path.write_text('{"env":{"KEEP_ME":"yes"}}\n', encoding="utf-8")
            before = settings_path.read_text(encoding="utf-8")

            result = self.run_provider(home, "bad-provider")
            self.assertEqual(2, result.returncode)
            self.assertEqual(before, settings_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
