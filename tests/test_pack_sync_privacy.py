"""Synthetic privacy controls for the public BACKS skill bridge."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASH = Path(r"C:\Program Files\Git\bin\bash.exe")


def bash_path(path: Path) -> str:
    resolved = path.resolve()
    return f"/{resolved.drive[0].lower()}{resolved.as_posix()[2:]}"


@unittest.skipUnless(BASH.is_file(), "Git Bash is needed for the shell bridge contract")
class PackSyncPrivacyTest(unittest.TestCase):
    def setUp(self) -> None:
        sandbox = ROOT / "sandbox"
        sandbox.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=sandbox)
        self.assertTrue(Path(self.tmp.name).resolve().is_relative_to(sandbox.resolve()))
        self.addCleanup(self._cleanup_sandbox)
        self.root = Path(self.tmp.name) / "public-pack"
        (self.root / "bin").mkdir(parents=True)
        (self.root / "skills").mkdir()
        (self.root / "public-bridges").mkdir()
        shutil.copyfile(ROOT / "bin" / "backs-pack-sync", self.root / "bin" / "backs-pack-sync")
        shutil.copyfile(ROOT / "bin" / "scrub-plugin-pack-literals", self.root / "bin" / "scrub-plugin-pack-literals")
        self.native = Path(self.tmp.name) / "private-runtime"
        self.native_skill = self.native / "skills" / "private-agent"
        self.native_skill.mkdir(parents=True)
        self.native_skill.joinpath("SKILL.md").write_text(
            '---\nname: private-agent\ndescription: fixture-private-description\n---\n'
            'fixture-private-body /' + 'home/fixture/secret\n', encoding="utf-8"
        )

    def _cleanup_sandbox(self) -> None:
        self.assertTrue(Path(self.tmp.name).resolve().is_relative_to((ROOT / "sandbox").resolve()))
        self.tmp.cleanup()

    def run_bridge(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["BACKS_SOURCE"] = bash_path(self.native)
        return subprocess.run(
            [str(BASH), bash_path(self.root / "bin" / "backs-pack-sync"), *args],
            cwd=self.root, env=env, capture_output=True, text=True, check=False,
        )

    def assert_private_unexposed(self, result: subprocess.CompletedProcess[str]) -> None:
        combined = result.stdout + result.stderr
        for marker in ("private-agent", "fixture-private-description", "fixture-private-body", "fixture/secret"):
            self.assertNotIn(marker, combined)
        self.assertFalse((self.root / "skills" / "private-agent").exists())

    def test_default_drift_reports_count_without_private_names_or_paths(self) -> None:
        result = self.run_bridge()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("1", result.stdout)
        self.assert_private_unexposed(result)

    def test_bulk_bridge_cannot_copy_private_source(self) -> None:
        result = self.run_bridge("--bridge-all-missing")
        self.assertNotEqual(0, result.returncode)
        self.assert_private_unexposed(result)

    def test_named_bridge_requires_curated_public_body(self) -> None:
        result = self.run_bridge("--bridge", "private-agent")
        self.assertNotEqual(0, result.returncode)
        self.assert_private_unexposed(result)

    def test_curated_bridge_uses_only_public_authored_body(self) -> None:
        curated = self.root / "public-bridges" / "public-safe"
        curated.mkdir()
        curated.joinpath("SKILL.md").write_text(
            "---\nname: public-safe\ndescription: Generic public skill\n---\n"
            "# Public body\nThis is public authored content.\n", encoding="utf-8"
        )
        result = self.run_bridge("--bridge", "public-safe")
        self.assertEqual(0, result.returncode, result.stderr)
        body = (self.root / "skills" / "public-safe" / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(curated.joinpath("SKILL.md").read_text(encoding="utf-8"), body)
        self.assertNotIn("fixture-private", body)

    def test_public_bridge_with_private_literal_is_rejected_before_copy(self) -> None:
        curated = self.root / "public-bridges" / "public-safe"
        curated.mkdir()
        curated.joinpath("SKILL.md").write_text(
            "---\nname: public-safe\ndescription: Generic public skill\n---\n"
            "private path /" + "home/fixture/secret\n", encoding="utf-8"
        )
        result = self.run_bridge("--bridge", "public-safe")
        self.assertNotEqual(0, result.returncode)
        self.assertFalse((self.root / "skills" / "public-safe").exists())
        self.assertNotIn("fixture/secret", result.stdout + result.stderr)

    def test_curated_bridge_accepts_quoted_frontmatter_name(self) -> None:
        curated = self.root / "public-bridges" / "public-safe"
        curated.mkdir()
        curated.joinpath("SKILL.md").write_text(
            '---\nname: "public-safe"\ndescription: Generic public skill\n---\n# Public body\n',
            encoding="utf-8",
        )
        result = self.run_bridge("--bridge", "public-safe")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_public_bridge_with_windows_absolute_path_is_rejected(self) -> None:
        curated = self.root / "public-bridges" / "public-safe"
        curated.mkdir()
        for literal in ("C:/Users/fixture/private", r"C:\Users\fixture\private"):
            curated.joinpath("SKILL.md").write_text(
                "---\nname: public-safe\ndescription: Generic public skill\n---\n"
                + literal + "\n", encoding="utf-8"
            )
            result = self.run_bridge("--bridge", "public-safe")
            self.assertNotEqual(0, result.returncode)
            self.assertFalse((self.root / "skills" / "public-safe").exists())
            self.assertNotIn(literal, result.stdout + result.stderr)

    def test_wrapped_plugin_script_resolves_pack_root(self) -> None:
        bridge = self.root / "skills" / "backs-pack-sync" / "scripts"
        guard = self.root / "skills" / "scrub-plugin-pack-literals" / "scripts"
        bridge.mkdir(parents=True)
        guard.mkdir(parents=True)
        shutil.copyfile(ROOT / "bin" / "backs-pack-sync", bridge / "backs-pack-sync")
        shutil.copyfile(ROOT / "bin" / "scrub-plugin-pack-literals", guard / "scrub-plugin-pack-literals")
        curated = self.root / "public-bridges" / "public-safe"
        curated.mkdir()
        curated.joinpath("SKILL.md").write_text(
            "---\nname: public-safe\ndescription: Generic public skill\n---\n# Public body\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [str(BASH), bash_path(bridge / "backs-pack-sync"), "--bridge", "public-safe"],
            cwd=self.root, capture_output=True, text=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.root / "skills" / "public-safe" / "SKILL.md").is_file())

    def test_private_runtime_seat_is_absent_from_public_source(self) -> None:
        self.assertFalse((ROOT / "skills" / "hive-clone-boot").exists())
        for locale in ("de", "es", "fr", "hi", "pt-BR", "zh-CN"):
            self.assertFalse((ROOT / "i18n" / locale / "skills" / "hive-clone-boot").exists())


if __name__ == "__main__":
    unittest.main()
