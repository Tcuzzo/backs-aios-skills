"""Isolated installer integration tests; never touch the real home or schedulers."""
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import installer
import rollout


class RolloutIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.home = self.base / "synthetic-home"
        self.project = self.home / "projects/fixture-project"
        self.data = self.home / ".local/share/backs-rollover"
        self.payload = self.base / "payload"
        self.home.mkdir()
        self.project.mkdir(parents=True)
        for name in ("backs-session-rollover", "backs-invariant-floor"):
            self.put(self.payload / "pack/skills" / name / "SKILL.md",
                     ("---\nname: " + name + "\ndescription: Isolated test fixture.\n---\nFixture policy.\n").encode())
        for module in (rollout, installer):
            source = Path(module.__file__)
            target = self.payload / "program" / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        self.claude = self.home / ".claude/settings.json"
        self.codex = self.home / ".codex/config.toml"
        self.hooks = {"SessionStart": [{"hooks": [{"type": "command", "command": "existing-local-hook"}]}]}
        self.put(self.claude, (json.dumps({"hooks": self.hooks, "env": {
            "UNRELATED_SETTING": "private-fixture-value", installer.CLAUDE_KEY: "180000"}}, indent=4) + "\n").encode(), 0o640)
        self.put(self.codex, b'''# preserve the existing provider and comments
model = "fixture-coder"
model_auto_compact_token_limit = 200000
[profiles.fast]
model_auto_compact_token_limit = 90000
[profiles.other]
model = "fixture-other"
''')
        self.project_claude = self.project / ".claude/settings.local.json"
        self.project_codex = self.project / ".codex/config.toml"
        self.put(self.project_claude, b'{"env":{"CLAUDE_CODE_AUTO_COMPACT_WINDOW":"100000"}}\n')
        self.put(self.project_codex, b'# project policy\nmodel_auto_compact_token_limit = 85000\n')
        self.project_agents = self.project / "AGENTS.md"
        self.outside_left = b"# Existing project rules\n\nPreserve these spaces.  \n"
        self.outside_right = b"\n\n## Existing notes\nKeep this ending. \n"
        self.put(self.project_agents, self.outside_left + rollout.MD_BEGIN.encode() +
                 b"\nOld managed instructions.\n" + rollout.MD_END.encode() + self.outside_right)
        (self.project / ".agents/skills").mkdir(parents=True)
        self.put(self.project / ".cursor/rules/backs-session-rollover.mdc",
                 b"---\nalwaysApply: true\n---\n\n" + rollout.MD_BEGIN.encode() +
                 b"\nOld Cursor text.\n" + rollout.MD_END.encode() + b"\n\nPreserve Cursor notes.\n")
        self.originals = {path: path.read_bytes() for path in (
            self.claude, self.codex, self.project_claude, self.project_codex,
            self.project_agents, self.project / ".cursor/rules/backs-session-rollover.mdc")}
        self.calls = []
        self.timer_enabled = False
        self.crontab = None
        self.disable_failure = False
        for mock in (patch.dict(os.environ, {}, clear=True),
                     patch.object(Path, "home", return_value=self.home),
                     patch.object(rollout.platform, "system", return_value="Linux"),
                     patch.object(rollout.shutil, "which", side_effect=self.which),
                     patch.object(rollout, "run", side_effect=self.run_stub)):
            mock.start()
            self.addCleanup(mock.stop)

    @staticmethod
    def put(path, content, mode=0o644):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        path.chmod(mode)

    @staticmethod
    def which(name):
        return "fixture-command" if name in {"systemctl", "loginctl", "crontab", "ps"} else None

    def run_stub(self, args, *, stdin=None):
        self.calls.append((list(args), stdin))
        code, output, error = 0, "", ""
        if args[0] == "systemctl":
            if "enable" in args:
                self.timer_enabled = True
            elif "disable" in args:
                if self.disable_failure:
                    code, error = 1, "simulated scheduler refusal"
                else:
                    self.timer_enabled = False
        elif args[0] == "loginctl":
            output = "no\n"
        elif args[0] == "crontab":
            if "-l" in args:
                if self.crontab is None:
                    code, error = 1, "no crontab for fixture"
                else:
                    output = self.crontab
            else:
                self.crontab = stdin
        elif args[0] == "ps":
            output = "101 codex\n102 unrelated\n"
        else:
            self.fail("unexpected external command: " + str(args))
        return subprocess.CompletedProcess(args, code, output, error)

    def invoke(self, action="install", *, boot="none", extra=()):
        arguments = [action, "--data-dir", str(self.data), "--quiet"]
        if action == "install":
            arguments += ["--payload-root", str(self.payload), "--project", str(self.project),
                          "--no-scan", "--boot", boot]
        arguments += list(extra)
        output, errors = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = rollout.main(arguments)
        return code, output.getvalue() + errors.getvalue()

    def report(self):
        return json.loads((self.data / "report.json").read_bytes())

    def test_install_then_reconcile_is_noop_and_preserves_existing_work(self):
        self.assertEqual(self.invoke()[0], 0)
        report = self.report()
        settings = json.loads(self.claude.read_bytes())
        self.assertEqual(settings["hooks"], self.hooks)
        self.assertEqual(settings["env"]["UNRELATED_SETTING"], "private-fixture-value")
        self.assertEqual(settings["env"][installer.CLAUDE_KEY], "125000")
        self.assertEqual(stat.S_IMODE(self.claude.stat().st_mode), 0o640)
        config = tomllib.loads(self.codex.read_text())
        self.assertEqual(config[installer.CODEX_KEY], 125000)
        self.assertEqual(config["profiles"]["fast"][installer.CODEX_KEY], 90000)
        self.assertNotIn(installer.CODEX_KEY, config["profiles"]["other"])
        self.assertEqual(self.project_claude.read_bytes(), self.originals[self.project_claude])
        self.assertEqual(self.project_codex.read_bytes(), self.originals[self.project_codex])
        self.assertEqual(report["fresh_session_handoff"]["status"], "UNBOUND")
        self.assertEqual(report["active_processes"][0]["status"], "not restarted; existing task state preserved")
        self.assertNotIn("private-fixture-value", json.dumps(report))
        manifest = Path(report["transaction_manifest"])
        self.assertEqual(stat.S_IMODE(manifest.stat().st_mode), 0o600)
        manifests = set(self.data.rglob("manifest.json"))
        receipt_bytes = manifest.read_bytes()
        self.assertEqual(self.invoke("reconcile")[0], 0)
        self.assertEqual(set(self.data.rglob("manifest.json")), manifests)
        self.assertEqual(manifest.read_bytes(), receipt_bytes)
        self.assertEqual(self.report()["transaction_manifest"], str(manifest))
        self.assertEqual(self.invoke()[0], 0)
        self.assertEqual(set(self.data.rglob("manifest.json")), manifests)
        for provider in ("claude", "codex"):
            wrapper = (self.home / ".local/bin" / ("backs-" + provider)).read_text()
            self.assertNotIn("-c model_auto_compact_token_limit=125000", wrapper)
            self.assertNotIn("export CLAUDE_CODE_AUTO_COMPACT_WINDOW=125000", wrapper)
        self.assertFalse(any(args[0] in {"kill", "pkill", "killall"} for args, _ in self.calls))

    def test_project_loaders_are_portable_and_outside_text_is_exact(self):
        self.assertEqual(self.invoke()[0], 0)
        after = self.project_agents.read_bytes()
        self.assertEqual(after.split(rollout.MD_BEGIN.encode(), 1)[0], self.outside_left)
        self.assertEqual(after.split(rollout.MD_END.encode(), 1)[1], self.outside_right)
        cursor = self.project / ".cursor/rules/backs-session-rollover.mdc"
        self.assertEqual(cursor.read_bytes().split(rollout.MD_END.encode(), 1)[1],
                         self.originals[cursor].split(rollout.MD_END.encode(), 1)[1])
        loader = self.project / ".agents/skills/backs-session-rollover/SKILL.md"
        self.assertTrue(loader.is_file())
        self.assertIn(b"$BACKS_ROLLOVER_HOME", loader.read_bytes())
        for path in self.project.rglob("*"):
            self.assertFalse(path.is_symlink(), "project install must not record machine-specific links")
            if path.is_file():
                self.assertNotIn(str(self.base).encode(), path.read_bytes())
                self.assertNotIn(str(Path(rollout.__file__).parent).encode(), path.read_bytes())

    def test_foreign_global_skill_and_named_wrapper_are_preserved(self):
        foreign = self.base / "foreign-rollover"
        self.put(foreign / "SKILL.md", b"Operator-owned skill.\n")
        link = self.home / ".claude/skills/backs-session-rollover"
        link.parent.mkdir(parents=True)
        link.symlink_to(foreign, target_is_directory=True)
        wrapper = self.home / ".local/bin/backs-codex"
        original = b"#!/bin/sh\n# Operator-owned wrapper.\nexit 0\n"
        self.put(wrapper, original, 0o700)
        self.assertEqual(self.invoke()[0], 1)
        self.assertEqual(os.readlink(link), str(foreign))
        self.assertEqual(wrapper.read_bytes(), original)
        report = self.report()
        self.assertIn(str(wrapper), report["managed_file_conflicts"])
        self.assertTrue(any(surface["conflicts"] for surface in report["skill_surfaces"]))
        self.assertEqual(report["fresh_session_handoff"]["status"], "UNBOUND")

    def test_config_race_is_reported_and_new_user_settings_survive(self):
        real_write = installer.Transaction.write
        edited = False
        new_bytes = b'{"env":{"UNRELATED_SETTING":"concurrent-user-edit"},"newSetting":true}\n'
        def racing_write(transaction, path, data, mode=None, **kwargs):
            nonlocal edited
            if Path(path) == self.claude and not edited:
                self.assertEqual(kwargs["expected_before"], self.originals[self.claude])
                self.claude.write_bytes(new_bytes)
                edited = True
            return real_write(transaction, path, data, mode, **kwargs)
        with patch.object(installer.Transaction, "write", racing_write):
            self.assertEqual(self.invoke()[0], 1)
        self.assertTrue(edited)
        self.assertEqual(self.claude.read_bytes(), new_bytes)
        report = self.report()
        record = next(item for item in report["native_configs"] if item["path"] == str(self.claude))
        self.assertEqual(record["status"], "APPLY_FAILED")
        self.assertIn(str(self.claude), report["apply_failures"])
        self.assertEqual(report["fresh_session_handoff"]["status"], "UNBOUND")

    def test_rollback_restores_exact_original_files_and_removes_created_links(self):
        self.assertEqual(self.invoke()[0], 0)
        manifest = self.report()["transaction_manifest"]
        self.assertEqual(self.invoke("rollback", extra=("--manifest", manifest))[0], 0)
        for path, original in self.originals.items():
            self.assertEqual(path.read_bytes(), original)
        self.assertFalse(os.path.lexists(self.home / ".agents/skills/backs-session-rollover"))
        self.assertFalse((self.home / ".local/bin/backs-rollover").exists())
        journal = json.loads(Path(manifest).read_bytes())
        self.assertEqual(journal["status"], "rolled_back")

    def test_disable_boot_is_persistent_and_does_not_disable_native_policy(self):
        self.assertEqual(self.invoke(boot="systemd")[0], 0)
        self.assertTrue(self.timer_enabled)
        self.assertEqual(self.report()["boot"]["status"], "enabled")
        self.assertEqual(self.invoke("disable-boot")[0], 0)
        self.assertFalse(self.timer_enabled)
        self.assertEqual(self.report()["boot"]["status"], "disabled")
        settings = json.loads((self.data / "installation.json").read_bytes())
        self.assertTrue(settings["boot_disabled"])
        self.assertEqual(self.invoke("reconcile", extra=("--from-boot",))[0], 0)
        self.assertEqual(self.invoke("reconcile")[0], 0)
        self.assertFalse(self.timer_enabled)
        self.assertEqual(self.report()["boot"]["status"], "disabled")
        self.assertEqual(json.loads(self.claude.read_bytes())["env"][installer.CLAUDE_KEY], "125000")
        self.assertEqual(self.report()["fresh_session_handoff"]["status"], "UNBOUND")


if __name__ == "__main__":
    unittest.main()
