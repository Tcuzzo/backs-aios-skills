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
  * Fail-open ONLY in stdin hook-mode errors: a broken hook must never brick a
    session. Hook errors print one warning line to stderr and exit 0 (no decision
    = allow). Explicit --load/--rearm errors are loud and exit nonzero.

Load a skill explicitly to arm the session:
  python3 aios_gate.py --load backs-aios:<skill> [session_id]
  python3 aios_gate.py --load <skill> [session_id]

Re-arm for a new job in the same session:
  python3 aios_gate.py --rearm [session_id]     (falls back to parent PID)

Zero dependencies. Python 3 stdlib only. State lives in ~/.aios/state/
(falls back to the system temp dir if that is not writable).
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import sys
import tempfile
import time

KILL_ENV = "AIOS_GATE"
MUTATING_TOOLS = {"Delete", "Edit", "MultiEdit", "NotebookEdit", "Write"}
DENY_MESSAGE = "Load the floor first — run /optimus. Set AIOS_GATE=off to disable."

# A verb counts only at a command position: line start, after ; & |, or inside
# a substitution. "grep rm" or "echo 'rm x'" can never match.
_CMD_POS = r"(?:^|[;&|\r\n]|\$\(|`)\s*(?:sudo\s+)?"

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

_SAFE_TARGET_PREFIXES = ("/tmp/", "/dev/shm/")


def _strip_quoted(command: str) -> str:
    """Blank out quoted segments so text inside quotes cannot false-match."""
    return re.sub(r"'[^']*'|\"[^\"]*\"", " ", command)


def _is_safe_path(token: str) -> bool:
    token = token.strip("'\"")
    return token.startswith(_SAFE_TARGET_PREFIXES) or token in {"/tmp", "/dev/shm", "/dev/null"}


def _bash_is_mutating(command: str) -> bool:
    stripped = _strip_quoted(command)
    for pattern in _BASH_MUTATING:
        if pattern.search(stripped):
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
    preferred = os.path.expanduser(os.path.join("~", ".aios", "state"))
    try:
        os.makedirs(preferred, exist_ok=True)
        return preferred
    except OSError:
        return tempfile.gettempdir()


def _state_component(raw: str) -> str:
    id_ = str(raw or "")
    if id_ and re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", id_):
        return id_
    if not id_:
        return "unknown"
    prefix = re.sub(r"[^A-Za-z0-9_.-]", "_", id_)[:15]
    digest = hashlib.sha256(id_.encode("utf-8")).hexdigest()
    return (prefix + "_" if prefix else "") + digest


def _state_file(session_id: str) -> str:
    return os.path.join(_state_dir(), f"aios_floor_{_state_component(session_id)}.state")


def _remove_state(session_id: str) -> None:
    path = _state_file(session_id)
    if os.path.isfile(path):
        os.remove(path)


def _state_exists(session_id: str) -> bool:
    return os.path.isfile(_state_file(session_id))


def _session_id(payload: dict, cli_arg: str | None = None) -> str:
    if cli_arg is not None:
        sid = str(cli_arg).strip()
        if sid:
            return sid
    sid = str(payload.get("session_id") or payload.get("conversation_id") or "").strip()
    if sid:
        return sid
    env_keys = (
        "BACKS_BUILD_SESSION",
        "CLAUDE_CODE_SESSION_ID",
        "CODEX_THREAD_ID",
        "CURSOR_SESSION_ID",
        "CURSOR_CONVERSATION_ID",
        "OPENCODE_SESSION_ID",
        "CODEX_SESSION_ID",
        "CLAUDE_SESSION_ID",
    )
    for key in env_keys:
        val = os.environ.get(key, "").strip()
        if val:
            return val
    return f"ppid{os.getppid()}"


def _pack_skill_names() -> set:
    """Enumerate real skill directories only.

    Returns the set of names under skills/<name>/SKILL.md. Symlink redirects and
    anything outside the real pack root are ignored. If the skills directory is
    missing/unreadable or no real skills exist, raises so the caller leaves the
    session RED and warns.
    """
    names = set()
    root = _plugin_root()
    root_real = os.path.realpath(root)
    skills_dir = os.path.join(root, "skills")
    if not os.path.isdir(skills_dir):
        raise OSError(f"skill catalog missing: {skills_dir}")
    for entry in os.listdir(skills_dir):
        skill_dir = os.path.join(skills_dir, entry)
        if not os.path.isdir(skill_dir):
            continue
        candidate = os.path.join(root, "skills", entry, "SKILL.md")
        expected = os.path.join(root_real, "skills", entry, "SKILL.md")
        try:
            real = os.path.realpath(candidate)
        except OSError:
            continue
        if real != expected:
            continue
        if os.path.isfile(real) and os.path.getsize(real) > 0:
            names.add(entry)
    if not names:
        raise ValueError("skill catalog empty")
    return names


def _invoked_skill(tool_input: dict) -> str:
    raw = str(tool_input.get("skill") or tool_input.get("name") or "").strip()
    # Plugin skills arrive namespaced ("backs-aios:optimus"); keep the last part.
    return raw.rsplit(":", 1)[-1]


def _resolve_skill_path(canonical: str) -> str | None:
    """Return the exact realpath of skills/<canonical>/SKILL.md, rejecting symlink tricks."""
    root = _plugin_root()
    root_real = os.path.realpath(root)
    candidate = os.path.join(root, "skills", canonical, "SKILL.md")
    expected = os.path.join(root_real, "skills", canonical, "SKILL.md")
    try:
        real = os.path.realpath(candidate)
        if real != expected:
            return None
        if os.path.isfile(real) and os.path.getsize(real) > 0:
            return real
    except OSError:
        return None
    return None


def _write_floor_marker(session_id: str) -> None:
    """Atomic marker writer shared by native Skill events and explicit --load."""
    target = _state_file(session_id)
    dir_ = os.path.dirname(target)
    os.makedirs(dir_, exist_ok=True)
    tmp = os.path.join(
        dir_,
        f".tmp-{os.getpid()}-{int(time.time() * 1000)}-{os.urandom(4).hex()}",
    )
    fd = None
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        data = b"floor loaded\n"
        written = 0
        while written < len(data):
            n = os.write(fd, data[written:])
            if n <= 0:
                raise OSError(f"write made no progress ({n} bytes)")
            written += n
        os.fsync(fd)
        os.close(fd)
        fd = None
        os.replace(tmp, target)
    except Exception:
        if fd is not None:
            with contextlib.suppress(OSError):
                os.close(fd)
        with contextlib.suppress(OSError):
            os.unlink(tmp)
        raise


def _deny(cursor_protocol: bool) -> None:
    if cursor_protocol:
        print(json.dumps({
            "permission": "deny",
            "user_message": DENY_MESSAGE,
            "agent_message": DENY_MESSAGE,
        }))
        return
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
    cursor_protocol = (
        event in {"sessionStart", "preToolUse", "postToolUse"}
        or bool(payload.get("cursor_version"))
    )
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        tool_input = {}
    session_id = _session_id(payload)

    if event in {"SessionStart", "sessionStart"}:
        _remove_state(session_id)
        return

    if event in {"PostToolUse", "postToolUse"}:
        if tool_name == "Skill":
            skill = _invoked_skill(tool_input)
            if skill:
                try:
                    pack = _pack_skill_names()
                except (OSError, ValueError) as exc:
                    print(
                        f"aios_gate: WARNING skill catalog unreadable or empty, floor stays RED ({exc})",
                        file=sys.stderr,
                    )
                else:
                    if skill in pack:
                        _write_floor_marker(session_id)
        return

    if event in {"PreToolUse", "preToolUse"}:
        red = not _state_exists(session_id)
        if tool_name in {"Bash", "Shell"}:
            if red and _bash_is_mutating(str(tool_input.get("command") or "")):
                _deny(cursor_protocol)
            return  # read-only shell always passes, red or green
        if tool_name not in MUTATING_TOOLS:
            return  # read-only and unknown tools always pass
        if not red:
            return  # floor loaded this session: allow
        _deny(cursor_protocol)
        return
    # Any other event: no decision.


def _load(argv: list) -> int:
    try:
        if not argv:
            sys.stderr.write("aios_gate: skill not found\n")
            return 2
        skill_arg = argv[0]
        if ":" in skill_arg:
            if not skill_arg.startswith("backs-aios:"):
                sys.stderr.write("aios_gate: skill not found\n")
                return 2
            canonical = skill_arg[len("backs-aios:"):]
        else:
            canonical = skill_arg
        if not canonical or not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", canonical):
            sys.stderr.write("aios_gate: skill not found\n")
            return 2
        resolved = _resolve_skill_path(canonical)
        if not resolved:
            sys.stderr.write("aios_gate: skill not found\n")
            return 2
        with open(resolved, "r", encoding="utf-8") as fh:
            body = fh.read()
        session_id = _session_id({}, argv[1] if len(argv) > 1 else None)
        _write_floor_marker(session_id)
        sys.stdout.write(body)
        return 0
    except Exception as exc:
        sys.stderr.write(f"aios_gate: load failed ({type(exc).__name__}: {exc})\n")
        return 1


def _rearm(argv: list) -> int:
    try:
        sid = _session_id({}, argv[0] if argv else None)
        path = _state_file(sid)
        if os.path.isfile(path):
            os.remove(path)
            print("aios_gate: re-armed")
        else:
            print("aios_gate: already armed")
        return 0
    except Exception as exc:
        sys.stderr.write(f"aios_gate: re-arm failed ({type(exc).__name__}: {exc})\n")
        return 1


def _run_stdin_hook() -> int:
    kill = os.environ.get(KILL_ENV, "").strip().lower()
    if kill in {"off", "0", "false", "no"}:
        print("aios_gate: disabled by AIOS_GATE; allowing", file=sys.stderr)
        return 0  # kill-switch: gate disabled, everything passes
    payload = json.loads(sys.stdin.read() or "{}")
    if not isinstance(payload, dict):
        raise ValueError("hook payload is not a JSON object")
    handle(payload)
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if argv and argv[0] in {"--load", "load"}:
        return _load(argv[1:])
    if argv and argv[0] == "--rearm":
        return _rearm(argv[1:])
    return _run_stdin_hook()


if __name__ == "__main__":
    argv = sys.argv[1:]
    is_explicit = bool(argv and argv[0] in {"--load", "load", "--rearm"})
    try:
        sys.exit(main())
    except Exception as exc:
        if is_explicit:
            sys.stderr.write(f"aios_gate: command failed ({type(exc).__name__}: {exc})\n")
            sys.exit(1)
        print(f"aios_gate: WARNING gate error, allowing ({type(exc).__name__}: {exc})",
              file=sys.stderr)
        sys.exit(0)
