"""Supplemental physical coverage for bounded Codex Stop state transitions."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest
import test_codex_stop_continuation as fixture_module


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "hooks/codex_stop_continuation.py"
PYTHON_HOOK = ROOT / "hooks/aios_gate.py"


@pytest.fixture
def continuation():
    case = fixture_module.CodexStopContinuationTest(
        methodName="test_active_continuation_is_idempotent_and_preserves_counters"
    )
    case.setUp()
    try:
        yield case
    finally:
        case.tearDown()


def _binding(case):
    return case.manifest()["codex_continuation"]


def _bind(case, binding):
    return subprocess.run(
        [sys.executable, str(ADAPTER), "bind", "run-one"],
        env=case.env,
        input=json.dumps(binding),
        text=True,
        capture_output=True,
        timeout=10,
    )


def test_repeated_progress_signature_persists_stall_reason(continuation):
    assert continuation.stop(turn_id="turn-1").stdout
    continuation.update(status="running")
    stalled = continuation.stop(turn_id="turn-2", stop_hook_active=True)
    assert stalled.stdout == ""
    saved = _binding(continuation)
    assert saved["terminal_reason"] == "stalled"
    assert saved["progress_history"] == ["p1", "p1", "p1"]


def test_two_process_replay_schedules_once_under_physical_lock(continuation):
    payload = {
        "hook_event_name": "Stop", "session_id": continuation.session,
        "cwd": str(continuation.cwd), "turn_id": "same-turn",
        "transcript_path": str(continuation.base / "transcript.jsonl"),
    }
    command = [sys.executable, str(ADAPTER), "stop"]
    processes = [subprocess.Popen(command, env=continuation.env, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                 for _ in range(2)]
    outputs = [process.communicate(json.dumps(payload), timeout=10) for process in processes]
    assert sum(bool(stdout.strip()) for stdout, _ in outputs) == 1
    assert _binding(continuation)["callback_count"] == 1


@pytest.mark.parametrize("field,value", [
    ("calls_used", True), ("call_ceiling", 3.5), ("stall_limit", -1),
    ("cost_used", float("nan")), ("cost_ceiling", -0.5),
])
def test_invalid_numeric_limits_are_rejected_without_rebinding(continuation, field, value):
    before = continuation.manifest()
    binding = {**_binding(continuation), field: value}
    result = _bind(continuation, binding)
    assert result.returncode == 2
    assert "continuation unavailable" in result.stderr
    assert continuation.manifest()["codex_continuation"] == before["codex_continuation"]


def test_unknown_cost_remains_unknown_but_call_and_deadline_bounds_apply(continuation):
    binding = dict(_binding(continuation))
    for key in ("original_binding", "progress_history", "callback_ceiling",
                "callback_count", "last_callback_identity",
                "consumed_callback_identity"):
        binding.pop(key, None)
    binding.update(cost_used=None, cost_ceiling=None)
    continuation.update(codex_continuation=None)
    assert _bind(continuation, binding).returncode == 0
    assert continuation.stop(turn_id="unknown-cost").stdout
    saved = _binding(continuation)
    assert saved["cost_used"] is None and saved["cost_ceiling"] is None
    assert saved["calls_used"] == 3


def test_operator_stop_precedes_progress_and_persists_reason(continuation):
    continuation.update(last_stop_sequence=1)
    result = continuation.stop(turn_id="cancelled")
    assert result.stdout == ""
    assert _binding(continuation)["terminal_reason"] == "cancelled:operator_stop"


def test_python_hook_emits_same_native_stop_decision(continuation):
    payload = {
        "hook_event_name": "Stop", "session_id": continuation.session,
        "cwd": str(continuation.cwd), "turn_id": "python-turn",
        "transcript_path": str(continuation.base / "transcript.jsonl"),
    }
    result = subprocess.run(
        [sys.executable, str(PYTHON_HOOK)], env=continuation.env,
        input=json.dumps(payload), text=True, capture_output=True, timeout=15,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["decision"] == "block"
