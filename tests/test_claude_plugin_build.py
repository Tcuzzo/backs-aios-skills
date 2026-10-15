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
