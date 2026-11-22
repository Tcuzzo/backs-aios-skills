"""Locale mirrors must not carry a word from another language.

A translated section that leaks one word from a neighbouring language — or
misspells one — reads as fluent nonsense to the very reader the mirror exists
for. Nothing else in this pack catches that: the link check and the frontmatter
check cannot see inside a sentence, and a reviewer reading only the English
body never notices.

Three rules, enforced loudly so the class cannot come back:

1. A Latin word in a locale mirror may only carry an accent that language uses.
   A Spanish word inside the French mirror is a Spanish word wearing French
   clothes, and the reader is the one who pays for it.
2. The blind-spot contract block in every turn-and-burn mirror must carry that
   locale's own spelling of its five load-bearing terms. A misspelling REMOVES
   the correct word, so requiring the correct word catches the corruption even
   when the corrupted one carries a perfectly legal accent for that language.
3. Every mirror translates the same six rules — one bullet per rule — so a
   dropped, duplicated or mangled rule is loud.

Rule 1 alone is not enough: a Portuguese typo can carry a legal Portuguese
accent. That is exactly why rule 2 exists.

This guard reads the real mirror files on disk. No mocks, no fixtures.
"""
from __future__ import annotations

import re
import unicodedata
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
I18N = REPO_ROOT / "i18n"

# The combining marks each language uses. A mark outside its own set means the
# word came from somewhere else, or the spelling is broken.
ALLOWED_MARKS = {
    # a o u
    "de": {"\u0308"},
    # a e i o u n
    "es": {"\u0301", "\u0303", "\u0308"},
    # a c e i o u y
    "fr": {"\u0300", "\u0301", "\u0302", "\u0308", "\u0327"},
    # a c e i o u
    "pt-BR": {"\u0300", "\u0301", "\u0302", "\u0303", "\u0327"},
    # Devanagari carries no Latin accent
    "hi": set(),
    # Han carries no Latin accent
    "zh-CN": set(),
}

# The five load-bearing terms of the blind-spot contract block, spelled the way
# each language spells them. The Hindi and Chinese mirrors keep the English
# technical terms on purpose, so their entries are the English words.
REQUIRED_WORDS = {
    "de": ("ausgeführt", "beobachtet", "Fortschritt", "Schlussfolgerung", "Organe"),
    "es": ("ejecutado", "observado", "progreso", "conclusión", "órganos"),
    "fr": ("exécuté", "observé", "progrès", "conclusion", "organes"),
    "hi": ("executed", "observed", "progress", "नतीजे", "अंग"),
    "pt-BR": ("executado", "observou", "progresso", "conclusão", "órgãos"),
    "zh-CN": ("执行", "观察到", "进展", "结论", "器官"),
}

# The heading that follows the contract block in every mirror.
_NEXT_HEADING = "absorbs flow runs"

_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def _latin_marks(word: str) -> set[str]:
    """The combining marks on a Latin word. Empty for a non-Latin word."""
    base = "".join(c for c in unicodedata.normalize("NFD", word) if not unicodedata.combining(c))
    if not base.isascii() or not base.isalpha():
        return set()
    return {c for c in unicodedata.normalize("NFD", word) if unicodedata.combining(c)}


def _contract_section(text: str) -> list[str]:
    """Every line of the blind-spot contract block in a turn-and-burn mirror."""
    lines = text.splitlines()
    end = next(
        i for i, line in enumerate(lines)
        if line.startswith("## ") and _NEXT_HEADING in line
    )
    start = max(i for i in range(end) if lines[i].startswith("## "))
    return lines[start:end]


def _contract_bullets(text: str) -> list[str]:
    """The rule bullets of that block — one line per rule."""
    return [line for line in _contract_section(text) if line.startswith("- **")]


class LocaleMirrorIntegrityTest(unittest.TestCase):
    """The mirrors are read by people who speak the language, not by tools."""

    def _mirrors(self) -> list[tuple[str, Path]]:
        found = []
        for locale_dir in sorted(I18N.iterdir()):
            if not locale_dir.is_dir():
                continue
            for skill_md in sorted(locale_dir.glob("skills/*/SKILL.md")):
                found.append((locale_dir.name, skill_md))
        return found

    def test_every_locale_mirror_only_carries_its_own_language_accents(self) -> None:
        for locale, path in self._mirrors():
            allowed = ALLOWED_MARKS.get(locale)
            with self.subTest(locale=locale, file=str(path.relative_to(REPO_ROOT))):
                self.assertIsNotNone(allowed, f"unknown locale {locale}")
                text = path.read_text(encoding="utf-8")
                for lineno, line in enumerate(text.splitlines(), 1):
                    for word in _WORD.findall(line):
                        marks = _latin_marks(word)
                        if not marks:
                            continue
                        foreign = marks - allowed
                        self.assertFalse(
                            foreign,
                            f"{path.relative_to(REPO_ROOT)}:{lineno}: {word!r} carries "
                            f"{sorted(foreign)} which {locale} does not use",
                        )

    def test_the_contract_block_carries_each_locale_own_words(self) -> None:
        for locale, path in self._mirrors():
            if path.parent.name != "turn-and-burn":
                continue
            with self.subTest(locale=locale):
                text = path.read_text(encoding="utf-8")
                block = "\n".join(_contract_section(text))
                for word in REQUIRED_WORDS[locale]:
                    self.assertIn(
                        word, block,
                        f"{path.relative_to(REPO_ROOT)}: the contract block does not "
                        f"spell {word!r}, the way {locale} spells it",
                    )

    def test_every_mirror_translates_the_same_six_rules(self) -> None:
        for locale, path in self._mirrors():
            if path.parent.name != "turn-and-burn":
                continue
            with self.subTest(locale=locale):
                text = path.read_text(encoding="utf-8")
                bullets = _contract_bullets(text)
                self.assertEqual(
                    len(bullets), 6,
                    f"{path.relative_to(REPO_ROOT)}: the contract block has "
                    f"{len(bullets)} rules, not six",
                )


if __name__ == "__main__":
    unittest.main()
