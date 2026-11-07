"""In-process coverage for the bounded Codex Stop continuation helper."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import importlib.util
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
DEPLOY = Path(os.environ["BACKS_DEPLOY_ROOT"])
HELPER_PATH = ROOT / "hooks/codex_stop_continuation.py"


def _load_helper():
    spec = importlib.util.spec_from_file_location("codex_stop_continuation_direct", HELPER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def helper(tmp_path, monkeypatch):
    monkeypatch.setenv("BACKS_DEPLOY_ROOT", str(DEPLOY))
    monkeypatch.setenv("BACKS_AI_DURABLE_RUN_DIR", str(tmp_path / "runs"))
    return _load_helper()


@pytest.fixture
def physical_run(helper, tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    store = helper._store()
    store.ensure_run(
        run_id="run-one", surface="codex", trace_id="trace", run_context_id="ctx",
        resume_identity="session-one", prompt="continue", mission_id="mission-one",
        status="running",
    )
    binding = {
        "mission_id": "mission-one", "session_id": "session-one",
        "workspace": str(workspace), "scope": ["hooks/"],
        "absolute_deadline": "2999-01-01T00:00:00+00:00",
        "call_ceiling": 8, "calls_used": 3, "cost_ceiling": 10.0,
        "cost_used": 2.5, "checkpoint_identity": "checkpoint-1",
        "stall_limit": 3, "stall_count": 0, "progress_signature": "p1",
    }
    return store, workspace, binding


@pytest.mark.parametrize("value,expected", [(0, 0), ("7", 7), (3.0, 3)])
def test_integer_accepts_only_nonnegative_whole_values(helper, value, expected):
    assert helper._integer(value, "limit") == expected


@pytest.mark.parametrize("value", [True, -1, 1.5, float("inf"), "nope"])
def test_integer_rejects_invalid_limits(helper, value):
    with pytest.raises(ValueError):
        helper._integer(value, "limit")


@pytest.mark.parametrize("value,expected", [(None, None), (0, 0.0), ("2.5", 2.5)])
def test_number_preserves_unknown_cost_and_parses_real_cost(helper, value, expected):
    assert helper._number(value, "cost") == expected


@pytest.mark.parametrize("value", [False, -0.1, float("nan"), float("inf"), "bad"])
def test_number_rejects_fabricated_or_invalid_cost(helper, value):
    with pytest.raises((ValueError, TypeError)):
        helper._number(value, "cost")


def test_progress_history_distinguishes_replay_from_observed_turn(helper):
    binding = {"progress_signature": "p1", "status_observation_pending": False}
    assert helper._observed_history(["p1"], binding) == ["p1"]
    binding["status_observation_pending"] = True
    assert helper._observed_history(["p1"], binding) == ["p1", "p1"]
    binding.update(progress_signature="p2", status_observation_pending=False)
    assert helper._observed_history(["p1"], binding) == ["p1", "p2"]


def test_bind_preserves_usage_ceilings_and_unknown_cost(helper, physical_run):
    store, _, incoming = physical_run
    incoming.update(cost_used=None, cost_ceiling=None)
    saved = helper.bind("run-one", incoming)["codex_continuation"]
    assert saved["calls_used"] == 3
    assert saved["call_ceiling"] == 8
    assert saved["callback_ceiling"] == 5
    assert saved["cost_used"] is None
    assert saved["cost_ceiling"] is None
    assert store.get_status("run-one")["run"]["status"] == "running"


def test_rebind_never_replaces_unknown_cumulative_cost_with_known_prior(helper, physical_run):
    _, _, incoming = physical_run
    incoming["cost_ceiling"] = None
    helper.bind("run-one", incoming)
    incoming.update(cost_used=None, progress_signature="p2")
    saved = helper.bind("run-one", incoming)["codex_continuation"]
    assert saved["cost_used"] is None


@pytest.mark.parametrize("terminal", ["completed", "cancelled", "failed", "blocked"])
def test_bind_does_not_resurrect_terminal_run(helper, physical_run, terminal):
    store, _, incoming = physical_run
    store.update_manifest("run-one", status=terminal)
    helper.bind("run-one", incoming)
    assert store.get_status("run-one")["run"]["status"] == terminal


def test_bind_does_not_clear_operator_stop(helper, physical_run):
    store, _, incoming = physical_run
    store.update_manifest("run-one", last_stop_sequence=1)
    helper.bind("run-one", incoming)
    manifest = store.get_status("run-one")["run"]
    assert manifest["last_stop_sequence"] == 1
    assert helper._stop_reason(
        manifest, manifest["codex_continuation"], store.read_control_state("run-one")
    ) == "cancelled:operator_stop"


def test_stop_is_idempotent_per_turn_and_successive_progress_continues(helper, physical_run):
    store, workspace, incoming = physical_run
    helper.bind("run-one", incoming)
    first_payload = {"session_id": "session-one", "cwd": str(workspace), "turn_id": "turn-1"}
    assert helper.stop(first_payload)["decision"] == "block"
    assert helper.stop(first_payload) is None
    bound = store.get_status("run-one")["run"]["codex_continuation"]
    assert bound["callback_count"] == 1
    bound["progress_signature"] = "p2"
    store.update_manifest("run-one", status="running", codex_continuation=bound)
    assert helper.stop({**first_payload, "turn_id": "turn-2"})["decision"] == "block"
    after = store.get_status("run-one")["run"]["codex_continuation"]
    assert after["callback_count"] == 2
    assert after["calls_used"] == 3 and after["cost_used"] == 2.5


@pytest.mark.parametrize(
    "change,expected",
    [
        ({"calls_used": 8}, "budget_exhausted:calls"),
        ({"cost_used": 10.0}, "budget_exhausted:cost"),
        ({"absolute_deadline": (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()},
         "budget_exhausted:deadline"),
    ],
)
def test_physical_stop_persists_real_budget_reason(helper, physical_run, change, expected):
    store, workspace, incoming = physical_run
    helper.bind("run-one", incoming)
    bound = store.get_status("run-one")["run"]["codex_continuation"]
    bound.update(change)
    store.update_manifest("run-one", status="running", codex_continuation=bound)
    assert helper.stop({"session_id": "session-one", "cwd": str(workspace), "turn_id": "turn"}) is None
    saved = store.get_status("run-one")["run"]["codex_continuation"]
    assert saved["terminal_reason"] == expected
