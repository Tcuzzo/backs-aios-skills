#!/usr/bin/env python3
"""Build a claude.ai-installable plugin pack from this repo.

The repo is BACKS source truth. Two of its contracts are deliberate:

  * alias directories stay BYTE-IDENTICAL to their canonical skill
    (tests/test_session_start_contract.py::test_alias_copies_stay_byte_identical)
  * every skill `name` is hyphen-cased and equals the directory or the skill_id
    (tests/test_pack_contract.py::test_all_skills_are_portable_agent_skills)

Together those force several directories to share one `name`. BACKS needs that:
hive agent profiles and the gate's wake-load message call the underscore spellings.

claude.ai's plugin validator rejects duplicate skill names and a top-level bin/.
Both are packaging concerns, not source concerns. This script resolves them at
BUILD time so neither tree has to bend: aliases are dropped (a Claude session
calls the canonical name), bin/ scripts move under the skill that wraps them,
and only one plugin.json ships.

Usage:  python3 tools/build_claude_plugin.py [OUT.plugin]
"""
from __future__ import annotations

import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Alias dir -> canonical skill. Keep in step with the byte-identical groups in
# tests/test_session_start_contract.py::test_alias_copies_stay_byte_identical.
ALIASES = {
    "context_engineer": "context-engineer",
    "context-compiler": "context-engineer",
    "operator_intent_deduction": "operator-intent-deduction",
}
# Only scripts that a published skill needs are allowed into the archive.
BIN_OWNERS = {
    "backs-pack-sync": "backs-pack-sync",
    "scrub-plugin-pack-literals": "scrub-plugin-pack-literals",
    "reload-vsc-and-verify": "reload-vsc-and-verify",
}
PUBLIC_TOP_LEVEL = frozenset({
    ".claude-plugin", "skills", "hooks", "plays", "command-adapters", "LICENSE",
})
# This seat boot encodes private BACKS topology and operator-specific handoffs.
PRIVATE_SKILLS = frozenset({"hive-clone-boot"})


def prune_to_public_payload(stage: pathlib.Path) -> None:
    """Allowlist the archive so repository scaffolding and runtime data cannot ship."""
    if stage.is_symlink():
        raise SystemExit("archive stage cannot be a symlink")
    root = stage.absolute()
    for path in stage.iterdir():
        if path.is_symlink():
            raise SystemExit(f"symlink at archive root: {path.name}")
        if path.name in PUBLIC_TOP_LEVEL:
            continue
        if path.absolute().parent != root:
            raise SystemExit(f"archive path escapes stage: {path.name}")
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    manifest_dir = stage / ".claude-plugin"
    for path in manifest_dir.iterdir():
        if path.name == "plugin.json" and path.is_file() and not path.is_symlink():
            continue
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.is_dir() and path.absolute().parent == manifest_dir.absolute():
            shutil.rmtree(path)
        else:
            raise SystemExit(f"unexpected manifest entry: {path.name}")
    skill_root = stage / "skills"
    for name in PRIVATE_SKILLS:
        private_dir = skill_root / name
        if private_dir.is_symlink():
            raise SystemExit(f"private skill is a symlink: {name}")
        if private_dir.is_dir():
            if private_dir.absolute().parent != skill_root.absolute():
                raise SystemExit(f"private skill path escapes archive: {name}")
            shutil.rmtree(private_dir)


def frontmatter(path: pathlib.Path) -> str:
    m = re.match(r"---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    if not m:
        raise SystemExit(f"{path}: no frontmatter")
    return m.group(1)


def build(stage: pathlib.Path) -> None:
    archive = subprocess.run(["git", "archive", "HEAD"], cwd=ROOT, check=True,
                             capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(stage)], input=archive, check=True)

    for alias in ALIASES:
        shutil.rmtree(stage / "skills" / alias, ignore_errors=True)

    bin_dir = stage / "bin"
    if bin_dir.is_dir():
        for script in sorted(bin_dir.iterdir()):
            owner = BIN_OWNERS.get(script.name)
            if owner is None:
                continue
            dest = stage / "skills" / owner / "scripts"
            dest.mkdir(parents=True, exist_ok=True)
            shutil.move(str(script), dest / script.name)
            skill = stage / "skills" / owner / "SKILL.md"
            text = skill.read_text(encoding="utf-8")
            text = text.replace(f"bash bin/{script.name}",
                                f"bash ${{CLAUDE_PLUGIN_ROOT}}/skills/{owner}/scripts/{script.name}")
            text = text.replace(f"`bin/{script.name}`",
                                f"`skills/{owner}/scripts/{script.name}`")
            text = text.replace(f"~/backs-aios-skills/bin/{script.name}",
                                f"${{CLAUDE_PLUGIN_ROOT}}/skills/{owner}/scripts/{script.name}")
            skill.write_text(text, encoding="utf-8")
        if bin_dir.absolute().parent != stage.absolute():
            raise SystemExit("bin path escapes archive stage")
        shutil.rmtree(bin_dir)

    prune_to_public_payload(stage)

    # claude.ai rejects angle brackets in a description: they parse as XML tags.
    for skill in sorted((stage / "skills").glob("*/SKILL.md")):
        head = frontmatter(skill)
        desc = re.split(r"\n[a-z_]+:", head.split("description:", 1)[1])[0]
        if "<" in desc or ">" in desc:
            text = skill.read_text(encoding="utf-8")
            skill.write_text(text.replace(desc, re.sub(r"<([a-z_]+)>", lambda m: m.group(1).upper(), desc)),
                             encoding="utf-8")

    verify(stage)


def verify(stage: pathlib.Path) -> None:
    """Fail loud on anything claude.ai's validator rejects."""
    manifests = [p for p in stage.rglob("plugin.json")]
    if len(manifests) != 1:
        raise SystemExit(f"expected exactly one plugin.json, found {len(manifests)}: {manifests}")
    if (stage / "bin").exists():
        raise SystemExit("top-level bin/ survived the build")
    seen: dict[str, str] = {}
    for skill in sorted((stage / "skills").glob("*/SKILL.md")):
        head = frontmatter(skill)
        match = re.search(r"^name:\s*\"?([^\"\n]+)\"?", head, re.M)
        if not match:
            raise SystemExit(f"{skill.parent.name}: SKILL.md has no name in its frontmatter")
        name = match.group(1).strip()
        desc = re.split(r"\n[a-z_]+:", head.split("description:", 1)[1])[0]
        if name in seen:
            raise SystemExit(f"duplicate skill name {name!r}: {seen[name]} and {skill.parent.name}")
        if "<" in desc or ">" in desc:
            raise SystemExit(f"{skill.parent.name}: angle bracket in description")
        seen[name] = skill.parent.name
    print(f"verified: {len(seen)} unique skills, one plugin.json, no top-level bin/")


def write_archive(stage: pathlib.Path, out: pathlib.Path) -> None:
    """Build the plugin ZIP with Python so Windows and Unix produce the same payload."""
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(stage.rglob("*")):
            if path.is_symlink():
                raise SystemExit(f"plugin payload contains a symlink: {path.relative_to(stage)}")
            if path.is_file():
                archive.write(path, path.relative_to(stage).as_posix())


def main() -> int:
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "backs-aios.plugin").resolve()
    with tempfile.TemporaryDirectory() as tmp:
        stage = pathlib.Path(tmp) / "pack"
        stage.mkdir()
        build(stage)
        if out.exists():
            out.unlink()
        write_archive(stage, out)
    print(f"wrote {out} ({out.stat().st_size // 1024} KiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
