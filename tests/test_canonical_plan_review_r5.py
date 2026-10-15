from pathlib import Path

def test_plan_review_preserves_quorum_and_session_independence():
    text=" ".join((Path(__file__).resolve().parents[1]/"skills/turn-and-burn/SKILL.md").read_text().split())
    paragraph=text.split("**Quick tribunal on plan + design.**",1)[1].split("5.",1)[0]
    assert "at least 2 independent jurors" in paragraph
    assert "fresh, author-disjoint sessions" in paragraph
    assert "Builder ≠ grader" in paragraph
    assert "cross-family seats" not in paragraph
