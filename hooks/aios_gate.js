#!/usr/bin/env node
/* aios_gate — the pack's grounding gate, programmed instead of prompted.
 *
 * Behavior-identical Node port of aios_gate.py (same state files, same deny
 * JSON, same Bash mutating-verb pattern, same AIOS_GATE=off kill-switch, same
 * fail-open). Node >= 18, zero dependencies.
 *
 * Every session starts RED. While RED, the file-edit tools (Edit, Write,
 * NotebookEdit, MultiEdit) are denied, and Bash is denied ONLY when its command
 * matches a conservative mutating-verb pattern — until a pack skill has been
 * invoked this session. Invoking any pack skill (PostToolUse on the Skill tool)
 * flips the session GREEN.
 *
 * Rules this script holds structurally:
 *   - Read-only tools are NEVER touched (the hooks.json matcher scopes to
 *     mutators, and this script re-checks the tool name as a second belt).
 *   - Read-only shell is NEVER blocked: Bash denies only on a positive match of
 *     a mutating verb at a command position (git commit/push, rm, mv/tee onto a
 *     tracked-looking path, sed -i, npm/pip/cargo install, systemctl/service
 *     restart, chmod/chown, > redirection outside /tmp). ls, cat, grep,
 *     git status/diff/log, and echo without redirection always pass.
 *   - Kill-switch: AIOS_GATE=off (also 0/false/no) disables the gate entirely.
 *     The capability defaults ON; the switch is loud, reversible, the only escape.
 *   - Fail-open on ANY script error: a broken gate must never brick a session.
 *     Errors print one warning line to stderr and exit 0 (no decision = allow).
 *
 * Re-arm for a new job in the same session:
 *   node aios_gate.js --rearm [session_id]     (falls back to parent PID)
 *
 * State lives in ~/.aios/state/ (falls back to the system temp dir if that
 * is not writable).
 */

"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");

const KILL_ENV = "AIOS_GATE";
const MUTATING_TOOLS = new Set([
  "Delete",
  "Edit",
  "MultiEdit",
  "NotebookEdit",
  "Write",
]);
const DENY_MESSAGE =
  "Load the floor first — run /optimus. Set AIOS_GATE=off to disable.";

// A verb counts only at a command position: line start, after ; & |, or inside
// a substitution. "grep rm" or "echo 'rm x'" can never match.
const CMD_POS = "(?:^|[;&|]|\\$\\(|`)\\s*(?:sudo\\s+)?";

// Conservative mutating-verb patterns for Bash. Deny fires ONLY on a positive
// match; everything unmatched — all read-only shell — passes untouched.
const BASH_MUTATING = [
  CMD_POS + "git\\s+(?:-\\S+\\s+)*(?:commit|push)\\b",
  CMD_POS + "rm\\s",
  CMD_POS + "sed\\s+(?:-\\S+\\s+)*-i",
  CMD_POS + "(?:npm|pip3?|cargo)\\s+(?:-\\S+\\s+)*install\\b",
  CMD_POS + "systemctl\\s+(?:-\\S+\\s+)*restart\\b",
  CMD_POS + "service\\s+\\S+\\s+restart\\b",
  CMD_POS + "chmod\\s",
  CMD_POS + "chown\\s",
].map((p) => new RegExp(p));

const SAFE_TARGET_PREFIXES = ["/tmp/", "/dev/null", "/dev/shm"];

/** Blank out quoted segments so text inside quotes cannot false-match. */
function stripQuoted(command) {
  return command.replace(/'[^']*'|"[^"]*"/g, " ");
}

function isSafePath(token) {
  token = token.replace(/^['"]+|['"]+$/g, "");
  return (
    SAFE_TARGET_PREFIXES.some((p) => token.startsWith(p)) ||
    token === "/tmp" ||
    token === "/dev/null"
  );
}

function bashIsMutating(command) {
  for (const pattern of BASH_MUTATING) {
    if (pattern.test(command)) return true;
  }
  // mv / tee: mutating only when a target looks tracked (outside /tmp, /dev).
  const mvTee = new RegExp(CMD_POS + "(?:mv|tee)\\s+([^;|&]*)", "g");
  for (const m of command.matchAll(mvTee)) {
    const args = m[1].split(/\s+/).filter((a) => a && !a.startsWith("-"));
    if (args.some((a) => !isSafePath(a))) return true;
  }
  // > redirection into a non-/tmp path (fd redirects like 2>&1 never match;
  // quoted text is stripped first so `awk '$1 > 5'` cannot false-match).
  for (const m of stripQuoted(command).matchAll(/>>?\s*([^\s;|&<>]+)/g)) {
    if (!isSafePath(m[1])) return true;
  }
  return false;
}

function pluginRoot() {
  return path.dirname(path.dirname(path.resolve(__filename)));
}

function stateDir() {
  const preferred = path.join(os.homedir(), ".aios", "state");
  try {
    fs.mkdirSync(preferred, { recursive: true });
    return preferred;
  } catch {
    return os.tmpdir();
  }
}

function stateFile(sessionId) {
  const safe =
    String(sessionId).replace(/[^A-Za-z0-9_.-]/g, "_").slice(0, 80) ||
    "unknown";
  return path.join(stateDir(), `aios_floor_${safe}.state`);
}

function sessionIdOf(payload) {
  const sid = String(payload.session_id || payload.conversation_id || "").trim();
  return sid || `ppid${process.ppid}`;
}

/** Names that count as 'the floor': skills/<dir>/SKILL.md + commands/*.md.
 *
 * Fail-open: if the pack layout cannot be read, return an empty set and let
 * the caller treat ANY skill invocation as grounding.
 */
function packSkillNames() {
  const names = new Set();
  const root = pluginRoot();
  try {
    const skillsDir = path.join(root, "skills");
    if (fs.existsSync(skillsDir) && fs.statSync(skillsDir).isDirectory()) {
      for (const entry of fs.readdirSync(skillsDir)) {
        const skillFile = path.join(skillsDir, entry, "SKILL.md");
        if (fs.existsSync(skillFile) && fs.statSync(skillFile).isFile()) {
          names.add(entry);
        }
      }
    }
    const commandsDir = path.join(root, "commands");
    if (fs.existsSync(commandsDir) && fs.statSync(commandsDir).isDirectory()) {
      for (const entry of fs.readdirSync(commandsDir)) {
        if (entry.endsWith(".md")) names.add(entry.slice(0, -3));
      }
    }
  } catch {
    return new Set();
  }
  return names;
}

function invokedSkill(toolInput) {
  const raw = String(toolInput.skill || toolInput.name || "").trim();
  // Plugin skills arrive namespaced ("backs-aios:optimus"); keep the last part.
  return raw.slice(raw.lastIndexOf(":") + 1);
}

function deny(cursorProtocol) {
  if (cursorProtocol) {
    process.stdout.write(
      JSON.stringify({
        permission: "deny",
        user_message: DENY_MESSAGE,
        agent_message: DENY_MESSAGE,
      }) + "\n",
    );
    return;
  }
  // Byte-identical to the Python gate's json.dumps output (ensure_ascii,
  // ", " / ": " separators) so both runtimes emit the same deny line.
  const reason = JSON.stringify(DENY_MESSAGE).replace(
    /[\u0080-\uffff]/g,
    (c) => "\\u" + c.charCodeAt(0).toString(16).padStart(4, "0"),
  );
  process.stdout.write(
    '{"hookSpecificOutput": {"hookEventName": "PreToolUse", ' +
      '"permissionDecision": "deny", ' +
      `"permissionDecisionReason": ${reason}}}\n`,
  );
}

function handle(payload) {
  const event = String(payload.hook_event_name || "");
  const toolName = String(payload.tool_name || "");
  const cursorProtocol =
    event === "sessionStart" ||
    event === "preToolUse" ||
    event === "postToolUse" ||
    Boolean(payload.cursor_version);
  let toolInput = payload.tool_input || {};
  if (typeof toolInput !== "object" || toolInput === null || Array.isArray(toolInput)) {
    toolInput = {};
  }
  const sessionId = sessionIdOf(payload);

  if (event === "SessionStart" || event === "sessionStart") {
    const p = stateFile(sessionId);
    if (fs.existsSync(p)) fs.unlinkSync(p);
    return;
  }

  if (event === "PostToolUse" || event === "postToolUse") {
    if (toolName === "Skill") {
      const skill = invokedSkill(toolInput);
      const pack = packSkillNames();
      if (skill && (pack.size === 0 || pack.has(skill))) {
        fs.writeFileSync(stateFile(sessionId), "floor loaded\n", "utf8");
      }
    }
    return;
  }

  if (event === "PreToolUse" || event === "preToolUse") {
    const red = !fs.existsSync(stateFile(sessionId));
    if (toolName === "Bash" || toolName === "Shell") {
      if (red && bashIsMutating(String(toolInput.command || ""))) {
        deny(cursorProtocol);
      }
      return; // read-only shell always passes, red or green
    }
    if (!MUTATING_TOOLS.has(toolName)) {
      return; // read-only and unknown tools always pass
    }
    if (!red) {
      return; // floor loaded this session: allow
    }
    deny(cursorProtocol);
    return;
  }
  // Any other event: no decision.
}

function rearm(argv) {
  const sid = argv.length ? argv[0] : `ppid${process.ppid}`;
  const p = stateFile(sid);
  if (fs.existsSync(p)) {
    fs.unlinkSync(p);
    console.log(`aios_gate: re-armed (removed ${p})`);
  } else {
    console.log(`aios_gate: already armed (no state at ${p})`);
  }
}

function main() {
  const argv = process.argv.slice(2);
  if (argv.length > 0 && argv[0] === "--rearm") {
    rearm(argv.slice(1));
    return 0;
  }
  const kill = String(process.env[KILL_ENV] || "").trim().toLowerCase();
  if (["off", "0", "false", "no"].includes(kill)) {
    process.stderr.write("aios_gate: disabled by AIOS_GATE; allowing\n");
    return 0; // kill-switch: gate disabled, everything passes
  }
  const raw = fs.readFileSync(0, "utf8");
  const payload = JSON.parse(raw || "{}");
  if (typeof payload !== "object" || payload === null || Array.isArray(payload)) {
    throw new TypeError("hook payload is not a JSON object");
  }
  handle(payload);
  return 0;
}

try {
  process.exit(main());
} catch (exc) {
  // fail-open, loudly: never brick a session
  const name = exc && exc.constructor ? exc.constructor.name : "Error";
  const msg = exc && exc.message !== undefined ? exc.message : String(exc);
  process.stderr.write(
    `aios_gate: WARNING gate error, allowing (${name}: ${msg})\n`,
  );
  process.exit(0);
}
