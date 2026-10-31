"""Exercise real Optimus delivery and committed-change scope, not skill-name claims."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "skills/sniper-testing/scripts/changed_files.py"
FLOW = "# Build Flow fixture\nKeep the base revision and remaining mission budget.\n"


@pytest.fixture
def pack(tmp_path):
    root = tmp_path / "pack"
    (root / "hooks").mkdir(parents=True)
    for suffix in ("js", "py"):
        shutil.copy2(ROOT / "hooks" / f"aios_gate.{suffix}", root / "hooks" / f"aios_gate.{suffix}")
    for name, body in {"optimus": "# Optimus fixture\n", "human-calibration": "# Yoke fixture\n", "backs-build-flow": FLOW}.items():
        target = root / "skills" / name / "SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text(body)
    env = dict(os.environ, HOME=str(tmp_path / "home"), USERPROFILE=str(tmp_path / "home"),
               BACKS_DEPLOY_ROOT=str(tmp_path / "missing-native"), AIOS_GATE="on")
    for key in ("CLAUDE_CODE_SESSION_ID", "CURSOR_SESSION_ID", "CURSOR_CONVERSATION_ID",
                "OPENCODE_SESSION_ID", "CODEX_SESSION_ID", "CODEX_THREAD_ID", "CLAUDE_SESSION_ID"):
        env.pop(key, None)
    return root, env


def run_gate(pack, suffix, *args, payload=None):
    root, env = pack
    return subprocess.run(["node" if suffix == "js" else sys.executable,
                           str(root / "hooks" / f"aios_gate.{suffix}"), *args],
                          input=json.dumps(payload or {}), text=True, capture_output=True,
                          env=env, timeout=10)


@pytest.mark.parametrize("suffix", ("js", "py"))
@pytest.mark.parametrize("event", ("SessionStart", "PreToolUse"))
def test_optimus_delivers_flow_once_and_hashes_actual_bytes(pack, suffix, event):
    result = run_gate(pack, suffix, payload={"session_id": "flow-session", "hook_event_name": event,
                                            "tool_name": "Write", "tool_input": {"path": "result.txt"}})
    assert result.returncode == 0, result.stderr
    context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    assert context.count(FLOW) == 1
    marker = Path(pack[1]["HOME"]) / ".aios/state/aios_floor_flow-session.state"
    receipt = json.loads(Path(str(marker) + ".load.json").read_text())
    rows = [row for row in receipt["bodies"] if row["canonical"] == "backs-build-flow"]
    assert len(rows) == 1
    assert rows[0]["sha256"] == hashlib.sha256(FLOW.encode()).hexdigest()
    again = run_gate(pack, suffix, payload={"session_id": "flow-session", "hook_event_name": "PreToolUse",
                                           "tool_name": "Write"})
    assert again.returncode == 0 and again.stdout == ""


@pytest.mark.parametrize("suffix", ("js", "py"))
def test_explicit_optimus_delivers_the_same_flow(pack, suffix):
    result = run_gate(pack, suffix, "--load", "backs-aios:optimus", "flow-explicit")
    assert result.returncode == 0, result.stderr
    assert result.stdout.count(FLOW) == 1
    state = Path(pack[1]["HOME"]) / ".claude/state/backs_ground_flow-explicit.hashes.json"
    assert json.loads(state.read_text())["backs-build-flow"] == hashlib.sha256(FLOW.encode()).hexdigest()


@pytest.mark.parametrize("suffix", ("js", "py"))
def test_missing_flow_has_no_false_receipt_or_tool_denial(pack, suffix):
    (pack[0] / "skills/backs-build-flow/SKILL.md").unlink()
    result = run_gate(pack, suffix, payload={"session_id": "missing-flow", "hook_event_name": "SessionStart"})
    assert result.returncode == 0
    assert "backs-build-flow" in result.stderr and "unavailable" in result.stderr
    assert '"deny"' not in result.stdout
    assert not (Path(pack[1]["HOME"]) / ".aios/state/aios_floor_missing-flow.state").exists()
    explicit = run_gate(pack, suffix, "--load", "optimus", "missing-flow-explicit")
    assert explicit.returncode != 0
    assert not (Path(pack[1]["HOME"]) / ".aios/state/aios_floor_missing-flow-explicit.state").exists()


@pytest.mark.parametrize("suffix", ("js", "py"))
def test_native_optimus_can_use_pack_flow(pack, suffix, tmp_path):
    native = tmp_path / "native"
    target = native / "skills/optimus/SKILL.md"
    target.parent.mkdir(parents=True)
    target.write_text("# Native Optimus fixture\n")
    pack[1]["BACKS_DEPLOY_ROOT"] = str(native)
    result = run_gate(pack, suffix, payload={"session_id": "native-flow", "hook_event_name": "SessionStart"})
    assert result.returncode == 0, result.stderr
    context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "# Native Optimus fixture" in context and context.count(FLOW) == 1


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


@pytest.fixture
def committed_change(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Fixture")
    git(repo, "config", "user.email", "fixture@example.invalid")
    (repo / "seam.py").write_text("value = 1\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "base")
    base = git(repo, "rev-parse", "HEAD")
    (repo / "test_seam.py").write_text("from seam import value\nassert value == 2\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "sealed regression")
    (repo / "seam.py").write_text("value = 2\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "fix")
    return repo, base, git(repo, "rev-parse", "HEAD")


def scope(repo, base, candidate, *args):
    return subprocess.run([sys.executable, str(SCOPE), "--repo", str(repo), "--base", base,
                           "--candidate", candidate, *args], capture_output=True, text=True, timeout=10)


def test_committed_fix_and_regression_remain_in_sniper_scope(committed_change):
    repo, base, candidate = committed_change
    assert git(repo, "diff", "--name-only", "HEAD") == ""
    result = scope(repo, base, candidate)
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["base_sha"] == base and data["candidate_sha"] == candidate
    assert data["files"] == ["seam.py", "test_seam.py"]
    assert data["changes"]["committed"] == data["files"]


def test_pending_paths_are_explicit_and_preserve_odd_filenames(committed_change):
    repo, base, candidate = committed_change
    (repo / "seam.py").write_text("value = 3\n")
    odd = "new file\nwith spaces.py"
    (repo / odd).write_text("new = True\n")
    git(repo, "add", "test_seam.py")
    (repo / "test_seam.py").write_text("from seam import value\nassert value == 3\n")
    git(repo, "add", "test_seam.py")
    result = scope(repo, base, candidate, "--include-worktree")
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["changes"]["staged"] == ["test_seam.py"]
    assert data["changes"]["unstaged"] == ["seam.py"]
    assert data["changes"]["untracked"] == [odd]
    assert set(data["files"]) == {"seam.py", "test_seam.py", odd}
    committed_only = json.loads(scope(repo, base, candidate).stdout)
    assert odd not in committed_only["files"]


def test_worktree_cannot_be_misattributed_to_another_candidate(committed_change):
    repo, base, _ = committed_change
    result = scope(repo, base, base, "--include-worktree")
    assert result.returncode != 0
    assert "candidate must match HEAD" in result.stderr


def test_invalid_revision_is_an_error_not_an_empty_scope(committed_change):
    repo, _, candidate = committed_change
    result = scope(repo, "missing-base", candidate)
    assert result.returncode != 0
    assert "revision" in result.stderr.lower()
