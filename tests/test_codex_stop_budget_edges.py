"""Progress and budget boundaries exposed by isolated mutation testing."""
import pytest

from test_codex_stop_direct import helper, physical_run


@pytest.mark.parametrize("history", ["p1", None, [""], [None], [False]])
def test_history_requires_a_list_of_nonempty_signatures(helper, history):
    assert helper._valid_history(history) is False


def test_stall_history_is_not_discarded(helper):
    helper._store()
    keep_going, reason, history = helper._progress_decision({
        "progress_history": ["p1", "p1"], "progress_signature": "p1",
        "status_observation_pending": True, "stall_limit": 3,
    })
    assert (keep_going, reason, history) == (False, "stalled", ["p1"] * 3)


def test_changed_checkpoint_appends_history_but_replay_does_not(helper):
    assert helper._bound_history({"progress_history": ["p1"]}, "p2") == ["p1", "p2"]
    assert helper._bound_history({"progress_history": ["p1"]}, "p1") == ["p1"]


@pytest.mark.parametrize("scope", [[], "hooks", None])
def test_valid_directory_does_not_make_invalid_scope_valid(helper, physical_run, scope):
    _, _, incoming = physical_run
    with pytest.raises(ValueError, match="workspace/scope invalid"):
        helper._validate_binding({**incoming, "scope": scope})


def test_usage_exactly_at_ceiling_can_be_checkpointed(helper):
    assert helper._validated_usage({"calls_used": 8, "call_ceiling": 8,
        "cost_used": 10, "cost_ceiling": 10}) == (8, 8, 10.0, 10.0)


def test_native_turn_without_progress_reaches_stall_limit(helper, physical_run):
    store, workspace, incoming = physical_run
    helper.bind("run-one", incoming)
    payload = {"session_id": "session-one", "cwd": str(workspace), "turn_id": "turn-1"}
    assert helper.stop(payload)["decision"] == "block"
    store.update_manifest("run-one", status="running")
    assert helper.stop({**payload, "turn_id": "turn-2"}) is None
    binding = store.get_status("run-one")["run"]["codex_continuation"]
    assert binding["terminal_reason"] == "stalled"
    assert binding["progress_history"] == ["p1", "p1", "p1"]
