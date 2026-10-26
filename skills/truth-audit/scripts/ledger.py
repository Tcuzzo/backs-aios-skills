"""Append-only, gated ledger for a truth audit.

Every change is one JSON line in the ledger file. Nothing is rewritten: an entry's
current state is the fold of its events, and every line carries the SHA-256 of the
line before it, so an edit or a deleted line in the middle breaks the chain and
`check` fails. A status board (STATUS.md) is regenerated from the log, never edited.

  python ledger.py add --id SVC-03 --sev P1 --title "..." --evidence "..." \\
                       --fix-seam "..." --proof "..." [--confidence med] [--task 1A] --by coordinator
  python ledger.py import-lane lanes/SVC_SERVICE.md --by ledger-keeper
  python ledger.py status SVC-03 PLANNED  --by coordinator --task 1A
  python ledger.py status SVC-03 IN-BUILD --by coordinator
  python ledger.py status SVC-03 PROVEN   --by reader --evidence "watchdog row ..."
  python ledger.py status SVC-03 CLOSED   --by grader --evidence "tribunal run ..."
  python ledger.py status DATA-02 ADJUDICATED-NOT-A-BUG --by coordinator --evidence "..."
  python ledger.py list [--open] [--lane SVC]
  python ledger.py check        # exit 1 if any rule is broken anywhere in the log (use as a gate)
  python ledger.py render       # rewrite STATUS.md next to the ledger

The ledger path is --ledger, else $TRUTH_AUDIT_LEDGER, else ./ledger.jsonl.

Rules (enforced on every write AND replayed over the whole log by `check`):
  - ids are unique; an id is added once
  - every entry has evidence, a fix seam and a proof of done
  - status moves forward only: OPEN -> PLANNED -> IN-BUILD -> PROVEN -> CLOSED;
    ADJUDICATED-NOT-A-BUG may end any open entry and needs evidence; terminal is terminal
  - PROVEN and CLOSED need evidence
  - a P0/P1 entry needs a plan task before it may go IN-BUILD
  - the actor who closes an entry is not anyone who set it IN-BUILD or PROVEN
  - the hash chain is intact (no line edited, inserted or removed mid-log)
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import sys

ORDER = ["OPEN", "PLANNED", "IN-BUILD", "PROVEN", "CLOSED"]
ADJUDICATED = "ADJUDICATED-NOT-A-BUG"
TERMINAL = {"CLOSED", ADJUDICATED}
SEVERITIES = ("P0", "P1", "P2", "P3")
CONFIDENCE = ("high", "med", "low")
GENESIS = "genesis"
ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)+$")


# ---------------------------------------------------------------- storage

def ledger_path(arg: str | None) -> pathlib.Path:
    return pathlib.Path(arg or os.environ.get("TRUTH_AUDIT_LEDGER") or "ledger.jsonl")


def _digest(line: str) -> str:
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def read_lines(path: pathlib.Path) -> list[str]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return [ln.rstrip("\r\n") for ln in fh if ln.strip()]


def read_events(path: pathlib.Path) -> list[dict]:
    return [json.loads(ln) for ln in read_lines(path)]


def append(path: pathlib.Path, event: dict) -> None:
    lines = read_lines(path)
    event = {**event, "at": _now(), "prev": _digest(lines[-1]) if lines else GENESIS}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


# ---------------------------------------------------------------- the rules (one place)

def apply(entries: dict[str, dict], ev: dict) -> str | None:
    """Apply one event to the folded state. Return a refusal reason, or None when it is legal.

    Commands call this before they append; `check` replays the whole log through it, so a
    hand-edited ledger fails the same rules a tool write would have."""
    kind = ev.get("kind")
    eid = ev.get("id", "")
    if kind == "add":
        if not ID_RE.match(eid):
            return f"{eid!r} is not a ledger id (want LANE-NN, e.g. SVC-03)"
        if eid in entries:
            return f"{eid} already exists (append-only; use `status`)"
        if ev.get("sev") not in SEVERITIES:
            return f"{eid}: severity must be one of {', '.join(SEVERITIES)}"
        if ev.get("confidence") not in CONFIDENCE:
            return f"{eid}: confidence must be one of {', '.join(CONFIDENCE)}"
        for field in ("evidence", "fix_seam", "proof"):
            if not str(ev.get(field) or "").strip():
                return f"{eid}: {field} is required"
        entries[eid] = {**ev, "status": "OPEN", "history": [("OPEN", ev.get("by") or "unattributed")]}
        return None
    if kind != "status":
        return f"unknown event kind {kind!r}"
    e = entries.get(eid)
    if e is None:
        return f"no entry {eid}"
    cur, new = e["status"], ev.get("status")
    by = ev.get("by") or ""
    evidence = str(ev.get("evidence") or "").strip()
    if not by:
        return f"{eid}: a status change needs --by"
    if cur in TERMINAL:
        return f"{eid} is {cur} (terminal)"
    if new == ADJUDICATED:
        if not evidence:
            return f"{eid}: adjudication needs --evidence"
    elif new not in ORDER or ORDER.index(new) <= ORDER.index(cur):
        return f"{eid}: {cur} -> {new} is not a forward move"
    if new in {"PROVEN", "CLOSED"} and not evidence:
        return f"{eid}: {new} needs --evidence"
    task = ev.get("task") or e.get("task")
    if new == "IN-BUILD" and e["sev"] in {"P0", "P1"} and not task:
        return f"{eid} is {e['sev']} and has no plan task (pass --task)"
    if new == "CLOSED":
        builders = {who for st, who in e["history"] if st in {"IN-BUILD", "PROVEN"}}
        if by in builders:
            return f"{by} built or proved {eid}; a different actor must close it"
    e["status"] = new
    e["history"].append((new, by))
    if ev.get("task"):
        e["task"] = ev["task"]
    return None


def fold(events: list[dict]) -> tuple[dict[str, dict], list[str]]:
    entries: dict[str, dict] = {}
    problems = []
    for n, ev in enumerate(events, 1):
        reason = apply(entries, ev)
        if reason:
            problems.append(f"line {n}: {reason}")
    return entries, problems


def chain_problems(lines: list[str]) -> list[str]:
    problems = []
    prev = GENESIS
    for n, line in enumerate(lines, 1):
        try:
            got = json.loads(line).get("prev")
        except json.JSONDecodeError:
            problems.append(f"line {n}: not JSON")
            prev = _digest(line)
            continue
        if got != prev:
            problems.append(f"line {n}: hash chain broken (a line before it was edited, inserted or removed)")
        prev = _digest(line)
    return problems


def _write(path: pathlib.Path, event: dict) -> int:
    entries, _ = fold(read_events(path))
    reason = apply(entries, dict(event))
    if reason:
        print(f"refused: {reason}", file=sys.stderr)
        return 1
    append(path, event)
    return 0


# ---------------------------------------------------------------- lane files

_KEYS = {
    "status": "status",
    "surface": "surface",
    "evidence": "evidence",
    "surface and evidence": "surface and evidence",
    "root cause": "root cause",
    "fix seam": "fix seam",
    "proof of done": "proof of done",
    "proof": "proof of done",
    "side effects": "side effects",
}
# "### SVC-03 · P1 · title" (also tolerates "|" or " - " as the separator)
BLOCK_RE = re.compile(
    r"^###\s+([A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)+)\s*(?:·|\||\s-\s)\s*(P[0-3])\s*(?:·|\||\s-\s)\s*(.+?)\s*$", re.M)
# "- evidence:", "- evidence (live, 18:24):", "* **Evidence:**", "- **fix-seam**:" ...
FIELD_RE = re.compile(
    r"^[-*]\s+(?:\*\*)?([A-Za-z][A-Za-z -]*?)(?:\*\*)?(\s*\([^)\n]*\))?\s*(?:\*\*)?:(?:\*\*)?[ \t]*", re.M)


def _key(raw: str) -> str | None:
    return _KEYS.get(" ".join(raw.lower().replace("-", " ").split()))


def parse_lane(text: str) -> list[dict]:
    """Split a lane file into finding blocks. A block runs to the next '### ' or '## ' heading.

    Formatting variants are not missing evidence: bold keys, '*' bullets, a qualifier in
    parentheses ('- evidence (read-only):') and the merged '- surface and evidence:' all parse.
    Sub-bullets under a field stay part of that field's value."""
    out = []
    heads = list(BLOCK_RE.finditer(text))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[m.end():end]
        nxt = re.search(r"^##\s", body, re.M)
        if nxt:
            body = body[:nxt.start()]
        fields: dict[str, str] = {}
        marks = [(fm, _key(fm.group(1))) for fm in FIELD_RE.finditer(body)]
        marks = [(fm, k) for fm, k in marks if k and not fm.group(0).startswith((" ", "\t"))]
        for j, (fm, k) in enumerate(marks):
            stop = marks[j + 1][0].start() if j + 1 < len(marks) else len(body)
            value = " ".join(((fm.group(2) or "").strip() + " " + body[fm.end():stop]).split())
            fields[k] = (fields.get(k, "") + " " + value).strip()
        if "surface and evidence" in fields:
            merged = fields.pop("surface and evidence")
            fields.setdefault("surface", merged)
            fields["evidence"] = (fields.get("evidence", "") + " " + merged).strip()
        status = fields.get("status", "")
        conf = re.search(r"confidence:\s*(high|med|low)", status, re.I)
        out.append({
            "id": m.group(1), "sev": m.group(2), "title": m.group(3).strip(),
            "surface": fields.get("surface", ""), "evidence": fields.get("evidence", ""),
            "root_cause": fields.get("root cause", ""), "fix_seam": fields.get("fix seam", ""),
            "proof": fields.get("proof of done", ""),
            "confidence": conf.group(1).lower() if conf else "med",
            "adjudicated": ADJUDICATED in status.upper(),
        })
    return out


# ---------------------------------------------------------------- commands

def cmd_add(a: argparse.Namespace) -> int:
    rc = _write(a.path, {"kind": "add", "id": a.id, "lane": a.lane or a.id.split("-")[0],
                         "sev": a.sev, "title": a.title, "evidence": a.evidence,
                         "fix_seam": a.fix_seam, "proof": a.proof, "confidence": a.confidence,
                         "task": a.task, "by": a.by})
    if rc == 0:
        print(f"added {a.id}")
    return rc


def cmd_import_lane(a: argparse.Namespace) -> int:
    src = pathlib.Path(a.file)
    blocks = parse_lane(src.read_text(encoding="utf-8"))
    entries, _ = fold(read_events(a.path))
    seen: set[str] = set()
    added = skipped = refused = 0
    for f in blocks:
        if f["id"] in seen:
            print(f"refused {f['id']}: duplicate id inside {src.name}", file=sys.stderr)
            refused += 1
            continue
        seen.add(f["id"])
        if f["id"] in entries:
            skipped += 1
            continue
        if f["adjudicated"]:
            # A positive finding (the data is real, the path works) is recorded, not dropped.
            f["fix_seam"] = f["fix_seam"] or "none (adjudicated not a bug)"
            f["proof"] = f["proof"] or "re-run the evidence command"
        missing = [k for k in ("evidence", "fix_seam", "proof") if not f[k]]
        if missing:
            print(f"refused {f['id']}: missing {', '.join(missing)}", file=sys.stderr)
            refused += 1
            continue
        rc = _write(a.path, {"kind": "add", "id": f["id"], "lane": f["id"].split("-")[0],
                             "sev": f["sev"], "title": f["title"], "surface": f["surface"],
                             "evidence": f["evidence"], "fix_seam": f["fix_seam"], "proof": f["proof"],
                             "root_cause": f["root_cause"], "confidence": f["confidence"],
                             "task": None, "by": a.by, "source": src.name})
        if rc:
            refused += 1
            continue
        if f["adjudicated"]:
            _write(a.path, {"kind": "status", "id": f["id"], "status": ADJUDICATED, "by": a.by,
                            "evidence": f["evidence"], "note": "imported as adjudicated", "task": None})
        added += 1
    print(f"{src.name}: {len(blocks)} blocks, added {added}, already present {skipped}, refused {refused}")
    if not blocks:
        print(f"refused: {src.name} has no '### ID · Pn · title' blocks", file=sys.stderr)
        return 1
    return 1 if refused else 0


def cmd_status(a: argparse.Namespace) -> int:
    entries, _ = fold(read_events(a.path))
    cur = entries.get(a.id, {}).get("status", "?")
    rc = _write(a.path, {"kind": "status", "id": a.id, "status": a.new_status, "by": a.by,
                         "evidence": a.evidence, "note": a.note, "task": a.task})
    if rc == 0:
        print(f"{a.id}: {cur} -> {a.new_status}")
    return rc


def _sorted(entries: dict[str, dict]) -> list[dict]:
    return sorted(entries.values(), key=lambda x: (x["sev"], x["id"]))


def cmd_list(a: argparse.Namespace) -> int:
    entries, _ = fold(read_events(a.path))
    for e in _sorted(entries):
        if a.open and e["status"] in TERMINAL:
            continue
        if a.lane and e.get("lane") != a.lane:
            continue
        print(f"{e['id']:<10} {e['sev']} {e['status']:<22} {e.get('task') or '-':<8} {e['title']}")
    return 0


def cmd_check(a: argparse.Namespace) -> int:
    lines = read_lines(a.path)
    problems = chain_problems(lines)
    events = []
    for ln in lines:
        try:
            events.append(json.loads(ln))
        except json.JSONDecodeError:
            pass
    entries, replay = fold(events)
    problems += replay
    for p in problems:
        print("FAIL", p)
    print(f"{len(entries)} entries, {len(lines)} events, {len(problems)} problems")
    return 1 if problems else 0


def cmd_render(a: argparse.Namespace) -> int:
    entries, _ = fold(read_events(a.path))
    rows = _sorted(entries)
    counts: dict[str, int] = {}
    for e in rows:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    out = pathlib.Path(a.out) if a.out else a.path.with_name("STATUS.md")
    lines = ["# Ledger status (generated by ledger.py render; do not edit)", "",
             f"_Generated {_now()}_ · " + " · ".join(f"{k}: {v}" for k, v in sorted(counts.items())), "",
             "| id | sev | status | task | title |", "|---|---|---|---|---|"]
    for e in rows:
        title = e["title"].replace("|", "/")
        lines.append(f"| {e['id']} | {e['sev']} | {e['status']} | {e.get('task') or ''} | {title} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(rows)} entries)")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ledger", help="ledger file (default $TRUTH_AUDIT_LEDGER or ./ledger.jsonl)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("add")
    s.add_argument("--id", required=True)
    s.add_argument("--lane", help="default: the id prefix before the first '-'")
    s.add_argument("--sev", required=True, choices=SEVERITIES)
    s.add_argument("--title", required=True)
    s.add_argument("--evidence", required=True)
    s.add_argument("--fix-seam", dest="fix_seam", required=True)
    s.add_argument("--proof", required=True)
    s.add_argument("--confidence", default="med", choices=CONFIDENCE)
    s.add_argument("--task")
    s.add_argument("--by", required=True)
    s.set_defaults(fn=cmd_add)

    s = sub.add_parser("status")
    s.add_argument("id")
    s.add_argument("new_status", choices=ORDER[1:] + [ADJUDICATED])
    s.add_argument("--by", required=True)
    s.add_argument("--evidence", default="")
    s.add_argument("--note", default="")
    s.add_argument("--task")
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("import-lane")
    s.add_argument("file")
    s.add_argument("--by", required=True)
    s.set_defaults(fn=cmd_import_lane)

    s = sub.add_parser("list")
    s.add_argument("--open", action="store_true")
    s.add_argument("--lane")
    s.set_defaults(fn=cmd_list)

    sub.add_parser("check").set_defaults(fn=cmd_check)
    s = sub.add_parser("render")
    s.add_argument("--out", help="default: STATUS.md next to the ledger")
    s.set_defaults(fn=cmd_render)

    a = p.parse_args(argv)
    a.path = ledger_path(a.ledger)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
