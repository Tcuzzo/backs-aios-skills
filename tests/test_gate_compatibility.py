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

    def run_gate(
        self,
        gate: tuple[str, str],
        payload: dict | str,
        *arguments: str,
        **env: str,
    ) -> subprocess.CompletedProcess:
        value = payload if isinstance(payload, str) else json.dumps(payload)
        merged_env = os.environ.copy()
        merged_env.update({"HOME": self.home.name, **env})
        return subprocess.run(
            (*gate, *arguments),
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

    def test_codex_loads_real_skill_and_rearm_uses_environment_session(self) -> None:
        for gate in GATES:
            with self.subTest(gate=gate[1]):
                session = f"codex-load-{Path(gate[1]).suffix.lstrip('.')}"
                payload = {
                    "session_id": session,
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Bash",
                    "tool_input": {"command": "git commit -m test"},
                }
                denied = self.run_gate(gate, payload)
                self.assert_denied(denied, "claude")

                loaded = self.run_gate(
                    gate,
                    "",
                    "--load",
                    "backs-aios:optimus",
                    CODEX_SESSION_ID=session,
                )
                self.assertEqual(0, loaded.returncode, loaded.stderr)
                self.assertIn("# Harness Boot", loaded.stdout)
                state = (
                    Path(self.home.name)
                    / ".aios"
                    / "state"
                    / f"aios_floor_{session}.state"
                )
                self.assertTrue(state.is_file())
                self.assertGreater(state.stat().st_size, 0)
                self.assertEqual([], list(state.parent.glob("*.tmp-*")))

                allowed = self.run_gate(gate, payload)
                self.assertEqual("", allowed.stdout)

                rearmed = self.run_gate(
                    gate,
                    "",
                    "--rearm",
                    CODEX_SESSION_ID=session,
                )
                self.assertEqual(0, rearmed.returncode, rearmed.stderr)
                self.assertIn("re-armed", rearmed.stdout)
                self.assertFalse(state.exists())
                self.assert_denied(self.run_gate(gate, payload), "claude")

    def test_unknown_skill_cannot_arm_environment_session(self) -> None:
        for gate in GATES:
            with self.subTest(gate=gate[1]):
                session = f"codex-unknown-{Path(gate[1]).suffix.lstrip('.')}"
                result = self.run_gate(
                    gate,
                    "",
                    "--load",
                    "backs-aios:not-a-real-skill",
                    CODEX_SESSION_ID=session,
                )
                self.assertEqual(2, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertIn("not found", result.stderr.lower())
                state = (
                    Path(self.home.name)
                    / ".aios"
                    / "state"
                    / f"aios_floor_{session}.state"
                )
                self.assertFalse(state.exists())

    def test_opencode_native_skill_event_arms_the_same_gate(self) -> None:
        plugin = ROOT / "hooks" / "opencode-plugin.js"
        script = f"""
import plugin from {json.dumps(plugin.as_uri())};
const hooks = await plugin({{}});
const before = hooks["tool.execute.before"];
const after = hooks["tool.execute.after"];
let denied = false;
try {{
  await before(
    {{tool: "bash", sessionID: "opencode-1", callID: "call-red"}},
    {{args: {{command: "git commit -m test"}}}},
  );
}} catch (error) {{
  denied = String(error.message || error).includes("Load the floor first");
}}
await after(
  {{
    tool: "skill",
    sessionID: "opencode-1",
    callID: "call-skill",
    args: {{name: "optimus"}},
  }},
  {{title: "optimus", output: "loaded", metadata: {{}}}},
);
let allowed = true;
try {{
  await before(
    {{tool: "bash", sessionID: "opencode-1", callID: "call-green"}},
    {{args: {{command: "git commit -m test"}}}},
  );
}} catch {{
  allowed = false;
}}
console.log(JSON.stringify({{denied, allowed}}));
"""
        result = subprocess.run(
            ("node", "--input-type=module", "--eval", script),
            text=True,
            capture_output=True,
            env={
                **os.environ,
                "HOME": self.home.name,
                "BACKS_AIOS_RUNTIME_ROOT": str(ROOT),
            },
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({"denied": True, "allowed": True}, json.loads(result.stdout))
        state = (
            Path(self.home.name)
            / ".aios"
            / "state"
            / "aios_floor_opencode-1.state"
        )
        self.assertTrue(state.is_file())
        self.assertGreater(state.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
