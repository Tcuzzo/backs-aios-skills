"""The blind-spot protocol must not be able to pass itself.

Two contradictions shipped in this file once, and a reader could not see
either of them: the evidence schema had no way to say "observed", so the
observation branch could never be taken, and the verdict function had no
status check, so a mechanism marked "unvalidated until demonstrated" could
still carry a +1. Both are soft passes, and rule 6 forbids a soft pass.

This guard reads the real protocol file on disk. It is a shape check on a
contract document, so the assertions are about the shape the contract must
have — a field that exists, a branch that is reachable, a gate that runs
before the pass.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROTOCOL = REPO_ROOT / "skills" / "turn-and-burn" / "references" / "blindspot_protocol.md"


def _schema(text: str) -> str:
    """The YAML evidence record block."""
    blocks = re.findall(r"```yaml\n(.*?)```", text, re.S)
    for block in blocks:
        if "blindspot:" in block and "evidence:" in block:
            return block
    raise AssertionError("the protocol has no evidence record block")


def _verdict_function(text: str) -> str:
    """The pseudocode of the verdict function."""
    blocks = re.findall(r"```text\n(.*?)```", text, re.S)
    for block in blocks:
        if "verdict(" in block:
            return block
    raise AssertionError("the protocol has no verdict function")


class BlindspotProtocolContractTest(unittest.TestCase):
    """The contract cannot talk itself into a pass."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = PROTOCOL.read_text(encoding="utf-8")
        cls.schema = _schema(cls.text)
        cls.verdict = _verdict_function(cls.text)

    def test_the_evidence_record_can_say_observed(self) -> None:
        self.assertIn("observed:", self.schema)
        self.assertIn("observed_at: <timestamp> | null", self.schema)

    def test_the_observation_branch_reads_the_observed_field(self) -> None:
        self.assertIn("not bound.observed", self.verdict)
        self.assertNotIn(
            "bound.kind != observed",
            self.verdict,
            "the evidence kind enum has no observed member, so that branch is dead code",
        )

    def test_the_verdict_function_takes_the_status(self) -> None:
        self.assertRegex(
            self.verdict,
            r"verdict\(claim, required_predicates, evidence, author, status\)",
            "the verdict function cannot see the status it is supposed to enforce",
        )

    def test_an_unvalidated_mechanism_cannot_carry_a_pass(self) -> None:
        gate = self.verdict.find('status != "validated"')
        self.assertNotEqual(
            gate, -1, "the verdict function never checks the status"
        )
        passed = self.verdict.find('return (+1, "")')
        self.assertNotEqual(passed, -1, "the verdict function has no pass branch")
        self.assertLess(
            gate, passed,
            "the status gate must run before the pass, not after it",
        )

    def test_the_reason_names_the_undemonstrated_mechanism(self) -> None:
        self.assertIn("unvalidated until demonstrated", self.verdict)

    def test_the_scenarios_cover_the_undemonstrated_mechanism(self) -> None:
        self.assertIn(
            "Fails (-1) on an undemonstrated mechanism",
            self.text,
            "a reader needs a worked example of the mechanism gate biting",
        )


if __name__ == "__main__":
    unittest.main()
