"""Second-turn regression: a session is not a callback identity."""
import json
import pytest
import test_codex_stop_continuation as fixture_module


@pytest.fixture
def continuation():
    case = fixture_module.CodexStopContinuationTest(methodName="test_active_continuation_is_idempotent_and_preserves_counters")
    case.setUp()
    try:
        yield case
    finally:
        case.tearDown()


def test_progressing_second_native_turn_continues_same_session(continuation):
    first = continuation.stop(turn_id="turn-one")
    assert json.loads(first.stdout)["decision"] == "block"
    binding = continuation.manifest()["codex_continuation"]
    binding["progress_signature"] = "verified-next-checkpoint"
    continuation.update(status="running", codex_continuation=binding)
    second = continuation.stop(turn_id="turn-two", stop_hook_active=True)
    assert second.stdout, "A progressing native continuation must not silently end after one turn"
    assert json.loads(second.stdout)["decision"] == "block"
    after = continuation.manifest()["codex_continuation"]
    assert after["callback_count"] == 2
    assert after["absolute_deadline"] == binding["absolute_deadline"]
    replay = continuation.stop(turn_id="turn-two", stop_hook_active=True)
    assert replay.stdout == ""
    assert continuation.manifest()["codex_continuation"]["callback_count"] == 2
