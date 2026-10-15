"""Installed provider must work in ordinary projects without native backend files."""
import json
import subprocess
import sys
from pathlib import Path

from test_provider_control import fixture_env

ROOT = Path(__file__).resolve().parents[1]


def test_install_backend_absent_preserves_explicit_provider(tmp_path):
    project = tmp_path / "ordinary-project"
    project.mkdir()
    settings = tmp_path / ".claude/settings.json"
    settings.parent.mkdir()
    original = {"model": "owner-explicit-model", "env": {"ANTHROPIC_BASE_URL": "https://provider.example.invalid"}}
    settings.write_text(json.dumps(original))
    env = fixture_env(tmp_path) | {"BACKS_PROVIDER_PYTHON": sys.executable}
    result = subprocess.run(["bash", str(ROOT / "install-provider.sh"), str(project)],
                            cwd=project, env=env, capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, result.stderr
    assert json.loads(settings.read_text()) == original
    assert not (project / "backend").exists()
    launcher = tmp_path / ".local/bin/backs-provider"
    assert launcher.is_file()
    status = subprocess.run([str(launcher), "status"], cwd=project, env=env,
                            capture_output=True, text=True, timeout=20)
    assert status.returncode == 0, status.stderr
    assert json.loads(settings.read_text()) == original
