#!/usr/bin/env python3
"""Aggregate strict signed predicates without truthiness or multiplication."""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

REASONS = frozenset({"satisfied", "failure", "missing_evidence", "stale_input", "timeout"})


@dataclass(frozen=True)
class Predicate:
    name: str
    verdict: object
    reason: str
    age_s: object
    input_digest: str
    authority: str


def strict_verdict(value: object) -> int:
    if type(value) is not int or value not in (-1, 1):
        raise ValueError("verdict must be exact integer -1 or +1")
    return value


def valid_age(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("age_s must be a finite non-negative number")
    age = float(value)
    if not math.isfinite(age) or age < 0:
        raise ValueError("age_s must be a finite non-negative number")
    return age


def validate(row: Predicate) -> None:
    for field_name in ("name", "reason", "input_digest", "authority"):
        if not isinstance(getattr(row, field_name), str):
            raise ValueError(f"{field_name} must be a string")
    verdict = strict_verdict(row.verdict)
    if row.reason not in REASONS:
        raise ValueError(f"unsupported reason: {row.reason!r}")
    if (verdict == 1) != (row.reason == "satisfied"):
        raise ValueError("verdict and reason contradict")
    valid_age(row.age_s)


def predicate_map(rows: list[Predicate]) -> dict[str, Predicate]:
    mapped: dict[str, Predicate] = {}
    for row in rows:
        validate(row)
        if not row.name.strip() or row.name in mapped:
            raise ValueError("predicate names must be non-empty and unique")
        mapped[row.name] = row
    return mapped


def names_without_authority(rows: list[Predicate]) -> list[str]:
    return [row.name for row in rows if not row.authority.strip()]


def stale_names(rows: list[Predicate], expected: str, maximum: float) -> list[str]:
    return [row.name for row in rows if row.input_digest != expected or valid_age(row.age_s) > maximum]


def timeout_names(rows: list[Predicate]) -> list[str]:
    return [row.name for row in rows if row.verdict == -1 and row.reason == "timeout"]


def first_failure(rows: list[Predicate], expected: str, maximum: float) -> tuple[str, list[str]] | None:
    missing_authority = names_without_authority(rows)
    if missing_authority:
        return "missing_evidence", missing_authority
    stale = stale_names(rows, expected, maximum)
    if stale:
        return "stale_input", stale
    timed_out = timeout_names(rows)
    if timed_out:
        return "timeout", timed_out
    failed = [row for row in rows if row.verdict != 1]
    return (failed[0].reason, [row.name for row in failed]) if failed else None


def valid_required(required: list[str]) -> bool:
    return bool(required) and all(isinstance(name, str) and name.strip() for name in required) and len(set(required)) == len(required)


def requirement_failure(required: list[str], expected: str) -> dict[str, object] | None:
    if not required:
        return {"verdict": -1, "reason": "missing_evidence", "failed_names": []}
    if not valid_required(required):
        raise ValueError("required names must be non-empty and unique")
    if not isinstance(expected, str) or not expected.strip():
        return {"verdict": -1, "reason": "missing_evidence", "failed_names": required}
    return None


def evaluate(rows: list[Predicate], required: list[str], expected: str, maximum: float) -> dict[str, object]:
    requirement = requirement_failure(required, expected)
    if requirement:
        return requirement
    maximum = valid_age(maximum)
    mapped = predicate_map(rows)
    missing = [name for name in required if name not in mapped]
    if missing:
        return {"verdict": -1, "reason": "missing_evidence", "failed_names": missing}
    failure = first_failure([mapped[name] for name in required], expected, maximum)
    if failure:
        return {"verdict": -1, "reason": failure[0], "failed_names": failure[1]}
    return {"verdict": 1, "reason": "satisfied", "failed_names": []}


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--predicates", type=Path, help="JSON list file; omit to read stdin")
    command.add_argument("--required", action="append", default=[], help="Required predicate name; repeatable")
    command.add_argument("--expected-input-digest", required=True)
    command.add_argument("--max-age-s", type=float, default=300.0)
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        text = args.predicates.read_text(encoding="utf-8") if args.predicates else sys.stdin.read()
        payload = json.loads(text)
        if not isinstance(payload, list):
            raise ValueError("predicates must be a JSON list")
        fields = ("name", "verdict", "reason", "age_s", "input_digest", "authority")
        rows = []
        for item in payload:
            if not isinstance(item, dict):
                raise ValueError("predicate item must be an object")
            rows.append(Predicate(**{field: item[field] for field in fields}))
        result = evaluate(rows, args.required, args.expected_input_digest, args.max_age_s)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        result = {"verdict": -1, "reason": "missing_evidence", "failed_names": [], "error": f"{type(exc).__name__}: {exc}"}
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["verdict"] == 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
