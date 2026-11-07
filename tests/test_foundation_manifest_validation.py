"""Adversarial real-file coverage for the portable foundation loader."""
import json
from pathlib import Path
import unittest
from foundation_fixture_support import FoundationManifestFixture


class FoundationManifestValidationTest(FoundationManifestFixture, unittest.TestCase):
    def _manifest(self):
        return self.deploy / "config/foundation_manifest.json"

    def _assert_both_fail(self, needle):
        errors = []
        for suffix in ("js", "py"):
            result = self.load(suffix)
            self.assertNotEqual(result.returncode, 0, suffix)
            self.assertEqual(result.stdout, "")
            errors.append(result.stderr.lower())
        self.assertTrue(all(needle in error for error in errors), errors)

    def test_missing_pin_fails_in_js_and_python(self):
        manifest = json.loads(self._manifest().read_text())
        manifest["bodies"][0].pop("sha256")
        self._manifest().write_text(json.dumps(manifest))
        self._assert_both_fail("hash mismatch")

    def test_stale_hash_fails_in_js_and_python(self):
        manifest = json.loads(self._manifest().read_text())
        manifest["bodies"][0]["sha256"] = "0" * 64
        self._manifest().write_text(json.dumps(manifest))
        self._assert_both_fail("hash mismatch")

    def test_path_escape_fails_in_js_and_python(self):
        outside = self.root / "outside.md"
        outside.write_text("outside\n")
        manifest = json.loads(self._manifest().read_text())
        manifest["bodies"][0]["path"] = "../outside.md"
        self._manifest().write_text(json.dumps(manifest))
        self._assert_both_fail("unsafe foundation path")

    def test_js_python_emit_identical_bytes(self):
        js = self.load("js")
        py = self.load("py")
        self.assertEqual(js.returncode, 0, js.stderr)
        self.assertEqual(py.returncode, 0, py.stderr)
        self.assertEqual(js.stdout.encode(), py.stdout.encode())
