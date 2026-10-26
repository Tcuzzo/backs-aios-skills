"""Run the truth-audit tool regressions (ledger gates, scope gates, tree hashing) in CI."""
from pathlib import Path
import os
import re
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

    def test_ledger_tamper_claim_matches_the_tool(self):
        # The skill may only claim what ledger.py check detects: edits via the hash
        # chain, truncation via the head file kept beside the ledger.
        body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(".head", body)
        self.assertIn("truncat", body)

    def test_examples_carry_no_domain_residue(self):
        texts = [(SKILL / "SKILL.md").read_text(encoding="utf-8")]
        texts += [p.read_text(encoding="utf-8") for p in (SKILL / "references").glob("*.md")]
        # Fixtures teach by example too: eval inputs and script test fixtures are scanned.
        texts += [p.read_text(encoding="utf-8") for p in (SKILL / "evals").rglob("*.md")]
        texts += [p.read_text(encoding="utf-8") for p in (SKILL / "scripts").glob("*.py")]
        self.assertGreater(len(texts), 10)
        for token in ("price bars", "/v2/bars", "bar data", "/api/positions", "buyers", '"positions"', "money path",
                      "paper or sandbox"):
            for text in texts:
                with self.subTest(token=token):
                    self.assertNotIn(token, text.lower())

    def test_close_out_text_matches_list_semantics(self):
        # `list --open` hides terminal entries, adjudicated ones included.
        tpl = (SKILL / "references" / "plan_template.md").read_text(encoding="utf-8")
        self.assertNotIn("prints only adjudicated", tpl)
        self.assertIn("`ledger.py list --open` prints nothing", tpl)
        self.assertIn("`ledger.py list`", tpl)

    def test_recorded_builder_is_documented(self):
        # IN-BUILD must name the builder; every doc that shows the move says how.
        for path in (SKILL / "SKILL.md", SKILL / "references" / "plan_template.md",
                     SKILL / "references" / "coder_prompt.md"):
            with self.subTest(doc=path.name):
                self.assertIn("--builder", path.read_text(encoding="utf-8"))

    def test_scope_hash_contract_is_documented(self):
        for name in ("plan_template.md", "coder_prompt.md"):
            with self.subTest(reference=name):
                self.assertIn("@sha256:", (SKILL / "references" / name).read_text(encoding="utf-8"))

    def test_eval_lane_fix_seams_sit_inside_the_ball_scope(self):
        sys.path.insert(0, str(SKILL / "scripts"))
        try:
            import ball_scope_check
            import ledger
        finally:
            sys.path.pop(0)
        case = SKILL / "evals" / "coder-prompt-for-one-ball" / "files"
        ball = ball_scope_check.find_ball((case / "PLAN.md").read_text(encoding="utf-8"), "1A")
        scope = ball_scope_check.scope_paths(ball["lines"])
        blocks = ledger.parse_lane((case / "lanes" / "SVC_SERVICE.md").read_text(encoding="utf-8"))
        cited = [b for b in blocks if b["id"] in {"SVC-01", "SVC-02"}]
        self.assertEqual(2, len(cited))
        for block in cited:
            for path in re.findall(r"`([^`\s]+\.[A-Za-z]+)`", block["fix_seam"]):
                with self.subTest(finding=block["id"], path=path):
                    self.assertTrue(ball_scope_check.in_scope(path, scope), scope)

    def test_readme_catalog_lists_the_skill(self):
        readme = (SKILL.parents[1] / "README.md").read_text(encoding="utf-8")
        self.assertIn("| [truth-audit](skills/truth-audit/SKILL.md) |", readme)


if __name__ == "__main__":
    unittest.main()
