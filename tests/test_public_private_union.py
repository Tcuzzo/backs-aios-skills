"""The public pack carries the private Codex continuation work as one whole seam.

Every check stages or reads the REAL pack in this checkout. Nothing is mocked:
the Codex bundle is built by the shipping refresh tool into a temp directory,
and the assertions read the files it actually wrote.
"""

import importlib.util
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "refresh_codex_local.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("refresh_codex_local_union", SCRIPT)
assert SPEC and SPEC.loader
REFRESH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REFRESH)


def staged_bundle(tmp_path: Path) -> Path:
    return REFRESH.stage_bundle(ROOT, tmp_path / "plugins", "contract")


def test_hooks_register_native_stop_continuation():
    hooks = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
    assert "Stop" in hooks
    assert (ROOT / "hooks" / "codex_stop_continuation.py").is_file()


def test_codex_bundle_ships_every_hook_file_the_gate_calls(tmp_path):
    stage = staged_bundle(tmp_path)
    gate = (ROOT / "hooks" / "aios_gate.js").read_text(encoding="utf-8")
    called = set(re.findall(r'"hooks",\s*"([A-Za-z0-9_.-]+)"', gate))
    assert "codex_stop_continuation.py" in called
    for name in called:
        assert (stage / "hooks" / name).is_file(), f"Codex bundle is missing hooks/{name}"


def test_codex_bundle_keeps_manifest_methods_and_one_name_per_skill(tmp_path):
    stage = staged_bundle(tmp_path)
    manifest = json.loads((stage / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "backs-aios"
    assert (stage / "plays").is_dir() and any((stage / "plays").glob("*.md"))
    assert (stage / "CLAUDE.md").is_file()
    for alias in REFRESH.ALIASES:
        assert (ROOT / "skills" / alias).is_dir(), f"source alias {alias} must stay loose-compatible"
        assert not (stage / "skills" / alias).exists(), f"bundle duplicates alias {alias}"


def test_build_flow_carries_public_links_and_private_continuation():
    body = (ROOT / "skills" / "backs-build-flow" / "SKILL.md").read_text(encoding="utf-8")
    for skill in ("operator-essence", "rea-investigation", "bounded-loops", "red-first"):
        assert f"](../{skill}/SKILL.md)" in body, skill
        assert (ROOT / "skills" / skill / "SKILL.md").is_file(), skill
    assert "codex_stop_continuation.py bind-task-packet" in body
    assert "**STILL-BUILDING**" in body
    packet = (ROOT / "skills" / "backs-build-flow" / "references" / "task-packet.md").read_text(encoding="utf-8")
    assert "continuation_binding:" in packet and "prior_counters:" in packet


def test_public_cam_iot_keeps_placeholders():
    for path in [ROOT / "skills" / "cam-iot-inventory" / "SKILL.md",
                 *sorted((ROOT / "i18n").glob("*/skills/cam-iot-inventory/SKILL.md"))]:
        text = path.read_text(encoding="utf-8")
        assert "<BACKS_DEPLOY_ROOT>" in text, path
        assert "<placeholder-mount>" not in text, path
        assert not re.search(r"`[0-9a-f]{8,40}`", text), path
