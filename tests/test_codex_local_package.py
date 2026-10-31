"""Contract for the Codex desktop local-marketplace entry point."""

import json
from pathlib import Path
import sys

import yaml


PACK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACK / "tools"))

import refresh_codex_local as REFRESH  # noqa: E402


def test_portable_manifest_exposes_the_existing_skill_pack():
    manifest = json.loads((PACK / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert manifest["name"] == "backs-aios"
    assert manifest["extensions"]["com.openai"]["hooks"] == "./hooks/hooks.json"
    assert (PACK / "hooks" / "hooks.json").is_file()
    assert manifest["extensions"]["com.openai"]["interface"]["category"] == "Developer Tools"
    assert (PACK / "skills" / "optimus" / "SKILL.md").is_file()
    assert (PACK / "skills" / "repair-loop" / "SKILL.md").is_file()


def test_repo_catalog_never_points_at_the_entire_source_tree():
    assert not (PACK / ".agents" / "plugins" / "marketplace.json").exists()


def test_staged_codex_package_exposes_each_skill_name_once(tmp_path):
    stage = REFRESH.stage_bundle(PACK, tmp_path / "plugins", "test-release")
    source_skills = list((PACK / "skills").glob("*/SKILL.md"))
    source_names = {
        yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])["name"]
        for path in source_skills
    }
    packaged_names = [
        yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])["name"]
        for path in (stage / "skills").glob("*/SKILL.md")
    ]

    assert set(packaged_names) == source_names
    assert len(packaged_names) == len(set(packaged_names))
    assert {p.name for p in (stage / "plays").glob("*.md")} == {
        p.name for p in (PACK / "plays").glob("*.md")
    }
