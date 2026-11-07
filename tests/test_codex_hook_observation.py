"""Observation is payload-shape evidence, never proof of delivered foundation."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMMAND = "printf '%s\\n' BACKS_CODEX_HOOK_SENTINEL_V1"


class CodexHookObservationTest(unittest.TestCase):
    def test_exact_sentinel_captures_shape_once_without_raw_values_or_grounding(self):
        (ROOT / 'sandbox/hook-tests').mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / 'sandbox/hook-tests') as temporary:
            home = Path(temporary)
            payload = {'hook_event_name': 'PostToolUse', 'tool_name': 'Bash',
                       'session_id': 'observer-session', 'turn_id': 'turn-private',
                       'tool_use_id': 'call-private', 'tool_input': {'command': COMMAND},
                       'tool_response': {'output': 'private-output-never-store', 'exit_code': 0}}
            run = subprocess.run(['node', str(ROOT/'hooks/aios_gate.js')],
                input=json.dumps(payload), text=True, capture_output=True,
                env={**os.environ, 'HOME': str(home)}, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            evidence = list((home/'.aios/state').glob('codex_tool_shape_*.json'))
            self.assertEqual(len(evidence), 1)
            raw = evidence[0].read_text()
            self.assertNotIn('private-output', raw)
            self.assertNotIn('turn-private', raw)
            receipt = json.loads(raw)
            self.assertEqual(receipt['kind'], 'tool_payload_shape')
            self.assertEqual(receipt['command_sha256'], hashlib.sha256(COMMAND.encode()).hexdigest())
            self.assertEqual(receipt['tool_response']['output']['type'], 'string')
            self.assertFalse((home/'.claude/state').exists())
            self.assertFalse(list((home/'.aios/state').glob('aios_floor_*')))
            prior = evidence[0].read_bytes()
            subprocess.run(['node', str(ROOT/'hooks/aios_gate.js')],
                input=json.dumps(payload), text=True, capture_output=True,
                env={**os.environ, 'HOME': str(home)}, timeout=10, check=True)
            self.assertEqual(evidence[0].read_bytes(), prior)
