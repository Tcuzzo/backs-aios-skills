#!/usr/bin/env node
/* aios_gate — the pack's grounding gate, programmed instead of prompted.
 *
 * Behavior-identical Node port of aios_gate.py (same state files, same deny
 * JSON, same Bash mutating-verb pattern, same AIOS_GATE=off kill-switch, same
 * hook fail-open). Node >= 18, zero dependencies.
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
 *   - Read-only shell is NEVER blocked: Bash denies only on a positive match
 *     of a mutating verb at a command position (git commit/push, rm, mv/tee onto
 *     a tracked-looking path, sed -i, npm/pip/cargo install, systemctl/service
 *     restart, chmod/chown, > redirection outside /tmp). ls, cat, grep,
 *     git status/diff/log, and echo without redirection always pass.
 *   - Kill-switch: AIOS_GATE=off (also 0/false/no) disables the gate entirely.
 *     The capability defaults ON; the switch is loud, reversible, the only escape.
 *   - Fail-open ONLY in stdin hook-mode errors: a broken hook must never brick
 *     a session. Hook errors print one warning line to stderr and exit 0
 *     (no decision = allow). Explicit --load/--rearm errors are loud and exit
 *     nonzero.
 *
 * Load a skill explicitly to arm the session:
 *   node aios_gate.js --load backs-aios:<skill> [session_id]
 *   node aios_gate.js --load <skill> [session_id]
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
const crypto = require("crypto");

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
const CMD_POS = "(?:^|[;&|\r\n]|\\$\\(|`)\\s*(?:sudo\\s+)?";

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

const SAFE_TARGET_PREFIXES = ["/tmp/", "/dev/shm/"];

/** Blank out quoted segments so text inside quotes cannot false-match. */
function stripQuoted(command) {
  return command.replace(/'[^']*'|"[^"]*"/g, " ");
}

function isSafePath(token) {
  token = token.replace(/^['"]+|['"]+$/g, "");
  return (
    SAFE_TARGET_PREFIXES.some((p) => token.startsWith(p)) ||
    token === "/tmp" ||
    token === "/dev/shm" ||
    token === "/dev/null"
  );
}

function bashIsMutating(command) {
  const stripped = stripQuoted(command);
  for (const pattern of BASH_MUTATING) {
    if (pattern.test(stripped)) return true;
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

function stateComponent(raw) {
  const id = raw == null ? "" : String(raw);
  if (id && /^[A-Za-z0-9_.-]{1,80}$/.test(id)) {
    return id;
  }
  if (!id) return "unknown";
  const prefix = id
    .replace(/[^A-Za-z0-9_.-]/g, "_")
    .slice(0, 15);
  const hash = crypto
    .createHash("sha256")
    .update(id, "utf8")
    .digest("hex");
  return (prefix ? prefix + "_" : "") + hash;
}

function stateFile(sessionId) {
  return path.join(stateDir(), `aios_floor_${stateComponent(sessionId)}.state`);
}

function removeState(sessionId) {
  const p = stateFile(sessionId);
  if (fs.existsSync(p)) fs.unlinkSync(p);
}

function stateExists(sessionId) {
  return fs.existsSync(stateFile(sessionId));
}

/** Atomic marker writer shared by native Skill events and explicit --load. */
function writeFloorMarker(sessionId) {
  const target = stateFile(sessionId);
  const dir = path.dirname(target);
  fs.mkdirSync(dir, { recursive: true });
  const tmp = path.join(
    dir,
    `.tmp-${process.pid}-${Date.now()}-${Math.random().toString(36).slice(2)}`,
  );
  let fd = null;
  try {
    fd = fs.openSync(tmp, "wx", 0o600);
    const data = Buffer.from("floor loaded\n", "utf8");
    let offset = 0;
    while (offset < data.length) {
      const written = fs.writeSync(fd, data, offset, data.length - offset);
      if (written <= 0) {
        throw new Error("write made no progress");
      }
      offset += written;
    }
    fs.fsyncSync(fd);
    fs.closeSync(fd);
    fd = null;
    fs.renameSync(tmp, target);
  } catch (err) {
    if (fd !== null) {
      try { fs.closeSync(fd); } catch {}
    }
    try { fs.unlinkSync(tmp); } catch {}
    throw err;
  }
}

function resolveSkillPath(canonical) {
  const root = pluginRoot();
  const rootReal = fs.realpathSync(root);
  const candidate = path.join(root, "skills", canonical, "SKILL.md");
  const expected = path.join(rootReal, "skills", canonical, "SKILL.md");
  try {
    const real = fs.realpathSync(candidate);
    if (real !== expected) return null;
    const st = fs.statSync(real);
    if (st.isFile() && st.size > 0) return real;
  } catch {
    return null;
  }
  return null;
}

function sessionIdOf(payload, cliArg) {
  if (cliArg) return String(cliArg).trim();
  const fromPayload = String(payload.session_id || payload.conversation_id || "").trim();
  if (fromPayload) return fromPayload;
  const envKeys = [
    "BACKS_BUILD_SESSION",
    "CLAUDE_CODE_SESSION_ID",
    "CODEX_THREAD_ID",
    "CURSOR_SESSION_ID",
    "CURSOR_CONVERSATION_ID",
    "OPENCODE_SESSION_ID",
    "CODEX_SESSION_ID",
    "CLAUDE_SESSION_ID",
  ];
  for (const key of envKeys) {
    const val = String(process.env[key] || "").trim();
    if (val) return val;
  }
  return `ppid${process.ppid}`;
}

/** Enumerate real skill directories only.
 *
 * Returns a Set of names under skills/<name>/SKILL.md. Symlink redirects and
 * anything outside the real pack root are ignored. If the skills directory is
 * missing/unreadable or no real skills exist, throws so the caller leaves the
 * session RED and warns.
 */
function packSkillNames() {
  const names = new Set();
  const root = pluginRoot();
  const rootReal = fs.realpathSync(root);
  const skillsDir = path.join(root, "skills");
  if (!fs.existsSync(skillsDir) || !fs.statSync(skillsDir).isDirectory()) {
    throw new Error(`skill catalog missing: ${skillsDir}`);
  }
  for (const entry of fs.readdirSync(skillsDir)) {
    const skillDir = path.join(skillsDir, entry);
    let dirStat;
    try {
      dirStat = fs.statSync(skillDir);
    } catch {
      continue;
    }
    if (!dirStat.isDirectory()) continue;
    const candidate = path.join(root, "skills", entry, "SKILL.md");
    const expected = path.join(rootReal, "skills", entry, "SKILL.md");
    let real;
    try {
      real = fs.realpathSync(candidate);
    } catch {
      continue;
    }
    if (real !== expected) continue;
    const st = fs.statSync(real);
    if (st.isFile() && st.size > 0) names.add(entry);
  }
  if (names.size === 0) {
    throw new Error("skill catalog empty");
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

function evaluate(payload, options = {}) {
  const kill = String(process.env[KILL_ENV] || "").trim().toLowerCase();
  if (["off", "0", "false", "no"].includes(kill)) {
    if (options.emit !== false) {
      process.stderr.write("aios_gate: disabled by AIOS_GATE; allowing\n");
    }
    return { decision: "allow", reason: "disabled by AIOS_GATE" };
  }

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
    removeState(sessionId);
    return { decision: "allow" };
  }

  if (event === "PostToolUse" || event === "postToolUse") {
    if (toolName === "Skill") {
      const skill = invokedSkill(toolInput);
      if (skill) {
        let pack = null;
        try {
          pack = packSkillNames();
        } catch (err) {
          process.stderr.write(
            `aios_gate: WARNING skill catalog unreadable or empty, floor stays RED (${err.name}: ${err.message})\n`,
          );
        }
        if (pack && pack.has(skill)) {
          writeFloorMarker(sessionId);
        }
      }
    }
    return { decision: "allow" };
  }

  if (event === "PreToolUse" || event === "preToolUse") {
    const red = !stateExists(sessionId);
    if (toolName === "Bash" || toolName === "Shell") {
      if (red && bashIsMutating(String(toolInput.command || ""))) {
        if (options.emit !== false) deny(cursorProtocol);
        return { decision: "deny", reason: DENY_MESSAGE };
      }
      return { decision: "allow" };
    }
    if (!MUTATING_TOOLS.has(toolName)) {
      return { decision: "allow" };
    }
    if (!red) {
      return { decision: "allow" };
    }
    if (options.emit !== false) deny(cursorProtocol);
    return { decision: "deny", reason: DENY_MESSAGE };
  }

  return { decision: "allow" };
}

function load(argv) {
  try {
    if (argv.length < 1) {
      process.stderr.write("aios_gate: skill not found\n");
      return 2;
    }
    const skillArg = argv[0];
    let canonical;
    if (skillArg.includes(":")) {
      if (!skillArg.startsWith("backs-aios:")) {
        process.stderr.write("aios_gate: skill not found\n");
        return 2;
      }
      canonical = skillArg.slice("backs-aios:".length);
    } else {
      canonical = skillArg;
    }
    if (!canonical || !/^[a-z0-9]+(-[a-z0-9]+)*$/.test(canonical)) {
      process.stderr.write("aios_gate: skill not found\n");
      return 2;
    }
    const resolved = resolveSkillPath(canonical);
    if (!resolved) {
      process.stderr.write("aios_gate: skill not found\n");
      return 2;
    }
    const body = fs.readFileSync(resolved, "utf8");
    const sessionId = sessionIdOf({}, argv[1]);
    writeFloorMarker(sessionId);
    process.stdout.write(body);
    return 0;
  } catch (err) {
    process.stderr.write(`aios_gate: load failed (${err.name}: ${err.message})\n`);
    return 1;
  }
}

function rearm(argv) {
  try {
    const sid = sessionIdOf({}, argv[0]);
    const p = stateFile(sid);
    if (fs.existsSync(p)) {
      fs.unlinkSync(p);
      console.log("aios_gate: re-armed");
    } else {
      console.log("aios_gate: already armed");
    }
    return 0;
  } catch (err) {
    process.stderr.write(`aios_gate: re-arm failed (${err.name}: ${err.message})\n`);
    return 1;
  }
}

function runStdinHook() {
  const raw = fs.readFileSync(0, "utf8");
  const payload = JSON.parse(raw || "{}");
  if (typeof payload !== "object" || payload === null || Array.isArray(payload)) {
    throw new TypeError("hook payload is not a JSON object");
  }
  evaluate(payload, { emit: true });
  return 0;
}

function main() {
  const argv = process.argv.slice(2);
  if (argv.length > 0 && (argv[0] === "--load" || argv[0] === "load")) {
    return load(argv.slice(1));
  }
  if (argv.length > 0 && argv[0] === "--rearm") {
    return rearm(argv.slice(1));
  }
  return runStdinHook();
}

module.exports = { evaluate, DENY_MESSAGE };
if (require.main === module) {
  const argv = process.argv.slice(2);
  const isExplicitCommand = argv.length > 0 && ["--load", "load", "--rearm"].includes(argv[0]);
  try {
    process.exit(main());
  } catch (exc) {
    const name = exc && exc.constructor ? exc.constructor.name : "Error";
    const msg = exc && exc.message !== undefined ? exc.message : String(exc);
    if (isExplicitCommand) {
      process.stderr.write(`aios_gate: command failed (${name}: ${msg})\n`);
      process.exit(1);
    }
    process.stderr.write(
      `aios_gate: WARNING gate error, allowing (${name}: ${msg})\n`,
    );
    process.exit(0);
  }
}
