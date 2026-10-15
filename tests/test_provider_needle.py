"""Actual installed controller selects Automatic through the real portable catalog."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from test_provider_control import fixture_env

ROOT = Path(__file__).resolve().parents[1]


def test_installed_needle_selects_automatic_not_concrete_model(tmp_path):
    isolated = Path(sys.executable)
    project = tmp_path / "project"
    project.mkdir()
    settings = tmp_path / ".claude/settings.json"
    settings.parent.mkdir()
    before = {"model": "owner-explicit-model", "env": {"ANTHROPIC_BASE_URL": "https://provider.example.invalid"}}
    settings.write_text(json.dumps(before))
    env = fixture_env(tmp_path) | {"BACKS_PROVIDER_PYTHON": sys.executable}
    # Carry only the test interpreter's installed dependencies into the empty HOME.
    env["PYTHONPATH"] = os.pathsep.join(path for path in sys.path
                                       if path.startswith(sys.base_prefix) or "site-packages" in path or "dist-packages" in path)
    install = subprocess.run(["bash", str(ROOT / "install-provider.sh"), str(project)],
                             env=env, capture_output=True, text=True, timeout=20)
    assert install.returncode == 0, install.stderr
    assert json.loads(settings.read_text()) == before
    config = tmp_path / "gateway.json"
    config.write_text(json.dumps({"upstream": {"endpoint": "https://provider.example.invalid", "model": "owner-explicit-model"}}))
    ready = tmp_path / "ready.json"
    runtime = tmp_path / ".local/share/backs-aios/provider-control/current"
    with (tmp_path / "server.log").open("w") as log:
        process = subprocess.Popen([str(isolated), str(runtime / "provider/portable_gateway.py"),
                                    "--config", str(config), "--port", "0", "--ready-file", str(ready)],
                                   env=env, stdout=log, stderr=log)
        try:
            deadline = time.monotonic() + 10
            while not ready.exists() and process.poll() is None and time.monotonic() < deadline:
                time.sleep(.05)
            assert ready.exists(), (tmp_path / "server.log").read_text()
            port = json.loads(ready.read_text())["port"]
            env["BACKS_ANTHROPIC_GATEWAY_URL"] = f"http://127.0.0.1:{port}"
            launcher = tmp_path / ".local/bin/backs-provider"
            result = subprocess.run([str(launcher), "kev"], cwd=project, env=env,
                                    capture_output=True, text=True, timeout=15)
            assert result.returncode == 0, result.stderr
            after = json.loads(settings.read_text())
            assert after["model"] == "backs/claude-auto"
            assert after["env"]["ANTHROPIC_MODEL"] == "backs/claude-auto"
            state = json.loads((tmp_path / ".config/backs-aios/provider-state.json").read_text())
            assert state["needle_rung"]["model"] == "owner-explicit-model"
            assert state["needle_rung"]["source"] == "portable_configured_host"
            restore = subprocess.run([str(launcher), "claude"], cwd=project, env=env,
                                     capture_output=True, text=True, timeout=15)
            assert restore.returncode == 0, restore.stderr
            assert json.loads(settings.read_text()) == before
        finally:
            process.terminate()
            process.wait(timeout=10)
