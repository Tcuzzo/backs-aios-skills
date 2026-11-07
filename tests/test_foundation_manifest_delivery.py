"""Real subprocess contract: canonical bodies are not delivery acknowledgments."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from foundation_fixture_support import FoundationManifestFixture


class FoundationManifestDeliveryTest(FoundationManifestFixture, unittest.TestCase):


    def test_explicit_load_emits_exact_manifest_bodies_in_order(self):
        for suffix in ("js", "py"):
            with self.subTest(runtime=suffix):
                result = self.load(suffix)
                self.assertEqual(result.returncode, 0, result.stderr)
                positions = [result.stdout.find(body) for body in self.bodies.values()]
                self.assertTrue(all(p >= 0 for p in positions), positions)
                self.assertEqual(positions, sorted(positions))

    def test_stdout_discard_never_certifies_foundation_delivery(self):
        for suffix in ("js", "py"):
            with self.subTest(runtime=suffix):
                result = self.load(suffix, discard=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                marker = self.root / "home/.aios/state/aios_floor_manifest-contract.state"
                self.assertFalse(marker.exists(), "stdout success is not host delivery")
                receipt = self.root / "home/.claude/state" / (
                    "backs_load_" + hashlib.sha256(b"manifest-contract").hexdigest() + ".json")
                self.assertFalse(receipt.exists(), "only host-observed output can certify delivery")
