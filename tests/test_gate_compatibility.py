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


class GateCompatibilityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.home = tempfile.TemporaryDirectory()
        self.addCleanup(self.home.cleanup)

    def run_gate(self, gate: tuple[str, str], payload: dict | str, **env: str) -> subprocess.CompletedProcess:
        value = payload if isinstance(payload, str) else json.dumps(payload)
        merged_env = os.environ.copy()
        merged_env.update({"HOME": self.home.name, **env})
        return subprocess.run(
            gate,
            input=value,
            text=True,
            capture_output=True,
            env=merged_env,
            check=False,
        )

    def assert_denied(self, result: subprocess.CompletedProcess, protocol: str) -> None:
        self.assertEqual(0, result.returncode, result.stderr)
        output = json.loads(result.stdout)
        if protocol == "claude":
            self.assertEqual("deny", output["hookSpecificOutput"]["permissionDecision"])
        else:
            self.assertEqual("deny", output["permission"])

    def test_claude_and_cursor_protocols_deny_red_then_allow_green(self) -> None:
        for gate in GATES:
            for protocol, session, pre_event, post_event, shell_name in (
                ("claude", "claude-1", "PreToolUse", "PostToolUse", "Bash"),
                ("cursor", "cursor-1", "preToolUse", "postToolUse", "Shell"),
            ):
                with self.subTest(gate=gate[1], protocol=protocol):
                    session = f"{session}-{Path(gate[1]).suffix.lstrip('.')}"
                    session_fields = (
                        {"session_id": session}
                        if protocol == "claude"
                        else {"conversation_id": session, "cursor_version": "3.17"}
                    )
                    denied = self.run_gate(gate, {
                        **session_fields,
                        "hook_event_name": pre_event,
                        "tool_name": shell_name,
                        "tool_input": {"command": "git commit -m test"},
                    })
                    self.assert_denied(denied, protocol)

                    armed = self.run_gate(gate, {
                        **session_fields,
                        "hook_event_name": post_event,
                        "tool_name": "Skill",
                        "tool_input": {"name": "optimus"},
                    })
                    self.assertEqual("", armed.stdout)

                    allowed = self.run_gate(gate, {
                        **session_fields,
                        "hook_event_name": pre_event,
                        "tool_name": shell_name,
                        "tool_input": {"command": "git commit -m test"},
                    })
                    self.assertEqual("", allowed.stdout)

    def test_cursor_write_is_denied_while_red(self) -> None:
        for gate in GATES:
            with self.subTest(gate=gate[1]):
                result = self.run_gate(gate, {
                    "conversation_id": "cursor-write",
                    "cursor_version": "3.17",
                    "hook_event_name": "preToolUse",
                    "tool_name": "Write",
                    "tool_input": {"path": "file.txt"},
                })
                self.assert_denied(result, "cursor")

    def test_kill_switch_allows_loudly(self) -> None:
        for gate in GATES:
            with self.subTest(gate=gate[1]):
                result = self.run_gate(gate, {
                    "session_id": "disabled",
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "tool_input": {},
                }, AIOS_GATE="off")
                self.assertEqual(0, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertIn("disabled", result.stderr.lower())

    def test_malformed_input_fails_open_loudly(self) -> None:
        for gate in GATES:
            with self.subTest(gate=gate[1]):
                result = self.run_gate(gate, "not json")
                self.assertEqual(0, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertIn("warning", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
