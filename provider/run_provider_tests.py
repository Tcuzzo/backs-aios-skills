#!/usr/bin/env python3
"""Validate provider code with an isolated environment and redacted reporting.

This is test-process isolation, not an OS filesystem sandbox. No production
project, credential, Python path, or HOME setting is forwarded to the worker.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


def worker(root: Path) -> int:
    result = unittest.TestResult()
    # Test/import stdout and tracebacks must never reach the operator console.
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            suite = unittest.defaultTestLoader.discover(str(root / "tests"), pattern="test_provider*.py")
            suite.run(result)
        report = {"run": result.testsRun, "failures": len(result.failures),
                  "errors": len(result.errors), "skipped": len(result.skipped),
                  "unexpected_successes": len(result.unexpectedSuccesses)}
    except BaseException:
        report = {"run": 0, "failures": 0, "errors": 1, "skipped": 0, "unexpected_successes": 0}
    print(json.dumps(report))
    return 0


def validate(root: Path) -> int:
    with tempfile.TemporaryDirectory(prefix="backs-provider-check-") as raw:
        home = Path(raw)
        env = {
            "HOME": str(home), "XDG_CONFIG_HOME": str(home / ".config"),
            "XDG_DATA_HOME": str(home / ".local/share"), "TMPDIR": str(home),
            "PATH": str(Path(sys.executable).parent) + os.pathsep + os.defpath,
            "LANG": "C.UTF-8", "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1",
        }
        try:
            completed = subprocess.run(
                [sys.executable, "-I", "-B", str(Path(__file__).resolve()), "--worker", str(root)],
                cwd=home, env=env, text=True, capture_output=True, timeout=120, check=False,
            )
            report = json.loads(completed.stdout)
            keys = ("run", "failures", "errors", "skipped", "unexpected_successes")
            if completed.returncode or not isinstance(report, dict) or any(
                type(report.get(key)) is not int or report[key] < 0 for key in keys
            ):
                raise ValueError("invalid report")
        except (OSError, subprocess.TimeoutExpired, ValueError):
            print("Provider validation failed; subprocess output withheld.", file=sys.stderr)
            return 1
    print("Provider validation: {run} run, {failures} failures, {errors} errors, "
          "{skipped} skipped, {unexpected_successes} unexpected successes.".format(**report))
    # No test identities, exception text, stdout, or stderr are replayed.
    return int(report["run"] == 0 or any(report[key] for key in keys[1:]))


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--worker":
        return worker(Path(sys.argv[2]).resolve())
    if len(sys.argv) > 2:
        print("usage: run_provider_tests.py [source-root]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path(__file__).resolve().parents[1]
    return validate(root)


if __name__ == "__main__":
    raise SystemExit(main())
