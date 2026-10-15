"""Active instructions must not turn model/vendor identity into review authority."""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATTERNS = (
    r"grader model MUST be a different model FAMILY",
    r"Builder and grader share a model family",
    r"grader is a different model family",
    r"a DIFFERENT model family than the builder",
    r"graders from a different model family than the builder",
    r"Cross-family grade must pass",
    r"Every rung of that family is refused",
    r"Same vendor = same family",
    r"Never route heavy planning.*through ollama cloud",
    r"Builder and grader never resolve to the same model",
)


class TaskRoutingPlaybooks(unittest.TestCase):
    def test_active_playbooks_and_direct_skills_have_no_identity_gate(self):
        files = list((ROOT / "plays").glob("*.md"))
        files += list((ROOT / "command-adapters").glob("*.md"))
        files += list((ROOT / "skills").glob("*/SKILL.md"))
        findings = []
        for path in files:
            text = path.read_text()
            for pattern in PATTERNS:
                if re.search(pattern, text, flags=re.I | re.S):
                    findings.append((str(path.relative_to(ROOT)), pattern))
        self.assertEqual([], findings)

    def test_grading_play_requires_blind_evidence_not_just_a_new_name(self):
        text = (ROOT / "plays/grading-verification.md").read_text().lower()
        for requirement in ("fresh", "author-redacted", "conversation", "session",
                            "exact", "evidence", "fail-to-pass", "pass-to-pass"):
            self.assertIn(requirement, text)

    def test_routing_skill_separates_access_from_capability(self):
        text = (ROOT / "skills/fleet-ladder/SKILL.md").read_text().lower()
        for requirement in ("task", "capability", "oauth", "api", "quota",
                            "harness", "local", "essence", "checkpoint"):
            self.assertIn(requirement, text)


if __name__ == "__main__":
    unittest.main()
