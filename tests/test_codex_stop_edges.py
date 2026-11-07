"""Physical Stop boundary cases, separate from sealed progression contracts."""
import pytest

from test_codex_stop_direct import helper, physical_run


def payload(workspace, **changes):
    return {"session_id": "session-one", "cwd": str(workspace),
            "turn_id": "edge-turn", **changes}


def test_missing_session_is_reported(helper, tmp_path):
    with pytest.raises(ValueError, match="session_id missing"):
        helper.stop({"cwd": str(tmp_path)})


def test_no_bound_runs_does_not_request_continuation(helper, tmp_path):
    assert helper.stop(payload(tmp_path)) is None


def test_unmatched_session_does_not_consume_another_run(helper, physical_run):
    store, workspace, incoming = physical_run
    helper.bind("run-one", incoming)
    with pytest.raises(ValueError, match="missing or ambiguous"):
        helper.stop(payload(workspace, session_id="other-session"))
    assert store.get_status("run-one")["run"]["codex_continuation"]["callback_count"] == 0


@pytest.mark.parametrize("state", ["paused", "continuation_pending"])
def test_nonconsumable_states_do_not_schedule(helper, physical_run, state):
    store, workspace, incoming = physical_run
    helper.bind("run-one", incoming)
    store.update_manifest("run-one", status=state)
    assert helper.stop(payload(workspace)) is None
    assert store.get_status("run-one")["run"]["codex_continuation"]["callback_count"] == 0


def test_wrong_workspace_keeps_original_checkpoint(helper, physical_run, tmp_path):
    store, _, incoming = physical_run
    helper.bind("run-one", incoming)
    assert helper.stop(payload(tmp_path / "other")) is None
    assert store.get_status("run-one")["run"]["status"] == "running"


def test_completed_stop_records_terminal_reason_once(helper, physical_run):
    store, workspace, incoming = physical_run
    helper.bind("run-one", incoming)
    store.update_manifest("run-one", status="completed")
    assert helper.stop(payload(workspace)) is None
    assert helper.stop(payload(workspace)) is None
    saved = store.get_status("run-one")["run"]
    assert saved["status"] == "completed"
    assert saved["codex_continuation"]["terminal_reason"] == "terminal:completed"


def test_callback_ceiling_is_physical_and_never_reset(helper, physical_run):
    store, workspace, incoming = physical_run
    helper.bind("run-one", incoming)
    binding = store.get_status("run-one")["run"]["codex_continuation"]
    binding["callback_count"] = binding["callback_ceiling"]
    store.update_manifest("run-one", codex_continuation=binding)
    assert helper.stop(payload(workspace)) is None
    saved = store.get_status("run-one")["run"]["codex_continuation"]
    assert saved["terminal_reason"] == "budget_exhausted:callbacks"
    assert saved["callback_count"] == saved["callback_ceiling"]
