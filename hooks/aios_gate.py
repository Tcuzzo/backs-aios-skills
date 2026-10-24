#!/usr/bin/env python3
"""BACKS grounding loader: deliver actual floor bodies without tool refusal.

Context delivery and explicit Skill evidence are separate. AIOS_GATE=off remains
available. Hook failures warn and allow; explicit load errors return nonzero.
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
MUTATING_TOOLS = {
    "Delete", "Edit", "MultiEdit", "NotebookEdit", "Write",
    # Codex exposes its patch primitive both directly and under its function namespace.
    "apply_patch", "functions.apply_patch",
}
CODEX_EXEC_TOOL = "functions.exec"
_CODEX_PATCH_CALL = re.compile(r"\b(?:tools|functions)\s*\.\s*apply_patch\s*\(")

# A verb counts only at a command position: line start, after ; & |, or inside
# a substitution. "grep rm" or "echo 'rm x'" can never match.
_CMD_POS = r"(?:^|[;&|\r\n]|\$\(|`)\s*(?:sudo\s+)?"

# Conservative mutating-verb patterns for Bash. Loading runs only on a positive
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
    # Audit 2026-10-07 AA-7: a child Codex session sets BOTH ``CODEX_SESSION_ID``
    # and ``CODEX_THREAD_ID``. The hook payload arrives with ``session_id`` (==
    # SESSION_ID); the explicit ``--load`` falls back to env. If the loader
    # picks THREAD_ID while the hook reads SESSION_ID, state is written at one
    # identity and read at the other -- the child session flips RED. The
    # documented invocation ``--load <skill> "$CODEX_SESSION_ID"`` aligned them
    # manually; the fix is to align the env chain itself: SESSION_ID wins over
    # THREAD_ID by default. Same env-key order as ``hooks/aios_gate.js`` so a
    # future change cannot reintroduce the divergence. Class scope (inv_23):
    # one identity seam, no new hook, no operator approval friction.
    env_keys = (
        "BACKS_BUILD_SESSION",
        "CLAUDE_CODE_SESSION_ID",
        "CODEX_SESSION_ID",
        "CURSOR_SESSION_ID",
        "CURSOR_CONVERSATION_ID",
        "OPENCODE_SESSION_ID",
        "CODEX_THREAD_ID",
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
    session without a new receipt and warns.
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


def _codex_exec_invokes_patch(tool_name: str, raw_tool_input: object) -> bool:
    """Match Codex's nested patch call without blocking unrelated exec calls."""
    if tool_name != CODEX_EXEC_TOOL:
        return False
    if isinstance(raw_tool_input, str):
        sources = (raw_tool_input,)
    elif isinstance(raw_tool_input, dict):
        sources = tuple(
            raw_tool_input[key]
            for key in ("code", "script", "input")
            if isinstance(raw_tool_input.get(key), str)
        )
    else:
        sources = ()
    return any(_CODEX_PATCH_CALL.search(source) for source in sources)


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



def _co_state_dir() -> str:
    preferred = os.path.join(os.path.expanduser("~"), ".claude", "state")
    try:
        os.makedirs(preferred, exist_ok=True)
        return preferred
    except OSError:
        return tempfile.gettempdir()


def _write_co_grounding_evidence(session_id: str, skill_digests: dict | None = None) -> dict:
    """Write CO-readable backs_ground_*.state + .hashes.json (smoking-gun seam)."""
    sid = _state_component(session_id)
    directory = _co_state_dir()
    state_path = os.path.join(directory, f"backs_ground_{sid}.state")
    hash_path = os.path.join(directory, f"backs_ground_{sid}.hashes.json")
    digests = {str(k): str(v) for k, v in dict(skill_digests or {}).items() if k and v}

    def _atomic(path: str, data: bytes) -> None:
        tmp = os.path.join(
            directory,
            f".tmp-{os.getpid()}-{time.time_ns()}-{os.path.basename(path)}",
        )
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        fd = os.open(tmp, flags, 0o600)
        try:
            os.write(fd, data)
            os.fsync(fd)
        finally:
            os.close(fd)
        os.replace(tmp, path)

    _atomic(state_path, b"true\n")
    _atomic(hash_path, json.dumps(digests, sort_keys=True).encode("utf-8"))
    return {"state": state_path, "hashes": hash_path}


def _deploy_root() -> str:
    env = str(os.environ.get("BACKS_DEPLOY_ROOT") or os.environ.get("BACKS_AI_ROOT") or "").strip()
    if env:
        return env
    for host in ('.codex', '.claude'):
        skill = os.path.realpath(os.path.expanduser(os.path.join('~', host, 'skills/optimus/SKILL.md')))
        candidate = os.path.dirname(os.path.dirname(os.path.dirname(skill)))
        if os.path.isfile(os.path.join(candidate, 'backend/prompts/BACKS_CODEX_HARNESS.md')):
            return candidate
    return ""


def _resolve_native_or_pack_skill(canonical: str):
    aliases = {
        "yoke": ("human-calibration", "yoke"),
        "human-calibration": ("human-calibration", "yoke"),
        "optimus": ("optimus",),
        "conscientious-objector": ("conscientious_objector", "conscientious-objector"),
        "conscientious_objector": ("conscientious_objector", "conscientious-objector"),
    }
    names = aliases.get(canonical, (canonical,))
    root = _deploy_root()
    if root:
        for name in names:
            p = os.path.join(root, "skills", name, "SKILL.md")
            if os.path.isfile(p) and os.path.getsize(p) > 0:
                return p, name, "deploy_native"
    for name in names:
        p = _resolve_skill_path(name)
        if p:
            return p, name, "installed_pack"
    return None


def _wake_load_context() -> str:
    """Name wake skills without copying their full bodies into every session."""
    return (
        "BACKS wake-load: invoke operator_intent_deduction before handing the "
        "operator a decision, and invoke context_engineer when compiling task "
        "context. context-compiler is a context_engineer alias; intent-compiler is a "
        "separate skill. Load skill bodies through the skill runtime only when needed."
    )


def _floor_context() -> tuple[str, list[dict]]:
    entries = []
    root = _deploy_root()
    harness = os.path.join(root, 'backend/prompts/BACKS_CODEX_HARNESS.md')
    if root and os.path.isfile(harness):
        entries.append((harness, 'harness', 'deploy_native'))
    for name in ('optimus', 'yoke'):
        resolved = _resolve_native_or_pack_skill(name)
        if not resolved:
            raise ValueError(f'{name} unavailable')
        entries.append(resolved)
    context = [_wake_load_context()]
    bodies = []
    for filename, canonical, source in entries:
        with open(filename, encoding='utf-8', newline='') as handle:
            body = handle.read()
        if not body.strip():
            raise ValueError(f'{canonical} unavailable')
        context.append(f'## BACKS loaded: {canonical}\n{body}')
        bodies.append({'path': filename, 'canonical': canonical, 'source': source,
                       'sha256': hashlib.sha256(body.encode()).hexdigest()})
    return '\n\n'.join(context), bodies


def _write_stdout(body: str) -> None:
    # Complete the real host write before recording delivery. Buffered stdout
    # can otherwise fail again at interpreter shutdown and change exit status.
    remaining = memoryview(body.encode('utf-8'))
    while remaining:
        written = os.write(sys.stdout.fileno(), remaining)
        if written <= 0:
            raise OSError('context output made no progress')
        remaining = remaining[written:]


def _deliver_floor(cursor_protocol: bool, session_id: str, event: str) -> None:
    """Deliver actual bodies, then record loading separately from Skill events."""
    try:
        context, bodies = _floor_context()
        output = ({'additional_context': context} if cursor_protocol else
                  {'hookSpecificOutput': {'hookEventName': event, 'additionalContext': context}})
        _write_stdout(json.dumps(output) + '\n')
        target = _state_file(session_id) + '.load.json'
        tmp = target + f'.{os.getpid()}.{os.urandom(6).hex()}.tmp'
        try:
            fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'w', encoding='utf-8') as handle:
                json.dump({'session_id': session_id, 'kind': 'context_delivery', 'bodies': bodies}, handle)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, target)
        finally:
            with contextlib.suppress(OSError):
                os.unlink(tmp)
        _write_floor_marker(session_id)
    except Exception as exc:
        print(f'aios_gate: grounding unavailable ({type(exc).__name__}: {exc}); allowing', file=sys.stderr)


def handle(payload: dict) -> None:
    event = str(payload.get("hook_event_name") or "")
    tool_name = str(payload.get("tool_name") or "")
    cursor_protocol = (
        event in {"sessionStart", "preToolUse", "postToolUse"}
        or bool(payload.get("cursor_version"))
    )
    raw_tool_input = payload.get("tool_input")
    tool_input = raw_tool_input or {}
    if not isinstance(tool_input, dict):
        tool_input = {}
    session_id = _session_id(payload)

    if event in {"SessionStart", "sessionStart"}:
        _deliver_floor(cursor_protocol, session_id, event)
        return

    if event in {"PostToolUse", "postToolUse"}:
        if tool_name == "Skill":
            skill = _invoked_skill(tool_input)
            if skill:
                try:
                    pack = _pack_skill_names()
                except (OSError, ValueError) as exc:
                    print(
                        f"aios_gate: WARNING skill catalog unreadable or empty, grounding evidence unavailable ({exc})",
                        file=sys.stderr,
                    )
                else:
                    if skill in pack:
                        _write_floor_marker(session_id)
                        try:
                            digests = {}
                            info = _resolve_native_or_pack_skill(skill)
                            if info:
                                rp, rn, _ = info
                                with open(rp, "rb") as sfh:
                                    digests[rn] = hashlib.sha256(sfh.read()).hexdigest()
                            _write_co_grounding_evidence(session_id, digests)
                        except Exception as err:
                            sys.stderr.write(f"aios_gate: WARNING CO evidence write failed ({err})\n")
        return

    if event in {"PreToolUse", "preToolUse"}:
        red = not _state_exists(session_id)
        if tool_name in {"Bash", "Shell"}:
            if red and _bash_is_mutating(str(tool_input.get("command") or "")):
                _deliver_floor(cursor_protocol, session_id, event)
            return  # read-only shell always passes, red or green
        if tool_name not in MUTATING_TOOLS and not _codex_exec_invokes_patch(
            tool_name, raw_tool_input
        ):
            return  # read-only and unknown tools always pass
        if not red:
            return  # floor loaded this session: allow
        _deliver_floor(cursor_protocol, session_id, event)
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
        if not canonical or not re.match(r"^[a-z0-9]+([_-][a-z0-9]+)*$", canonical):
            sys.stderr.write("aios_gate: skill not found\n")
            return 2
        resolved_info = _resolve_native_or_pack_skill(canonical)
        if not resolved_info:
            sys.stderr.write("aios_gate: skill not found\n")
            return 2
        resolved, resolved_name, _src = resolved_info
        with open(resolved, "r", encoding="utf-8", newline="") as fh:
            body = fh.read()
        session_id = _session_id({}, argv[1] if len(argv) > 1 else None)
        digests = {resolved_name: hashlib.sha256(body.encode("utf-8")).hexdigest()}
        if resolved_name == "optimus" or canonical == "optimus":
            yoke = _resolve_native_or_pack_skill("yoke")
            if yoke:
                yp, yn, _ = yoke
                with open(yp, encoding='utf-8', newline='') as yfh:
                    yoke_body = yfh.read()
                digests[yn] = hashlib.sha256(yoke_body.encode()).hexdigest()
                body += '\n\n' + yoke_body
        _write_stdout(body)
        _write_floor_marker(session_id)
        try:
            _write_co_grounding_evidence(session_id, digests)
        except Exception as err:
            sys.stderr.write(f"aios_gate: WARNING CO evidence write failed ({err})\n")
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
