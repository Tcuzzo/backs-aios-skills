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
    "CLAUDE_CODE_SESSION_ID", "CURSOR_SESSION_ID", "CURSOR_CONVERSATION_ID",
    "OPENCODE_SESSION_ID", "CODEX_SESSION_ID", "CLAUDE_SESSION_ID",
)


class SessionStartContractTest(unittest.TestCase):
    def run_gate(
        self, gate: tuple[str, str], home: str, payload: dict | str, *arguments: str,
        **env: str,
    ) -> subprocess.CompletedProcess:
        merged_env = os.environ.copy()
        for key in SESSION_IDENTITY_KEYS:
            merged_env.pop(key, None)
        merged_env.update({"HOME": home, **env})
        return subprocess.run(
            (*gate, *arguments),
            input=payload if isinstance(payload, str) else json.dumps(payload),
            text=True,
            capture_output=True,
            env=merged_env,
            check=False,
        )

    def test_claude_start_is_compact_accurate_and_rearms_red(self) -> None:
        for gate in GATES:
            with self.subTest(gate=gate[1]), tempfile.TemporaryDirectory() as home:
                session = f"claude-start-{Path(gate[1]).suffix.lstrip('.')}"
                loaded = self.run_gate(
                    gate, home, "", "--load", "backs-aios:optimus",
                    CODEX_SESSION_ID=session,
                )
                self.assertEqual(0, loaded.returncode, loaded.stderr)
                state = Path(home) / ".aios" / "state" / f"aios_floor_{session}.state"
                self.assertTrue(state.is_file())

                started = self.run_gate(gate, home, {
                    "session_id": session,
                    "hook_event_name": "SessionStart",
                })
                self.assertEqual(0, started.returncode, started.stderr)
                self.assertLessEqual(len(started.stdout.encode()), 2048)
                context = json.loads(started.stdout)["hookSpecificOutput"]["additionalContext"]
                self.assertIn("operator_intent_deduction", context)
                self.assertIn("context_engineer", context)
                self.assertIn("context-compiler is a context_engineer alias", context)
                self.assertIn("intent-compiler is a separate skill", context)
                self.assertNotIn("## WAKE_SKILL", context)
                self.assertFalse(state.exists())
                denied = self.run_gate(gate, home, {
                    "session_id": session,
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                })
                self.assertEqual(0, denied.returncode, denied.stderr)
                self.assertEqual(
                    "deny",
                    json.loads(denied.stdout)["hookSpecificOutput"]["permissionDecision"],
                )

    def test_alias_copies_stay_byte_identical(self) -> None:
        groups = (
            ("context-compiler", "context-engineer", "context_engineer"),
            ("operator-intent-deduction", "operator_intent_deduction"),
        )
        for group in groups:
            bodies = [(ROOT / "skills" / name / "SKILL.md").read_bytes() for name in group]
            self.assertTrue(all(body == bodies[0] for body in bodies[1:]), group)


if __name__ == "__main__":
    unittest.main()
