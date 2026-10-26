"""Run the truth-audit tool regressions (ledger gates, scope gates, tree hashing) in CI."""
from pathlib import Path
import os
import subprocess
import sys
import unittest

SKILL = Path(__file__).resolve().parents[1] / "skills" / "truth-audit"


class TruthAuditToolsTest(unittest.TestCase):
    def test_tool_regressions(self):
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(SKILL / "scripts"), "-p", "test_*.py", "-v"],
            text=True, capture_output=True, timeout=120,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_skill_ships_the_references_it_names(self):
        body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for name in ("lane_prompt.md", "lane_format.md", "plan_template.md", "coder_prompt.md",
                     "live_truth_checklist.md"):
            with self.subTest(reference=name):
                self.assertTrue((SKILL / "references" / name).is_file())
        for name in ("ledger.py", "ball_scope_check.py", "cmp_trees.py"):
            with self.subTest(script=name):
                self.assertTrue((SKILL / "scripts" / name).is_file())
                self.assertIn(f"scripts/{name}", body)


if __name__ == "__main__":
    unittest.main()
