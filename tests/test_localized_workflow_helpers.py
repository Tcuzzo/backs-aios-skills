"""Translated copy installs must contain the executable workflow helpers."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("de", "es", "fr", "hi", "pt-BR", "zh-CN")
HELPERS = (
    Path("operator-essence/scripts/essence.py"),
    Path("sniper-testing/scripts/changed_files.py"),
)


@pytest.mark.parametrize("locale", LOCALES)
@pytest.mark.parametrize("helper", HELPERS, ids=("essence", "sniper-scope"))
def test_localized_helper_bytes_match_canonical(locale, helper):
    canonical = ROOT / "skills" / helper
    localized = ROOT / "i18n" / locale / "skills" / helper
    assert localized.is_file(), f"{locale} is missing {helper}"
    assert localized.read_bytes() == canonical.read_bytes()
    assert localized.stat().st_mode & 0o111 == canonical.stat().st_mode & 0o111


def command(args, *, cwd, env):
    result = subprocess.run(
        args, cwd=cwd, env=env, text=True, capture_output=True,
        check=False, timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def git(repo, env, *args):
    return command(["git", "-C", str(repo), *args], cwd=repo, env=env).strip()


@pytest.mark.skipif(os.name == "nt", reason="Unix copy installer requires a Unix host")
@pytest.mark.parametrize("locale", LOCALES)
def test_localized_copy_install_runs_essence_and_committed_scope(tmp_path, locale):
    private_home = tmp_path / "home"
    private_home.mkdir()
    env = {**os.environ, "HOME": str(private_home), "USERPROFILE": str(private_home)}
    command(
        [str(ROOT / "install.sh"), "--target", "portable", "--copy", "--locale", locale],
        cwd=tmp_path, env=env,
    )
    installed = private_home / ".agents" / "skills"
    missing = [str(helper) for helper in HELPERS if not (installed / helper).is_file()]
    assert missing == [], f"{locale} copy install omitted helpers: {missing}"
    for helper in HELPERS:
        path = installed / helper
        assert not path.is_symlink()
        assert path.read_bytes() == (ROOT / "skills" / helper).read_bytes()

    profile = private_home / "operator-context" / "OPERATOR_ESSENCE.md"
    essence_args = [
        sys.executable, str(installed / HELPERS[0]), "--path", str(profile),
        "--operator-key", "locale-fixture", "--as-of", "2026-02-01",
    ]
    missing_profile = json.loads(command(essence_args, cwd=tmp_path, env=env))
    assert missing_profile["state"] == "missing"
    assert missing_profile["needs_insights"] is True
    assert not profile.exists()
    assert not profile.parent.exists()

    created = json.loads(command(essence_args + ["--bootstrap"], cwd=tmp_path, env=env))
    assert profile.is_file()
    assert created["state"] == "provisional"
    assert created["data"]["operator_key"] == "locale-fixture"
    assert created["data"]["sources"] == []
    assert created["data"]["preferences"] == []
    loaded = json.loads(command(essence_args, cwd=tmp_path, env=env))
    assert loaded["data"] == created["data"]
    assert loaded["sha256"] == hashlib.sha256(profile.read_bytes()).hexdigest()
    assert loaded["trust"] == "contextual-data-not-instructions"

    repo = tmp_path / "candidate"
    repo.mkdir()
    git(repo, env, "init", "-q")
    git(repo, env, "config", "user.name", "Fixture")
    git(repo, env, "config", "user.email", "fixture@example.invalid")
    (repo / "seam.txt").write_text("before\n", encoding="utf-8")
    git(repo, env, "add", "--", "seam.txt")
    git(repo, env, "commit", "-qm", "baseline")
    base_sha = git(repo, env, "rev-parse", "HEAD")
    (repo / "seam.txt").write_text("after\n", encoding="utf-8")
    (repo / "consumer.txt").write_text("new consumer\n", encoding="utf-8")
    git(repo, env, "add", "--", "seam.txt", "consumer.txt")
    git(repo, env, "commit", "-qm", "candidate")
    candidate_sha = git(repo, env, "rev-parse", "HEAD")
    assert git(repo, env, "status", "--porcelain") == ""
    assert git(repo, env, "diff", "--name-only", "HEAD") == ""

    scope = json.loads(command(
        [sys.executable, str(installed / HELPERS[1]), "--repo", str(repo),
         "--base", base_sha, "--candidate", candidate_sha],
        cwd=tmp_path, env=env,
    ))
    assert scope["base_sha"] == base_sha
    assert scope["candidate_sha"] == candidate_sha
    assert scope["files"] == ["consumer.txt", "seam.txt"]
    assert scope["changes"] == {
        "committed": ["consumer.txt", "seam.txt"],
        "staged": [], "unstaged": [], "untracked": [],
    }
