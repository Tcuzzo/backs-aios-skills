from __future__ import annotations

import hmac
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_provider_control import fixture_env, fixture_project

ROOT = Path(__file__).resolve().parents[1]


class ProviderCliContractTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.project = self.home / "project"
        fixture_project(self.project)
        self.env = fixture_env(self.home)
        self.env["BACKS_PROVIDER_PYTHON"] = sys.executable
        self.base = self.home / ".local/share/backs-aios/current"
        self.base.parent.mkdir(parents=True)
        self.base.symlink_to(self.home / "primary-runtime")

    def install(self):
        before = {p: (p.read_bytes(), p.stat().st_mode) for p in
                  [ROOT / "install-provider.sh", ROOT / "bin/backs-provider", ROOT / "provider/ollama-key-helper.sh"]}
        result = subprocess.run(["bash", str(ROOT / "install-provider.sh"), str(self.project)],
            env=self.env, cwd=self.home, text=True, capture_output=True, timeout=20)
        self.assertEqual(0, result.returncode, "Fixture install failed; output withheld")
        self.assertTrue(all(p.read_bytes() == data and p.stat().st_mode == mode for p, (data, mode) in before.items()))
        self.assertEqual(str(self.home / "primary-runtime"), os.readlink(self.base))

    def test_installer_pins_python_and_does_not_dirty_source(self):
        self.install()
        config = self.home / ".config/backs-aios/provider-control"
        self.assertEqual(sys.executable, (config / "python-executable").read_text().strip())
        self.assertEqual(str(self.project), (config / "project-root").read_text().strip())
        self.assertFalse((self.home / ".config/backs-aios/secrets").exists())

    def test_installed_helper_works_without_venv_activation_or_project_cwd(self):
        self.install()
        fakebin = self.home / "fakebin"
        fakebin.mkdir()
        fake_python = fakebin / "python3"
        fake_python.write_text("#!/bin/sh\nexit 87\n")
        fake_python.chmod(0o755)
        env = fixture_env(self.home)
        env["PATH"] = str(fakebin) + os.pathsep + os.defpath
        result = subprocess.run([str(self.home / ".local/bin/backs-ollama-key")], cwd=self.home,
                                env=env, capture_output=True, timeout=20)
        self.assertEqual(0, result.returncode, "Helper failed; output withheld")
        self.assertTrue(hmac.compare_digest(result.stdout, b"fixture-only-key"), "Helper mismatch; values withheld")
        self.assertEqual(b"", result.stderr)

    def test_backend_prints_do_not_contaminate_credential_helper_output(self):
        self.install()
        file = self.project / "backend/core/__init__.py"
        file.write_text("print('fixture-private-log')\n")
        result = subprocess.run([str(self.home / ".local/bin/backs-ollama-key")], cwd=self.home,
                                env=fixture_env(self.home), capture_output=True, timeout=20)
        self.assertEqual(0, result.returncode)
        self.assertTrue(hmac.compare_digest(result.stdout, b"fixture-only-key"), "Helper mismatch; values withheld")
        self.assertFalse(b"fixture-private-log" in result.stdout + result.stderr)

    def test_backend_error_is_redacted(self):
        self.install()
        (self.project / "backend/core/__init__.py").write_text("raise ValueError('fixture-private-log')\n")
        result = subprocess.run([str(self.home / ".local/bin/backs-ollama-key")], cwd=self.home,
                                env=fixture_env(self.home), capture_output=True, timeout=20)
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(b"fixture-private-log" in result.stdout + result.stderr)
        self.assertEqual(b"", result.stdout)

    def test_conflicting_skill_is_not_overwritten(self):
        conflict = self.project / ".claude/skills/provider"
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("user-owned")
        result = subprocess.run(["bash", str(ROOT / "install-provider.sh"), str(self.project)],
            env=self.env, cwd=self.home, capture_output=True, timeout=20)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("user-owned", (conflict / "SKILL.md").read_text())
        self.assertFalse((self.home / ".local/share/backs-aios/provider-control/current").exists())

    def test_reinstall_is_idempotent(self):
        self.install()
        self.install()


if __name__ == "__main__":
    unittest.main()
