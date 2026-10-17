import json
import os
from pathlib import Path
import stat
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import installer


class MergeTests(unittest.TestCase):
    def test_claude_preserves_hooks_env_and_stricter_cap(self):
        original = {"hooks": {"SessionStart": [{"hooks": [{"type": "command", "command": "existing-hook"}]}]},
                    "permissions": {"allow": ["Read"]},
                    "env": {"UNRELATED_SETTING": "preserve", installer.CLAUDE_KEY: "100000",
                            "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "80"}}
        raw = (json.dumps(original, indent=4) + "\n").encode()
        result = installer.merge_claude(raw)
        self.assertEqual(result.data, raw)
        self.assertFalse(result.changed)
        self.assertIn("percentage override", result.warnings[0])
        original["env"][installer.CLAUDE_KEY] = "150000"
        changed = installer.merge_claude(json.dumps(original).encode())
        parsed = json.loads(changed.data)
        self.assertEqual(parsed["hooks"], original["hooks"])
        self.assertEqual(parsed["permissions"], original["permissions"])
        self.assertEqual(parsed["env"]["UNRELATED_SETTING"], "preserve")
        self.assertEqual(parsed["env"][installer.CLAUDE_KEY], "125000")
        self.assertFalse(installer.merge_claude(changed.data).changed)

    def test_claude_invalid_data_refused_and_invalid_cap_repaired(self):
        for raw in (b'{"env":', b'{"env":"unexpected"}', b'[]', b'{"a":1,"a":2}', b'{"x":NaN}'):
            with self.assertRaises(installer.InstallerError):
                installer.merge_claude(raw)
        for invalid in (True, "90000", 90000, "2000000", 2000000, "125_000"):
            result = installer.merge_claude(json.dumps({"env": {installer.CLAUDE_KEY: invalid}}).encode())
            self.assertEqual(json.loads(result.data)["env"][installer.CLAUDE_KEY], "125000")
            self.assertTrue(any("Repaired an invalid" in warning for warning in result.warnings))
        for invalid_threshold in (90000, 2000000):
            with self.assertRaises(installer.InstallerError):
                installer.merge_claude(b"{}", invalid_threshold)

    def test_codex_preserves_comments_and_only_existing_profile_keys(self):
        raw = b'''# keep this header
model = "example-coder"
model_auto_compact_token_limit = 200_000 # keep this comment

[profiles.quick]
model_auto_compact_token_limit = 90_000
model = "example-quick"

[profiles.deep]
model_auto_compact_token_limit = 175000

[profiles.unconfigured]
model = "example-default"

[mcp_servers.local]
command = "existing-command"
'''
        result = installer.merge_codex(raw)
        parsed = tomllib.loads(result.data.decode())
        self.assertEqual(parsed[installer.CODEX_KEY], 125000)
        self.assertEqual(parsed["profiles"]["quick"][installer.CODEX_KEY], 90000)
        self.assertEqual(parsed["profiles"]["deep"][installer.CODEX_KEY], 125000)
        self.assertNotIn(installer.CODEX_KEY, parsed["profiles"]["unconfigured"])
        self.assertIn(b"= 90_000", result.data)
        self.assertIn(b"# keep this comment", result.data)
        self.assertEqual(parsed["mcp_servers"]["local"]["command"], "existing-command")
        self.assertFalse(installer.merge_codex(result.data).changed)

    def test_codex_top_level_insert_cannot_land_inside_table(self):
        raw = b'[profiles.only]\nmodel = "example"\n'
        result = installer.merge_codex(raw)
        self.assertTrue(result.data.startswith(b"model_auto_compact_token_limit = 125000\n"))
        parsed = tomllib.loads(result.data.decode())
        self.assertEqual(parsed[installer.CODEX_KEY], 125000)
        self.assertNotIn(installer.CODEX_KEY, parsed["profiles"]["only"])

    def test_codex_quoted_dotted_and_inline_profile_keys(self):
        examples = [
            b'"model_auto_compact_token_limit" = 200000\n[profiles."name.with.dots"]\n\'model_auto_compact_token_limit\' = 190000\n',
            b'profiles."name.with.dots".model_auto_compact_token_limit = 190000\n',
            b'profiles = { "name.with.dots" = { model_auto_compact_token_limit = 190000, model = "keep" } }\n',
            b'[profiles]\n"name.with.dots" = { model_auto_compact_token_limit = 190000, model = "keep" }\n',
        ]
        for raw in examples:
            parsed = tomllib.loads(installer.merge_codex(raw).data.decode())
            self.assertEqual(parsed[installer.CODEX_KEY], 125000)
            self.assertEqual(parsed["profiles"]["name.with.dots"][installer.CODEX_KEY], 125000)

    def test_codex_multiline_strings_arrays_and_fake_assignments_untouched(self):
        raw = b'''instructions = """Keep this text.
[profiles.fake]
model_auto_compact_token_limit = 900000
"""
items = [
  "model_auto_compact_token_limit = 800000", # comment
  { nested = "[profiles.another_fake]" },
]
model_auto_compact_token_limit = 200000
[profiles.actual]
model_auto_compact_token_limit = 180000
'''
        before = tomllib.loads(raw.decode())
        after = tomllib.loads(installer.merge_codex(raw).data.decode())
        self.assertEqual(before["instructions"], after["instructions"])
        self.assertEqual(before["items"], after["items"])
        self.assertEqual(after[installer.CODEX_KEY], 125000)
        self.assertEqual(after["profiles"]["actual"][installer.CODEX_KEY], 125000)
        for invalid in (b'[broken', b'a=1\na=2', b'model_auto_compact_token_limit = 1oops'):
            with self.assertRaises(installer.InstallerError):
                installer.merge_codex(invalid)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.home = self.base / "home"
        self.home.mkdir()
        self.state = self.home / ".local/state/rollover"

    def transaction(self):
        return installer.Transaction(self.state)

    def test_discovery_default_override_and_existing_project_paths(self):
        project = self.base / "project"
        (project / ".claude").mkdir(parents=True)
        (project / ".claude/settings.local.json").write_text("{}")
        overrides = {"CLAUDE_CONFIG_DIR": str(self.base / "alternate-claude"),
                     "CODEX_HOME": str(self.base / "alternate-codex")}
        with patch.dict(os.environ, overrides):
            found = installer.discover(self.home, [project])
        self.assertEqual(len(found["configs"]), 5)
        paths = {row["path"] for row in found["configs"]}
        self.assertIn(str(project / ".claude/settings.local.json"), paths)
        self.assertNotIn(str(project / ".codex/config.toml"), paths)

    def test_exact_backup_idempotence_modes_and_guarded_rollback(self):
        path = self.home / "config.json"
        original = b'{"credential":"private-fixture-value","keep":true}\n'
        path.write_bytes(original)
        path.chmod(0o640)
        transaction = self.transaction()
        self.assertTrue(transaction.write(path, b'{"updated":true}\n', expected_before=original))
        report = transaction.finish()
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o640)
        manifest = Path(report["manifest_path"])
        self.assertEqual(stat.S_IMODE(manifest.stat().st_mode), 0o600)
        backup = manifest.parent / report["entries"][0]["backup"]
        self.assertEqual(backup.read_bytes(), original)
        self.assertEqual(stat.S_IMODE(backup.stat().st_mode), 0o600)
        self.assertNotIn("private-fixture-value", json.dumps(report))
        noop = self.transaction()
        self.assertFalse(noop.write(path, path.read_bytes()))
        self.assertIsNone(noop.finish()["manifest_path"])
        restored = installer.rollback(manifest)
        self.assertFalse(restored["conflicts"])
        self.assertEqual(path.read_bytes(), original)
        self.assertFalse(installer.rollback(manifest)["conflicts"])

    def test_rollback_does_not_overwrite_later_user_edit_or_mode(self):
        path = self.home / "config"
        path.write_bytes(b"original")
        transaction = self.transaction()
        transaction.write(path, b"installed")
        manifest = transaction.finish()["manifest_path"]
        path.write_bytes(b"user edit")
        result = installer.rollback(manifest)
        self.assertEqual(result["status"], "rollback_conflicts")
        self.assertEqual(path.read_bytes(), b"user edit")
        if os.name != "nt":
            path.write_bytes(b"installed")
            path.chmod(0o700)
            self.assertTrue(installer.rollback(manifest)["conflicts"])
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o700)

    def test_concurrent_change_since_merge_refused(self):
        path = self.home / "config"
        path.write_bytes(b"new user state")
        transaction = self.transaction()
        with self.assertRaises(installer.Conflict):
            transaction.write(path, b"merged from old state", expected_before=b"old state")
        self.assertEqual(path.read_bytes(), b"new user state")
        self.assertIsNone(transaction.report()["manifest_path"])

    def test_symlink_config_ancestor_and_foreign_registration_retained(self):
        outside = self.base / "outside"
        outside.mkdir()
        target = outside / "settings.json"
        target.write_bytes(b"{}")
        try:
            (self.home / ".claude").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("symlinks unavailable")
        with patch.dict(os.environ, {"CLAUDE_CONFIG_DIR": "", "CODEX_HOME": ""}):
            discovered = installer.discover(self.home)
        self.assertTrue(discovered["configs"][0]["symlink"])
        with self.assertRaises(installer.Conflict):
            installer.read_config(self.home / ".claude/settings.json")
        with self.assertRaises(installer.Conflict):
            self.transaction().write(self.home / ".claude/settings.json", b"changed")
        self.assertEqual(target.read_bytes(), b"{}")
        registration = self.home / "foreign-skill"
        registration.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(installer.Conflict):
            self.transaction().symlink(registration, self.home)
        self.assertEqual(os.readlink(registration), str(outside))

    def test_new_registration_and_file_rollback_and_changed_link_protected(self):
        source = self.base / "skill"
        source.mkdir()
        registration = self.home / "skills/rollover"
        launcher = self.home / "bin/rollover"
        transaction = self.transaction()
        transaction.write(launcher, b"#!/bin/sh\nexit 0\n", 0o755)
        transaction.symlink(registration, source)
        self.assertFalse(transaction.symlink(registration, source))
        manifest = transaction.finish()["manifest_path"]
        result = installer.rollback(manifest)
        self.assertFalse(result["conflicts"])
        self.assertFalse(os.path.lexists(registration))
        self.assertFalse(launcher.exists())
        second = self.transaction()
        second.symlink(registration, source)
        manifest = second.finish()["manifest_path"]
        registration.unlink()
        registration.symlink_to(self.home, target_is_directory=True)
        self.assertTrue(installer.rollback(manifest)["conflicts"])
        self.assertEqual(os.readlink(registration), str(self.home))

    def test_interrupted_write_journal_remains_recoverable(self):
        path = self.home / "config"
        path.write_bytes(b"original")
        transaction = self.transaction()
        real_write = installer._atomic_write
        def fail_target(target, data, mode):
            if Path(target) == path:
                raise OSError("simulated write interruption")
            return real_write(target, data, mode)
        with patch.object(installer, "_atomic_write", side_effect=fail_target):
            with self.assertRaises(OSError):
                transaction.write(path, b"new")
        self.assertEqual(transaction.report()["status"], "failed")
        self.assertFalse(installer.rollback(transaction.report()["manifest_path"])["conflicts"])
        self.assertEqual(path.read_bytes(), b"original")

    def test_owned_link_upgrade_checks_expected_and_restores_previous_target(self):
        original, updated = self.base / "release-old", self.base / "release-new"
        original.mkdir()
        updated.mkdir()
        link = self.home / "managed-skill"
        try:
            link.symlink_to(original, target_is_directory=True)
        except OSError:
            self.skipTest("symlinks unavailable")
        transaction = self.transaction()
        with self.assertRaises(installer.Conflict):
            transaction.replace_symlink(link, updated, expected="unexpected")
        self.assertEqual(os.readlink(link), str(original))
        self.assertTrue(transaction.replace_symlink(link, updated, expected=str(original)))
        self.assertEqual(os.readlink(link), str(updated))
        manifest = transaction.finish()["manifest_path"]
        self.assertFalse(installer.rollback(manifest)["conflicts"])
        self.assertEqual(os.readlink(link), str(original))


if __name__ == "__main__":
    unittest.main()
