"""The Codex refresh must preserve user state and ship only allowed pack files."""

import importlib.util
import json
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "refresh_codex_local.py"
SPEC = importlib.util.spec_from_file_location("refresh_codex_local", SCRIPT)
assert SPEC and SPEC.loader
REFRESH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REFRESH)


def source_fixture(tmp_path: Path) -> Path:
    source = tmp_path / "source"
    (source / "skills" / "optimus").mkdir(parents=True)
    (source / "skills" / "invariant-floor").mkdir()
    (source / "hooks").mkdir()
    (source / "config" / "codex").mkdir(parents=True)
    (source / "provider").mkdir()
    (source / "plugin.json").write_text(json.dumps({
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": "backs-aios", "version": "0.9.0",
    }), encoding="utf-8")
    (source / "install.ps1").write_text("# test only\n", encoding="utf-8")
    (source / "LICENSE").write_text("MIT\n", encoding="utf-8")
    for name in ("optimus", "invariant-floor"):
        (source / "skills" / name / "SKILL.md").write_text(f"---\nname: {name}\ndescription: test\n---\n", encoding="utf-8")
    for name in REFRESH.HOOK_FILES:
        (source / "hooks" / name).write_text("hook\n", encoding="utf-8")
    (source / "config" / "codex" / "AGENTS.md").write_text(
        f"{REFRESH.START}\nUse the skill pack.\n{REFRESH.END}\n", encoding="utf-8")
    (source / "provider" / "secret.txt").write_text("PRIVATE\n", encoding="utf-8")
    return source


def test_refresh_is_allowlisted_idempotent_and_preserves_other_user_entries(tmp_path):
    source = source_fixture(tmp_path)
    home = tmp_path / "home"
    home.mkdir()
    catalog = home / ".agents" / "plugins" / "marketplace.json"
    catalog.parent.mkdir(parents=True)
    catalog.write_text(json.dumps({"name": "personal", "plugins": [
        {"name": "another-plugin", "source": {"source": "local", "path": "./another"}}
    ]}), encoding="utf-8")
    policy = home / ".codex" / "AGENTS.md"
    policy.parent.mkdir(parents=True)
    policy.write_text("User instructions stay.\n", encoding="utf-8")

    first = REFRESH.refresh(source, home, allow_dirty=True, skip_host_install=True)
    second = REFRESH.refresh(source, home, allow_dirty=True, skip_host_install=True)

    assert first["plugin_changed"] is True
    assert second["plugin_changed"] is False
    assert second["catalog_changed"] is False
    assert second["policy_changed"] is False
    bundle = home / ".codex" / "plugins" / "backs-aios"
    assert (bundle / "skills" / "optimus" / "SKILL.md").is_file()
    assert (bundle / "hooks" / "hooks.json").is_file()
    assert not (bundle / "provider").exists()
    assert "PRIVATE" not in "".join(p.read_text(encoding="utf-8") for p in bundle.rglob("*") if p.is_file())
    data = json.loads(catalog.read_text(encoding="utf-8"))
    assert data["name"] == "personal"
    assert [p["name"] for p in data["plugins"]] == ["another-plugin", "backs-aios"]
    assert policy.read_text(encoding="utf-8").startswith("User instructions stay.\n")
    assert policy.read_text(encoding="utf-8").count(REFRESH.START) == 1


def test_refresh_refuses_unmanaged_plugin_and_preserves_it(tmp_path):
    source = source_fixture(tmp_path)
    home = tmp_path / "home"
    home.mkdir()
    bundle = home / ".codex" / "plugins" / "backs-aios"
    bundle.mkdir(parents=True)
    (bundle / "owner.txt").write_text("keep", encoding="utf-8")
    with pytest.raises(RuntimeError, match="not BACKS AIOS managed"):
        REFRESH.refresh(source, home, allow_dirty=True, skip_host_install=True)
    assert (bundle / "owner.txt").read_text(encoding="utf-8") == "keep"


def test_retired_skill_prune_requires_marker_containment_and_exact_snapshot(tmp_path, monkeypatch):
    source = source_fixture(tmp_path)
    home = tmp_path / "home"
    home.mkdir()
    codex = home / ".codex" / "skills" / "hive-clone-boot"
    claude = home / ".claude" / "skills" / "hive-clone-boot"
    for directory in (codex, claude):
        directory.mkdir(parents=True)
        (directory / REFRESH.SKILL_MARKER).write_text("backs-aios-managed 0.8.1\n", encoding="utf-8")
        for n in range(26):
            (directory / f"file-{n:02d}.md").write_text(f"original {n}\n", encoding="utf-8")
    monkeypatch.setattr(REFRESH, "RETIRED_SNAPSHOTS", {"hive-clone-boot": REFRESH.digest(codex, exclude_marker=REFRESH.SKILL_MARKER)})
    (claude / "file-00.md").write_text("user change\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="differs from verified prior managed copy"):
        REFRESH.prune_retired_managed_skills(source, home)
    assert codex.exists() and claude.exists()
    (claude / "file-00.md").write_text("original 0\n", encoding="utf-8")
    (claude / "user-empty-dir").mkdir()
    with pytest.raises(RuntimeError, match="differs from verified prior managed copy"):
        REFRESH.prune_retired_managed_skills(source, home)
    assert codex.exists() and claude.exists()
    (claude / "user-empty-dir").rmdir()
    removed = REFRESH.prune_retired_managed_skills(source, home)
    assert len(removed) == 2
    assert not codex.exists() and not claude.exists()
