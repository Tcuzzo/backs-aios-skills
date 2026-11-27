#!/usr/bin/env python3
"""Run one bounded command and emit a deterministic signed observation receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import time


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def command_argv(remainder: list[str]) -> list[str]:
    argv = remainder[1:] if remainder[:1] == ["--"] else remainder
    if not argv:
        raise ValueError("a command is required after --")
    return argv


def output_bytes(value: bytes | str | None) -> bytes:
    if value is None:
        return b""
    return value if isinstance(value, bytes) else value.encode("utf-8", errors="replace")


def run_probe(argv: list[str], timeout_s: float) -> dict[str, object]:
    if not math.isfinite(timeout_s) or timeout_s <= 0:
        raise ValueError("timeout_s must be positive and finite")
    started = time.monotonic_ns()
    try:
        result = subprocess.run(argv, capture_output=True, timeout=timeout_s, check=False)
        exit_code, stdout, stderr, timed_out = result.returncode, result.stdout, result.stderr, False
    except subprocess.TimeoutExpired as exc:
        exit_code, stdout, stderr, timed_out = None, output_bytes(exc.stdout), output_bytes(exc.stderr), True
    duration_ms = (time.monotonic_ns() - started) // 1_000_000
    reason = "timeout" if timed_out else ("satisfied" if exit_code == 0 else "failure")
    return {
        "argv": argv,
        "exit_code": exit_code,
        "stdout_sha256": digest(output_bytes(stdout)),
        "stderr_sha256": digest(output_bytes(stderr)),
        "duration_ms": duration_ms,
        "timed_out": timed_out,
        "verdict": 1 if exit_code == 0 and not timed_out else -1,
        "reason": reason,
    }


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--name", required=True)
    command.add_argument("--input-digest", required=True)
    command.add_argument("--authority", required=True)
    command.add_argument("--timeout-s", required=True, type=float)
    command.add_argument("command", nargs=argparse.REMAINDER)
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        for field_name in ("name", "input_digest", "authority"):
            if not getattr(args, field_name).strip():
                raise ValueError(f"{field_name.replace('_', '-')} must be non-empty")
        receipt = run_probe(command_argv(args.command), args.timeout_s)
        receipt.update(name=args.name, input_digest=args.input_digest, authority=args.authority, age_s=0.0)
    except (OSError, ValueError) as exc:
        receipt = {
            "name": args.name,
            "verdict": -1,
            "reason": "missing_evidence",
            "input_digest": args.input_digest,
            "authority": args.authority,
            "age_s": 0.0,
            "error": f"{type(exc).__name__}: {exc}",
        }
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
    return 0 if receipt["verdict"] == 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
