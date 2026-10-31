"""Deduplicated packages must still load legacy names and advertise usable actions."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from refresh_codex_local import stage_bundle  # noqa: E402


@pytest.fixture
def packaged_gate(tmp_path):
    pack = stage_bundle(ROOT, tmp_path / "plugins", "alias-regression")
    home = tmp_path / "home"
    home.mkdir()
    env = dict(os.environ, HOME=str(home), USERPROFILE=str(home),
               BACKS_DEPLOY_ROOT=str(tmp_path / "missing-native"), AIOS_GATE="on")
    return pack, home, env


def run_gate(packaged_gate, suffix, *args, payload=None):
    pack, _, env = packaged_gate
    return subprocess.run(
        ["node" if suffix == "js" else sys.executable,
         str(pack / "hooks" / f"aios_gate.{suffix}"), *args],
        input=json.dumps(payload or {}), text=True, capture_output=True,
        env=env, timeout=10,
    )


@pytest.mark.parametrize("suffix", ("js", "py"))
@pytest.mark.parametrize("prefix", ("", "backs-aios:"))
@pytest.mark.parametrize("alias, canonical", (
    ("context_engineer", "context-engineer"),
    ("context-compiler", "context-engineer"),
    ("operator_intent_deduction", "operator-intent-deduction"),
))
def test_packaged_legacy_alias_loads_canonical_body(packaged_gate, suffix, prefix, alias, canonical):
    pack, home, _ = packaged_gate
    assert not (pack / "skills" / alias).exists()
    expected = (pack / "skills" / canonical / "SKILL.md").read_text(encoding="utf-8")

    result = run_gate(packaged_gate, suffix, "--load", prefix + alias, "legacy-alias")

    assert result.returncode == 0, result.stderr
    assert result.stdout == expected
    receipt = home / ".claude/state/backs_ground_legacy-alias.hashes.json"
    assert json.loads(receipt.read_text(encoding="utf-8")) == {
        canonical: hashlib.sha256(expected.encode("utf-8")).hexdigest(),
    }
    assert not (pack / "skills" / alias).exists()


@pytest.mark.parametrize("suffix", ("js", "py"))
def test_packaged_wake_actions_name_discoverable_and_loadable_canonical_skills(packaged_gate, suffix):
    pack, _, _ = packaged_gate
    started = run_gate(packaged_gate, suffix, payload={
        "hook_event_name": "SessionStart", "session_id": "packaged-wake",
    })
    assert started.returncode == 0, started.stderr
    context = json.loads(started.stdout)["hookSpecificOutput"]["additionalContext"]
    wake = context.split("\n\n", 1)[0]
    actions = re.findall(r"\binvoke ([a-z0-9_-]+)", wake)
    assert actions == ["operator-intent-deduction", "context-engineer"]
    for action in actions:
        expected = pack / "skills" / action / "SKILL.md"
        assert expected.is_file()
        loaded = run_gate(packaged_gate, suffix, "--load", action, "canonical-wake")
        assert loaded.returncode == 0, loaded.stderr
        assert loaded.stdout == expected.read_text(encoding="utf-8")
