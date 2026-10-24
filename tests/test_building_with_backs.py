from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills/building-with-backs/scripts/resolve_target.py"
TEST_TMP_ROOT = Path(os.environ.get("AIOS_TEST_SANDBOX", tempfile.gettempdir())) / "backs-aios-target-tests"
TEST_TMP_ROOT.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location("resolve_target", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TargetResolutionTest(unittest.TestCase):
    def test_accepts_requested_target_inside_root(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            result, code = module.resolve(str(root), "src/new.py", str(root), True)
            self.assertEqual(0, code)
            self.assertTrue(result["ok"])
            self.assertEqual(str(root / "src/new.py"), result["target"])

    def test_refuses_path_outside_root(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            result, code = module.resolve(str(root), "../other/new.py", str(root))
            self.assertEqual(2, code)
            self.assertIn("target resolves outside the checkout", result["errors"])

    def test_refuses_mismatched_checkout(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            root = Path(tmp) / "project"
            other = Path(tmp) / "other"
            root.mkdir()
            other.mkdir()
            result, code = module.resolve(str(root), "new.py", str(other))
            self.assertEqual(2, code)
            self.assertIn("resolved checkout differs from expected root", result["errors"])

    def test_refuses_missing_target_parent(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            root = Path(tmp)
            result, code = module.resolve(str(root), "missing/new.py", str(root))
            self.assertEqual(2, code)
            self.assertIn("target parent does not exist", result["errors"])

    def test_non_git_requires_explicit_flag(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            result, code = module.resolve(tmp, "new.py", tmp)
            self.assertEqual(2, code)
            self.assertFalse(result["git"])
            self.assertTrue(any("Git revision unavailable" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
