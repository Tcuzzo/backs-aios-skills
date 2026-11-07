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
import subprocess
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


def _canonical_manifest_path() -> str:
    root = _deploy_root()
    return os.path.join(root, "config/foundation_manifest.json") if root else ""


def _has_canonical_manifest() -> bool:
    return bool(_canonical_manifest_path() and os.path.isfile(_canonical_manifest_path()))


def _receipt_matches(receipt, session_id, root, rows) -> bool:
    expected = {'kind': 'foundation_delivery', 'session_id': session_id,
                'source_root': root, 'order': [row['path'] for row in rows],
                'sha256': {row['path']: row['sha256'] for row in rows}}
    if not isinstance(receipt, dict):
        return False
    return (all(receipt.get(key) == value for key, value in expected.items())
            and float(receipt.get('expires_at', 0)) > time.time())


def _canonical_receipt_valid(session_id: str) -> bool:
    try:
        root = os.path.realpath(_deploy_root())
        _foundation_manifest_bodies(root)
        key = hashlib.sha256(str(session_id).encode()).hexdigest()
        receipt_path = os.path.join(os.path.expanduser('~'), '.claude/state', f'backs_load_{key}.json')
        with open(receipt_path, encoding='utf-8') as handle:
            receipt = json.load(handle)
        return _receipt_matches(receipt, session_id, root, _foundation_rows(root))
    except (OSError, ValueError, KeyError, TypeError):
        return False


def _state_exists(session_id: str) -> bool:
    if _has_canonical_manifest():
        return _canonical_receipt_valid(session_id)
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
        "context-engineer": ("context-engineer", "context_engineer", "context-compiler"),
        "context_engineer": ("context-engineer", "context_engineer", "context-compiler"),
        "context-compiler": ("context-engineer", "context_engineer", "context-compiler"),
        "operator-intent-deduction": ("operator-intent-deduction", "operator_intent_deduction"),
        "operator_intent_deduction": ("operator-intent-deduction", "operator_intent_deduction"),
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
        "BACKS wake-load: invoke operator-intent-deduction before handing the "
        "operator a decision, and invoke context-engineer when compiling task "
        "context. Legacy compatibility: operator_intent_deduction resolves to "
        "operator-intent-deduction; context-compiler is a context_engineer alias, "
        "and both resolve to context-engineer. intent-compiler is a separate skill. "
        "Build Flow owns the current task packet; reuse current evidence "
        "and apply operator-essence when operator context is needed. "
        "Load skill bodies through the skill runtime only when needed."
    )


def _read_body(entry) -> dict:
    filename, canonical, source = entry
    with open(filename, encoding='utf-8', newline='') as handle:
        body = handle.read()
    if not body.strip():
        raise ValueError(f'{canonical} unavailable')
    return {'path': filename, 'canonical': canonical, 'source': source,
            'body': body, 'sha256': hashlib.sha256(body.encode()).hexdigest()}


def _foundation_bodies() -> list[dict]:
    bodies = []
    for name in ('optimus', 'yoke', 'backs-build-flow'):
        resolved = _resolve_native_or_pack_skill(name)
        if not resolved:
            raise ValueError(f'{name} unavailable')
        bodies.append(_read_body(resolved))
    return bodies


def _canonical_pointer(root: str) -> str:
    _foundation_manifest_bodies(root)
    rows = _foundation_rows(root)
    context = '=== BACKS FOUNDATION (pinned; not yet delivered whole this session) ===\n'
    context += 'Load every file below in full. Only actual host-observed complete output can certify delivery; a skill marker or stdout success cannot.\n'
    context += '\n'.join(f"{index}. {os.path.join(root, row['path'])} sha256:{row['sha256']}" for index, row in enumerate(rows, 1))
    if len(context.encode()) > 10000:
        raise ValueError('foundation pointer exceeds measured host limit')
    return context


def _floor_context() -> tuple[str, list[dict]]:
    bodies = []
    root = _deploy_root()
    if _has_canonical_manifest():
        return _canonical_pointer(root), []
    harness = os.path.join(root, 'backend/prompts/BACKS_CODEX_HARNESS.md')
    if root and os.path.isfile(harness):
        bodies.append(_read_body((harness, 'harness', 'deploy_native')))
    bodies.extend(_foundation_bodies())
    context = [_wake_load_context()]
    for entry in bodies:
        context.append(f"## BACKS loaded: {entry['canonical']}\n{entry['body']}")
    receipts = [{key: value for key, value in entry.items() if key != 'body'} for entry in bodies]
    return '\n\n'.join(context), receipts


def _foundation_rows(root: str) -> list:
    with open(os.path.join(root, 'config/foundation_manifest.json'), encoding='utf-8') as handle:
        manifest = json.load(handle)
    if not isinstance(manifest, dict):
        raise ValueError('foundation manifest must be an object')
    rows = manifest.get('bodies')
    if not isinstance(rows, list) or not rows:
        raise ValueError('foundation manifest bodies missing')
    return rows


def _foundation_relative(row: dict) -> str:
    if not isinstance(row, dict):
        raise ValueError('unsafe foundation row')
    relative = row.get('path')
    if not isinstance(relative, str) or not relative:
        raise ValueError('unsafe foundation path')
    if os.path.isabs(relative) or "\\" in relative:
        raise ValueError('unsafe foundation path')
    if any(part in {'', '.', '..'} for part in relative.split('/')):
        raise ValueError('unsafe foundation path')
    return relative


def _foundation_body(root: str, row: dict) -> bytes:
    relative = _foundation_relative(row)
    target = os.path.realpath(os.path.join(root, *relative.split('/')))
    if os.path.commonpath((root, target)) != root or not os.path.isfile(target):
        raise ValueError(f'foundation body unavailable: {relative}')
    with open(target, 'rb') as handle:
        body = handle.read()
    expected = row.get('sha256')
    if not isinstance(expected, str) or not re.fullmatch(r'[0-9a-f]{64}', expected):
        raise ValueError(f'foundation hash mismatch: {relative}')
    if hashlib.sha256(body).hexdigest() != expected:
        raise ValueError(f'foundation hash mismatch: {relative}')
    return body + b'\n\n'


def _foundation_manifest_bodies(root: str) -> bytes | None:
    """Verify the whole ordered set before writing any body to stdout."""
    if not root or not os.path.isfile(os.path.join(root, 'config/foundation_manifest.json')):
        return None
    root = os.path.realpath(root)
    return b''.join(_foundation_body(root, row) for row in _foundation_rows(root))


_CODEX_SENTINEL = "printf '%s\\n' BACKS_CODEX_HOOK_SENTINEL_V1"


def _shape_of(value, depth: int = 0):
    """Describe bounded payload structure without retaining raw values."""
    if isinstance(value, str):
        bounded = value[:262144]
        return {'type': 'string', 'bytes': len(value.encode()),
                'sha256': hashlib.sha256(bounded.encode()).hexdigest()}
    primitive = _primitive_shape(value)
    if primitive is not None:
        return primitive
    return _collection_shape(value, depth)


def _primitive_shape(value):
    if value is None:
        return {'type': 'null'}
    if isinstance(value, (bool, int, float)):
        return {'type': type(value).__name__}
    return None


def _collection_shape(value, depth):
    if depth >= 3:
        return {'type': 'array' if isinstance(value, list) else 'object'}
    if isinstance(value, list):
        return {'type': 'array', 'length': len(value),
                'items': [_shape_of(item, depth + 1) for item in value[:8]]}
    if not isinstance(value, dict):
        return {'type': type(value).__name__}
    safe = {'output', 'stdout', 'stderr', 'content', 'text', 'type',
            'exit_code', 'session_id'}
    return {(key if key in safe else f'field_{index}'):
            _shape_of(value[key], depth + 1)
            for index, key in enumerate(list(value)[:16])}


def _observe_codex_tool(payload: dict) -> None:
    tool_input = payload.get('tool_input') or {}
    if (payload.get('tool_name') != 'Bash'
            or tool_input.get('command') != _CODEX_SENTINEL
            or not all(payload.get(key) for key in ('turn_id', 'tool_use_id', 'session_id'))):
        return
    digest = lambda value: hashlib.sha256(str(value).encode()).hexdigest()
    target = os.path.join(_state_dir(), f"codex_tool_shape_{digest(payload['session_id'])}.json")
    evidence = {
        'kind': 'tool_payload_shape',
        'session_sha256': digest(payload['session_id']),
        'turn_sha256': digest(payload['turn_id']),
        'call_sha256': digest(payload['tool_use_id']),
        'command_sha256': digest(_CODEX_SENTINEL),
        'observed_at': time.time(),
        'tool_response': _shape_of(payload.get('tool_response')),
    }
    try:
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            json.dump(evidence, handle)
    except FileExistsError:
        return
    except OSError as exc:
        sys.stderr.write(f'BACKS observer unavailable: {exc.errno}\n')


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
        if _has_canonical_manifest():
            return
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
    cursor_protocol = _cursor_protocol(payload, event)
    raw_tool_input = payload.get("tool_input")
    tool_input = raw_tool_input or {}
    if not isinstance(tool_input, dict):
        tool_input = {}
    session_id = _session_id(payload)

    if event == "Stop":
        _handle_stop(payload)
        return

    if event in {"SessionStart", "sessionStart", "UserPromptSubmit"}:
        _deliver_floor(cursor_protocol, session_id, event)
        return

    if event in {"PostToolUse", "postToolUse"}:
        _handle_post(payload, tool_name, tool_input, session_id)
        return

    if event in {"PreToolUse", "preToolUse"}:
        _handle_pre(tool_name, tool_input, raw_tool_input, session_id, cursor_protocol, event)
        return
    # Any other event: no decision.


def _handle_stop(payload: dict) -> None:
    adapter = os.path.join(_plugin_root(), "hooks", "codex_stop_continuation.py")
    root = _deploy_root()
    if not root or not os.path.isfile(adapter):
        sys.stderr.write("BACKS continuation unavailable: deployed owner or adapter missing\n")
        return
    try:
        result = subprocess.run(
            [os.environ.get("PYTHON", "python3"), adapter, "stop"],
            input=json.dumps(payload), text=True, capture_output=True,
            env={**os.environ, "BACKS_DEPLOY_ROOT": root,
                 "PYTHONPATH": os.path.join(root, "backend")},
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        sys.stderr.write("BACKS continuation unavailable: adapter did not finish (ETIMEDOUT)\n")
        return
    if result.stderr:
        sys.stderr.write(result.stderr)
    if result.returncode != 0 or not result.stdout.strip():
        return
    try:
        json.loads(result.stdout)
    except ValueError as exc:
        sys.stderr.write(f"BACKS continuation unavailable: malformed adapter output ({exc})\n")
        return
    _write_stdout(result.stdout.rstrip("\n") + "\n")


def _cursor_protocol(payload, event):
    return event in {'sessionStart', 'preToolUse', 'postToolUse'} or bool(payload.get('cursor_version'))


def _handle_post(payload, tool_name, tool_input, session_id):
    _observe_codex_tool(payload)
    if tool_name != 'Skill' or not (skill := _invoked_skill(tool_input)):
        return
    try:
        pack = _pack_skill_names()
    except (OSError, ValueError) as exc:
        print(f"aios_gate: WARNING skill catalog unreadable or empty, grounding evidence unavailable ({exc})", file=sys.stderr)
        return
    if skill in pack:
        _record_skill_evidence(skill, session_id)


def _record_skill_evidence(skill, session_id):
    _write_floor_marker(session_id)
    try:
        digests = {}
        if info := _resolve_native_or_pack_skill(skill):
            filename, name, _ = info
            with open(filename, 'rb') as handle_:
                digests[name] = hashlib.sha256(handle_.read()).hexdigest()
        _write_co_grounding_evidence(session_id, digests)
    except Exception as exc:
        sys.stderr.write(f"aios_gate: WARNING CO evidence write failed ({exc})\n")


def _handle_pre(tool_name, tool_input, raw_tool_input, session_id, cursor_protocol, event):
    red = not _state_exists(session_id)
    if tool_name in {'Bash', 'Shell'}:
        mutating = _bash_is_mutating(str(tool_input.get('command') or ''))
    else:
        mutating = (tool_name in MUTATING_TOOLS
                    or _codex_exec_invokes_patch(tool_name, raw_tool_input))
    if red and mutating:
        _deliver_floor(cursor_protocol, session_id, event)


def _load(argv: list) -> int:
    try:
        canonical = _canonical_skill_arg(argv[0] if argv else '')
        if canonical is None:
            return _skill_not_found()
        resolved_info = _resolve_native_or_pack_skill(canonical)
        if not resolved_info:
            return _skill_not_found()
        return _emit_load(canonical, resolved_info, argv[1] if len(argv) > 1 else None)
    except Exception as exc:
        sys.stderr.write(f"aios_gate: load failed ({type(exc).__name__}: {exc})\n")
        return 1


def _emit_load(canonical, resolved_info, session_arg):
    manifest_body = _foundation_manifest_bodies(_deploy_root()) if canonical == 'optimus' else None
    if manifest_body is not None:
        _write_stdout(manifest_body.decode('utf-8'))
        return 0
    bodies = (_foundation_bodies() if resolved_info[1] == 'optimus'
              else [_read_body(resolved_info)])
    _write_stdout('\n\n'.join(entry['body'] for entry in bodies))
    session_id = _session_id({}, session_arg)
    _write_floor_marker(session_id)
    _write_invocation_digests(session_id, bodies)
    return 0


def _write_invocation_digests(session_id, bodies):
    digests = {entry['canonical']: entry['sha256'] for entry in bodies}
    target = os.path.join(_co_state_dir(), f"backs_ground_{_state_component(session_id)}.hashes.json")
    temporary = target + f".{os.getpid()}.tmp"
    try:
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as handle_:
            json.dump(digests, handle_)
        os.replace(temporary, target)
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(temporary)


def _canonical_skill_arg(skill_arg: str) -> str | None:
    if ':' in skill_arg:
        if not skill_arg.startswith('backs-aios:'):
            return None
        skill_arg = skill_arg[len('backs-aios:'):]
    return skill_arg if re.fullmatch(r'[a-z0-9]+(?:[_-][a-z0-9]+)*', skill_arg) else None


def _skill_not_found() -> int:
    sys.stderr.write('aios_gate: skill not found\n')
    return 2


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
