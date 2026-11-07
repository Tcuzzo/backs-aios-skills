"""Physical edge checks added after the dependency contract found coverage gaps."""
import shutil
import pytest
from test_refresh_codex_local import REFRESH, source_fixture


def test_new_nested_destination_and_existing_destination_both_stage(tmp_path):
    source = source_fixture(tmp_path)
    destination = tmp_path / "new-parent" / "nested" / "plugins"
    first = REFRESH.stage_bundle(source, destination, "edge-contract")
    second = REFRESH.stage_bundle(source, destination, "edge-contract")
    assert first != second
    assert first.is_dir() and second.is_dir()
    assert REFRESH.digest(first) == REFRESH.digest(second)


@pytest.mark.parametrize("name", ["plays", "CLAUDE.md"])
def test_method_symlink_is_reported_without_copying_target(tmp_path, name):
    source = source_fixture(tmp_path)
    outside = tmp_path / "not-part-of-pack"
    outside.write_text("unrelated user content", encoding="utf-8")
    existing = source / name
    if existing.is_dir() and not existing.is_symlink():
        shutil.rmtree(existing)
    elif existing.exists() or existing.is_symlink():
        existing.unlink()
    existing.symlink_to(outside)
    destination = tmp_path / "plugins"
    with pytest.raises(RuntimeError, match="Symlink in packaged method"):
        REFRESH.stage_bundle(source, destination, "edge-contract")
    assert outside.read_text(encoding="utf-8") == "unrelated user content"
    assert not list(destination.iterdir())
