"""Scope gates for a repair plan written in waves of balls.

  python ball_scope_check.py <ball-id> --plan PLAN.md [--repo .] [--base main] [--repo-key APP]
  python ball_scope_check.py --disjoint --plan PLAN.md

Ball mode: read the ball's `**Scope:**` / `**Scope (KEY):**` lines, collect every backticked
path, and compare them with what the branch changed (`git diff --name-only <base>...HEAD`, plus
staged, unstaged and untracked files). A changed file is in scope when it equals a scope path,
ends with "/<scope path>", or matches it as a glob. With --repo-key APP, only untagged Scope
lines and lines tagged (APP) count, and a leading "APP/" is stripped from each path.
Exit 0 = in scope, 1 = out of scope (files listed), 2 = the ball declares no scope.

Disjoint mode: every ball inside one `## Wave` section must own different files. Prints each
path two balls of the same wave both claim. Exit 0 = disjoint, 1 = overlap.

A ball heading is any markdown heading that starts with "Ball <id>", e.g. `#### Ball 1A · title`.
"""
from __future__ import annotations

import argparse
import fnmatch
import pathlib
import re
import subprocess
import sys

HEADING_RE = re.compile(r"^(#{2,6})\s+(.*\S)\s*$")
BALL_RE = re.compile(r"^Ball\s+([A-Za-z0-9][\w.-]*)")
WAVE_RE = re.compile(r"^Wave\b", re.I)
SCOPE_RE = re.compile(r"\*\*Scope(?:\s*\(([^)]*)\))?:\*\*(.*)")
PATH_RE = re.compile(r"`([^`\s]+)`")


def parse_plan(plan: str) -> list[dict]:
    """Return balls in order: {id, wave, lines}."""
    balls: list[dict] = []
    wave = ""
    current: dict | None = None
    for line in plan.splitlines():
        h = HEADING_RE.match(line)
        if h:
            level, title = len(h.group(1)), h.group(2)
            b = BALL_RE.match(title)
            if b:
                current = {"id": b.group(1).rstrip(".·"), "wave": wave, "level": level, "lines": []}
                balls.append(current)
                continue
            if WAVE_RE.match(title):
                wave = title
            if current and level <= current["level"]:
                current = None
            continue
        if current is not None:
            current["lines"].append(line)
    return balls


def scope_paths(lines: list[str], repo_key: str | None = None) -> list[str]:
    paths: list[str] = []
    for line in lines:
        s = SCOPE_RE.search(line)
        if not s:
            continue
        tag = (s.group(1) or "").strip()
        if repo_key and tag and tag != repo_key:
            continue
        for p in PATH_RE.findall(s.group(2)):
            p = p.rstrip(",;")
            if repo_key and p.startswith(repo_key + "/"):
                p = p[len(repo_key) + 1:]
            if "/" in p or "." in p or "*" in p:
                paths.append(p)
    return paths


def find_ball(plan: str, ball: str) -> dict:
    for b in parse_plan(plan):
        if b["id"] == ball:
            return b
    raise SystemExit(f"no ball {ball!r} in plan")


def changed_files(repo: str, base: str) -> set[str]:
    def git(*args: str) -> list[str]:
        out = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout
        return [ln.strip() for ln in out.splitlines() if ln.strip()]
    files = set(git("diff", "--name-only", f"{base}...HEAD"))
    files |= set(git("diff", "--name-only"))
    files |= set(git("diff", "--name-only", "--cached"))
    files |= set(git("ls-files", "--others", "--exclude-standard"))
    return files


def in_scope(path: str, scope: list[str]) -> bool:
    for s in scope:
        if path == s or path.endswith("/" + s) or fnmatch.fnmatch(path, s) or fnmatch.fnmatch(path, "*/" + s):
            return True
    return False


def overlaps(plan: str) -> list[str]:
    """Paths two balls of the same wave both claim (exact or glob match)."""
    problems = []
    by_wave: dict[str, list[dict]] = {}
    for b in parse_plan(plan):
        by_wave.setdefault(b["wave"], []).append(b)
    for wave, balls in by_wave.items():
        scopes = [(b["id"], scope_paths(b["lines"])) for b in balls]
        for i, (a_id, a_paths) in enumerate(scopes):
            for b_id, b_paths in scopes[i + 1:]:
                for pa in a_paths:
                    for pb in b_paths:
                        if pa == pb or fnmatch.fnmatch(pa, pb) or fnmatch.fnmatch(pb, pa):
                            problems.append(f"{wave or '(no wave)'}: balls {a_id} and {b_id} both own {pa}"
                                            + ("" if pa == pb else f" ~ {pb}"))
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ball", nargs="?")
    ap.add_argument("--plan", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--base", default="main")
    ap.add_argument("--repo-key", help="plan repo key for this checkout, e.g. APP")
    ap.add_argument("--disjoint", action="store_true", help="check that balls in a wave share no file")
    a = ap.parse_args(argv)
    plan = pathlib.Path(a.plan).read_text(encoding="utf-8")

    if a.disjoint:
        problems = overlaps(plan)
        for p in problems:
            print("OVERLAP", p)
        print(f"{len(parse_plan(plan))} balls, {len(problems)} overlaps")
        return 1 if problems else 0

    if not a.ball:
        ap.error("give a ball id, or --disjoint")
    scope = scope_paths(find_ball(plan, a.ball)["lines"], a.repo_key)
    if not scope:
        print(f"ball {a.ball} declares no Scope (coordinator ball); nothing to check")
        return 2
    out = sorted(f for f in changed_files(a.repo, a.base) if not in_scope(f, scope))
    for f in out:
        print("OUT OF SCOPE", f)
    print(f"ball {a.ball}: {len(scope)} scope paths, {len(out)} out-of-scope files")
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main())
