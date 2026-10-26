"""Compare two directory trees by content, not by names or commit ids.

  python cmp_trees.py <dir-A> <dir-B> [--labels running github] [--skip build --skip dist] [--limit 45] [--json]

Each file is hashed (SHA-256) after CRLF -> LF normalization, so a Windows checkout and a
POSIX checkout of the same source compare equal. Caches and VCS folders are skipped; the
skip list is printed so the reader knows exactly what was not compared.

To compare a remote ref, export it to a scratch directory first, for example
  git -C <repo> worktree add --detach <scratch>/ref <ref>      or
  git -C <repo> archive <ref> | tar -x -C <scratch>/ref

Exit 0 = identical, 1 = differ, 2 = error (a directory is missing or unreadable, or bad
arguments). A failed probe never reads as clean.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

DEFAULT_SKIP = {"__pycache__", ".git", ".hg", ".svn", ".venv", "venv", "node_modules",
                ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox"}
SKIP_SUFFIXES = (".pyc", ".pyo")


def walk(root: str, skip: set[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in skip)
        for f in files:
            if f.endswith(SKIP_SUFFIXES):
                continue
            p = os.path.join(d, f)
            if os.path.islink(p):
                out[os.path.relpath(p, root).replace(os.sep, "/")] = "link:" + os.readlink(p)
                continue
            with open(p, "rb") as fh:
                data = fh.read().replace(b"\r\n", b"\n")
            out[os.path.relpath(p, root).replace(os.sep, "/")] = hashlib.sha256(data).hexdigest()
    return out


def compare(a: dict[str, str], b: dict[str, str]) -> dict[str, list[str]]:
    return {
        "only_a": sorted(set(a) - set(b)),
        "only_b": sorted(set(b) - set(a)),
        "changed": sorted(k for k in set(a) & set(b) if a[k] != b[k]),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--labels", nargs=2, default=("A", "B"))
    ap.add_argument("--skip", action="append", default=[], help="extra directory name to skip (repeatable)")
    ap.add_argument("--limit", type=int, default=45, help="max paths printed per list")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    for d in (args.a, args.b):
        if not os.path.isdir(d):
            print(f"not a directory: {d}", file=sys.stderr)
            return 2
    skip = DEFAULT_SKIP | set(args.skip)
    try:
        a, b = walk(args.a, skip), walk(args.b, skip)
    except OSError as exc:
        # A probe that could not read is an error, never "differ" and never "same".
        print(f"error reading tree: {exc}", file=sys.stderr)
        return 2
    res = compare(a, b)
    la, lb = args.labels
    if args.json:
        print(json.dumps({"labels": [la, lb], "files": [len(a), len(b)], "skipped_dirs": sorted(skip), **res},
                         indent=2))
    else:
        print(f"{la} files {len(a)}  {lb} files {len(b)}  only-{la} {len(res['only_a'])}  "
              f"only-{lb} {len(res['only_b'])}  changed {len(res['changed'])}")
        print("skipped dirs:", ", ".join(sorted(skip)), "| CRLF normalized | sha256")
        for name, lst in ((f"ONLY IN {la}", res["only_a"]), (f"ONLY IN {lb}", res["only_b"]),
                          ("CHANGED", res["changed"])):
            print("==", name)
            for x in lst[:args.limit]:
                print("  ", x)
            if len(lst) > args.limit:
                print("   ...", len(lst) - args.limit, "more")
    return 0 if not any(res.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
