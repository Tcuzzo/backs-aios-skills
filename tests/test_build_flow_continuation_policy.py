from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "backs-build-flow" / "SKILL.md"
PACKET = ROOT / "skills" / "backs-build-flow" / "references" / "task-packet.md"


def test_build_flow_continues_past_self_imposed_limits_truthfully() -> None:
    body = SKILL.read_text(encoding="utf-8")

    assert "ends the bounded episode, not the authorized" in body
    assert "continue with the" in body and "next useful action" in body
    assert "Bind [bounded-loops]" in body
    assert "preserve the counters" in body
    assert "actual provider limits" in body
    assert "actual worker state" in body
    assert "On exhausted limits, checkpoint unresolved work" not in body
    assert "remaining allowance" not in body


def test_build_flow_task_packet_preserves_external_constraints_and_worker_state() -> None:
    body = PACKET.read_text(encoding="utf-8")

    assert "operator-specified limits and applicable provider constraints" in body
    assert "actual unresolved external boundary" in body
    assert "worker_state:" in body
    assert "active | idle | failed | completed" in body
    assert "episode:" in body
    assert "deadline:" in body
    assert "attempts_used:" in body
    assert "resource_budget:" in body
    assert "prior_counters:" in body
    assert "next_action: concrete action and owner" in body
