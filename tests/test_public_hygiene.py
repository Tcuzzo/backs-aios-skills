"""Public-repo hygiene guard (BACKS invariants 21 + 26, generic shapes only).

Two rules, enforced loudly so a leak fails CI instead of shipping:

21. No model-authorship trailers on commits (Co-Authored-By: <model>,
    Generated-with-<model> footers), and no model-credit lines in files.
26. No real PII/topology in tracked content or commit metadata: real
    emails, private IPs, real home paths, phone numbers, model-credit
    trailers. This file deliberately carries NO real literals — patterns
    are generic shapes plus allowlisted public/test identities, mirroring
    the shared-primitive design (env/literal-free guards).

Self-exclusion: this test file contains pattern strings, so it is exempt
from the content scan (a guard that greps itself lies).
"""
from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# Guard tests plant offender literals by design (assert-not-present checks);
# a guard that greps another guard's planted offenders lies, so the known
# guard files are named here. A NEW guard test planting offenders must join
# this set explicitly — that is the friction that keeps the audit honest.
_SELF = "tests/test_public_hygiene.py"
_GUARD_TESTS = {_SELF, "tests/test_provider_public_safety.py"}

# Generic shapes only — never a real literal.
_PRIVATE_IP = re.compile(
    r"\b(192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|"
    r"172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+)\b"
)
# First char after the slash must be a word char, so prose shapes like
# "/mnt/..." or "/opt/..." in documentation do not false-fire.
_HOME_PATH = re.compile(r"(/home/[A-Za-z][\w.-]*|/mnt/[\w-][\w.-]*|/opt/[A-Za-z][\w.-]*)")
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_COAUTHOR = re.compile(r"Co-Authored-By:\s*", re.I)
_GENERATED_WITH = re.compile(r"Generated with\s+\[?[A-Za-z]", re.I)

# Public, test-only, or bot identities that are allowed to appear.
_ALLOWED_EMAIL_EXACT = {"noreply@github.com"}

_ALLOWED_EMAIL_SUFFIXES = (
    ".example.invalid",
    "example.com",
    "example.org",
    "users.noreply.github.com",
    "noreply.github.com",
    "noreply@anthropic.com",  # allowed only inside this scan's allowlist; trailers still barred
    "backs.local",
    "ollama.com",  # documented cloud endpoint + test fixtures
)
_TEXT_EXT = {
    ".md", ".py", ".sh", ".json", ".yaml", ".yml", ".txt", ".cff", ".js",
    ".ts", ".toml", ".cfg", ".ini", ".rst", ""  # empty ext = shell scripts
}


def _tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=REPO_ROOT, capture_output=True, check=True
    ).stdout
    return [p for p in out.decode().split("\0") if p]


def _git_log(fmt: str, max_n: int = 200) -> str:
    return subprocess.run(
        ["git", "log", f"--format={fmt}", f"-n{max_n}"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8", "replace")


class PublicHygieneTest(unittest.TestCase):
    def _violations(self, pattern: re.Pattern[str]) -> list[str]:
        bad: list[str] = []
        for rel in _tracked_files():
            if rel in _GUARD_TESTS or Path(rel).suffix not in _TEXT_EXT:
                continue
            p = REPO_ROOT / rel
            if not p.is_file() or p.is_symlink():
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if pattern.search(line):
                    bad.append(f"{rel}:{i}: {line.strip()[:80]}")
        return bad

    def test_no_private_ips_in_tracked_files(self) -> None:
        bad = self._violations(_PRIVATE_IP)
        self.assertEqual(
            [], bad, "private IP literals found in tracked files:\n" + "\n".join(bad[:20])
        )

    def test_no_real_home_paths_in_tracked_files(self) -> None:
        bad = self._violations(_HOME_PATH)
        self.assertEqual(
            [], bad, "real machine paths found in tracked files:\n" + "\n".join(bad[:20])
        )

    def test_no_real_emails_in_tracked_files(self) -> None:
        bad: list[str] = []
        for rel in _tracked_files():
            if rel in _GUARD_TESTS or Path(rel).suffix not in _TEXT_EXT:
                continue
            p = REPO_ROOT / rel
            if not p.is_file() or p.is_symlink():
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                for addr in _EMAIL.findall(line):
                    if addr in _ALLOWED_EMAIL_EXACT or addr.endswith(".invalid") or any(
                        addr.endswith(sfx) for sfx in _ALLOWED_EMAIL_SUFFIXES
                    ):
                        continue
                    bad.append(f"{rel}:{i}: {addr}")
        self.assertEqual(
            [], bad, "real email addresses found in tracked files:\n" + "\n".join(bad[:20])
        )

    def test_no_model_coauthor_trailers_in_history(self) -> None:
        body = _git_log("%B")
        bad = [l for l in body.splitlines() if _COAUTHOR.match(l) or _GENERATED_WITH.search(l)]
        self.assertEqual(
            [], bad, "model-authorship trailers in recent history:\n" + "\n".join(bad[:20])
        )

    def test_commit_identities_use_public_safe_emails(self) -> None:
        pairs = [
            ln
            for ln in _git_log("%ae|%ce").splitlines()
            if ln.strip() and ln != "|"
        ]
        bad = [
            ln
            for ln in pairs
            for addr in ln.split("|")
            if addr
            and not addr.endswith(".invalid")
            and addr not in _ALLOWED_EMAIL_EXACT
            and not any(addr.endswith(sfx) for sfx in _ALLOWED_EMAIL_SUFFIXES)
        ]
        self.assertEqual(
            [], bad, "non-public commit author/committer emails:\n" + "\n".join(sorted(set(bad)))
        )


if __name__ == "__main__":
    unittest.main()
