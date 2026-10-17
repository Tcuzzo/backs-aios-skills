"""Run the portable rollover regression suite from the normal repository CI."""
from pathlib import Path
import subprocess
import sys
import unittest


class SessionRolloverContractTest(unittest.TestCase):
    def test_portable_regressions(self):
        scripts = Path(__file__).resolve().parents[1] / "skills" / "backs-session-rollover" / "scripts"
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(scripts), "-p", "test_*.py", "-v"],
            text=True, capture_output=True, timeout=90,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_installer_regressions(self):
        scripts = Path(__file__).resolve().parents[1] / "scripts" / "rollover"
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(scripts), "-p", "test_*.py", "-v"],
            text=True, capture_output=True, timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
