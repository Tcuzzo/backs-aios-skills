from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProviderCliContractTest(unittest.TestCase):
    def test_installer_does_not_chmod_provider_source_files(self) -> None:
        text = (ROOT / "install-provider.sh").read_text(encoding="utf-8")
        self.assertNotIn('chmod +x "$ROOT/provider/', text)
        self.assertNotIn('chmod +x "$ROOT/bin/', text)
        self.assertIn('install -m 0755', text)

    def test_cli_uses_persisted_project_context(self) -> None:
        text = (ROOT / "bin" / "backs-provider").read_text(encoding="utf-8")
        self.assertIn("provider-control/project-root", text)
        self.assertIn("BACKS_PROJECT_ROOT", text)

    def test_updater_reinstalls_with_saved_project_root(self) -> None:
        text = (ROOT / "bin" / "backs-aios-update").read_text(encoding="utf-8")
        self.assertIn("provider-control/project-root", text)
        self.assertIn('bash "$SOURCE/install-provider.sh" "$PROJECT_ROOT"', text)


if __name__ == "__main__":
    unittest.main()
