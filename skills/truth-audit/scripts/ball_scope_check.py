"""Scope gates for a repair plan written in waves of balls.

  python ball_scope_check.py <ball-id> --plan PLAN.md [--repo .] [--base main] [--repo-key APP]
  python ball_scope_check.py --disjoint --plan PLAN.md

A ball heading is any markdown heading that starts with "Ball <id>", e.g. `#### Ball 1A · title`.
A ball's scope starts at a `**Scope:**` or `**Scope (KEY):**` field and runs until the next
bold field (`**Interfaces:**`), a blank line, a heading or a checklist item, so a scope that
wraps over several lines is read whole. Every backticked token in it is a path, except tokens
inside parentheses, which qualify the path before them (`api/health.py` (`health` only)).
A path must be relative and stay inside the repo: absolute paths, drive letters, `..`
segments and tokens with spaces are refused by name (exit 2), never silently dropped.

Ball mode: compare the scope with what the branch changed (`git diff --name-only <base>...HEAD`
plus staged, unstaged and untracked files). With --repo-key APP, only untagged Scope fields and
fields tagged (APP) count, and a leading "APP/" is stripped from each path.
Exit 0 = in scope, 1 = out of scope (files listed), 2 = no scope, unparseable scope, or git error.

Disjoint mode: balls inside one `## Wave` section must own different files. Uses the same
matcher as ball mode, in both directions. Exit 0 = disjoint, 1 = overlap, 2 = unparseable scope.
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
FIELD_START_RE = re.compile(r"^\s*(?:[-*]\s+)?\*\*[^*]+:\*\*")
CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[[ xX]\]")
PAREN_RE = re.compile(r"\([^()]*\)")
PATH_RE = re.compile(r"`([^`]+)`")
DRIVE_RE = re.compile(r"^[A-Za-z]:")


class ScopeError(ValueError):
    """A scope token that is not a relative path inside the repo."""


def parse_plan(plan: str) -> list[dict]:
    """Return balls in order: {id, wave, level, lines}."""
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


def _scope_fields(lines: list[str]) -> list[tuple[str, str]]:
    """(tag, text) for each Scope field, with its continuation lines joined."""
    fields: list[list[str]] = []
    open_field: list[str] | None = None
    for line in lines:
        s = SCOPE_RE.search(line)
        if s:
            open_field = [(s.group(1) or "").strip(), s.group(2)]
            fields.append(open_field)
            continue
        if open_field is None:
            continue
        if (not line.strip() or FIELD_START_RE.match(line) or CHECKBOX_RE.match(line)
                or line.lstrip().startswith("#")):
            open_field = None
            continue
        open_field[1] += " " + line.strip()
    return [(tag, text) for tag, text in fields]


def check_path(token: str) -> str:
    p = token.strip().rstrip(",;")
    if not p or any(c.isspace() for c in p):
        raise ScopeError(f"scope token `{token}` is not a path (contains spaces)")
    if p.startswith(("/", "\\")) or DRIVE_RE.match(p):
        raise ScopeError(f"scope token `{token}` is absolute; scope paths are relative to the repo")
    if ".." in re.split(r"[\\/]", p):
        raise ScopeError(f"scope token `{token}` leaves the repo (`..`)")
    return p.replace("\\", "/")


def scope_paths(lines: list[str], repo_key: str | None = None) -> list[str]:
    paths: list[str] = []
    for tag, text in _scope_fields(lines):
        if repo_key and tag and tag != repo_key:
            continue
        # Parenthesized tokens qualify the path before them; they are symbols, not files.
        while PAREN_RE.search(text):
            text = PAREN_RE.sub(" ", text)
        for token in PATH_RE.findall(text):
            p = check_path(token)
            if repo_key and p.startswith(repo_key + "/"):
                p = p[len(repo_key) + 1:]
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


def matches(path: str, entry: str) -> bool:
    """The one matcher: exact, suffix under a prefix dir, or glob (also under a prefix)."""
    return (path == entry or path.endswith("/" + entry)
            or fnmatch.fnmatch(path, entry) or fnmatch.fnmatch(path, "*/" + entry))


def in_scope(path: str, scope: list[str]) -> bool:
    return any(matches(path, s) for s in scope)


def overlaps(plan: str) -> list[str]:
    """Paths two balls of the same wave both claim, by the same matcher ball mode uses."""
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
                        if matches(pa, pb) or matches(pb, pa):
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

    try:
        if a.disjoint:
            problems = overlaps(plan)
            for p in problems:
                print("OVERLAP", p)
            print(f"{len(parse_plan(plan))} balls, {len(problems)} overlaps")
            return 1 if problems else 0
        if not a.ball:
            ap.error("give a ball id, or --disjoint")
        scope = scope_paths(find_ball(plan, a.ball)["lines"], a.repo_key)
    except ScopeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if not scope:
        print(f"ball {a.ball} declares no Scope (coordinator ball); nothing to check")
        return 2
    try:
        changed = changed_files(a.repo, a.base)
    except (subprocess.CalledProcessError, OSError) as exc:
        detail = (getattr(exc, "stderr", "") or str(exc)).strip().splitlines()
        print(f"error: git could not list changes against {a.base!r} in {a.repo}: "
              f"{detail[0] if detail else exc}", file=sys.stderr)
        return 2
    out = sorted(f for f in changed if not in_scope(f, scope))
    for f in out:
        print("OUT OF SCOPE", f)
    print(f"ball {a.ball}: {len(scope)} scope paths, {len(out)} out-of-scope files")
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main())
