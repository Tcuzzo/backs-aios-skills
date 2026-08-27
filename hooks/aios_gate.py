#!/usr/bin/env python3
"""aios_gate — the pack's grounding gate, programmed instead of prompted.

Every session starts RED. While RED, the file-edit tools (Edit, Write,
NotebookEdit, MultiEdit) are denied, and Bash is denied ONLY when its command
matches a conservative mutating-verb pattern — until a pack skill has been
invoked this session. Invoking any pack skill (PostToolUse on the Skill tool)
flips the session GREEN.

Rules this script holds structurally:
  * Read-only tools are NEVER touched (the hooks.json matcher scopes to mutators,
    and this script re-checks the tool name as a second belt).
  * Read-only shell is NEVER blocked: Bash denies only on a positive match of a
    mutating verb at a command position (git commit/push, rm, mv/tee onto a
    tracked-looking path, sed -i, npm/pip/cargo install, systemctl/service
    restart, chmod/chown, > redirection outside /tmp). ls, cat, grep,
    git status/diff/log, and echo without redirection always pass.
  * Kill-switch: AIOS_GATE=off (also 0/false/no) disables the gate entirely.
    The capability defaults ON; the switch is loud, reversible, and the only escape.
  * Fail-open on ANY script error: a broken gate must never brick a session.
    Errors print one warning line to stderr and exit 0 (no decision = allow).

Re-arm for a new job in the same session:
  python3 aios_gate.py --rearm [session_id]     (falls back to parent PID)

Zero dependencies. Python 3 stdlib only. State lives in ~/.claude/state/
(falls back to the system temp dir if that is not writable).
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile

KILL_ENV = "AIOS_GATE"
MUTATING_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}
DENY_MESSAGE = "Load the floor first — run /optimus. Set AIOS_GATE=off to disable."

# A verb counts only at a command position: line start, after ; & |, or inside
# a substitution. "grep rm" or "echo 'rm x'" can never match.
_CMD_POS = r"(?:^|[;&|]|\$\(|`)\s*(?:sudo\s+)?"

# Conservative mutating-verb patterns for Bash. Deny fires ONLY on a positive
# match; everything unmatched — all read-only shell — passes untouched.
_BASH_MUTATING = tuple(re.compile(p) for p in (
    _CMD_POS + r"git\s+(?:-\S+\s+)*(?:commit|push)\b",
    _CMD_POS + r"rm\s",
    _CMD_POS + r"sed\s+(?:-\S+\s+)*-i",
    _CMD_POS + r"(?:npm|pip3?|cargo)\s+(?:-\S+\s+)*install\b",
    _CMD_POS + r"systemctl\s+(?:-\S+\s+)*restart\b",
    _CMD_POS + r"service\s+\S+\s+restart\b",
    _CMD_POS + r"chmod\s",
    _CMD_POS + r"chown\s",
))

_SAFE_TARGET_PREFIXES = ("/tmp/", "/dev/null", "/dev/shm")


def _strip_quoted(command: str) -> str:
    """Blank out quoted segments so text inside quotes cannot false-match."""
    return re.sub(r"'[^']*'|\"[^\"]*\"", " ", command)


def _is_safe_path(token: str) -> bool:
    token = token.strip("'\"")
    return token.startswith(_SAFE_TARGET_PREFIXES) or token in {"/tmp", "/dev/null"}


def _bash_is_mutating(command: str) -> bool:
    for pattern in _BASH_MUTATING:
        if pattern.search(command):
            return True
    # mv / tee: mutating only when a target looks tracked (outside /tmp, /dev).
    for m in re.finditer(_CMD_POS + r"(?:mv|tee)\s+([^;|&]*)", command):
        args = [a for a in m.group(1).split() if not a.startswith("-")]
        if any(not _is_safe_path(a) for a in args):
            return True
    # > redirection into a non-/tmp path (fd redirects like 2>&1 never match;
    # quoted text is stripped first so `awk '$1 > 5'` cannot false-match).
    for m in re.finditer(r">>?\s*([^\s;|&<>]+)", _strip_quoted(command)):
        if not _is_safe_path(m.group(1)):
            return True
    return False


def _plugin_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _state_dir() -> str:
    preferred = os.path.expanduser(os.path.join("~", ".claude", "state"))
    try:
        os.makedirs(preferred, exist_ok=True)
        return preferred
    except OSError:
        return tempfile.gettempdir()


def _state_file(session_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id)[:80] or "unknown"
    return os.path.join(_state_dir(), f"aios_floor_{safe}.state")


def _session_id(payload: dict) -> str:
    sid = str(payload.get("session_id") or "").strip()
    return sid if sid else f"ppid{os.getppid()}"


def _pack_skill_names() -> set:
    """Names that count as 'the floor': skills/<dir>/SKILL.md + commands/*.md.

    Fail-open: if the pack layout cannot be read, return an empty set and let
    the caller treat ANY skill invocation as grounding.
    """
    names = set()
    root = _plugin_root()
    try:
        skills_dir = os.path.join(root, "skills")
        if os.path.isdir(skills_dir):
            for entry in os.listdir(skills_dir):
                if os.path.isfile(os.path.join(skills_dir, entry, "SKILL.md")):
                    names.add(entry)
        commands_dir = os.path.join(root, "commands")
        if os.path.isdir(commands_dir):
            for entry in os.listdir(commands_dir):
                if entry.endswith(".md"):
                    names.add(entry[:-3])
    except OSError:
        return set()
    return names


def _invoked_skill(tool_input: dict) -> str:
    raw = str(tool_input.get("skill") or tool_input.get("name") or "").strip()
    # Plugin skills arrive namespaced ("backs-aios:optimus"); keep the last part.
    return raw.rsplit(":", 1)[-1]


def _deny() -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": DENY_MESSAGE,
        }
    }))


def handle(payload: dict) -> None:
    event = str(payload.get("hook_event_name") or "")
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        tool_input = {}
    session_id = _session_id(payload)

    if event == "PostToolUse":
        if tool_name == "Skill":
            skill = _invoked_skill(tool_input)
            pack = _pack_skill_names()
            if skill and (not pack or skill in pack):
                with open(_state_file(session_id), "w", encoding="utf-8") as fh:
                    fh.write("floor loaded\n")
        return

    if event == "PreToolUse":
        red = not os.path.isfile(_state_file(session_id))
        if tool_name == "Bash":
            if red and _bash_is_mutating(str(tool_input.get("command") or "")):
                _deny()
            return  # read-only shell always passes, red or green
        if tool_name not in MUTATING_TOOLS:
            return  # read-only and unknown tools always pass
        if not red:
            return  # floor loaded this session: allow
        _deny()
        return
    # Any other event: no decision.


def _rearm(argv: list) -> None:
    sid = argv[0] if argv else f"ppid{os.getppid()}"
    path = _state_file(sid)
    if os.path.isfile(path):
        os.remove(path)
        print(f"aios_gate: re-armed (removed {path})")
    else:
        print(f"aios_gate: already armed (no state at {path})")


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--rearm":
        _rearm(sys.argv[2:])
        return 0
    if os.environ.get(KILL_ENV, "").strip().lower() in {"off", "0", "false", "no"}:
        return 0  # kill-switch: gate disabled, everything passes
    payload = json.loads(sys.stdin.read() or "{}")
    if not isinstance(payload, dict):
        raise ValueError("hook payload is not a JSON object")
    handle(payload)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # fail-open, loudly: never brick a session
        print(f"aios_gate: WARNING gate error, allowing ({type(exc).__name__}: {exc})",
              file=sys.stderr)
        sys.exit(0)
