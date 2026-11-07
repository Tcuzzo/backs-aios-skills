"""Build Flow task packets physically bind the native Stop continuation owner."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "hooks/codex_stop_continuation.py"


def _helper():
    spec = importlib.util.spec_from_file_location("codex_stop_packet", HELPER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _packet(workspace: Path) -> dict:
    return {
        "mission": {"mission_id": "mission-one"},
        "episode": {
            "deadline": "2999-01-01T00:00:00+00:00",
            "resource_budget": {"call_ceiling": 8, "cost_ceiling": None},
            "resources_used": {"calls_used": 3, "cost_used": None},
            "prior_counters": [{"calls_used": 5, "cost_used": 2.5}],
        },
        "worker_state": {"status": "active", "workers": []},
        "continuation_binding": {
            "session_id": "session-one", "workspace": str(workspace),
            "scope": ["hooks/"], "checkpoint_identity": "checkpoint-1",
            "stall_limit": 3, "stall_count": 0, "progress_signature": "p1",
        },
        "next_action": "run the focused continuation contract",
    }


def test_task_packet_maps_to_the_single_stop_binding(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    binding = _helper().binding_from_task_packet(_packet(workspace))
    assert binding == {
        "mission_id": "mission-one", "session_id": "session-one",
        "workspace": str(workspace.resolve()), "scope": ["hooks/"],
        "absolute_deadline": "2999-01-01T00:00:00+00:00",
        "call_ceiling": 8, "calls_used": 8,
        "cost_ceiling": None, "cost_used": None,
        "checkpoint_identity": "checkpoint-1", "stall_limit": 3,
        "stall_count": 0, "progress_signature": "p1",
        "next_action": "run the focused continuation contract",
    }


def test_task_packet_rejects_ambiguous_or_missing_owner_fields(tmp_path):
    packet = _packet(tmp_path)
    del packet["continuation_binding"]["session_id"]
    try:
        _helper().binding_from_task_packet(packet)
    except ValueError as exc:
        assert "session_id" in str(exc)
    else:
        raise AssertionError("missing session owner was accepted")


def test_task_packet_rejects_malformed_identity_scope_and_deadline(tmp_path):
    cases = [
        ("mission", "mission_id", None),
        ("continuation_binding", "session_id", None),
        ("continuation_binding", "checkpoint_identity", None),
        ("continuation_binding", "scope", [None]),
        ("episode", "deadline", "not-a-date"),
    ]
    for section, field, value in cases:
        packet = _packet(tmp_path)
        packet[section][field] = value
        try:
            _helper().binding_from_task_packet(packet)
        except ValueError:
            continue
        raise AssertionError(f"malformed {section}.{field} was accepted")


def test_task_packet_accumulates_every_prior_episode_counter(tmp_path):
    packet = _packet(tmp_path)
    packet["episode"]["resource_budget"]["call_ceiling"] = 20
    packet["episode"]["prior_counters"] = [
        {"calls_used": 2, "cost_used": 1.0},
        {"calls_used": 4, "cost_used": None},
    ]
    binding = _helper().binding_from_task_packet(packet)
    assert binding["calls_used"] == 9
    assert binding["cost_used"] is None


def test_build_flow_documents_the_real_packet_bind_command():
    skill = (ROOT / "skills/backs-build-flow/SKILL.md").read_text()
    packet = (ROOT / "skills/backs-build-flow/references/task-packet.md").read_text()
    assert "bind-task-packet RUN_ID" in skill
    assert "continuation_binding:" in packet
    assert "codex_stop_continuation.py bind-task-packet" in skill
