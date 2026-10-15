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

    def test_every_surface_records_verification_and_sizes_its_context(self) -> None:
        """Record verification state and size context for the complete artifact.

        Required task votes remain required; optional verifier outages do not
        invalidate an otherwise sufficient independent review.
        """
        for path in self.surfaces():
            text = path.read_text(encoding="utf-8")
            with self.subTest(surface=str(path.relative_to(ROOT))):
                self.assertIn("UNVERIFIED", text)
                self.assertIn("num_ctx", text)

    def test_every_surface_records_unverified_state_reads_only_and_carries_a_run_id(self) -> None:
        """Jurors are read-only and record run identity and verification state.

        UNVERIFIED is evidence status, not an unconditional optional-vote veto.
        """
        for path in self.surfaces():
            text = path.read_text(encoding="utf-8")
            with self.subTest(surface=str(path.relative_to(ROOT))):
                self.assertIn("read-only", text)
                self.assertIn("run_id", text)
                self.assertIn("UNVERIFIED", text)

    def test_every_surface_owns_its_evidence_and_what_it_sweeps(self) -> None:
        """A pass carrying a [blocker] is refused; the out dir is owned
        (stamp) before it is swept; evidence is 0600;
        a rewritten already-dirty file is named (changed_paths); a proof harness must be
        able to say INVALID. Session independence is covered by the review-policy
        contracts; requiring a nonexistent --builder option would not prove it.
        """
        for path in self.surfaces():
            text = path.read_text(encoding="utf-8")
            with self.subTest(surface=str(path.relative_to(ROOT))):
                for token in ("[blocker]", "0600", "changed_paths", "INVALID"):
                    self.assertIn(token, text, f"{token} missing")

    def test_every_surface_names_the_lens_in_the_footer_and_keeps_a_rejected_rungs_words(self) -> None:
        """0.8.4/0.8.5 (tribunal rounds 4 and 6): the footer carries the
        literal lens, never the placeholder; a rejected rung keeps a bounded raw_tail; every
        selected rung declares context_tokens for its actual workload. The
        canonical recipe fills the placeholder at render time. Tokens ride every language."""
        for path in self.surfaces():
            text = path.read_text(encoding="utf-8")
            with self.subTest(surface=str(path.relative_to(ROOT))):
                for token in ('"lens": "defect"', "<your lens>", "raw_tail", "context_tokens", "reasoning_effort: none", "finish_reason=length"):
                    self.assertIn(token, text, f"{token} missing")
        canonical = (ROOT / "skills" / "blind-tribunal" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('protocol.replace("<your lens>", lens)', canonical)

    def test_no_surface_still_seats_three_jurors(self) -> None:
        stale = ("Three jurors", "three jurors", "Tres jurados", "Trois jurés", "Drei Juroren", "Três jurados", "तीन jurors", "三位陪审员")
        for path in self.surfaces():
            text = path.read_text(encoding="utf-8")
            with self.subTest(surface=str(path.relative_to(ROOT))):
                self.assertEqual([], [s for s in stale if s in text])


if __name__ == "__main__":
    unittest.main()
