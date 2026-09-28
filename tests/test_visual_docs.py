from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VisualDocumentationContractTest(unittest.TestCase):
    def test_readme_links_the_visual_guide(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("[Visual guide](docs/FLOWCHARTS.md)", readme)

    def test_visual_guide_covers_every_skill_and_play(self) -> None:
        guide = (ROOT / "docs" / "FLOWCHARTS.md").read_text(encoding="utf-8")
        skills = {
            path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")
        }
        plays = {path.stem for path in (ROOT / "plays").glob("*.md")}

        self.assertEqual(36, len(skills))
        self.assertEqual(8, len(plays))
        for skill in sorted(skills):
            with self.subTest(skill=skill):
                self.assertIn(f"../skills/{skill}/SKILL.md", guide)
        for play in sorted(plays):
            with self.subTest(play=play):
                self.assertIn(f"../plays/{play}.md", guide)

    def test_each_chart_is_accessible_and_has_a_terminal_fallback(self) -> None:
        guide = (ROOT / "docs" / "FLOWCHARTS.md").read_text(encoding="utf-8")
        charts = re.findall(r"```mermaid\n(.*?)\n```", guide, flags=re.DOTALL)

        self.assertGreaterEqual(len(charts), 7)
        self.assertEqual(len(charts), guide.count("<summary>Text version</summary>"))
        for index, chart in enumerate(charts, start=1):
            with self.subTest(chart=index):
                self.assertIn("accTitle:", chart)
                self.assertIn("accDescr:", chart)


if __name__ == "__main__":
    unittest.main()
