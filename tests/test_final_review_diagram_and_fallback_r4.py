"""Final review catches diagram contradictions and incomplete fallback text."""
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[1]
PATHS = ['skills/turn-and-burn/SKILL.md', 'i18n/de/skills/turn-and-burn/SKILL.md', 'i18n/es/skills/turn-and-burn/SKILL.md', 'i18n/fr/skills/turn-and-burn/SKILL.md', 'i18n/hi/skills/turn-and-burn/SKILL.md', 'i18n/pt-BR/skills/turn-and-burn/SKILL.md', 'i18n/zh-CN/skills/turn-and-burn/SKILL.md']

@pytest.mark.parametrize("path", PATHS)
def test_fallback_paragraph_is_complete_and_uses_measured_configured_routes(path):
    body=(ROOT/path).read_text()
    paragraph=body.split("**Do not bench a model for a single 429.**",1)[1].split("## Cross-references",1)[0]
    text=" ".join(paragraph.split())
    assert "configured, live-preflighted rung" in text
    assert "sufficient" in text and "checkpoint" in text and "bounded backoff" in text
    assert "(qwen +" not in text and "deepseek)" not in text
    assert text.endswith(".")

@pytest.mark.parametrize("path", PATHS)
def test_decision_bar_is_not_mislabeled_as_the_canonical_three_laws(path):
    text=" ".join((ROOT/path).read_text().split())
    assert "3-laws gate (taste" not in text
    assert "existing decision bar (taste, vision, destructive risk)" in text


def test_portuguese_diagram_uses_session_independence():
    text=(ROOT/"i18n/pt-BR/plays/grading-verification.md").read_text()
    assert "builder + grader families differ" not in text
    assert "fresh author-disjoint review" in text
