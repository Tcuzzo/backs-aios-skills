#!/usr/bin/env python3
"""Refresh managed BACKS AIOS host skills and a personal Codex local plugin.

The source must be a clean, released public-pack checkout by default. The Codex
bundle is an allowlist: skill folders, the grounding hook, manifest, and license.
It never copies provider code, private runtime state, or a Codex cache directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid


MANAGED = ".backs-aios-managed"
SKILL_MARKER = "backs-aios-managed"
START = "<!-- BACKS-AIOS-CODEX-MANAGED:START -->"
END = "<!-- BACKS-AIOS-CODEX-MANAGED:END -->"
HOOK_FILES = ("aios_gate.js", "aios_gate.py", "hooks.json")
# Exact 26-file tree observed in the prior managed host install. The retired
# public skill is absent from the new source. Its previous Git HEAD tree has a
# different hash, so do not claim this is a Git HEAD hash.
RETIRED_SNAPSHOTS = {"hive-clone-boot": "1f819aff84015e4b9f57f0bcc7b6277ecaeb3760d239c1b5340f79b1fad6b08d"}


def command(*args: str, cwd: Path) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed ({result.returncode}): {result.stderr.strip()}")
    return result.stdout.strip()


def checked_source(source: Path, *, allow_dirty: bool, update_source: bool) -> str:
    source = source.resolve(strict=False)
    if not source.is_dir():
        raise RuntimeError("Public-pack checkout does not exist")
    if not (source / "install.ps1").is_file():
        raise RuntimeError("Source is not a BACKS AIOS public-pack checkout")
    if not allow_dirty:
        if command("git", "status", "--porcelain", "--untracked-files=all", cwd=source):
            raise RuntimeError("Public-pack checkout is dirty; release it before automatic refresh")
        if update_source:
            command("git", "pull", "--ff-only", cwd=source)
            if command("git", "status", "--porcelain", "--untracked-files=all", cwd=source):
                raise RuntimeError("Public-pack checkout changed locally during pull")
        revision = command("git", "rev-parse", "HEAD", cwd=source)
    else:
        if update_source:
            raise RuntimeError("--allow-dirty cannot be combined with --update-source")
        revision = "unreleased-local"
    manifest = json.loads((source / "plugin.json").read_text(encoding="utf-8"))
    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise RuntimeError("Portable root plugin.json is missing or invalid")
    if manifest.get("name") != "backs-aios":
        raise RuntimeError("Unexpected plugin identity")
    if not (source / "skills" / "optimus" / "SKILL.md").is_file():
        raise RuntimeError("Canonical optimus skill is missing")
    if not (source / "skills" / "invariant-floor" / "SKILL.md").is_file():
        raise RuntimeError("Canonical invariant floor skill is missing")
    for name in HOOK_FILES:
        if not (source / "hooks" / name).is_file():
            raise RuntimeError(f"Grounding hook is missing: {name}")
    if not (source / "config" / "codex" / "AGENTS.md").is_file():
        raise RuntimeError("Codex policy template is missing")
    return revision


def assert_inside(path: Path, root: Path) -> None:
    resolved_root = root.resolve(strict=False)
    resolved_path = path.resolve(strict=False)
    if not resolved_path.is_relative_to(resolved_root) or resolved_path == resolved_root:
        raise RuntimeError("Refusing to move or remove a path outside the managed plugin root")


def copy_safe_tree(source: Path, destination: Path) -> None:
    for path in source.rglob("*"):
        if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
            raise RuntimeError(f"Symlink in packaged skills: {path.relative_to(source)}")
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"),
    )


def digest(root: Path, *, exclude_marker: str = MANAGED) -> str:
    h = hashlib.sha256()
    for file in sorted(p for p in root.rglob("*") if p.is_file() and p.name != exclude_marker):
        h.update(file.relative_to(root).as_posix().encode("utf-8"))
        h.update(b"\0")
        h.update(file.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def stage_bundle(source: Path, plugin_root: Path, revision: str) -> Path:
    plugin_root.mkdir(parents=True, exist_ok=True)
    stage = plugin_root / f".backs-aios-stage-{uuid.uuid4().hex}"
    assert_inside(stage, plugin_root)
    stage.mkdir()
    try:
        for name in ("plugin.json", "LICENSE"):
            if (source / name).is_symlink():
                raise RuntimeError(f"Symlink in packaged root file: {name}")
        shutil.copy2(source / "plugin.json", stage / "plugin.json")
        shutil.copy2(source / "LICENSE", stage / "LICENSE")
        copy_safe_tree(source / "skills", stage / "skills")
        (stage / "hooks").mkdir()
        for name in HOOK_FILES:
            path = source / "hooks" / name
            if path.is_symlink():
                raise RuntimeError(f"Symlink in packaged hooks: {name}")
            shutil.copy2(path, stage / "hooks" / name)
        (stage / MANAGED).write_text(f"BACKS AIOS local plugin\nsource={revision}\n", encoding="utf-8")
        return stage
    except BaseException:
        assert_inside(stage, plugin_root)
        shutil.rmtree(stage)
        raise


def install_bundle(stage: Path, plugin_root: Path) -> tuple[str, bool]:
    destination = plugin_root / "backs-aios"
    assert_inside(destination, plugin_root)
    new_digest = digest(stage)
    if destination.exists():
        if destination.is_symlink() or not (destination / MANAGED).is_file():
            raise RuntimeError("Existing Codex plugin is not BACKS AIOS managed")
        if digest(destination) == new_digest:
            assert_inside(stage, plugin_root)
            shutil.rmtree(stage)
            return new_digest, False
    backup = plugin_root / f".backs-aios-backup-{uuid.uuid4().hex}"
    assert_inside(backup, plugin_root)
    had_previous = destination.exists()
    try:
        if had_previous:
            destination.rename(backup)
        stage.rename(destination)
    except BaseException:
        if had_previous and backup.exists() and not destination.exists():
            backup.rename(destination)
        if stage.exists():
            assert_inside(stage, plugin_root)
            shutil.rmtree(stage)
        raise
    if backup.exists():
        assert_inside(backup, plugin_root)
        shutil.rmtree(backup)
    return new_digest, True


def preflight_home(home: Path) -> None:
    plugin_root = home / ".codex" / "plugins"
    destination = plugin_root / "backs-aios"
    assert_inside(destination, plugin_root)
    if destination.exists():
        if destination.is_symlink() or not (destination / MANAGED).is_file():
            raise RuntimeError("Existing Codex plugin is not BACKS AIOS managed")
        for path in destination.rglob("*"):
            if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
                raise RuntimeError("Existing managed plugin contains a link")
    catalog_path = home / ".agents" / "plugins" / "marketplace.json"
    if catalog_path.is_symlink():
        raise RuntimeError("Personal marketplace is a symlink; preserving it")
    if catalog_path.exists():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        if not isinstance(catalog, dict) or not isinstance(catalog.get("plugins"), list):
            raise RuntimeError("Existing personal marketplace is not a plugin catalog")
        own = [p for p in catalog["plugins"] if isinstance(p, dict) and p.get("name") == "backs-aios"]
        expected = {
            "name": "backs-aios",
            "source": {"source": "local", "path": "./.codex/plugins/backs-aios"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Developer Tools",
        }
        if len(own) > 1 or (own and own[0] != expected):
            raise RuntimeError("Existing BACKS AIOS marketplace entry differs; preserving it")
    policy_path = home / ".codex" / "AGENTS.md"
    if policy_path.is_symlink():
        raise RuntimeError("Global Codex instructions are a symlink; preserving them")
    if policy_path.exists():
        policy = policy_path.read_text(encoding="utf-8")
        if policy.count(START) != policy.count(END) or policy.count(START) > 1:
            raise RuntimeError("Existing Codex policy has mismatched managed markers")


def write_atomic(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    temporary = path.with_name(f".{path.name}.backs-aios-{uuid.uuid4().hex}.tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    os.replace(temporary, path)
    return True


def update_catalog(home: Path) -> bool:
    path = home / ".agents" / "plugins" / "marketplace.json"
    if path.exists():
        catalog = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(catalog, dict) or not isinstance(catalog.get("plugins"), list):
            raise RuntimeError("Existing personal marketplace is not a plugin catalog")
    else:
        catalog = {"name": "backs-aios-local", "interface": {"displayName": "BACKS AIOS Local"}, "plugins": []}
    entry = {
        "name": "backs-aios",
        "source": {"source": "local", "path": "./.codex/plugins/backs-aios"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Developer Tools",
    }
    prior = [p for p in catalog["plugins"] if isinstance(p, dict) and p.get("name") == "backs-aios"]
    if len(prior) > 1:
        raise RuntimeError("Duplicate BACKS AIOS entries in personal marketplace")
    if prior and prior[0] != entry:
        raise RuntimeError("Existing BACKS AIOS marketplace entry is user-owned or differs; preserving it")
    if not prior:
        catalog["plugins"].append(entry)
    return write_atomic(path, json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")


def update_policy(source: Path, home: Path) -> bool:
    template = (source / "config" / "codex" / "AGENTS.md").read_text(encoding="utf-8").strip()
    if template.count(START) != 1 or template.count(END) != 1:
        raise RuntimeError("Codex policy template has invalid managed markers")
    target = home / ".codex" / "AGENTS.md"
    current = target.read_text(encoding="utf-8") if target.exists() else ""
    if START in current or END in current:
        if current.count(START) != 1 or current.count(END) != 1:
            raise RuntimeError("Existing Codex policy has mismatched managed markers")
        begin = current.index(START)
        finish = current.index(END, begin) + len(END)
        updated = current[:begin] + template + current[finish:]
    else:
        updated = current.rstrip() + ("\n\n" if current.strip() else "") + template + "\n"
    return write_atomic(target, updated)


def install_hosts(source: Path) -> None:
    shell = shutil.which("pwsh") or shutil.which("powershell.exe") or shutil.which("powershell")
    if not shell:
        raise RuntimeError("PowerShell is required for the all-surface installer")
    command(shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(source / "install.ps1"), "-Target", "all", cwd=source)


def prune_retired_managed_skills(source: Path, home: Path) -> list[str]:
    roots = (
        home / ".codex" / "skills",
        home / ".claude" / "skills",
        home / ".config" / "opencode" / "skills",
        home / ".agents" / "skills",
    )
    approved: list[Path] = []
    for name, expected_hash in RETIRED_SNAPSHOTS.items():
        if (source / "skills" / name).exists():
            continue
        for root in roots:
            candidate = root / name
            if not candidate.exists():
                continue
            assert_inside(candidate, root)
            marker = candidate / SKILL_MARKER
            if candidate.is_symlink() or not marker.is_file():
                raise RuntimeError(f"Retired skill is not managed; preserving {candidate}")
            if not marker.read_text(encoding="utf-8").strip().startswith("backs-aios-managed "):
                raise RuntimeError(f"Retired skill marker differs; preserving {candidate}")
            files = [p for p in candidate.rglob("*") if p.is_file() and p.name != SKILL_MARKER]
            directories = {p for p in candidate.rglob("*") if p.is_dir()}
            used_directories = {parent for file in files for parent in file.parents if parent != candidate and parent.is_relative_to(candidate)}
            if any(p.is_symlink() or (hasattr(p, "is_junction") and p.is_junction()) for p in candidate.rglob("*")):
                raise RuntimeError(f"Retired skill contains links; preserving {candidate}")
            if directories != used_directories or len(files) != 26 or digest(candidate, exclude_marker=SKILL_MARKER) != expected_hash:
                raise RuntimeError(f"Retired skill differs from verified prior managed copy; preserving {candidate}")
            approved.append(candidate)
    # Validate every target first. No host tree is removed if one fails.
    for candidate in approved:
        assert_inside(candidate, candidate.parent)
        shutil.rmtree(candidate)
    return [str(path) for path in approved]


def refresh(source: Path, home: Path, *, update_source: bool = False,
            allow_dirty: bool = False, skip_host_install: bool = False) -> dict[str, object]:
    source = source.resolve(strict=False)
    home = home.resolve(strict=False)
    if not home.is_dir():
        raise RuntimeError("Target home directory does not exist")
    revision = checked_source(source, allow_dirty=allow_dirty, update_source=update_source)
    preflight_home(home)
    if not skip_host_install:
        install_hosts(source)
    retired_pruned = prune_retired_managed_skills(source, home)
    plugin_root = home / ".codex" / "plugins"
    stage = stage_bundle(source, plugin_root, revision)
    try:
        bundle_hash, plugin_changed = install_bundle(stage, plugin_root)
    finally:
        if stage.exists():
            assert_inside(stage, plugin_root)
            shutil.rmtree(stage)
    catalog_changed = update_catalog(home)
    policy_changed = update_policy(source, home)
    return {
        "source_revision": revision,
        "bundle_sha256": bundle_hash,
        "plugin_changed": plugin_changed,
        "catalog_changed": catalog_changed,
        "policy_changed": policy_changed,
        "retired_skill_paths_pruned": retired_pruned,
        "new_codex_session_required": plugin_changed or catalog_changed or policy_changed or bool(retired_pruned),
        "desktop_restart_required_for_local_plugin": plugin_changed or catalog_changed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--update-source", action="store_true", help="Pull a clean public checkout with --ff-only")
    parser.add_argument("--allow-dirty", action="store_true", help="Developer testing only; never use for scheduled refresh")
    parser.add_argument("--skip-host-install", action="store_true", help="Developer testing only; skip all-surface installer")
    args = parser.parse_args()
    try:
        print(json.dumps(refresh(args.source, args.home, update_source=args.update_source,
                                 allow_dirty=args.allow_dirty, skip_host_install=args.skip_host_install), sort_keys=True))
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"BACKS AIOS refresh failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
