from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SKILL = Path(__file__).resolve().parents[1] / "skills" / "karpathy"
TEST_TMP_ROOT = Path(__file__).resolve().parents[1] / "sandbox"
TEST_TMP_ROOT.mkdir(exist_ok=True)
sys.path.insert(0, str(SKILL))
from evolve import Metric, MetricField, cleanup_sandbox, prepare_sandbox  # noqa: E402
from program import ProgramError, parse_program, run_program  # noqa: E402


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True,
                          capture_output=True, text=True).stdout.strip()


def source_repo(root: Path) -> Path:
    repo = root / "source"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Test")
    git(repo, "config", "user.email", "test@example.com")
    (repo / "allowed.txt").write_text("10\n", encoding="utf-8")
    (repo / "forbidden.txt").write_text("fixed\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "baseline")
    return repo


def program() -> str:
    return """# Test improvement
## Goal
Lower cost without changing the evaluator.
## Metric
- cost | min | 10
## Fair game
- allowed.txt
## Budget
rounds: 1
## Sandbox
required: true
"""


def score_candidate(repo: Path) -> dict[str, float]:
    return {"cost": float((repo / "allowed.txt").read_text().strip())}


def cleanup(result: dict) -> None:
    cleanup_sandbox(result["sandbox_dir"])


class KarpathyBundleTest(unittest.TestCase):
    def test_sandbox_typo_is_rejected(self) -> None:
        with self.assertRaisesRegex(ProgramError, "Sandbox required must be true"):
            parse_program(program().replace("required: true", "required: tru"))

    def test_one_gated_metric_can_improve(self) -> None:
        metric = Metric([MetricField("success_rate", "max", 0.95)])
        self.assertTrue(metric.dominates({"success_rate": 0.96}, {"success_rate": 0.90}))
        self.assertFalse(metric.dominates({"success_rate": 0.94}, {"success_rate": 0.90}))

    def test_nonfinite_and_boolean_metrics_are_rejected(self) -> None:
        metric = Metric([MetricField("score", "max", 0.5)])
        for invalid in (float("nan"), float("inf"), -float("inf"), True):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(Exception, "finite number"):
                    metric.dominates({"score": invalid}, {"score": 0.5})
                with self.assertRaisesRegex(Exception, "finite number"):
                    metric.dominates({"score": 0.6}, {"score": invalid})
        with self.assertRaisesRegex(ProgramError, "gate must be finite"):
            parse_program(program().replace("cost | min | 10", "cost | min | Infinity"))

    def test_forbidden_edit_cannot_be_kept(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))

            def propose(repo: Path) -> None:
                (repo / "forbidden.txt").write_text("tampered\n", encoding="utf-8")

            result = run_program(parse_program(program()), target_dir=source,
                                 propose=propose, test=lambda _: {"cost": 1.0},
                                 sandbox_root=TEST_TMP_ROOT)
            try:
                clone = Path(result["sandbox_dir"])
                self.assertEqual(0, result["kept"])
                self.assertIn("outside Fair game", result["errors"][0])
                self.assertEqual("fixed\n", (clone / "forbidden.txt").read_text())
                self.assertEqual("", git(clone, "status", "--porcelain"))
                self.assertEqual("fixed\n", (source / "forbidden.txt").read_text())
            finally:
                cleanup(result)

    def test_staged_and_ignored_edits_revert(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))

            def propose(repo: Path) -> None:
                (repo / "allowed.txt").write_text("1\n", encoding="utf-8")
                git(repo, "add", "allowed.txt")
                (repo / ".pytest_cache").mkdir()
                (repo / ".pytest_cache" / "artifact").write_text("hidden")

            result = run_program(parse_program(program()), target_dir=source,
                                 propose=propose, test=score_candidate,
                                 sandbox_root=TEST_TMP_ROOT)
            try:
                clone = Path(result["sandbox_dir"])
                self.assertEqual(0, result["kept"])
                self.assertIn("outside Fair game", result["errors"][0])
                self.assertEqual("10\n", (clone / "allowed.txt").read_text())
                self.assertFalse((clone / ".pytest_cache").exists())
                self.assertEqual("", git(clone, "status", "--porcelain"))
            finally:
                cleanup(result)

    def test_kept_round_changes_only_allowed_file_and_log_stays_outside(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))

            def propose(repo: Path) -> None:
                (repo / "allowed.txt").write_text("1\n", encoding="utf-8")

            result = run_program(parse_program(program()), target_dir=source,
                                 propose=propose, test=score_candidate,
                                 sandbox_root=TEST_TMP_ROOT)
            try:
                clone = Path(result["sandbox_dir"])
                self.assertEqual(1, result["kept"])
                self.assertEqual("1\n", (clone / "allowed.txt").read_text())
                self.assertEqual("10\n", (source / "allowed.txt").read_text())
                self.assertEqual("allowed.txt", git(clone, "show", "--format=", "--name-only", "HEAD"))
                self.assertFalse(Path(result["log"]).is_relative_to(clone))
                self.assertEqual("", git(clone, "status", "--porcelain"))
            finally:
                cleanup(result)

    def test_penalty_hook_cannot_mutate_candidate(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))

            def propose(repo: Path) -> None:
                (repo / "allowed.txt").write_text("1\n", encoding="utf-8")

            def penalty(repo: Path) -> float:
                (repo / "allowed.txt").write_text("0\n", encoding="utf-8")
                return 0

            result = run_program(parse_program(program()), target_dir=source,
                                 propose=propose, test=score_candidate, penalty=penalty,
                                 sandbox_root=TEST_TMP_ROOT)
            try:
                clone = Path(result["sandbox_dir"])
                self.assertEqual(0, result["kept"])
                self.assertIn("penalty hook modified", result["errors"][0])
                self.assertEqual("10\n", (clone / "allowed.txt").read_text())
                self.assertEqual("", git(clone, "status", "--porcelain"))
            finally:
                cleanup(result)

    def test_evaluator_cannot_change_candidate_index_mode(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))
            eval_program = program().replace(
                "## Budget", "## Eval\ncmd: git update-index --chmod=+x allowed.txt\n## Budget"
            )

            def propose(repo: Path) -> None:
                (repo / "allowed.txt").write_text("1\n", encoding="utf-8")

            result = run_program(parse_program(eval_program), target_dir=source,
                                 propose=propose, test=score_candidate,
                                 sandbox_root=TEST_TMP_ROOT)
            try:
                clone = Path(result["sandbox_dir"])
                self.assertEqual(0, result["kept"])
                self.assertIn("evaluation modified candidate files", result["errors"][0])
                self.assertEqual("10\n", (clone / "allowed.txt").read_text())
                self.assertEqual("100644", git(clone, "ls-files", "--stage", "allowed.txt")[:6])
            finally:
                cleanup(result)

    def test_proposer_commit_cannot_hide_forbidden_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))

            def propose(repo: Path) -> None:
                (repo / "allowed.txt").write_text("1\n", encoding="utf-8")
                (repo / "forbidden.txt").write_text("tampered\n", encoding="utf-8")
                git(repo, "add", ".")
                git(repo, "commit", "-q", "-m", "hidden change")

            result = run_program(parse_program(program()), target_dir=source,
                                 propose=propose, test=score_candidate,
                                 sandbox_root=TEST_TMP_ROOT)
            try:
                clone = Path(result["sandbox_dir"])
                self.assertEqual(0, result["kept"])
                self.assertIn("proposer changed Git HEAD", result["errors"][0])
                self.assertEqual("fixed\n", (clone / "forbidden.txt").read_text())
                self.assertEqual("10\n", (clone / "allowed.txt").read_text())
                self.assertEqual("baseline", git(clone, "log", "-1", "--format=%s"))
            finally:
                cleanup(result)

    def test_rejected_nested_git_repository_is_removed(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))

            def propose(repo: Path) -> None:
                nested = repo / "nested"
                nested.mkdir()
                git(nested, "init", "-q")

            result = run_program(parse_program(program()), target_dir=source,
                                 propose=propose, test=score_candidate,
                                 sandbox_root=TEST_TMP_ROOT)
            try:
                clone = Path(result["sandbox_dir"])
                self.assertEqual(0, result["kept"])
                self.assertFalse((clone / "nested").exists())
                self.assertEqual("", git(clone, "status", "--porcelain"))
            finally:
                cleanup(result)

    def test_proposer_git_hook_mutation_aborts_experiment(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))
            created: list[Path] = []

            def capture(target: Path, sandbox_root=None) -> Path:
                clone = prepare_sandbox(target, sandbox_root=sandbox_root)
                created.append(clone)
                return clone

            def propose(repo: Path) -> None:
                (repo / "allowed.txt").write_text("1\n", encoding="utf-8")
                hook = repo / ".git" / "hooks" / "pre-commit"
                hook.write_text(
                    "#!/usr/bin/env python3\n"
                    "from pathlib import Path\n"
                    "import subprocess\n"
                    "Path('forbidden.txt').write_text('tampered\\n')\n"
                    "subprocess.run(['git', 'add', 'forbidden.txt'], check=True)\n",
                    encoding="utf-8",
                )
                os.chmod(hook, 0o755)

            with patch("evolve.prepare_sandbox", side_effect=capture):
                with self.assertRaisesRegex(Exception, "Git control metadata"):
                    run_program(parse_program(program()), target_dir=source,
                                propose=propose, test=score_candidate,
                                sandbox_root=TEST_TMP_ROOT)
            self.assertEqual(1, len(created))
            self.assertFalse(created[0].parent.exists())

    def test_engine_commit_does_not_execute_git_hooks(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))

            def prepared(target: Path, sandbox_root=None) -> Path:
                clone = prepare_sandbox(target, sandbox_root=sandbox_root)
                hook = clone / ".git" / "hooks" / "pre-commit"
                hook.write_text(
                    "#!/usr/bin/env python3\n"
                    "from pathlib import Path\n"
                    "import subprocess\n"
                    "Path('forbidden.txt').write_text('tampered\\n')\n"
                    "subprocess.run(['git', 'add', 'forbidden.txt'], check=True)\n",
                    encoding="utf-8",
                )
                os.chmod(hook, 0o755)
                return clone

            def propose(repo: Path) -> None:
                (repo / "allowed.txt").write_text("1\n", encoding="utf-8")

            with patch("evolve.prepare_sandbox", side_effect=prepared):
                result = run_program(parse_program(program()), target_dir=source,
                                     propose=propose, test=score_candidate,
                                     sandbox_root=TEST_TMP_ROOT)
            try:
                clone = Path(result["sandbox_dir"])
                self.assertEqual(1, result["kept"], result["round_results"])
                self.assertEqual("fixed\n", (clone / "forbidden.txt").read_text())
                self.assertEqual("allowed.txt", git(clone, "show", "--format=", "--name-only", "HEAD"))
            finally:
                cleanup(result)

    def test_evaluator_commit_cannot_hide_forbidden_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))
            (source / "tamper.py").write_text(
                "from pathlib import Path\n"
                "import subprocess\n"
                "Path('forbidden.txt').write_text('tampered\\n')\n"
                "subprocess.run(['git', 'add', 'forbidden.txt'], check=True)\n"
                "subprocess.run(['git', 'commit', '-q', '-m', 'evaluator tamper'], check=True)\n",
                encoding="utf-8",
            )
            git(source, "add", ".")
            git(source, "commit", "-q", "-m", "add evaluator")
            eval_program = program().replace("## Budget", "## Eval\ncmd: python tamper.py\n## Budget")

            def propose(repo: Path) -> None:
                (repo / "allowed.txt").write_text("1\n", encoding="utf-8")

            result = run_program(parse_program(eval_program), target_dir=source,
                                 propose=propose, test=score_candidate,
                                 sandbox_root=TEST_TMP_ROOT)
            try:
                clone = Path(result["sandbox_dir"])
                self.assertEqual(0, result["kept"])
                self.assertIn("evaluation changed Git HEAD", result["errors"][0])
                self.assertEqual("fixed\n", (clone / "forbidden.txt").read_text())
                self.assertEqual("10\n", (clone / "allowed.txt").read_text())
                self.assertEqual("add evaluator", git(clone, "log", "-1", "--format=%s"))
            finally:
                cleanup(result)

    def test_eval_generated_pytest_cache_is_removed_before_keep(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))
            (source / "test_demo.py").write_text("def test_pass():\n    assert True\n")
            (source / ".gitignore").write_text(".pytest_cache/\n__pycache__/\n")
            git(source, "add", ".")
            git(source, "commit", "-q", "-m", "add evaluator")
            eval_program = program().replace("## Budget", "## Eval\ncmd: python -m pytest -q\n## Budget")

            def propose(repo: Path) -> None:
                (repo / "allowed.txt").write_text("1\n", encoding="utf-8")

            result = run_program(parse_program(eval_program), target_dir=source,
                                 propose=propose, test=score_candidate,
                                 sandbox_root=TEST_TMP_ROOT)
            try:
                clone = Path(result["sandbox_dir"])
                self.assertEqual(1, result["kept"], result["round_results"])
                self.assertFalse((clone / ".pytest_cache").exists())
                self.assertFalse((clone / "__pycache__").exists())
                self.assertEqual("", git(clone, "status", "--porcelain"))
            finally:
                cleanup(result)

    def test_broad_glob_cannot_include_git_metadata(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))
            called = False

            def propose(_repo: Path) -> None:
                nonlocal called
                called = True

            with self.assertRaisesRegex(Exception, "Git metadata"):
                run_program(parse_program(program().replace("- allowed.txt", "- **/*")),
                            target_dir=source, propose=propose, test=score_candidate,
                            sandbox_root=TEST_TMP_ROOT)
            self.assertFalse(called)

    def test_baseline_exception_cleans_disposable_clone(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            source = source_repo(Path(tmp))
            created: list[Path] = []

            def capture(target: Path, sandbox_root=None) -> Path:
                clone = prepare_sandbox(target, sandbox_root=sandbox_root)
                created.append(clone)
                return clone

            with patch("evolve.prepare_sandbox", side_effect=capture):
                with self.assertRaisesRegex(RuntimeError, "scorer crashed"):
                    run_program(parse_program(program()), target_dir=source,
                                propose=lambda _: None,
                                test=lambda _: (_ for _ in ()).throw(RuntimeError("scorer crashed")),
                                sandbox_root=TEST_TMP_ROOT)
            self.assertEqual(1, len(created))
            self.assertFalse(created[0].parent.exists())

    def test_explicit_sandbox_root_works(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            root = Path(tmp)
            source = source_repo(root)
            work = root / "experiments"

            def propose(repo: Path) -> None:
                (repo / "allowed.txt").write_text("1\n", encoding="utf-8")

            result = run_program(parse_program(program()), target_dir=source,
                                 propose=propose, test=score_candidate,
                                 sandbox_root=work)
            try:
                self.assertEqual(work.resolve(), Path(result["sandbox_dir"]).parent.parent)
                self.assertEqual(1, result["kept"])
            finally:
                cleanup(result)


if __name__ == "__main__":
    unittest.main()
