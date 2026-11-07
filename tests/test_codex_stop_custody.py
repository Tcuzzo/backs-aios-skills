"""Real checkpoint custody and lock creation across continuation turns."""
from test_codex_stop_direct import helper, physical_run


def test_lock_creates_missing_owned_run_directory(helper):
    store = helper._store()
    path = store.run_dir("new-run") / ".codex_stop.lock"
    assert not path.parent.exists()
    with helper._run_lock(store, "new-run"):
        assert path.is_file()


def test_checkpoint_acknowledges_callback_and_keeps_next_action(helper, physical_run):
    store, workspace, incoming = physical_run
    incoming["next_action"] = "verify the real operator surface"
    helper.bind("run-one", incoming)
    first = store.get_status("run-one")["run"]["codex_continuation"]
    assert first["next_action"] == incoming["next_action"]
    assert first["last_callback_identity"] == first["consumed_callback_identity"] == ""
    assert first["status_observation_pending"] is False
    response = helper.stop({"session_id": "session-one", "cwd": str(workspace),
                            "turn_id": "first-turn"})
    assert incoming["next_action"] in response["reason"]
    pending = store.get_status("run-one")["run"]["codex_continuation"]
    assert pending["last_callback_identity"]
    assert pending["status_observation_pending"] is False
    incoming["progress_signature"] = "verified-next-step"
    helper.bind("run-one", incoming)
    consumed = store.get_status("run-one")["run"]["codex_continuation"]
    assert consumed["last_callback_identity"] == pending["last_callback_identity"]
    assert consumed["consumed_callback_identity"] == pending["last_callback_identity"]
    assert consumed["callback_count"] == 1
    assert consumed["status_observation_pending"] is False
    assert store.get_status("run-one")["run"]["status"] == "running"


def test_no_progress_count_records_completed_observations(helper, physical_run):
    store, workspace, incoming = physical_run
    helper.bind("run-one", incoming)
    payload = {"session_id": "session-one", "cwd": str(workspace), "turn_id": "turn-1"}
    helper.stop(payload)
    store.update_manifest("run-one", status="running")
    assert helper.stop({**payload, "turn_id": "turn-2"}) is None
    binding = store.get_status("run-one")["run"]["codex_continuation"]
    assert binding["stall_count"] == 2
    assert binding["terminal_reason"] == "stalled"
