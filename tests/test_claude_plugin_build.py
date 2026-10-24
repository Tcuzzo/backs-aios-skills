"""The claude.ai plugin pack must validate without bending BACKS source truth.

The repo deliberately keeps byte-identical alias directories and hyphen-cased
names (see test_session_start_contract and test_pack_contract). Those two
contracts force duplicate `name` values, which claude.ai's plugin validator
rejects. The resolution lives in the BUILD, not in the source, so this test
locks the build instead of weakening either contract.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import build_claude_plugin as bp  # noqa: E402


class ClaudePluginBuildTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.stage = pathlib.Path(self._tmp.name) / "pack"
        self.stage.mkdir()
        bp.build(self.stage)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_exactly_one_plugin_manifest(self) -> None:
        self.assertEqual(1, len(list(self.stage.rglob("plugin.json"))))

    def test_no_top_level_bin_directory(self) -> None:
        self.assertFalse((self.stage / "bin").exists())

    def test_private_runtime_skill_is_not_published(self) -> None:
        self.assertFalse((self.stage / "skills" / "hive-clone-boot").exists())
        for hook in (self.stage / "hooks").glob("aios_gate.*"):
            with self.subTest(hook=hook.name):
                self.assertFalse("hive-clone-boot" in hook.read_text(encoding="utf-8"))

    def test_skill_names_are_unique(self) -> None:
        names = [
            re.search(r"^name:\s*\"?([^\"\n]+)\"?", bp.frontmatter(p), re.M).group(1).strip()
            for p in sorted((self.stage / "skills").glob("*/SKILL.md"))
        ]
        self.assertEqual(len(names), len(set(names)), sorted(names))

    def test_no_angle_brackets_in_descriptions(self) -> None:
        for skill in sorted((self.stage / "skills").glob("*/SKILL.md")):
            head = bp.frontmatter(skill)
            desc = re.split(r"\n[a-z_]+:", head.split("description:", 1)[1])[0]
            with self.subTest(skill=skill.parent.name):
                self.assertNotIn("<", desc)
                self.assertNotIn(">", desc)

    def test_source_aliases_are_untouched(self) -> None:
        """The build drops aliases from the pack; it never edits the repo."""
        for alias, canon in bp.ALIASES.items():
            with self.subTest(alias=alias):
                self.assertTrue((ROOT / "skills" / alias / "SKILL.md").exists())
                self.assertEqual(
                    (ROOT / "skills" / alias / "SKILL.md").read_bytes(),
                    (ROOT / "skills" / canon / "SKILL.md").read_bytes(),
                )
                self.assertFalse((self.stage / "skills" / alias).exists())

    def test_wrapped_bin_scripts_ship_with_their_skill(self) -> None:
        for script, owner in bp.BIN_OWNERS.items():
            with self.subTest(script=script):
                self.assertTrue((self.stage / "skills" / owner / "scripts" / script).exists())
                body = (self.stage / "skills" / owner / "SKILL.md").read_text(encoding="utf-8")
                self.assertNotIn(f"bash bin/{script}", body)


if __name__ == "__main__":
    unittest.main()


class AliasDriftTest(unittest.TestCase):
    """[major] state_continuity: the build's alias map duplicated the byte-identical
    groups in test_session_start_contract. A comment is not a guard — add an alias
    there without adding it here and the pack ships a duplicate name again."""

    def test_build_alias_map_matches_the_byte_identical_groups(self) -> None:
        source = (ROOT / "tests" / "test_session_start_contract.py").read_text(encoding="utf-8")
        block = re.search(r"def test_alias_copies_stay_byte_identical.*?groups = \((.*?)\n        \)", source, re.S)
        self.assertIsNotNone(block, "could not locate the byte-identical groups")
        contract = {tuple(re.findall(r'"([^"]+)"', line))
                    for line in block.group(1).strip().splitlines() if '"' in line}
        declared = set()
        for group in contract:
            canon = [n for n in group if n in bp.ALIASES.values()]
            self.assertTrue(canon, f"no canonical skill in group {group}")
            for name in group:
                if name != canon[0]:
                    declared.add((name, canon[0]))
        self.assertEqual(declared, set(bp.ALIASES.items()))


class PublicPayloadTest(unittest.TestCase):
    def test_archive_is_portable_and_contains_only_stage_files(self) -> None:
        local_sandbox = ROOT / "sandbox"
        with tempfile.TemporaryDirectory(dir=local_sandbox if local_sandbox.is_dir() else None) as tmp:
            stage = pathlib.Path(tmp) / "stage"
            (stage / "skills" / "example").mkdir(parents=True)
            (stage / "skills" / "example" / "SKILL.md").write_text("public", encoding="utf-8")
            output = pathlib.Path(tmp) / "pack.plugin"
            bp.write_archive(stage, output)
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(["skills/example/SKILL.md"], archive.namelist())

    def test_build_prunes_private_runtime_and_repo_scaffolding(self) -> None:
        local_sandbox = ROOT / "sandbox"
        with tempfile.TemporaryDirectory(dir=local_sandbox if local_sandbox.is_dir() else None) as tmp:
            stage = pathlib.Path(tmp)
            for rel in (
                "skills/example/SKILL.md",
                "hooks/aios_gate.js",
                "plays/repair-loop.md",
                "command-adapters/repair-loop.md",
                ".claude-plugin/plugin.json",
                "LICENSE",
                "provider/private-runtime.json",
                "config/internal-routing.json",
                "tests/customer-fixture.json",
                "docs/operator-notes.md",
                "tools/secret-helper.py",
            ):
                path = stage / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("synthetic private fixture" if "private" in rel else "public", encoding="utf-8")

            bp.prune_to_public_payload(stage)

            expected = {
                "skills/example/SKILL.md",
                "hooks/aios_gate.js",
                "plays/repair-loop.md",
                "command-adapters/repair-loop.md",
                ".claude-plugin/plugin.json",
                "LICENSE",
            }
            actual = {p.relative_to(stage).as_posix() for p in stage.rglob("*") if p.is_file()}
            self.assertEqual(expected, actual)
