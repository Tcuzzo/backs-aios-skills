from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PROVIDER_PATHS = (
    ROOT / "provider",
    ROOT / "claude-skills" / "provider",
    ROOT / "bin" / "backs-aios-update",
    ROOT / "install-provider.sh",
)

PRIVATE_IPV4 = re.compile(
    r"\b(?:10\.(?:\d{1,3}\.){2}\d{1,3}|"
    r"192\.168\.(?:\d{1,3}\.)\d{1,3}|"
    r"172\.(?:1[6-9]|2\d|3[01])\.(?:\d{1,3}\.)\d{1,3})\b"
)
ABSOLUTE_USER_PATH = re.compile(r"(?:/home/[^/$\s\"']+|/Users/[^/$\s\"']+)")
SECRET_LITERAL = re.compile(
    r"(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{20,}|AKIA[0-9A-Z]{16})"
)
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)


def iter_public_files():
    for entry in PUBLIC_PROVIDER_PATHS:
        if entry.is_file():
            yield entry
        elif entry.is_dir():
            yield from (
                path
                for path in entry.rglob("*")
                if path.is_file() and path.suffix in {".py", ".sh", ".json", ".md"}
            )


class ProviderPublicSafetyTest(unittest.TestCase):
    def test_provider_distribution_contains_no_private_network_or_secret_literals(self) -> None:
        for path in iter_public_files():
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertIsNone(PRIVATE_IPV4.search(text))
                self.assertIsNone(ABSOLUTE_USER_PATH.search(text))
                self.assertIsNone(SECRET_LITERAL.search(text))
                self.assertIsNone(EMAIL.search(text))
                self.assertNotIn("/opt/JarvisAI", text)
                self.assertNotIn("/mnt/", text)

    def test_profiles_never_embed_api_keys(self) -> None:
        for path in (ROOT / "provider" / "profiles").glob("*.json"):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotRegex(text, r'"(?:api_?key|token|secret)"\s*:\s*"[^"]+"')


if __name__ == "__main__":
    unittest.main()
