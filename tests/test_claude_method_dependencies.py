"""The actual Claude plugin archive carries every referenced public method."""
import zipfile

from test_claude_plugin_build import bp
from test_packaged_skill_dependencies import local_dependencies


def test_claude_archive_resolves_transitive_skill_methods(tmp_path):
    stage = tmp_path / "stage"
    stage.mkdir()
    bp.build(stage)
    archive = tmp_path / "backs.plugin"
    bp.write_archive(stage, archive)
    installed = tmp_path / "installed"
    with zipfile.ZipFile(archive) as package:
        package.extractall(installed)
    pending = list((installed / "skills").rglob("SKILL.md"))
    assert pending
    visited = set()
    missing = []
    while pending:
        document = pending.pop()
        if document in visited:
            continue
        visited.add(document)
        for dependency in local_dependencies(document):
            assert dependency.is_relative_to(installed)
            if not dependency.is_file():
                missing.append((str(document.relative_to(installed)),
                                str(dependency.relative_to(installed))))
            elif dependency.suffix == ".md":
                pending.append(dependency)
    assert not missing, f"Claude archive drops referenced methods: {missing}"
    assert (installed / "CLAUDE.md") in visited
    assert (installed / "CLAUDE.md").read_bytes() == (bp.ROOT / "CLAUDE.md").read_bytes()
