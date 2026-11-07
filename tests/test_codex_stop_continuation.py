"""Physical subprocess contract for bounded same-thread Codex Stop continuation."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from backs_owner import deployed_owner


ROOT = Path(__file__).resolve().parents[1]
DEPLOY = deployed_owner()
HOOK = ROOT / "hooks/aios_gate.js"
ADAPTER = ROOT / "hooks/codex_stop_continuation.py"


class CodexStopContinuationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.runs = self.base / "runs"
        self.session = "session-one"
        self.cwd = self.base / "workspace"
        self.cwd.mkdir()
        self.env = {**os.environ, "BACKS_DEPLOY_ROOT": str(DEPLOY),
                    "BACKS_AI_DURABLE_RUN_DIR": str(self.runs),
                    "CODEX_SESSION_ID": self.session}
        self._seed()

    def tearDown(self):
        self.tmp.cleanup()

    def _seed(self):
        code = """
from core.durable_runs import DurableRunStore
s=DurableRunStore()
s.ensure_run(run_id='run-one', surface='codex', trace_id='trace', run_context_id='ctx',
 resume_identity='session-one', prompt='continue', mission_id='mission-one', status='running')
"""
        subprocess.run([sys.executable, "-c", code], env={**self.env, "PYTHONPATH": str(DEPLOY / "backend")}, check=True)
        binding = {"mission_id": "mission-one", "session_id": self.session,
                   "workspace": str(self.cwd), "scope": ["hooks/"],
                   "absolute_deadline": "2999-01-01T00:00:00+00:00",
                   "call_ceiling": 8, "calls_used": 3, "cost_ceiling": 10.0,
                   "cost_used": 2.5, "checkpoint_identity": "checkpoint-1",
                   "stall_limit": 3, "stall_count": 0, "progress_signature": "p1"}
        result = subprocess.run([sys.executable, str(ADAPTER), "bind", "run-one"],
            env={**self.env, "PYTHONPATH": str(DEPLOY / "backend")},
            input=json.dumps(binding), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def stop(self, **changes):
        payload = {"hook_event_name": "Stop", "session_id": self.session,
                   "cwd": str(self.cwd), "stop_hook_active": False,
                   "transcript_path": str(self.base / "transcript.jsonl"), **changes}
        return subprocess.run(["node", str(HOOK)], env=self.env, input=json.dumps(payload),
                              text=True, capture_output=True)

    def manifest(self):
        return json.loads((self.runs / "run-one/run_manifest.json").read_text())

    def update(self, **fields):
        path = self.runs / "run-one/run_manifest.json"
        value = json.loads(path.read_text()); value.update(fields); path.write_text(json.dumps(value))

    def test_active_continuation_is_idempotent_and_preserves_counters(self):
        first = self.stop()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)["decision"], "block")
        after = self.manifest()["codex_continuation"]
        self.assertEqual((after["calls_used"], after["cost_used"], after["checkpoint_identity"]), (3, 2.5, "checkpoint-1"))
        duplicate = self.stop()
        self.assertEqual(duplicate.returncode, 0)
        self.assertEqual(duplicate.stdout, "")
        self.assertEqual(self.manifest()["codex_continuation"]["callback_count"], 1)

    def test_terminal_cancelled_expired_stalled_and_exhausted_stop(self):
        cases = [
            {"status": "completed"},
            {"status": "running", "last_stop_sequence": 1},
            {"status": "running", "codex_continuation": {**self.manifest()["codex_continuation"], "absolute_deadline": "2000-01-01T00:00:00+00:00"}},
            {"status": "running", "codex_continuation": {**self.manifest()["codex_continuation"], "stall_count": 3}},
            {"status": "running", "codex_continuation": {**self.manifest()["codex_continuation"], "calls_used": 8}},
        ]
        for fields in cases:
            with self.subTest(fields=fields):
                self._seed(); self.update(**fields)
                result = self.stop()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, "")

    def test_wrong_session_or_cwd_and_malformed_state_stop_truthfully(self):
        self.assertEqual(self.stop(session_id="wrong").stdout, "")
        self.assertEqual(self.stop(cwd=str(self.base / "wrong")).stdout, "")
        (self.runs / "run-one/run_manifest.json").write_text("{")
        malformed = self.stop()
        self.assertEqual(malformed.stdout, "")
        self.assertIn("continuation unavailable", malformed.stderr)

    def test_restart_reuses_physical_manifest_counters(self):
        one = self.stop(); self.assertEqual(json.loads(one.stdout)["decision"], "block")
        self.update(status="running")
        binding = self.manifest()["codex_continuation"]
        binding.update(progress_signature="p2", stall_count=1)
        rebound = subprocess.run([sys.executable, str(ADAPTER), "bind", "run-one"], env={**self.env, "PYTHONPATH": str(DEPLOY / "backend")}, input=json.dumps(binding), text=True, capture_output=True)
        self.assertEqual(rebound.returncode, 0, rebound.stderr)
        saved = self.manifest()["codex_continuation"]
        self.assertEqual((saved["calls_used"], saved["cost_used"], saved["callback_count"]), (3, 2.5, 1))


if __name__ == "__main__":
    unittest.main()
