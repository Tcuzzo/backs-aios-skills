#!/usr/bin/env python3
"""Bound native Codex Stop callbacks to one existing durable BACKS run."""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import sys

TERMINAL = {"completed", "complete", "done", "cancelled", "canceled", "failed", "blocked"}

def _store():
    root = Path(os.environ.get("BACKS_DEPLOY_ROOT") or os.environ.get("BACKS_AI_ROOT") or "")
    if not root.is_dir():
        raise RuntimeError("deployed BACKS root unavailable")
    sys.path.insert(0, str(root / "backend"))
    from core.durable_runs import DurableRunStore
    return DurableRunStore(repo_root=root)

def _read_stdin() -> dict:
    value = json.load(sys.stdin)
    if not isinstance(value, dict):
        raise ValueError("payload must be an object")
    return value

def _integer(value, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
    if isinstance(value, float) and (not math.isfinite(value) or not value.is_integer()):
        raise ValueError(f"{name} must be an integer")
    text = str(int(value) if isinstance(value, float) else value).strip()
    if not text.isdigit():
        raise ValueError(f"{name} must be a nonnegative integer")
    return int(text)

def _number(value, name: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError(f"{name} must be numeric or null")
    parsed = float(value)
    if not math.isfinite(parsed) or parsed < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return parsed

@contextmanager
def _run_lock(store, run_id: str):
    path = store.run_dir(run_id) / ".codex_stop.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        yield

def _binding(manifest: dict) -> dict:
    value = manifest.get("codex_continuation")
    if not isinstance(value, dict):
        raise ValueError("bound continuation state malformed")
    return dict(value)

def _progress_decision(binding: dict) -> tuple[bool, str, list[str]]:
    from repo_relay.flexible_budget import ProgressBudget
    history = binding.get("progress_history") or []
    if not _valid_history(history):
        raise ValueError("progress history malformed")
    history = _observed_history(history, binding)
    budget = ProgressBudget(stall_limit=_integer(binding["stall_limit"], "stall_limit"))
    for signature in history:
        budget.record(signature)
    keep_going, reason = budget.should_continue()
    return keep_going, reason, history

def _observed_history(history: list[str], binding: dict) -> list[str]:
    current = str(binding.get("progress_signature") or "").strip()
    if not current:
        raise ValueError("progress signature missing")
    if not history or history[-1] != current or binding.get("status_observation_pending"):
        return [*history, current]
    return history

def _valid_history(history) -> bool:
    return isinstance(history, list) and all(isinstance(item, str) and item for item in history)

def _validate_binding(incoming: dict) -> tuple[str, int, int, float | None, float | None]:
    required = ("mission_id", "session_id", "workspace", "scope", "absolute_deadline",
                "call_ceiling", "calls_used", "cost_ceiling", "cost_used",
                "checkpoint_identity", "stall_limit", "stall_count", "progress_signature")
    if any(key not in incoming for key in required):
        raise ValueError("continuation binding incomplete")
    for key in ("mission_id", "session_id", "checkpoint_identity", "progress_signature"):
        if not isinstance(incoming[key], str) or not incoming[key].strip():
            raise ValueError(f"{key} must be a nonempty string")
    workspace = str(Path(str(incoming["workspace"])).resolve())
    scope = incoming["scope"]
    if (not Path(workspace).is_dir() or not isinstance(scope, list) or not scope
            or any(not isinstance(item, str) or not item.strip() for item in scope)):
        raise ValueError("continuation workspace/scope invalid")
    _deadline(incoming["absolute_deadline"])
    calls_used, call_ceiling, cost_used, cost_ceiling = _validated_usage(incoming)
    return workspace, calls_used, call_ceiling, cost_used, cost_ceiling

def _deadline(value: object) -> datetime:
    try:
        deadline = datetime.fromisoformat(str(value or "").replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("absolute_deadline must be an ISO-8601 timestamp") from exc
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)
    return deadline.astimezone(timezone.utc)

def _validated_usage(incoming: dict) -> tuple[int, int, float | None, float | None]:
    calls_used = _integer(incoming["calls_used"], "calls_used")
    call_ceiling = _integer(incoming["call_ceiling"], "call_ceiling")
    cost_used = _number(incoming["cost_used"], "cost_used")
    cost_ceiling = _number(incoming["cost_ceiling"], "cost_ceiling")
    if calls_used > call_ceiling:
        raise ValueError("calls_used exceeds call_ceiling")
    if cost_used is not None and cost_ceiling is not None and cost_used > cost_ceiling:
        raise ValueError("cost_used exceeds cost_ceiling")
    return calls_used, call_ceiling, cost_used, cost_ceiling

def _mapping(value: object, name: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"task packet {name} must be an object")
    return value

def binding_from_task_packet(packet: dict) -> dict:
    """Normalize the Build Flow packet into the one native Stop binding."""
    packet = _mapping(packet, "root")
    mission = _mapping(packet.get("mission"), "mission")
    episode = _mapping(packet.get("episode"), "episode")
    budget = _mapping(episode.get("resource_budget"), "episode.resource_budget")
    used = _mapping(episode.get("resources_used"), "episode.resources_used")
    calls_used, cost_used = _cumulative_packet_usage(episode, used)
    owner = _mapping(packet.get("continuation_binding"), "continuation_binding")
    required_owner = ("session_id", "workspace", "scope", "checkpoint_identity",
                      "stall_limit", "stall_count", "progress_signature")
    missing = [name for name in required_owner if name not in owner]
    if missing:
        raise ValueError("task packet continuation_binding missing " + ", ".join(missing))
    binding = {
        "mission_id": mission.get("mission_id"),
        "session_id": owner["session_id"],
        "workspace": str(Path(str(owner["workspace"])).resolve()),
        "scope": owner["scope"],
        "absolute_deadline": episode.get("deadline"),
        "call_ceiling": budget.get("call_ceiling"),
        "calls_used": calls_used,
        "cost_ceiling": budget.get("cost_ceiling"),
        "cost_used": cost_used,
        "checkpoint_identity": owner["checkpoint_identity"],
        "stall_limit": owner["stall_limit"],
        "stall_count": owner["stall_count"],
        "progress_signature": owner["progress_signature"],
        "next_action": packet.get("next_action"),
    }
    _validate_binding(binding)
    return binding

def _cumulative_packet_usage(episode: dict, current: dict) -> tuple[int, float | None]:
    if "prior_counters" not in episode:
        raise ValueError("task packet episode.prior_counters is required")
    prior = episode["prior_counters"]
    if not isinstance(prior, list):
        raise ValueError("task packet episode.prior_counters must be a list")
    rows = [*_packet_counter_rows(prior), current]
    calls = sum(_integer(row.get("calls_used"), "calls_used") for row in rows)
    costs = [_number(row.get("cost_used"), "cost_used") for row in rows]
    cost = None if any(value is None for value in costs) else sum(costs)
    return calls, cost

def _packet_counter_rows(rows: list) -> list[dict]:
    return [_mapping(row, f"episode.prior_counters[{index}]") for index, row in enumerate(rows)]

def _original_binding(incoming: dict, prior: dict, workspace: str, callback_ceiling: int) -> dict:
    immutable = ("mission_id", "session_id", "workspace", "scope", "absolute_deadline",
                 "call_ceiling", "cost_ceiling", "checkpoint_identity", "stall_limit")
    originals = dict(prior.get("original_binding") or {})
    if not originals:
        originals = {key: incoming.get(key) for key in immutable}
        originals.update(workspace=workspace, callback_ceiling=callback_ceiling)
    for key in immutable:
        candidate = workspace if key == "workspace" else incoming.get(key)
        if candidate != originals.get(key):
            raise ValueError(f"continuation rebind changed original {key}")
    return originals

def _merged_binding(incoming: dict, prior: dict, originals: dict,
                    usage: tuple[int, float | None], callback_ceiling: int) -> dict:
    calls_used, cost_used = usage
    prior_calls = _integer(prior.get("calls_used", 0), "calls_used")
    prior_cost = _number(prior.get("cost_used"), "cost_used")
    signature = str(incoming["progress_signature"] or "").strip()
    if not signature:
        raise ValueError("progress signature missing")
    history = _bound_history(prior, signature)
    bound = {**originals, **prior}
    bound.update(version="codex_stop_continuation.v2", original_binding=originals,
        progress_signature=signature, progress_history=history,
        stall_count=_integer(incoming["stall_count"], "stall_count"),
        calls_used=max(prior_calls, calls_used),
        cost_used=_retained_cost(prior_cost, cost_used, has_prior=bool(prior)),
        callback_count=_integer(prior.get("callback_count", 0), "callback_count"),
        callback_ceiling=callback_ceiling,
        last_callback_identity=str(prior.get("last_callback_identity") or ""),
        consumed_callback_identity=str(prior.get("last_callback_identity") or ""),
        next_action=str(incoming.get("next_action") or prior.get("next_action") or "resume the durable checkpoint"),
        status_observation_pending=False)
    return bound

def _bound_history(prior: dict, signature: str) -> list[str]:
    history = list(prior.get("progress_history") or [])
    if not history or history[-1] != signature:
        history.append(signature)
    return history

def _retained_cost(prior: float | None, incoming: float | None, *, has_prior: bool) -> float | None:
    if not has_prior:
        return incoming
    if prior is None or incoming is None:
        return None
    return max(prior, incoming)

def bind(run_id: str, incoming: dict) -> dict:
    store = _store()
    workspace, calls_used, call_ceiling, cost_used, _ = _validate_binding(incoming)
    with _run_lock(store, run_id):
        manifest = store.get_status(run_id)["run"]
        prior = manifest.get("codex_continuation") or {}
        prior_originals = prior.get("original_binding") or {}
        callback_ceiling = _integer(prior_originals.get("callback_ceiling", max(0, call_ceiling - calls_used)), "callback_ceiling")
        originals = _original_binding(incoming, prior, workspace, callback_ceiling)
        bound = _merged_binding(incoming, prior, originals, (calls_used, cost_used), callback_ceiling)
        bound["workspace"] = workspace
        status = str(manifest.get("status") or "").lower()
        next_status = status if status in TERMINAL else "running"
        saved = store.update_manifest(run_id, status=next_status, codex_continuation=bound)
        store.append_event(run_id, event_type="codex.stop.checkpoint_bound", payload={
            "checkpoint_identity": bound["checkpoint_identity"],
            "consumed_callback_identity": bound["consumed_callback_identity"]})
        return saved

def _expired(value: object, *, now: datetime | None = None) -> bool:
    deadline = _deadline(value)
    current = datetime.now(timezone.utc) if now is None else now
    return current >= deadline.astimezone(timezone.utc)

def _callback_identity(payload: dict, session: str, cwd: str) -> str:
    turn_id = str(payload.get("turn_id") or "").strip()
    source = ("turn\0" + session + "\0" + turn_id if turn_id else
              "legacy\0" + session + "\0" + cwd + "\0" + str(payload.get("transcript_path") or ""))
    return hashlib.sha256(source.encode()).hexdigest()

def _stop_reason(manifest: dict, binding: dict, control: dict) -> str:
    status = str(manifest.get("status") or "").lower()
    if status in TERMINAL:
        return f"terminal:{status}"
    if _integer(control.get("stop_sequence") or 0, "stop_sequence") > 0:
        return "cancelled:operator_stop"
    budget_reason = _resource_stop_reason(binding)
    if budget_reason:
        return budget_reason
    if _expired(binding["absolute_deadline"]):
        return "budget_exhausted:deadline"
    return ""

def _resource_stop_reason(binding: dict) -> str:
    if _integer(binding["calls_used"], "calls_used") >= _integer(binding["call_ceiling"], "call_ceiling"):
        return "budget_exhausted:calls"
    cost_used = _number(binding.get("cost_used"), "cost_used")
    cost_ceiling = _number(binding.get("cost_ceiling"), "cost_ceiling")
    if cost_used is not None and cost_ceiling is not None and cost_used >= cost_ceiling:
        return "budget_exhausted:cost"
    return ""

def _persist_stop(store, run_id: str, binding: dict, reason: str) -> None:
    if binding.get("terminal_reason") == reason:
        return
    binding["terminal_reason"] = reason
    store.update_manifest(run_id, codex_continuation=binding)
    store.append_event(run_id, event_type="codex.stop.terminal", payload={"reason": reason})

def stop(payload: dict) -> dict | None:
    store = _store()
    session = str(payload.get("session_id") or "").strip()
    cwd = str(Path(str(payload.get("cwd") or ".")).resolve())
    if not session:
        raise ValueError("Stop session_id missing")
    rows = store.list_recent_runs(resume_identity=session, surface="codex", limit=2, max_scan=100)
    if len(rows) != 1:
        if any(store._base_dir().glob("*/run_manifest.json")):
            raise ValueError("bound continuation state missing or ambiguous")
        return None
    run_id = str(rows[0].get("run_id") or "")
    with _run_lock(store, run_id):
        return _stop_locked(store, run_id, payload, session, cwd)

def _stop_locked(store, run_id: str, payload: dict, session: str, cwd: str) -> dict | None:
    manifest = store.get_status(run_id)["run"]
    binding = _binding(manifest)
    if binding.get("session_id") != session or binding.get("workspace") != cwd:
        return None
    reason = _stop_reason(manifest, binding, store.read_control_state(run_id))
    if reason:
        _persist_stop(store, run_id, binding, reason); return None
    status = str(manifest.get("status") or "").lower()
    callback = _callback_identity(payload, session, cwd)
    if status not in {"running", "state_escalation", "continuation_pending"}:
        return None
    if binding.get("last_callback_identity") == callback or status == "continuation_pending":
        return None
    return _schedule_callback(store, run_id, binding, callback)

def _schedule_callback(store, run_id: str, binding: dict, callback: str) -> dict | None:
    binding["status_observation_pending"] = True
    keep_going, reason, history = _progress_decision(binding)
    binding.update(progress_history=history, stall_count=max(0, len(history) - len(set(history))))
    if not keep_going:
        _persist_stop(store, run_id, binding, reason); return None
    count = _integer(binding.get("callback_count", 0), "callback_count")
    ceiling = _integer(binding.get("callback_ceiling", 0), "callback_ceiling")
    if count >= ceiling:
        _persist_stop(store, run_id, binding, "budget_exhausted:callbacks"); return None
    binding.update(last_callback_identity=callback, callback_count=count + 1,
                   status_observation_pending=False, terminal_reason="")
    store.update_manifest(run_id, status="continuation_pending", codex_continuation=binding)
    store.append_event(run_id, event_type="codex.stop.continuation_pending", payload={
        "mission_id": binding["mission_id"], "checkpoint_identity": binding["checkpoint_identity"],
        "callback_identity": callback})
    limits = (f"callbacks {binding['callback_count']}/{ceiling}; provider calls "
              f"{binding['calls_used']}/{binding['call_ceiling']}; deadline {binding['absolute_deadline']}")
    return {"decision": "block", "reason": f"Continue existing run {run_id} in this thread from checkpoint "
        f"{binding['checkpoint_identity']}. Next action: {binding['next_action']}. Limits: {limits}."}

def main() -> int:
    try:
        if len(sys.argv) == 3 and sys.argv[1] == "bind":
            bind(sys.argv[2], _read_stdin()); return 0
        if len(sys.argv) == 3 and sys.argv[1] == "bind-task-packet":
            bind(sys.argv[2], binding_from_task_packet(_read_stdin())); return 0
        if len(sys.argv) == 2 and sys.argv[1] == "stop":
            result = stop(_read_stdin())
            if result is not None:
                print(json.dumps(result, separators=(",", ":")))
            return 0
        raise ValueError("usage: codex_stop_continuation.py bind RUN_ID|bind-task-packet RUN_ID|stop")
    except Exception as exc:
        print(f"BACKS continuation unavailable: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
