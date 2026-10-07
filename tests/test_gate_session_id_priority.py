"""RED contract: aios_gate session-identity resolution must prefer SESSION_ID over THREAD_ID.

Bug class (audit 2026-10-07, AA-7): ``hooks/aios_gate.js`` and ``hooks/aios_gate.py``
enumerated the Codex env keys as ``CODEX_THREAD_ID`` BEFORE ``CODEX_SESSION_ID``,
so an explicit ``--load <skill>`` (with no session_id arg) picked
``CODEX_THREAD_ID`` while the hook payload (which arrives with ``session_id``
/ ``conversation_id``) used that field. State was written at one identity and
read at the other; the child session flipped RED until the operator passed
``--load <skill> "$CODEX_SESSION_ID"`` explicitly to align them. The fix:
SESSION_ID must win over THREAD_ID in the env fallback chain so loader and
hook agree by default -- one class fix at the identity seam, no new gate,
no operator approval.

Class scope (inv_23): both the JS and Python gates must share the SAME env
key order, so a future change cannot reintroduce the divergence. The
acceptance is automatic harness loading under the actual child session --
no friction, no extra `--load` arg, no deny/ask condition.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES = (
    ("node", str(ROOT / "hooks" / "aios_gate.js")),
    ("python3", str(ROOT / "hooks" / "aios_gate.py")),
)
SESSION_IDENTITY_KEYS = (
    "BACKS_BUILD_SESSION",
    "CLAUDE_CODE_SESSION_ID",
    "CODEX_THREAD_ID",
    "CURSOR_SESSION_ID",
    "CURSOR_CONVERSATION_ID",
    "OPENCODE_SESSION_ID",
    "CODEX_SESSION_ID",
    "CLAUDE_SESSION_ID",
)


class SessionIdPriorityTest(unittest.TestCase):
    """When BOTH CODEX_SESSION_ID and CODEX_THREAD_ID are set, SESSION_ID wins."""

    def setUp(self) -> None:
        self.home = tempfile.TemporaryDirectory()
        self.addCleanup(self.home.cleanup)

    def _scrubbed_env(self, **overrides: str) -> dict[str, str]:
        merged = os.environ.copy()
        for key in SESSION_IDENTITY_KEYS:
            merged.pop(key, None)
        merged.update({"HOME": self.home.name, **overrides})
        return merged

    def test_session_id_wins_when_both_codex_env_vars_set(self):
        """Both gates: CODEX_SESSION_ID must beat CODEX_THREAD_ID in the env chain."""
        # The gate writes its state file to ``~/.aios/state/`` (HOME-scoped).
        state_dir = Path(self.home.name) / ".aios" / "state"
        for gate in GATES:
            with self.subTest(gate=gate[1]):
                env = self._scrubbed_env(
                    CODEX_THREAD_ID="thread-should-NOT-win",
                    CODEX_SESSION_ID="session-MUST-win",
                )
                res = subprocess.run(
                    (*gate, "--load", "optimus"),
                    input="",
                    text=True,
                    capture_output=True,
                    env=env,
                    check=False,
                )
                self.assertEqual(
                    0, res.returncode,
                    f"{gate[1]} failed: stderr={res.stderr!r}",
                )
                expected_state = state_dir / "aios_floor_session-MUST-win.state"
                self.assertTrue(
                    expected_state.exists(),
                    f"{gate[1]}: state file {expected_state.name} missing -- "
                    f"loader picked the wrong identity. Files in state dir: "
                    f"{list(state_dir.glob('*.state')) if state_dir.exists() else 'dir missing'}",
                )
                forbidden_state = state_dir / "aios_floor_thread-should-NOT-win.state"
                self.assertFalse(
                    forbidden_state.exists(),
                    f"{gate[1]}: state file {forbidden_state.name} written -- "
                    f"loader picked THREAD_ID over SESSION_ID (the AA-7 bug).",
                )
                # Clean up between subtests so each gate writes to a fresh state dir.
                for p in (expected_state, forbidden_state):
                    p.unlink(missing_ok=True)

    def test_session_id_wins_under_claude_protocol(self):
        """Hook payload session_id matches the loader's SESSION_ID resolution.

        Live parent reproduction: a child Codex session sets BOTH env vars;
        the hook payload arrives with ``session_id`` (== SESSION_ID). After
        ``--load <skill>`` writes state at SESSION_ID, the PostToolUse hook
        must agree (empty stdout = armed = green) -- NOT deny (the AA-7 bug).
        """
        payload = {
            "session_id": "session-MUST-win",
            "hook_event_name": "PostToolUse",
            "tool_name": "Skill",
            "tool_input": {"name": "optimus"},
        }
        state_dir = Path(self.home.name) / ".aios" / "state"
        for gate in GATES:
            with self.subTest(gate=gate[1]):
                env = self._scrubbed_env(
                    CODEX_THREAD_ID="thread-should-NOT-win",
                    CODEX_SESSION_ID="session-MUST-win",
                )
                # Pre-write the state at the SESSION_ID identity (what the
                # loader SHOULD have written) so the hook sees green; if the
                # loader resolved to THREAD_ID instead, the hook would arrive
                # at SESSION_ID with no state and deny.
                state_dir.mkdir(parents=True, exist_ok=True)
                (state_dir / "aios_floor_session-MUST-win.state").write_text(
                    "armed", encoding="utf-8"
                )
                res = subprocess.run(
                    gate,
                    input=json.dumps(payload),
                    text=True,
                    capture_output=True,
                    env=env,
                    check=False,
                )
                self.assertEqual(
                    0, res.returncode,
                    f"{gate[1]} failed: stderr={res.stderr!r}",
                )
                self.assertEqual(
                    "",
                    res.stdout,
                    f"{gate[1]}: hook denied when env keys conflicted "
                    f"(the AA-7 bug). stderr={res.stderr!r}",
                )
                # Clean up state for the next subtest.
                (state_dir / "aios_floor_session-MUST-win.state").unlink(
                    missing_ok=True
                )


if __name__ == "__main__":
    unittest.main()