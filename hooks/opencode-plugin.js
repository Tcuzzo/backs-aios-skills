import { createRequire } from "node:module";
import path from "node:path";
import os from "node:os";

const warned = new Set();

function warnOnce(key, message) {
  if (!warned.has(key)) {
    warned.add(key);
    console.warn(message);
  }
}

const runtimeRoot = process.env.BACKS_AIOS_RUNTIME_ROOT;
const gatePath = runtimeRoot
  ? path.join(path.resolve(runtimeRoot), "hooks", "aios_gate.js")
  : path.join(
      os.homedir(),
      ".local",
      "share",
      "backs-aios",
      "current",
      "hooks",
      "aios_gate.js",
    );

let evaluate;
let DENY_MESSAGE;
let gateAvailable = false;
let unavailableReason = "load failed";

try {
  const require = createRequire(import.meta.url);
  const gate = require(gatePath);
  if (
    typeof gate?.evaluate === "function" &&
    typeof gate?.DENY_MESSAGE === "string" &&
    gate.DENY_MESSAGE.length > 0
  ) {
    evaluate = gate.evaluate;
    DENY_MESSAGE = gate.DENY_MESSAGE;
    gateAvailable = true;
  } else {
    unavailableReason = "invalid gate shape";
  }
} catch (err) {
  unavailableReason = err?.code || err?.name || "Error";
}

function warnUnavailable(key) {
  warnOnce(key, `aios-plugin: gate unavailable (${unavailableReason}); allowing`);
}

const TRANSLATIONS = {
  bash: "Bash",
  shell: "Bash",
  edit: "Edit",
  write: "Write",
  applypatch: "MultiEdit",
  multiedit: "MultiEdit",
  notebookedit: "NotebookEdit",
  delete: "Delete",
};

function translateToolName(raw) {
  const key = String(raw || "")
    .toLowerCase()
    .replace(/[-_]/g, "");
  return TRANSLATIONS[key] || String(raw || "");
}

function handleDisabled(result) {
  if (result?.reason === "disabled by AIOS_GATE") {
    warnOnce(
      "disabled",
      "aios-plugin: AIOS_GATE=off; gate disabled, allowing",
    );
    return true;
  }
  return false;
}

async function toolExecuteBefore(input, output) {
  if (!gateAvailable) {
    warnUnavailable("unavailable");
    return;
  }

  const sessionID = input?.sessionID;
  if (!sessionID) {
    warnOnce("no-session-before", "aios-plugin: missing sessionID; allowing");
    return;
  }

  const toolName = translateToolName(input?.tool);
  const args = output?.args ?? {};

  let result;
  try {
    result = await evaluate(
      {
        session_id: sessionID,
        hook_event_name: "PreToolUse",
        tool_name: toolName,
        tool_input: args,
      },
      { emit: false },
    );
  } catch (err) {
    const bounded = err?.code || err?.name || "Error";
    warnOnce(
      "evaluate-before",
      `aios-plugin: before hook failed (${bounded}); allowing`,
    );
    return;
  }

  if (handleDisabled(result)) return;
  if (result?.decision === "deny") {
    throw new Error(DENY_MESSAGE);
  }
}

async function toolExecuteAfter(input, output) {
  if (!gateAvailable) {
    warnUnavailable("unavailable");
    return;
  }

  const name = input?.args?.name;
  if (input?.tool !== "skill" || !name) return;

  const sessionID = input?.sessionID;
  if (!sessionID) {
    warnOnce("no-session-after", "aios-plugin: missing sessionID; allowing");
    return;
  }

  let result;
  try {
    result = await evaluate(
      {
        session_id: sessionID,
        hook_event_name: "PostToolUse",
        tool_name: "Skill",
        tool_input: { name },
      },
      { emit: false },
    );
  } catch (err) {
    const bounded = err?.code || err?.name || "Error";
    warnOnce(
      "evaluate-after",
      `aios-plugin: after hook failed (${bounded}); allowing`,
    );
    return;
  }

  handleDisabled(result);
}

export default async function aiosOpenCodePlugin() {
  return {
    "tool.execute.before": toolExecuteBefore,
    "tool.execute.after": toolExecuteAfter,
  };
}
