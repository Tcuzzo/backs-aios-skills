from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "provider/run_provider_tests.py"
UPDATER = ROOT / "bin/backs-aios-update"


def isolated_env(home: Path) -> dict[str, str]:
    return {"HOME": str(home), "PATH": str(Path(sys.executable).parent) + os.pathsep + os.defpath,
            "LANG": "C.UTF-8", "TMPDIR": str(home), "PYTHONDONTWRITEBYTECODE": "1"}


class ProviderValidationTest(unittest.TestCase):
    def run_fixture(self, code: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "tests").mkdir()
            (root / "tests/test_provider_fixture.py").write_text(code)
            env = isolated_env(root)
            env.update({"OLLAMA_API_KEY": "fixture-parent-credential",
                        "BACKS_PROJECT_ROOT": str(root / "not-a-runtime"),
                        "CREDENTIALS_DIRECTORY": str(root / "not-credentials"),
                        "ANTHROPIC_AUTH_TOKEN": "fixture-auth-token"})
            return subprocess.run([sys.executable, "-I", "-B", str(RUNNER), str(root)],
                                  env=env, cwd=root, text=True, capture_output=True, timeout=30)

    def test_validation_does_not_inherit_production_context(self) -> None:
        result = self.run_fixture(
            "import os, unittest\n"
            "class Fixture(unittest.TestCase):\n"
            " def test_clean(self):\n"
            "  for key in ('OLLAMA_API_KEY', 'BACKS_PROJECT_ROOT', 'CREDENTIALS_DIRECTORY', 'ANTHROPIC_AUTH_TOKEN'):\n"
            "   self.assertNotIn(key, os.environ)\n")
        self.assertEqual(0, result.returncode, "Isolated validation failed; output withheld")

    def test_failed_assertion_and_printed_output_are_not_replayed(self) -> None:
        marker = "fixture-output-must-stay-private"
        result = self.run_fixture(
            "import unittest\nprint('" + marker + "')\n"
            "class Fixture(unittest.TestCase):\n"
            " def test_bad(self):\n"
            "  self.assertEqual('expected', '" + marker + "')\n")
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(marker in result.stdout + result.stderr, "Output disclosure regression")
        self.assertTrue("1 failures" in result.stdout)

    def test_discovery_error_details_are_not_replayed(self) -> None:
        marker = "fixture-import-error-must-stay-private"
        result = self.run_fixture("raise RuntimeError('" + marker + "')\n")
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(marker in result.stdout + result.stderr, "Import disclosure regression")

    def test_empty_suite_is_not_success(self) -> None:
        self.assertNotEqual(0, self.run_fixture("# intentionally empty fixture\n").returncode)

    def exercise_update(self, fail: bool) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            home = root / "home"
            home.mkdir()
            source = root / "source"
            env = isolated_env(home)
            env.update({"GIT_AUTHOR_NAME": "Fixture", "GIT_COMMITTER_NAME": "Fixture",
                        "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                        "GIT_COMMITTER_EMAIL": "fixture@example.invalid"})

            def git(*args: str, cwd: Path = root) -> str:
                completed = subprocess.run(["git", *args], cwd=cwd, env=env,
                                           text=True, capture_output=True, timeout=20)
                self.assertEqual(0, completed.returncode, "Fixture git command failed; output withheld")
                return completed.stdout.strip()

            git("init", "-q", "-b", "main", str(source))
            (source / "provider").mkdir()
            (source / "tests").mkdir()
            shutil.copyfile(RUNNER, source / "provider/run_provider_tests.py")
            (source / "install-provider.sh").write_text('#!/bin/sh\nprintf installed > "$HOME/installed"\n')
            fixture = source / "tests/test_provider_fixture.py"
            fixture.write_text("import unittest\nclass Fixture(unittest.TestCase):\n def test_ok(self): pass\n")
            git("add", ".", cwd=source)
            git("commit", "-qm", "fixture base", cwd=source)
            before = git("rev-parse", "HEAD", cwd=source)
            remote = root / "remote.git"
            git("clone", "-q", "--bare", str(source), str(remote))
            git("remote", "add", "origin", str(remote), cwd=source)
            publisher = root / "publisher"
            git("clone", "-q", str(remote), str(publisher))
            (publisher / "tests/test_provider_fixture.py").write_text(
                "import unittest\nclass Fixture(unittest.TestCase):\n"
                + (" def test_fail(self): self.fail('fixture-update-private-output')\n" if fail
                   else " def test_new(self): self.assertTrue(True)\n"))
            git("add", ".", cwd=publisher)
            git("commit", "-qm", "fixture candidate", cwd=publisher)
            candidate = git("rev-parse", "HEAD", cwd=publisher)
            git("push", "-q", "origin", "main", cwd=publisher)
            runtime = home / "provider-current"
            runtime.symlink_to(source, target_is_directory=True)
            env["BACKS_AIOS_PROVIDER_RUNTIME"] = str(runtime)
            env["BACKS_PROJECT_ROOT"] = str(root / "not-a-project")
            env["OLLAMA_API_KEY"] = "fixture-not-a-real-key"
            completed = subprocess.run(["bash", str(UPDATER)], env=env, cwd=home,
                                       capture_output=True, text=True, timeout=45)
            self.assertFalse("fixture-update-private-output" in completed.stdout + completed.stderr)
            if fail:
                self.assertNotEqual(0, completed.returncode)
                self.assertEqual(before, git("rev-parse", "HEAD", cwd=source))
                self.assertFalse((home / "installed").exists())
            else:
                self.assertEqual(0, completed.returncode, "Update failed; output withheld")
                self.assertEqual(candidate, git("rev-parse", "HEAD", cwd=source))
                self.assertTrue((home / "installed").is_file())
            self.assertEqual("", git("status", "--porcelain", cwd=source))

    def test_failed_candidate_leaves_checkout_and_installation_unchanged(self) -> None:
        self.exercise_update(fail=True)

    def test_successful_candidate_is_validated_then_installed(self) -> None:
        self.exercise_update(fail=False)


if __name__ == "__main__":
    unittest.main()
