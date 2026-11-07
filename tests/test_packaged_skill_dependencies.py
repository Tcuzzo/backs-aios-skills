"""A staged Codex pack must carry the methods its actual skills reference."""
from pathlib import Path
import re

from test_refresh_codex_local import REFRESH

ROOT = Path(__file__).resolve().parents[1]


def local_dependencies(document):
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
        target = target.split("#", 1)[0]
        if target and not re.match(r"[a-z]+:|/|~", target):
            yield (document.parent / target).resolve()


def test_staged_pack_resolves_every_transitive_skill_method(tmp_path):
    stage = REFRESH.stage_bundle(ROOT, tmp_path / "plugins", "sealed-dependency-contract")
    pending = list((stage / "skills").rglob("SKILL.md"))
    assert pending, "A pack without any skills cannot satisfy dependency closure"
    visited = set()
    missing = []
    while pending:
        document = pending.pop()
        if document in visited:
            continue
        visited.add(document)
        for dependency in local_dependencies(document):
            assert dependency.is_relative_to(stage), "A packaged method must resolve within its artifact"
            if not dependency.is_file():
                missing.append((str(document.relative_to(stage)), str(dependency.relative_to(stage))))
            elif dependency.suffix == ".md":
                pending.append(dependency)
    assert not missing, f"Packaged skills reference missing methods: {missing}"
    # Traversal includes real method bodies, not only the discovered skill catalog.
    assert (stage / "plays" / "agent-builds.md") in visited
    assert (stage / "CLAUDE.md") in visited
