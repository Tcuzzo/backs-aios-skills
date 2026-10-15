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
let gateAvailable = false;
let unavailableReason = "load failed";

try {
  const require = createRequire(import.meta.url);
  const gate = require(gatePath);
  if (
    typeof gate?.evaluate === "function"
  ) {
    evaluate = gate.evaluate;
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
  // Grounding is delivered through the host context hook, never tool refusal.
}

async function systemTransform(input, output) {
  if (!gateAvailable) {
    warnUnavailable("unavailable-context");
    return;
  }
  if (!Array.isArray(output?.system)) return;
  try {
    const result = await evaluate(
      {session_id: input?.sessionID, hook_event_name: "SessionStart"},
      {emit: false, deliverContext(context) {
        // The host retains this array. Merge into its leading system block.
        if (output.system.length) output.system[0] += "\n\n" + context;
        else output.system.push(context);
      }},
    );
    handleDisabled(result);
  } catch (err) {
    warnOnce("context", `aios-plugin: grounding unavailable (${err?.name || "Error"}); allowing`);
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
    "experimental.chat.system.transform": systemTransform,
    "tool.execute.before": toolExecuteBefore,
    "tool.execute.after": toolExecuteAfter,
  };
}
