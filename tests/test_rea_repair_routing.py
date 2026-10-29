from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("en", "de", "es", "fr", "hi", "pt-BR", "zh-CN")

class ReaRepairRouting(unittest.TestCase):
    def test_copied_skills_route_without_colliding_with_upstream(self):
        for locale in LOCALES:
            root = ROOT if locale == "en" else ROOT / "i18n" / locale
            with self.subTest(locale=locale), tempfile.TemporaryDirectory(dir=os.environ.get('BACKS_TEST_TEMP')) as tmp:
                dest = Path(tmp)
                upstream = dest / "reverse-engineer-anything"
                upstream.mkdir()
                (upstream / "SKILL.md").write_text("upstream sentinel", encoding="utf-8")
                for name in ("fix-shit", "rea-investigation", "absorb", "fleet-ladder", "blind-tribunal"):
                    shutil.copytree(root / "skills" / name, dest / name)
                text = (dest / "fix-shit/SKILL.md").read_text(encoding="utf-8-sig").lower()
                for term in ("rea-investigation", "reverse-engineer-anything", "ghidra", "absorb", "fleet-ladder", "blind-tribunal", "author-disjoint"):
                    self.assertIn(term, text)
                for name in ("rea-investigation", "absorb", "fleet-ladder", "blind-tribunal"):
                    self.assertTrue((dest / name / "SKILL.md").is_file())
                self.assertEqual((upstream / "SKILL.md").read_text(encoding="utf-8"), "upstream sentinel")

    def test_windows_installer_preserves_upstream_and_installs_locale_routing(self):
        if os.name != "nt":
            self.skipTest("Windows installer")
        with tempfile.TemporaryDirectory(dir=os.environ.get('BACKS_TEST_TEMP')) as tmp:
            dest = Path(tmp) / "skills"
            upstream = dest / "reverse-engineer-anything"
            upstream.mkdir(parents=True)
            (upstream / "SKILL.md").write_text("upstream sentinel", encoding="utf-8")
            script = (ROOT / "install.ps1").read_text(encoding="utf-8-sig")
            script = script.split("function Install-CommandSkills", 1)[0]
            script = script.replace("Split-Path -Parent $MyInvocation.MyCommand.Path", "$env:BACKS_TEST_ROOT", 1)
            script += "\n$Skills = Join-Path $Root 'i18n/es/skills'\nInstall-Skills 'test' $env:BACKS_TEST_DEST\nif ($script:Conflicts -ne 0) { exit 1 }\n"
            env = dict(os.environ, BACKS_TEST_ROOT=str(ROOT), BACKS_TEST_DEST=str(dest))
            shell = shutil.which("pwsh") or shutil.which("powershell")
            if shell is None:
                self.skipTest("PowerShell unavailable")
            result = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-Command", script], env=env, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((upstream / "SKILL.md").read_text(encoding="utf-8"), "upstream sentinel")
            for name in ("rea-investigation", "fix-shit", "absorb", "fleet-ladder", "blind-tribunal"):
                self.assertTrue((dest / name / "SKILL.md").is_file(), name)
            self.assertIn("rea-investigation", (dest / "fix-shit/SKILL.md").read_text(encoding="utf-8-sig"))
    def test_all_locales_match_canonical_ladder_policy(self):
        anchors = {
            "de": ("keinen resolver", "frischen, vom autor getrennten ausführung", "live-inferenz"),
            "es": ("no incluye resolutor", "ejecución nueva y separada del autor", "inferencia real"),
            "fr": ("ni résolveur", "nouvelle exécution séparée de l’auteur", "inférence réelle"),
            "hi": ("resolver या fleet executable नहीं", "नई author से अलग execution", "वास्तविक bounded inference"),
            "pt-BR": ("não inclui resolvedor", "execução nova e separada do autor", "inferência real"),
            "zh-CN": ("不提供解析器", "与作者分离的新执行", "真实、有界的推理"),
        }
        for locale, terms in anchors.items():
            with self.subTest(locale=locale):
                text = (ROOT / "i18n" / locale / "skills/fleet-ladder/SKILL.md").read_text(encoding="utf-8-sig").lower()
                for term in terms:
                    self.assertIn(term, text)

    def test_rea_bridge_preserves_provider_boundaries(self):
        text = (ROOT / "skills/rea-investigation/SKILL.md").read_text(encoding="utf-8-sig").lower()
        for term in ("ghidra", "evidence", "static", "runtime", "read-only", "unavailable"):
            with self.subTest(term=term):
                self.assertIn(term, text)

if __name__ == "__main__":
    unittest.main()
