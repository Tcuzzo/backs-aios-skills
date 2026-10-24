"""Contract for the Codex desktop local-marketplace entry point."""

import json
from pathlib import Path


PACK = Path(__file__).resolve().parents[1]


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
