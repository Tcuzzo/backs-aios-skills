from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST_TEMP = ROOT / "sandbox" / "hook-tests"
GATES = (
    ("node", str(ROOT / "hooks" / "aios_gate.js")),
    (sys.executable, str(ROOT / "hooks" / "aios_gate.py")),
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


class GateCompatibilityTest(unittest.TestCase):
    def setUp(self) -> None:
        TEST_TEMP.mkdir(parents=True, exist_ok=True)
        self.home = tempfile.TemporaryDirectory(dir=TEST_TEMP)
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
        # The gate resolves the session identity from the host's own variables in a
        # declared order; a test run from inside a live agent session inherits that
        # host's id (e.g. CLAUDE_CODE_SESSION_ID) and the state file lands under it
        # instead of the id the test declares. Scrub every identity source so only
        # the test's own **env wins — the gate under test is unchanged.
        for key in SESSION_IDENTITY_KEYS:
            merged_env.pop(key, None)
        merged_env.update({"HOME": self.home.name, "USERPROFILE": self.home.name, "BACKS_DEPLOY_ROOT": str(Path(self.home.name)/"missing-deploy"), "AIOS_GATE": "on", **env})
        return subprocess.run(
            (*gate, *arguments),
            input=value,
            text=True,
            capture_output=True,
            env=merged_env,
            check=False,
        )

    def assert_grounding_delivered(self, result: subprocess.CompletedProcess, protocol: str) -> None:
        self.assertEqual(0, result.returncode, result.stderr)
        output = json.loads(result.stdout)
        if protocol == "claude":
            self.assertNotIn("permissionDecision", output["hookSpecificOutput"])
            self.assertIn("## BACKS loaded: optimus", output["hookSpecificOutput"]["additionalContext"])
        else:
            self.assertNotIn("permission", output)
            self.assertIn("## BACKS loaded: optimus", output["additional_context"])

    def test_claude_and_cursor_protocols_load_grounding_then_allow(self) -> None:
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
                    self.assert_grounding_delivered(denied, protocol)

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

    def test_cursor_write_loads_missing_grounding(self) -> None:
        for gate in GATES:
            with self.subTest(gate=gate[1]):
                result = self.run_gate(gate, {
                    "conversation_id": f"cursor-write-{Path(gate[1]).suffix}",
                    "cursor_version": "3.17",
                    "hook_event_name": "preToolUse",
                    "tool_name": "Write",
                    "tool_input": {"path": "file.txt"},
                })
                self.assert_grounding_delivered(result, "cursor")

    def test_codex_patch_surfaces_load_grounding_then_allow(self) -> None:
        """Drive the real CLI evaluators with Codex's direct and nested payloads."""
        mutations = (
            ("apply_patch", "*** Begin Patch\n*** Update File: example.txt"),
            ("functions.apply_patch", "*** Begin Patch\n*** Update File: example.txt"),
            (
                "functions.exec",
                "await tools.apply_patch(\"*** Begin Patch\\n*** Update File: example.txt\")",
            ),
        )
        for gate in GATES:
            suffix = Path(gate[1]).suffix.lstrip(".")
            for index, (tool_name, tool_input) in enumerate(mutations):
                with self.subTest(gate=gate[1], tool_name=tool_name):
                    session = f"codex-patch-{suffix}-{index}"
                    payload = {
                        "session_id": session,
                        "hook_event_name": "PreToolUse",
                        "tool_name": tool_name,
                        "tool_input": tool_input,
                    }
                    self.assert_grounding_delivered(self.run_gate(gate, payload), "claude")

                    loaded = self.run_gate(
                        gate,
                        "",
                        "--load",
                        "backs-aios:optimus",
                        CODEX_SESSION_ID=session,
                    )
                    self.assertEqual(0, loaded.returncode, loaded.stderr)
                    self.assertEqual("", self.run_gate(gate, payload).stdout)

    def test_hook_registration_covers_codex_patch_surfaces(self) -> None:
        manifest = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        matchers = {
            entry["matcher"]
            for entry in manifest["hooks"]["PreToolUse"]
        }
        registered = set().union(*(set(matcher.split("|")) for matcher in matchers))
        self.assertTrue(
            {"apply_patch", "functions.apply_patch", "functions.exec"} <= registered
        )

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

    def test_session_start_delivers_floor_bodies_and_wake_pointers(self) -> None:
        for gate in GATES:
            with self.subTest(gate=gate[1]):
                result = self.run_gate(gate, {
                    "conversation_id": f"compact-{Path(gate[1]).suffix.lstrip('.')}",
                    "cursor_version": "3.17",
                    "hook_event_name": "sessionStart",
                })
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("## BACKS loaded: optimus", result.stdout)
                output = json.loads(result.stdout)
                context = output["additional_context"]
                self.assertIn("operator_intent_deduction", context)
                self.assertIn("context_engineer", context)
                self.assertNotIn("## WAKE_SKILL", context)
                self.assertNotIn("# Operator Intent Deduction", context)

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
                self.assert_grounding_delivered(denied, "claude")

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
                self.assert_grounding_delivered(self.run_gate(gate, payload), "claude")

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
                "USERPROFILE": self.home.name,
                "BACKS_AIOS_RUNTIME_ROOT": str(ROOT),
                "BACKS_DEPLOY_ROOT": str(Path(self.home.name)/"missing-deploy"),
                "AIOS_GATE": "on",
            },
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({"denied": False, "allowed": True}, json.loads(result.stdout))
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
