"""Supplemental contracts from blind review of the native Stop continuation.

Each test runs the REAL gate scripts as subprocesses against a temporary pack
whose Stop adapter misbehaves on purpose. Nothing is mocked: the gate spawns a
real Python adapter process and the test reads the gate's real exit, stdout and
stderr. A Stop hook may continue a run; it must never hang it or crash it.
"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNTIMES = {"js": "node", "py": sys.executable}
GATE_FILES = ("aios_gate.js", "aios_gate.py")
FLOOR_EVENTS = ("SessionStart", "PreToolUse", "PostToolUse", "UserPromptSubmit")


def pack_with_adapter(tmp_path: Path, adapter_body: str) -> tuple[Path, dict]:
    pack = tmp_path / "pack"
    (pack / "hooks").mkdir(parents=True)
    for name in GATE_FILES:
        shutil.copyfile(ROOT / "hooks" / name, pack / "hooks" / name)
    (pack / "hooks" / "codex_stop_continuation.py").write_text(adapter_body, encoding="utf-8")
    deploy = tmp_path / "deploy"
    (deploy / "backend").mkdir(parents=True)
    home = tmp_path / "home"
    home.mkdir()
    env = {**os.environ, "HOME": str(home), "USERPROFILE": str(home),
           "BACKS_DEPLOY_ROOT": str(deploy), "PYTHON": sys.executable}
    return pack, env


def run_stop(pack: Path, env: dict, suffix: str, timeout: float):
    payload = {"hook_event_name": "Stop", "session_id": "stop-edge", "cwd": str(pack)}
    started = time.monotonic()
    result = subprocess.run([RUNTIMES[suffix], str(pack / "hooks" / f"aios_gate.{suffix}")],
                            input=json.dumps(payload), text=True, capture_output=True,
                            env=env, timeout=timeout)
    return result, time.monotonic() - started


def test_every_floor_delivering_hook_declares_the_measured_context_ceiling():
    hooks = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
    for event in FLOOR_EVENTS:
        for row in hooks[event]:
            for handler in row["hooks"]:
                limit = handler.get("additionalContextLimit")
                assert isinstance(limit, int) and 16325 <= limit <= 32768, (event, handler)


@pytest.mark.parametrize("suffix", sorted(RUNTIMES))
def test_hung_stop_adapter_is_bounded_and_allows_stop(tmp_path, suffix):
    pack, env = pack_with_adapter(tmp_path, "import time\ntime.sleep(300)\n")
    result, elapsed = run_stop(pack, env, suffix, timeout=90)
    assert elapsed < 60, f"{suffix} gate waited {elapsed:.0f}s on a hung adapter"
    assert result.returncode == 0, result.stderr
    assert "block" not in result.stdout
    assert "BACKS continuation unavailable" in result.stderr


@pytest.mark.parametrize("suffix", sorted(RUNTIMES))
def test_malformed_adapter_output_is_reported_and_allows_stop(tmp_path, suffix):
    pack, env = pack_with_adapter(tmp_path, "print('not json {')\n")
    result, _ = run_stop(pack, env, suffix, timeout=30)
    assert result.returncode == 0, result.stderr
    assert "Traceback" not in result.stderr
    assert "malformed adapter output" in result.stderr
    assert "not json" not in result.stdout


def test_codex_bundle_fails_loud_without_playbooks(tmp_path):
    script = ROOT / "tools" / "refresh_codex_local.py"
    spec = importlib.util.spec_from_file_location("refresh_codex_local_edges", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source = tmp_path / "source"
    shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(".git", "plays", "sandbox", "__pycache__"))
    with pytest.raises(RuntimeError, match="plays"):
        module.stage_bundle(source, tmp_path / "plugins", "missing-plays")
    assert not any((tmp_path / "plugins").glob(".backs-aios-stage-*")), "failed stage left behind"
