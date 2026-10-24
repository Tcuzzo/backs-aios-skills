"""Public pack must never teach model-family diversity as a shipping gate."""

from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_SURFACES = (
    "skills/blind-tribunal/SKILL.md",
    "skills/design-taste/SKILL.md",
    "i18n/hi/NAMING.md",
)
FORBIDDEN = (
    "cross-family",
    "family-disjoint",
    "different model families",
)


@pytest.mark.parametrize("relative", ACTIVE_SURFACES)
def test_active_public_guidance_never_requires_model_family_diversity(relative: str) -> None:
    body = (ROOT / relative).read_text(encoding="utf-8").lower()
    for phrase in FORBIDDEN:
        assert phrase not in body, f"{relative} still carries family gate {phrase!r}"
