"""Canonical delivery receipts, rather than legacy markers, drive refresh."""
import json
import unittest
from foundation_fixture_support import FoundationManifestFixture


class FoundationHookRefreshTest(FoundationManifestFixture, unittest.TestCase):
    def test_legacy_marker_does_not_suppress_canonical_refresh(self):
        for suffix in ('js', 'py'):
            state = self.root/'home/.aios/state'
            state.mkdir(parents=True, exist_ok=True)
            (state/'aios_floor_floor-contract.state').write_text('floor loaded\n')
            result = self.run_gate(suffix, 'PreToolUse', tool_name='Write', tool_input={})
            self.assertEqual(result.returncode, 0, result.stderr)
            context = json.loads(result.stdout)['hookSpecificOutput']['additionalContext']
            self.assertIn('BACKS FOUNDATION', context)
            self.assertIn('not yet delivered', context)
            self.assertLess(len(context.encode()), 10000)

    def test_user_turn_refreshes_canonical_pointer_without_delivery_claim(self):
        for suffix in ('js', 'py'):
            result = self.run_gate(suffix, 'UserPromptSubmit', prompt='continue original task')
            self.assertEqual(result.returncode, 0, result.stderr)
            context = json.loads(result.stdout)['hookSpecificOutput']['additionalContext']
            self.assertIn('BACKS FOUNDATION', context)
            self.assertIn('not yet delivered', context)
            self.assertFalse((self.root/'home/.aios/state/aios_floor_floor-contract.state').exists())
