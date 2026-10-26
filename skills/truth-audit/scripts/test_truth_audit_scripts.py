"""Regression tests for the truth-audit tools. Stdlib only:
python -m unittest discover -s <this dir> -p "test_*.py"
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import ball_scope_check  # noqa: E402
import cmp_trees  # noqa: E402
import ledger  # noqa: E402

LANE = """# Lane SVC · service loop

Isolation: read-only.

### SVC-01 · P0 · Worker retries forever on a rejected credential
- status: OPEN · confidence: high
- surface: background worker behind the main window
- evidence (read-only, service log):
  - `service.log`: 602 of 602 loop errors today are HTTP 401
  - heartbeat state is "error"
- root cause (theater): the loop swallows every exception
- root cause (product): the credential was rotated
- fix seam: `runtime/loop.py` run_forever
- proof of done: an injected 401 in a sandbox stops the loop and shows one alert

### SVC-02 | P2 | Health page says green while the worker is down
* **Surface and evidence:** `GET /health` returns ok=true while heartbeat says error
* **Fix-seam**: `health.py` health()
* **Proof:** health is red within one loop of the injected failure

### SVC-03 · P3 · The bar data is real (checked against the provider)
- status: ADJUDICATED-NOT-A-BUG · confidence: high
- evidence: 20 random rows match the provider's API byte for byte

### SVC-04 · P1 · No evidence here
- status: OPEN · confidence: low
- fix seam: somewhere
- proof of done: something

## Side effects
none
"""

PLAN = """# Plan

## Wave 1 - Stop the bleeding

#### Ball 1A · Loop tells the truth - SVC-01
**Scope:** `runtime/loop.py`, `tests/test_loop.py` (new)

#### Ball 1B · Health - SVC-02
**Scope:** `health.py`, `tests/test_health.py`
**Scope (OPS):** `OPS/deploy/unit.service`

## Wave 2 - Next

#### Ball 2A · Again
**Scope:** `runtime/loop.py`

#### Ball 2B · Clash
**Scope:** `runtime/*.py`
"""


class LedgerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)
        self.path = self.dir / "ledger.jsonl"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_ledger(self, *args: str) -> int:
        return ledger.main(["--ledger", str(self.path), *args])

    def add(self, eid: str = "SVC-09", sev: str = "P1", **kw: str) -> int:
        args = ["add", "--id", eid, "--sev", sev, "--title", "t", "--evidence", kw.get("evidence", "cmd -> out"),
                "--fix-seam", "x.py", "--proof", "observed", "--by", kw.get("by", "coordinator")]
        if "task" in kw:
            args += ["--task", kw["task"]]
        return self.run_ledger(*args)

    def test_duplicate_id_refused(self) -> None:
        self.assertEqual(0, self.add())
        self.assertEqual(1, self.add())

    def test_missing_evidence_refused(self) -> None:
        self.assertEqual(1, self.add(evidence="  "))

    def test_backward_move_refused(self) -> None:
        self.add(task="1A")
        self.assertEqual(0, self.run_ledger("status", "SVC-09", "IN-BUILD", "--by", "coordinator"))
        self.assertEqual(1, self.run_ledger("status", "SVC-09", "PLANNED", "--by", "coordinator"))

    def test_p1_needs_task_before_in_build(self) -> None:
        self.add()
        self.assertEqual(1, self.run_ledger("status", "SVC-09", "IN-BUILD", "--by", "coordinator"))
        self.assertEqual(0, self.run_ledger("status", "SVC-09", "PLANNED", "--by", "coordinator", "--task", "1A"))
        self.assertEqual(0, self.run_ledger("status", "SVC-09", "IN-BUILD", "--by", "coordinator"))

    def test_p2_may_build_without_task(self) -> None:
        self.add(sev="P2")
        self.assertEqual(0, self.run_ledger("status", "SVC-09", "IN-BUILD", "--by", "coordinator"))

    def test_proven_and_closed_need_evidence(self) -> None:
        self.add(task="1A")
        self.run_ledger("status", "SVC-09", "IN-BUILD", "--by", "builder")
        self.assertEqual(1, self.run_ledger("status", "SVC-09", "PROVEN", "--by", "reader"))
        self.assertEqual(0, self.run_ledger("status", "SVC-09", "PROVEN", "--by", "reader", "--evidence", "row 7"))
        self.assertEqual(1, self.run_ledger("status", "SVC-09", "CLOSED", "--by", "grader"))

    def test_builder_or_prover_cannot_close(self) -> None:
        self.add(task="1A")
        self.run_ledger("status", "SVC-09", "IN-BUILD", "--by", "builder")
        self.run_ledger("status", "SVC-09", "PROVEN", "--by", "reader", "--evidence", "row 7")
        self.assertEqual(1, self.run_ledger("status", "SVC-09", "CLOSED", "--by", "builder", "--evidence", "x"))
        self.assertEqual(1, self.run_ledger("status", "SVC-09", "CLOSED", "--by", "reader", "--evidence", "x"))
        self.assertEqual(0, self.run_ledger("status", "SVC-09", "CLOSED", "--by", "grader", "--evidence", "run 3"))
        self.assertEqual(1, self.run_ledger("status", "SVC-09", "ADJUDICATED-NOT-A-BUG", "--by", "g",
                                            "--evidence", "x"))
        self.assertEqual(0, self.run_ledger("check"))

    def test_adjudication_needs_evidence(self) -> None:
        self.add()
        self.assertEqual(1, self.run_ledger("status", "SVC-09", "ADJUDICATED-NOT-A-BUG", "--by", "c"))
        self.assertEqual(0, self.run_ledger("status", "SVC-09", "ADJUDICATED-NOT-A-BUG", "--by", "c",
                                            "--evidence", "re-ran: data matches"))

    def test_check_catches_hand_edit_and_rule_break(self) -> None:
        self.add()
        self.add(eid="SVC-10")
        self.assertEqual(0, self.run_ledger("check"))
        lines = self.path.read_text(encoding="utf-8").splitlines()
        first = json.loads(lines[0])
        first["evidence"] = "rewritten later"
        lines[0] = json.dumps(first, sort_keys=True)
        self.path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assertEqual(1, self.run_ledger("check"))

    def test_check_replays_rules_over_appended_lines(self) -> None:
        self.add()
        # Someone bypasses the tool and appends an illegal close with a valid chain link.
        ledger.append(self.path, {"kind": "status", "id": "SVC-09", "status": "CLOSED", "by": "x", "evidence": ""})
        self.assertEqual(1, self.run_ledger("check"))

    def test_import_lane_tolerates_variants_and_keeps_positive_findings(self) -> None:
        lane = self.dir / "SVC_SERVICE.md"
        lane.write_text(LANE, encoding="utf-8")
        rc = self.run_ledger("import-lane", str(lane), "--by", "ledger-keeper")
        self.assertEqual(1, rc, "SVC-04 has no evidence and must be refused")
        entries, problems = ledger.fold(ledger.read_events(self.path))
        self.assertEqual([], problems)
        self.assertEqual({"SVC-01", "SVC-02", "SVC-03"}, set(entries))
        self.assertIn("602 of 602", entries["SVC-01"]["evidence"])
        self.assertIn("(read-only, service log)", entries["SVC-01"]["evidence"])
        self.assertIn("theater", entries["SVC-01"]["root_cause"])
        self.assertIn("product", entries["SVC-01"]["root_cause"])
        self.assertEqual("high", entries["SVC-01"]["confidence"])
        self.assertIn("/health", entries["SVC-02"]["evidence"])
        self.assertEqual("health.py health()", entries["SVC-02"]["fix_seam"].replace("`", ""))
        self.assertEqual("ADJUDICATED-NOT-A-BUG", entries["SVC-03"]["status"])
        # Re-import is idempotent.
        self.run_ledger("import-lane", str(lane), "--by", "ledger-keeper")
        self.assertEqual(4, len(ledger.read_lines(self.path)))
        self.assertEqual(0, self.run_ledger("check"))

    def test_render_writes_status_board(self) -> None:
        self.add()
        self.assertEqual(0, self.run_ledger("render"))
        text = (self.dir / "STATUS.md").read_text(encoding="utf-8")
        self.assertIn("| SVC-09 | P1 | OPEN |", text)


class ScopeCheckTest(unittest.TestCase):
    def test_parse_and_scope(self) -> None:
        ball = ball_scope_check.find_ball(PLAN, "1B")
        self.assertEqual(["health.py", "tests/test_health.py", "OPS/deploy/unit.service"],
                         ball_scope_check.scope_paths(ball["lines"]))
        self.assertEqual(["health.py", "tests/test_health.py", "deploy/unit.service"],
                         ball_scope_check.scope_paths(ball["lines"], "OPS"))
        self.assertEqual(["health.py", "tests/test_health.py"],
                         ball_scope_check.scope_paths(ball["lines"], "APP"))

    def test_in_scope(self) -> None:
        scope = ["runtime/loop.py", "tests/*.py"]
        self.assertTrue(ball_scope_check.in_scope("src/pkg/runtime/loop.py", scope))
        self.assertTrue(ball_scope_check.in_scope("tests/test_loop.py", scope))
        self.assertFalse(ball_scope_check.in_scope("runtime/other.py", scope))

    def test_disjoint_flags_shared_files_in_a_wave_only(self) -> None:
        problems = ball_scope_check.overlaps(PLAN)
        self.assertEqual(1, len(problems), problems)
        self.assertIn("2A and 2B", problems[0])

    def test_branch_out_of_scope_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = pathlib.Path(raw)
            env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
                   "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"}

            def git(*a: str) -> None:
                subprocess.run(["git", "-c", "safe.directory=*", "-C", str(repo), *a],
                               check=True, capture_output=True, env=env)
            git("init", "-q", "-b", "main")
            (repo / "health.py").write_text("x\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-q", "-m", "base")
            git("switch", "-q", "-c", "ball/1B")
            (repo / "health.py").write_text("y\n", encoding="utf-8")
            git("add", "health.py")
            git("commit", "-q", "-m", "fix")
            plan = pathlib.Path(raw + "-plan.md")
            plan.write_text(PLAN, encoding="utf-8")
            self.addCleanup(plan.unlink)
            args = ["1B", "--plan", str(plan), "--repo", str(repo), "--base", "main"]
            self.assertEqual(0, ball_scope_check.main(args))
            # An untracked drive-by file is a change outside the ball's scope.
            (repo / "other.py").write_text("z\n", encoding="utf-8")
            self.assertEqual(1, ball_scope_check.main(args))
            # A coordinator ball with no Scope line is reported, not silently passed.
            plan.write_text(PLAN + "\n#### Ball 0.1 · Freeze what runs (coordinator)\n- [ ] snapshot\n",
                            encoding="utf-8")
            self.assertEqual(2, ball_scope_check.main(["0.1", "--plan", str(plan), "--repo", str(repo)]))


class CmpTreesTest(unittest.TestCase):
    def test_crlf_is_equal_and_content_change_is_not(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            a, b = pathlib.Path(raw, "a"), pathlib.Path(raw, "b")
            for d in (a, b):
                (d / "src").mkdir(parents=True)
                (d / "__pycache__").mkdir()
            (a / "src" / "m.py").write_bytes(b"x = 1\r\ny = 2\r\n")
            (b / "src" / "m.py").write_bytes(b"x = 1\ny = 2\n")
            (a / "__pycache__" / "junk.txt").write_bytes(b"1")
            (b / "__pycache__" / "junk.txt").write_bytes(b"2")
            self.assertEqual(0, cmp_trees.main([str(a), str(b)]))
            (b / "src" / "m.py").write_bytes(b"x = 1\ny = 3\n")
            (b / "only_b.txt").write_bytes(b"new")
            res = cmp_trees.compare(cmp_trees.walk(str(a), cmp_trees.DEFAULT_SKIP),
                                    cmp_trees.walk(str(b), cmp_trees.DEFAULT_SKIP))
            self.assertEqual(["src/m.py"], res["changed"])
            self.assertEqual(["only_b.txt"], res["only_b"])
            self.assertEqual(1, cmp_trees.main([str(a), str(b)]))

    def test_missing_dir_is_loud(self) -> None:
        self.assertEqual(2, cmp_trees.main(["no-such-dir-a", "no-such-dir-b"]))


if __name__ == "__main__":
    unittest.main()
