from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOCALES = ("de", "es", "fr", "hi", "pt-BR", "zh-CN")
COMMAND_NAMES = {
    "agent-build",
    "bughunt",
    "design-taste",
    "elite-build",
    "grade",
    "optimus",
    "parallel-work",
    "secure-delivery",
    "tribunal",
    "web-build",
}
COMMAND_SKILL_NAMES = COMMAND_NAMES - {"design-taste", "optimus"}


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise AssertionError(f"{path.relative_to(ROOT)} has no leading YAML frontmatter")
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        raise AssertionError(f"{path.relative_to(ROOT)} has invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise AssertionError(f"{path.relative_to(ROOT)} frontmatter is not a mapping")
    return data


class PackContractTest(unittest.TestCase):
    def test_all_skills_are_portable_agent_skills(self) -> None:
        roots = [ROOT / "skills", *(ROOT / "i18n" / locale / "skills" for locale in LOCALES)]
        for skills_root in roots:
            for skill_file in sorted(skills_root.glob("*/SKILL.md")):
                with self.subTest(skill=str(skill_file.relative_to(ROOT))):
                    data = frontmatter(skill_file)
                    name = data.get("name")
                    description = data.get("description")
                    self.assertEqual(skill_file.parent.name, name)
                    self.assertRegex(name, NAME_RE)
                    self.assertLessEqual(len(name), 64)
                    self.assertIsInstance(description, str)
                    self.assertLessEqual(len(description), 1024)
                    self.assertGreater(len(description), 0)
                    self.assertLessEqual(len(skill_file.read_text(encoding="utf-8").splitlines()), 500)

    def test_language_mirrors_match_the_canonical_skill_set(self) -> None:
        canonical = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(36, len(canonical))
        translated_core = canonical - COMMAND_SKILL_NAMES
        self.assertEqual(28, len(translated_core))
        for locale in LOCALES:
            translated = {
                path.parent.name
                for path in (ROOT / "i18n" / locale / "skills").glob("*/SKILL.md")
            }
            self.assertEqual(translated_core, translated, locale)

    def test_commands_are_valid_for_claude_and_cursor(self) -> None:
        commands = sorted((ROOT / "commands").glob("*.md"))
        self.assertEqual(10, len(commands))
        self.assertEqual(COMMAND_NAMES, {command.stem for command in commands})
        for command in commands:
            with self.subTest(command=command.name):
                data = frontmatter(command)
                self.assertEqual(command.stem, data.get("name"))
                self.assertIsInstance(data.get("description"), str)

    def test_codex_command_skill_adapters_cover_noncanonical_commands(self) -> None:
        adapters = [ROOT / "skills" / name / "SKILL.md" for name in COMMAND_SKILL_NAMES]
        self.assertTrue(all(path.is_file() for path in adapters))
        for adapter in adapters:
            with self.subTest(adapter=adapter.parent.name):
                data = frontmatter(adapter)
                self.assertEqual(adapter.parent.name, data.get("name"))
                body = adapter.read_text(encoding="utf-8")
                self.assertIn("plays/", body)
                self.assertIn("~/.local/share/backs-aios/current/", body)

        codex = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual("./skills/", codex["skills"])

    def test_plugin_manifests_share_one_release_version(self) -> None:
        manifests = (
            ROOT / ".claude-plugin" / "plugin.json",
            ROOT / ".codex-plugin" / "plugin.json",
            ROOT / ".cursor-plugin" / "plugin.json",
        )
        parsed = [json.loads(path.read_text(encoding="utf-8")) for path in manifests]
        self.assertEqual({"backs-aios"}, {manifest["name"] for manifest in parsed})
        self.assertEqual(1, len({manifest["version"] for manifest in parsed}))
        marketplace = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
        )
        self.assertEqual(parsed[0]["version"], marketplace["plugins"][0]["version"])
        citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
        self.assertEqual(parsed[0]["version"], str(citation["version"]))
        self.assertNotIn("hooks", parsed[0], "Claude auto-loads hooks/hooks.json")
        cursor = parsed[2]
        self.assertEqual("./skills/", cursor["skills"])
        self.assertEqual("./commands/", cursor["commands"])
        self.assertEqual("./hooks/cursor-hooks.json", cursor["hooks"])

    def test_cursor_hook_config_uses_native_event_shape(self) -> None:
        path = ROOT / "hooks" / "cursor-hooks.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(1, data["version"])
        self.assertIn("sessionStart", data["hooks"])
        self.assertIn("preToolUse", data["hooks"])
        self.assertIn("postToolUse", data["hooks"])

    def test_installers_cover_unix_and_windows(self) -> None:
        self.assertTrue((ROOT / "install.sh").is_file())
        self.assertTrue((ROOT / "install.ps1").is_file())
        shell = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertNotIn("readlink -f", shell, "stock macOS readlink has no -f")
        self.assertNotIn("python3", shell, "the Unix installer must not require Python")
        powershell = (ROOT / "install.ps1").read_text(encoding="utf-8")
        for text in (shell, powershell):
            self.assertIn(".config/opencode/commands", text)
            self.assertIn(".claude/commands", text)
            self.assertIn(".local/share/backs-aios/current", text)

    def test_unix_all_install_registers_real_host_commands(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            env = {**os.environ, "HOME": home}
            result = subprocess.run(
                [str(ROOT / "install.sh"), "--target", "all"],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)

            runtime = Path(home) / ".local" / "share" / "backs-aios" / "current"
            self.assertTrue(runtime.exists())
            for relative in (".config/opencode/commands", ".claude/commands"):
                command_root = Path(home) / relative
                installed = {path.stem for path in command_root.glob("*.md")}
                self.assertEqual(COMMAND_NAMES, installed, relative)
                for command in command_root.glob("*.md"):
                    body = command.read_text(encoding="utf-8")
                    self.assertIn("backs-aios-managed-command", body)
                    self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", body)
                    self.assertNotIn("${CURSOR_PLUGIN_ROOT}", body)
                    self.assertIn(str(runtime), body)

            for relative in (".codex/skills", ".agents/skills"):
                skill_root = Path(home) / relative
                installed = {
                    path.parent.name for path in skill_root.glob("*/SKILL.md")
                }
                self.assertTrue(COMMAND_NAMES <= installed, relative)

    def test_copy_install_excludes_repository_internals(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            env = {**os.environ, "HOME": home}
            result = subprocess.run(
                [str(ROOT / "install.sh"), "--target", "all", "--copy"],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            copies = (
                Path(home) / ".local" / "share" / "backs-aios" / "current",
                Path(home) / ".cursor" / "plugins" / "local" / "backs-aios",
            )
            for copied_root in copies:
                with self.subTest(copied_root=copied_root):
                    self.assertFalse((copied_root / ".git").exists())
                    self.assertFalse((copied_root / ".pytest_cache").exists())
                    self.assertEqual([], list(copied_root.rglob("__pycache__")))
                    self.assertEqual([], list(copied_root.rglob("*.pyc")))

    def test_install_docs_name_each_supported_host(self) -> None:
        text = (ROOT / "INSTALL.md").read_text(encoding="utf-8").lower()
        for host in ("codex", "cursor", "opencode", "claude code", ".agents/skills"):
            with self.subTest(host=host):
                self.assertIn(host, text)

    def test_relative_markdown_links_resolve(self) -> None:
        link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts:
                continue
            for raw_target in link_re.findall(path.read_text(encoding="utf-8")):
                target = raw_target.strip().split()[0]
                if target.startswith(("http://", "https://", "mailto:", "#", "codex://")):
                    continue
                file_part = target.split("#", 1)[0]
                if not file_part:
                    continue
                with self.subTest(path=str(path.relative_to(ROOT)), target=target):
                    self.assertTrue((path.parent / file_part).resolve().exists())


if __name__ == "__main__":
    unittest.main()
