"""The eight tribunal lenses are one set across the canonical skill, every locale,
and the command adapter — a surface that names fewer lenses is stale."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("de", "es", "fr", "hi", "pt-BR", "zh-CN")
LENSES = (
    "defect",
    "proportion",
    "operator_consequence",
    "reversibility",
    "state_continuity",
    "resource_economy",
    "boundary_condition",
    "telemetry",
)
TIERS = ("deep_state", "fast_structural", "operator_safety", "generalist")


class TribunalLensesTest(unittest.TestCase):
    def surfaces(self) -> list[Path]:
        return [
            ROOT / "skills" / "blind-tribunal" / "SKILL.md",
            ROOT / "command-adapters" / "tribunal.md",
            *(ROOT / "i18n" / locale / "skills" / "blind-tribunal" / "SKILL.md" for locale in LOCALES),
        ]

    def test_every_surface_names_all_eight_lens_ids(self) -> None:
        for path in self.surfaces():
            text = path.read_text(encoding="utf-8")
            with self.subTest(surface=str(path.relative_to(ROOT))):
                missing = [lens for lens in LENSES if lens not in text]
                self.assertEqual([], missing)

    def test_canonical_skill_carries_the_portable_render_recipe_and_protocol(self) -> None:
        text = (ROOT / "skills" / "blind-tribunal" / "SKILL.md").read_text(encoding="utf-8")
        for tier in TIERS:
            self.assertIn(tier, text)
        self.assertIn("CRITICAL OUTPUT PROTOCOL", text)
        self.assertIn('"verdict": "pass" | "refuse"', text)
        self.assertIn("PRIOR_ADJUDICATIONS", text)
        self.assertIn("hold", text)

    def test_no_surface_still_seats_three_jurors(self) -> None:
        stale = ("Three jurors", "three jurors", "Tres jurados", "Trois jurés", "Drei Juroren", "Três jurados", "तीन jurors", "三位陪审员")
        for path in self.surfaces():
            text = path.read_text(encoding="utf-8")
            with self.subTest(surface=str(path.relative_to(ROOT))):
                self.assertEqual([], [s for s in stale if s in text])


if __name__ == "__main__":
    unittest.main()
