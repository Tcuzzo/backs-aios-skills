"""The Codex refresh must preserve user state and ship only allowed pack files."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "refresh_codex_local.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("refresh_codex_local", SCRIPT)
assert SPEC and SPEC.loader
REFRESH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REFRESH)


def source_fixture(tmp_path: Path) -> Path:
    source = tmp_path / "source"
    (source / "skills" / "optimus").mkdir(parents=True)
    (source / "skills" / "invariant-floor").mkdir()
    (source / "hooks").mkdir()
    (source / "plays").mkdir()
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
    (source / "plays" / "elite-build.md").write_text("Use the bounded build play.\n", encoding="utf-8")
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
    assert {p.name for p in bundle.iterdir()} == {
        "plugin.json", "LICENSE", "skills", "plays", "hooks", REFRESH.MANAGED,
    }
    assert not (bundle / "provider").exists()
    assert "PRIVATE" not in "".join(p.read_text(encoding="utf-8") for p in bundle.rglob("*") if p.is_file())
    data = json.loads(catalog.read_text(encoding="utf-8"))
    assert data["name"] == "personal"
    assert [p["name"] for p in data["plugins"]] == ["another-plugin", "backs-aios"]
    assert policy.read_text(encoding="utf-8").startswith("User instructions stay.\n")
    assert policy.read_text(encoding="utf-8").count(REFRESH.START) == 1


@pytest.mark.parametrize("home_variable", ["HOME", "USERPROFILE"])
def test_refresh_host_installer_uses_selected_home_without_changing_parent_environment(
    tmp_path, monkeypatch, home_variable,
):
    """A subprocess probe exercises both host home conventions without real-home writes."""
    source = source_fixture(tmp_path)
    home = tmp_path / "selected home"
    ambient = tmp_path / "ambient home"
    home.mkdir()
    ambient.mkdir()
    monkeypatch.setenv("HOME", str(ambient))
    monkeypatch.setenv("USERPROFILE", str(ambient))
    monkeypatch.setenv("BACKS_REFRESH_PROBE", "retained")
    monkeypatch.setattr(REFRESH.shutil, "which", lambda _: sys.executable)
    real_run = subprocess.run
    probe = (
        "import os; from pathlib import Path; "
        f"target = Path(os.environ[{home_variable!r}]) / 'installer-probe.txt'; "
        "target.write_text(os.environ['BACKS_REFRESH_PROBE'], encoding='utf-8')"
    )

    def run_installer_probe(args, **kwargs):
        # PowerShell is an external dependency. Keep command() and the real
        # subprocess environment; replace only the PowerShell interpreter.
        if "-File" in args:
            return real_run([sys.executable, "-c", probe], **kwargs)
        return real_run(args, **kwargs)

    monkeypatch.setattr(REFRESH.subprocess, "run", run_installer_probe)

    REFRESH.refresh(source, home, allow_dirty=True)

    assert (home / "installer-probe.txt").is_file()
    assert (home / "installer-probe.txt").read_text(encoding="utf-8") == "retained"
    assert not (ambient / "installer-probe.txt").exists()
    assert os.environ["HOME"] == str(ambient)
    assert os.environ["USERPROFILE"] == str(ambient)


@pytest.mark.skipif(
    not (shutil.which("pwsh") or shutil.which("powershell.exe") or shutil.which("powershell")),
    reason="PowerShell is not installed",
)
def test_real_powershell_installer_keeps_all_host_writes_in_selected_home(tmp_path, monkeypatch):
    home = tmp_path / "selected home"
    ambient = tmp_path / "ambient home"
    home.mkdir()
    ambient.mkdir()
    monkeypatch.setenv("HOME", str(ambient))
    monkeypatch.setenv("USERPROFILE", str(ambient))
    shell = shutil.which("pwsh") or shutil.which("powershell.exe") or shutil.which("powershell")
    # Before invoking an installer, prove a regression would still land inside
    # the disposable ambient home rather than the actual host account.
    probe = subprocess.run(
        [shell, "-NoProfile", "-Command", "$HOME"],
        text=True, capture_output=True, check=True,
    )
    assert Path(probe.stdout.strip()).resolve() == ambient.resolve()

    REFRESH.refresh(SCRIPT.parents[1], home, allow_dirty=True)

    for skill_root in (
        ".codex/skills", ".claude/skills", ".agents/skills", ".config/opencode/skills",
    ):
        assert (home / skill_root / "optimus" / "SKILL.md").is_file()
        assert (home / skill_root / "context_engineer" / "SKILL.md").is_file()
    assert (home / ".cursor/plugins/local/backs-aios/skills/optimus/SKILL.md").is_file()
    for target in (
        ".codex", ".claude", ".agents", ".config/opencode",
        ".cursor/plugins/local/backs-aios", ".local/share/backs-aios",
    ):
        assert not (ambient / target).exists()


def test_refresh_bundle_resolves_play_adapter_without_shared_runtime(tmp_path):
    source = source_fixture(tmp_path)
    adapter = source / "skills" / "elite-build" / "SKILL.md"
    adapter.parent.mkdir()
    adapter.write_text(
        "---\nname: elite-build\ndescription: test\n---\n"
        "Read [the play](../../plays/elite-build.md).\n", encoding="utf-8",
    )
    home = tmp_path / "home"
    home.mkdir()

    REFRESH.refresh(source, home, allow_dirty=True, skip_host_install=True)

    bundle = home / ".codex" / "plugins" / "backs-aios"
    packaged_adapter = bundle / "skills" / "elite-build" / "SKILL.md"
    packaged_play = packaged_adapter.parent / "../../plays/elite-build.md"
    assert packaged_adapter.is_file()
    assert packaged_play.is_file()
    assert packaged_play.read_text(encoding="utf-8") == "Use the bounded build play.\n"
    assert not (home / ".local" / "share" / "backs-aios").exists()


def test_refresh_dedupes_packaged_aliases_and_preserves_loose_compatibility_copies(tmp_path):
    source = source_fixture(tmp_path)
    home = tmp_path / "home"
    home.mkdir()
    groups = {
        "context-engineer": ("context_engineer", "context-compiler"),
        "operator-intent-deduction": ("operator_intent_deduction",),
    }
    original = {}
    for canonical, aliases in groups.items():
        body = f"---\nname: {canonical}\ndescription: test\n---\nKeep context.\n"
        for name in (canonical, *aliases):
            source_skill = source / "skills" / name / "SKILL.md"
            source_skill.parent.mkdir()
            source_skill.write_text(body, encoding="utf-8")
            loose_skill = home / ".codex" / "skills" / name / "SKILL.md"
            loose_skill.parent.mkdir(parents=True)
            loose_skill.write_text(body, encoding="utf-8")
            original[source_skill] = body
            original[loose_skill] = body

    REFRESH.refresh(source, home, allow_dirty=True, skip_host_install=True)

    skills = home / ".codex" / "plugins" / "backs-aios" / "skills"
    assert {p.name for p in skills.iterdir()} == {
        "optimus", "invariant-floor", "context-engineer", "operator-intent-deduction",
    }
    for path, expected in original.items():
        assert path.read_text(encoding="utf-8") == expected


@pytest.mark.parametrize("tree", ["skills", "plays"])
@pytest.mark.parametrize("root_link", [False, True])
def test_refresh_refuses_linked_bundle_payload_and_cleans_stage(tmp_path, tree, root_link):
    source = source_fixture(tmp_path)
    home = tmp_path / "home"
    home.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "private.md").write_text("keep outside\n", encoding="utf-8")
    if root_link:
        original_tree = source / tree
        shutil.copytree(original_tree, outside, dirs_exist_ok=True)
        original_tree.rename(source / f"original-{tree}")
        original_tree.symlink_to(outside, target_is_directory=True)
    else:
        (source / tree / "linked-private").symlink_to(outside, target_is_directory=True)

    with pytest.raises(RuntimeError, match="[Ss]ymlink|[Ll]ink"):
        REFRESH.refresh(source, home, allow_dirty=True, skip_host_install=True)

    assert not (home / ".codex" / "plugins" / "backs-aios").exists()
    assert not list(home.rglob(".backs-aios-stage-*"))
    assert (outside / "private.md").read_text(encoding="utf-8") == "keep outside\n"


@pytest.mark.parametrize("invalid", ["not JSON", '{"plugins": {}}'])
def test_refresh_preserves_malformed_catalog_before_installing(tmp_path, invalid):
    source = source_fixture(tmp_path)
    home = tmp_path / "home"
    catalog = home / ".agents" / "plugins" / "marketplace.json"
    catalog.parent.mkdir(parents=True)
    catalog.write_text(invalid, encoding="utf-8")

    with pytest.raises((ValueError, RuntimeError)):
        REFRESH.refresh(source, home, allow_dirty=True, skip_host_install=True)

    assert catalog.read_text(encoding="utf-8") == invalid
    assert not (home / ".codex").exists()


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
        (directory / REFRESH.SKILL_MARKER).write_text("\ufeffbacks-aios-managed 0.8.1\n", encoding="utf-8")
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
