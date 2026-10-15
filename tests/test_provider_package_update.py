"""Updater regression through real installed commands and local Git repositories."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageUpdateTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.project = self.root / "project"
        self.project.mkdir()
        self.env = {"HOME": str(self.home), "PATH": os.defpath, "LANG": "C.UTF-8",
                    "PYTHONDONTWRITEBYTECODE": "1", "BACKS_PROVIDER_PYTHON": sys.executable,
                    "GIT_AUTHOR_NAME": "Fixture", "GIT_COMMITTER_NAME": "Fixture",
                    "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                    "GIT_COMMITTER_EMAIL": "fixture@example.invalid"}
        self.source = self.root / "source"
        self.source.mkdir()
        for name in ("bin", "provider", "claude-skills"):
            shutil.copytree(ROOT / name, self.source / name)
        shutil.copy2(ROOT / "install-provider.sh", self.source / "install-provider.sh")
        (self.source / "tests").mkdir()
        self.fixture = self.source / "tests/test_provider_fixture.py"
        self.fixture.write_text("import unittest\nclass Good(unittest.TestCase):\n def test_ok(self): pass\n")
        self.git("init", "-q", "-b", "main", str(self.source))
        self.git("add", ".", cwd=self.source)
        self.git("commit", "-qm", "base", cwd=self.source)
        self.remote = self.root / "remote.git"
        self.git("clone", "-q", "--bare", str(self.source), str(self.remote))
        self.git("remote", "add", "origin", str(self.remote), cwd=self.source)
        self.release = self.root / "immutable-release"
        shutil.copytree(self.source, self.release, ignore=shutil.ignore_patterns(".git"))
        (self.release / ".codex-plugin").mkdir()
        (self.release / ".codex-plugin/plugin.json").write_text(json.dumps({"repository": str(self.remote)}))
        (self.release / "skills/native-extra").mkdir(parents=True)
        (self.release / "skills/native-extra/SKILL.md").write_text("keep exact extra body\n")
        (self.release / "extra-symlink").symlink_to("skills/native-extra/SKILL.md")
        self.settings = self.home / ".claude/settings.json"
        self.settings.parent.mkdir()
        self.settings.write_text('{"env":{"ANTHROPIC_MODEL":"owner-choice"}}\n')
        self.run_command(["bash", str(self.release / "install-provider.sh"), str(self.project)], check=True)
        self.runtime = self.home / ".local/share/backs-aios/provider-control/current"
        self.config = self.home / ".config/backs-aios/provider-control"
        self.before = self.snapshot(self.release)
        self.settings_before = self.settings.read_bytes()
        self.python_before = (self.config / "python-executable").read_bytes()
        self.project_before = (self.config / "project-root").read_bytes()
        # Installation explicitly chose the interpreter; updates must keep it
        # even when a different ambient environment is present later.
        self.env.pop("BACKS_PROVIDER_PYTHON")
        self.env["VIRTUAL_ENV"] = "/unrelated/ambient/environment"

    def run_command(self, args, *, cwd=None, check=False):
        result = subprocess.run(args, cwd=cwd or self.root, env=self.env,
                                capture_output=True, text=True, timeout=45)
        if check:
            self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def git(self, *args, cwd=None):
        return self.run_command(["git", *args], cwd=cwd, check=True).stdout.strip()

    @staticmethod
    def snapshot(root):
        return {str(p.relative_to(root)): (os.readlink(p) if p.is_symlink()
                else hashlib.sha256(p.read_bytes()).hexdigest())
                for p in root.rglob("*") if p.is_file() or p.is_symlink()}

    def publish(self, *, fail=False):
        self.fixture.write_text("import unittest\nclass Candidate(unittest.TestCase):\n def test_candidate(self): "
                                + ("self.fail('fixture-private-detail')\n" if fail else "pass\n"))
        (self.source / "provider/update-marker").write_text("new candidate\n")
        self.git("add", ".", cwd=self.source)
        self.git("commit", "-qm", "candidate", cwd=self.source)
        self.git("push", "-q", "origin", "main", cwd=self.source)
        return self.git("rev-parse", "HEAD", cwd=self.source)

    def update(self):
        return self.run_command([str(self.home / ".local/bin/backs-aios-update")])

    def assert_owner_unchanged(self):
        self.assertEqual(self.before, self.snapshot(self.release))
        self.assertEqual(self.settings_before, self.settings.read_bytes())
        self.assertEqual(self.python_before, (self.config / "python-executable").read_bytes())
        self.assertEqual(self.project_before, (self.config / "project-root").read_bytes())

    def test_copied_release_updates_actual_command_preserving_extras_and_owner(self):
        candidate = self.publish()
        result = self.update()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertNotEqual(self.release, self.runtime.resolve())
        self.assertEqual("new candidate\n", (self.runtime / "provider/update-marker").read_text())
        self.assertEqual("keep exact extra body\n", (self.runtime / "skills/native-extra/SKILL.md").read_text())
        self.assertTrue((self.runtime / "extra-symlink").is_symlink())
        self.assertIn(candidate, result.stdout)
        status = self.run_command([str(self.home / ".local/bin/backs-provider"), "--help"])
        self.assertEqual(0, status.returncode, status.stderr)
        self.assertIn("serve", status.stdout)
        self.assert_owner_unchanged()

    def test_failed_candidate_leaves_copied_release_and_wrappers_unchanged(self):
        self.publish(fail=True)
        wrapper = (self.home / ".local/bin/backs-aios-update").read_bytes()
        result = self.update()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("validation failed", result.stderr.lower())
        self.assertNotIn("fixture-private-detail", result.stdout + result.stderr)
        self.assertEqual(self.release, self.runtime.resolve())
        self.assertEqual(wrapper, (self.home / ".local/bin/backs-aios-update").read_bytes())
        self.assert_owner_unchanged()

    def test_git_worktree_git_file_is_updateable(self):
        linked = self.root / "linked"
        self.git("branch", "-m", "author", cwd=self.source)
        self.git("worktree", "add", "-q", "-b", "main", str(linked), cwd=self.source)
        self.assertTrue((linked / ".git").is_file())
        self.runtime.unlink()
        self.runtime.symlink_to(linked)
        result = self.update()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(linked, self.runtime.resolve())
        self.assert_owner_unchanged()


if __name__ == "__main__":
    unittest.main()
