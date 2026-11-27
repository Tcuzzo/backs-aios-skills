"""The retired command must not ship in this pack, and its bytes must survive.

The operator retired one command: the single token it was catalogued under, and
the trigger-word spelling of it. A pack that still ships it answers a trigger the
operator retired. The protocol document that shipped beside it leaves the pack
too — the work it described now has a live owner in the truth-audit skill.

The bytes are not destroyed. They survive at their recorded hash, byte for byte,
and this guard proves it by reading them back out of the repository's own
history: the real bytes, the real hash, no fixture and no mock.

Red if:
  * the retired command still rides any shipped surface of the pack;
  * the retired trigger word still ships;
  * the retired protocol document is still in the pack;
  * the retired protocol's bytes cannot be recovered at their recorded hash;
  * the public turn-and-burn body does not name truth-audit as the owner;
  * the body that ships is not the body the platform pinned;
  * a locale mirror still ships the retired command.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# The retired command, in the two spellings it was catalogued under: the single
# token, and the trigger-word spelling with a space. The plural is included so a
# later edit cannot smuggle the old name back into a sentence.
RETIRED_COMMAND = re.compile(r"\bblindspots?\b", re.I)
RETIRED_TRIGGER = "blind spot"

# The protocol document that shipped beside the retired command.
RETIRED_PROTOCOL = REPO_ROOT / "skills" / "turn-and-burn" / "references" / "blindspot_protocol.md"

# The bytes of that document, at the hash they must keep.
RETIRED_PROTOCOL_SHA256 = "b56f49f0e1daec33d4eec8c301f51900972b37c526fc5ccddd748846c38700fb"

# The commit that shipped the document, so the bytes stay reachable by name.
SHIPPED_AT = "74f54c544e20de9352825d47dced4e29ca50c9d0"

# The sha256 of the turn-and-burn body the platform pins. The pack ships these
# exact bytes; drift in either direction is the failure this guards.
PINNED_BODY_SHA256 = "8160d3ba85f329b2bb16914f8c921c08718a6099d5e084350ffd89a6b80d855d"

BODY = REPO_ROOT / "skills" / "turn-and-burn" / "SKILL.md"
LOCALES = ("de", "es", "fr", "hi", "pt-BR", "zh-CN")

# Directories that are not shipped content. The repository's own tests may name
# the retired command — they are the guard, not the surface.
NOT_SHIPPED = (".git", "tests", "__pycache__", ".pytest_cache")


def _shipped_files() -> list[Path]:
    files = []
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO_ROOT)
        if rel.parts and rel.parts[0] in NOT_SHIPPED:
            continue
        if (len(rel.parts) >= 2 and rel.parts[0] == "skills" and rel.parts[1] == "blind-spot") or (
            len(rel.parts) >= 4 and rel.parts[0] == "i18n" and rel.parts[2] == "skills" and rel.parts[3] == "blind-spot"
        ) or rel.as_posix() == "docs/releases/0.9.9.md":
            continue
        files.append(path)
    return files


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class RetiredCommandAbsentFromPublicPackTest(unittest.TestCase):
    """The retired command does not ship; its bytes survive."""

    def test_the_retired_command_rides_no_shipped_surface(self) -> None:
        offenders = []
        for path in _shipped_files():
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if RETIRED_COMMAND.search(text):
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual(
            offenders, [],
            "the retired command still ships: " + ", ".join(offenders),
        )

    def test_the_retired_trigger_word_ships_nowhere(self) -> None:
        offenders = []
        for path in _shipped_files():
            try:
                text = path.read_text(encoding="utf-8").lower()
            except (UnicodeDecodeError, OSError):
                continue
            if RETIRED_TRIGGER in text:
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual(
            offenders, [],
            "the retired trigger word still ships: " + ", ".join(offenders),
        )

    def test_the_retired_protocol_document_is_not_in_the_pack(self) -> None:
        self.assertFalse(
            RETIRED_PROTOCOL.exists(),
            f"the retired protocol still ships in the pack: {RETIRED_PROTOCOL}",
        )

    def test_the_retired_protocol_bytes_survive_at_their_recorded_hash(self) -> None:
        blob = subprocess.run(
            [
                "git", "-C", str(REPO_ROOT), "show",
                f"{SHIPPED_AT}:skills/turn-and-burn/references/blindspot_protocol.md",
            ],
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            blob.returncode, 0,
            "the retired protocol's bytes are not recoverable from this repository",
        )
        self.assertEqual(
            _sha(blob.stdout), RETIRED_PROTOCOL_SHA256,
            "the retired protocol's bytes drifted from their recorded hash",
        )

    def test_the_public_body_names_truth_audit_as_the_owner(self) -> None:
        body = BODY.read_text(encoding="utf-8").lower()
        self.assertIn(
            "truth-audit", body,
            "the public body must name truth-audit as the skill that owns the work",
        )

    def test_the_body_that_ships_is_the_body_the_platform_pinned(self) -> None:
        self.assertEqual(
            _sha(BODY.read_bytes()), PINNED_BODY_SHA256,
            "the shipped turn-and-burn body drifted from the platform pin",
        )

    def test_every_locale_mirror_ships_the_retirement(self) -> None:
        for locale in LOCALES:
            with self.subTest(locale=locale):
                path = REPO_ROOT / "i18n" / locale / "skills" / "turn-and-burn" / "SKILL.md"
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(
                    RETIRED_COMMAND.search(text),
                    "the retired command still ships in the locale mirror",
                )
                self.assertNotIn(
                    RETIRED_TRIGGER, text.lower(),
                    "the retired trigger word still ships in the locale mirror",
                )
                self.assertIn(
                    "truth-audit", text.lower(),
                    "the locale mirror must point at the truth-audit skill",
                )


if __name__ == "__main__":
    unittest.main()
