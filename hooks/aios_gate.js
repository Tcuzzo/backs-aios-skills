#!/usr/bin/env node
/* BACKS grounding loader. Session start delivers the actual Optimus/Yoke bodies
 * and the deployed harness when present. Missing grounding triggers loading,
 * never tool refusal. Context delivery and explicit Skill evidence are separate.
 * AIOS_GATE=off remains the operator's existing kill switch. Hook failures warn
 * and allow; explicit --load failures return a nonzero status.
 */

"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");
const crypto = require("crypto");
const childProcess = require("child_process");

const KILL_ENV = "AIOS_GATE";
const MUTATING_TOOLS = new Set([
  "Delete",
  "Edit",
  "MultiEdit",
  "NotebookEdit",
  "Write",
  // Codex exposes its patch primitive both directly and under its function namespace.
  "apply_patch",
  "functions.apply_patch",
]);
const CODEX_EXEC_TOOL = "functions.exec";
const CODEX_PATCH_CALL = /\b(?:tools|functions)\s*\.\s*apply_patch\s*\(/;
// Retained export for older installed adapters; evaluate never returns deny.
const DENY_MESSAGE = "BACKS grounding loads automatically; tools remain available.";

// A verb counts only at a command position: line start, after ; & |, or inside
// a substitution. "grep rm" or "echo 'rm x'" can never match.
const CMD_POS = "(?:^|[;&|\r\n]|\\$\\(|`)\\s*(?:sudo\\s+)?";

// Conservative mutating-verb patterns for Bash. Loading runs only on a positive
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

function canonicalManifestPath() {
  const root = deployRoot();
  return root ? path.join(root, "config/foundation_manifest.json") : "";
}
function hasCanonicalManifest() {
  const filename = canonicalManifestPath();
  return Boolean(filename && fs.existsSync(filename));
}
function canonicalReceiptValid(sessionId) {
  try {
    const root = fs.realpathSync(deployRoot());
    foundationManifestBodies(root);
    const rows = JSON.parse(fs.readFileSync(canonicalManifestPath(), "utf8")).bodies;
    const key = crypto.createHash("sha256").update(String(sessionId)).digest("hex");
    const receipt = JSON.parse(fs.readFileSync(path.join(os.homedir(), ".claude/state", `backs_load_${key}.json`), "utf8"));
    return receiptMatches(receipt, sessionId, root, rows);
  } catch { return false; }
}
function receiptMatches(receipt, sessionId, root, rows) {
  const expectedHashes = Object.fromEntries(rows.map(row => [row.path, row.sha256]));
  return receipt.kind === "foundation_delivery" &&
    receipt.session_id === sessionId && receipt.source_root === root &&
    receipt.expires_at > Date.now() / 1000 &&
    JSON.stringify(receipt.order) === JSON.stringify(rows.map(row => row.path)) &&
    JSON.stringify(receipt.sha256) === JSON.stringify(expectedHashes);
}
function stateExists(sessionId) {
  return hasCanonicalManifest() ? canonicalReceiptValid(sessionId) : fs.existsSync(stateFile(sessionId));
}


/** CO-readable grounding evidence (shared seam with conscientious_objector).
 * Smoking gun fix: also write ~/.claude/state/backs_ground_<sid>.state + .hashes.json
 * while keeping the existing ~/.aios/state/aios_floor_*.state marker.
 */
function coStateDir() {
  const preferred = path.join(os.homedir(), ".claude", "state");
  try {
    fs.mkdirSync(preferred, { recursive: true });
    return preferred;
  } catch {
    return os.tmpdir();
  }
}

function writeCoGroundingEvidence(sessionId, skillDigests) {
  const sid = stateComponent(sessionId);
  const dir = coStateDir();
  const statePath = path.join(dir, `backs_ground_${sid}.state`);
  const hashPath = path.join(dir, `backs_ground_${sid}.hashes.json`);
  const tmpState = path.join(dir, `.tmp-state-${process.pid}-${Date.now()}`);
  const tmpHash = path.join(dir, `.tmp-hash-${process.pid}-${Date.now()}`);
  let fd = null;
  try {
    fd = fs.openSync(tmpState, "wx", 0o600);
    fs.writeSync(fd, Buffer.from("true\n", "utf8"));
    fs.fsyncSync(fd);
    fs.closeSync(fd);
    fd = null;
    fs.renameSync(tmpState, statePath);
  } catch (err) {
    if (fd !== null) { try { fs.closeSync(fd); } catch {} }
    try { fs.unlinkSync(tmpState); } catch {}
    throw err;
  }
  const digests = skillDigests && typeof skillDigests === "object" ? skillDigests : {};
  const keys = Object.keys(digests).sort();
  const ordered = {};
  for (const k of keys) ordered[k] = digests[k];
  const payload = Buffer.from(JSON.stringify(ordered), "utf8");
  fd = null;
  try {
    fd = fs.openSync(tmpHash, "wx", 0o600);
    fs.writeSync(fd, payload);
    fs.fsyncSync(fd);
    fs.closeSync(fd);
    fd = null;
    fs.renameSync(tmpHash, hashPath);
  } catch (err) {
    if (fd !== null) { try { fs.closeSync(fd); } catch {} }
    try { fs.unlinkSync(tmpHash); } catch {}
    throw err;
  }
  return { statePath, hashPath };
}

function deployRoot() {
  const env = String(process.env.BACKS_DEPLOY_ROOT || process.env.BACKS_AI_ROOT || "").trim();
  if (env) return env;
  for (const host of [".codex", ".claude"]) {
    try {
      const skill = fs.realpathSync(path.join(os.homedir(), host, "skills/optimus/SKILL.md"));
      const candidate = path.dirname(path.dirname(path.dirname(skill)));
      if (fs.statSync(path.join(candidate, "backend/prompts/BACKS_CODEX_HARNESS.md")).isFile()) return candidate;
    } catch {}
  }
  return "";
}

function resolveNativeOrPackSkill(canonical) {
  const aliases = {
    yoke: ["human-calibration", "yoke"],
    "human-calibration": ["human-calibration", "yoke"],
    optimus: ["optimus"],
    "context-engineer": ["context-engineer", "context_engineer", "context-compiler"],
    context_engineer: ["context-engineer", "context_engineer", "context-compiler"],
    "context-compiler": ["context-engineer", "context_engineer", "context-compiler"],
    "operator-intent-deduction": ["operator-intent-deduction", "operator_intent_deduction"],
    operator_intent_deduction: ["operator-intent-deduction", "operator_intent_deduction"],
    "conscientious-objector": ["conscientious_objector", "conscientious-objector"],
    conscientious_objector: ["conscientious_objector", "conscientious-objector"],
  };
  const names = aliases[canonical] || [canonical];
  const root = deployRoot();
  if (root) {
    for (const name of names) {
      const p = path.join(root, "skills", name, "SKILL.md");
      try {
        if (fs.existsSync(p) && fs.statSync(p).isFile() && fs.statSync(p).size > 0) {
          return { path: p, canonical: name, source: "deploy_native" };
        }
      } catch {}
    }
  }
  for (const name of names) {
    const p = resolveSkillPath(name);
    if (p) return { path: p, canonical: name, source: "installed_pack" };
  }
  return null;
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
  // Audit 2026-10-07 AA-7: a child Codex session sets BOTH CODEX_SESSION_ID
// and CODEX_THREAD_ID. The hook payload arrives with session_id (== SESSION_ID);
// the explicit --load falls back to env. If the loader picks THREAD_ID while
// the hook reads SESSION_ID, state lands at one identity and is read at the
// other -- the child session flips RED. The documented invocation
// ``--load <skill> "$CODEX_SESSION_ID"`` aligned them manually; the fix is to
// align the env chain itself: SESSION_ID wins over THREAD_ID by default. Same
// env-key order as hooks/aios_gate.py so a future change cannot reintroduce
// the divergence. Class scope (inv_23): one identity seam, no new hook, no
// operator approval friction.
  const envKeys = [
    "BACKS_BUILD_SESSION",
    "CLAUDE_CODE_SESSION_ID",
    "CODEX_SESSION_ID",
    "CURSOR_SESSION_ID",
    "CURSOR_CONVERSATION_ID",
    "OPENCODE_SESSION_ID",
    "CODEX_THREAD_ID",
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
 * session without a new receipt and warns.
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

/** True only for Codex's real nested patch call inside functions.exec.
 *
 * The exec transport may carry its source as a freeform string or in one of
 * the documented code/script/input fields. We leave every other exec payload
 * alone so automatic loading stays scoped to the existing mutation matcher.
 */
function codexExecInvokesPatch(toolName, rawToolInput) {
  if (toolName !== CODEX_EXEC_TOOL) return false;
  const sources = [];
  if (typeof rawToolInput === "string") {
    sources.push(rawToolInput);
  } else if (rawToolInput && typeof rawToolInput === "object" && !Array.isArray(rawToolInput)) {
    for (const key of ["code", "script", "input"]) {
      if (typeof rawToolInput[key] === "string") sources.push(rawToolInput[key]);
    }
  }
  return sources.some((source) => CODEX_PATCH_CALL.test(source));
}

function wakeLoadContext() {
  return (
    "BACKS wake-load: invoke operator-intent-deduction before handing the " +
    "operator a decision, and invoke context-engineer when compiling task " +
    "context. Legacy compatibility: operator_intent_deduction resolves to " +
    "operator-intent-deduction; context-compiler is a context_engineer alias, " +
    "and both resolve to context-engineer. intent-compiler is a separate skill. " +
    "Build Flow owns the current task packet; reuse current evidence " +
    "and apply operator-essence when operator context is needed. " +
    "Load skill bodies through the skill runtime only when needed."
  );
}

/** Reading a pointer is not delivery. Record only bodies handed to the host. */
function readBody(entry) {
  const body = fs.readFileSync(entry.path, "utf8");
  if (!body.trim()) throw new Error(`${entry.canonical} unavailable`);
  return {...entry, body, sha256: crypto.createHash("sha256").update(body).digest("hex")};
}

function foundationBodies() {
  return ["optimus", "yoke", "backs-build-flow"].map((name) => {
    const resolved = resolveNativeOrPackSkill(name);
    if (!resolved) throw new Error(`${name} unavailable`);
    return readBody(resolved);
  });
}

function floorContext() {
  if (hasCanonicalManifest()) {
    foundationManifestBodies(deployRoot());
    const rows = JSON.parse(fs.readFileSync(canonicalManifestPath(), "utf8")).bodies;
    const context = "=== BACKS FOUNDATION (pinned; not yet delivered whole this session) ===\n" +
      "Load every file below in full. Only actual host-observed complete output can certify delivery; a skill marker or stdout success cannot.\n" +
      rows.map((row, index) => `${index + 1}. ${path.join(deployRoot(), row.path)} sha256:${row.sha256}`).join("\n");
    if (Buffer.byteLength(context) > 10000) throw new Error("foundation pointer exceeds measured host limit");
    return {context, bodies: [], pending: true};
  }
  const bodies = [];
  const root = deployRoot();
  if (root && fs.existsSync(path.join(root, "backend/prompts/BACKS_CODEX_HARNESS.md"))) {
    bodies.push(readBody({path: path.join(root, "backend/prompts/BACKS_CODEX_HARNESS.md"), canonical: "harness", source: "deploy_native"}));
  }
  bodies.push(...foundationBodies());
  return {context: wakeLoadContext() + "\n\n" + bodies.map(x => `## BACKS loaded: ${x.canonical}\n${x.body}`).join("\n\n"), bodies};
}

function foundationManifestBodies(root) {
  const manifestPath = root && path.join(root, "config", "foundation_manifest.json");
  if (!manifestPath || !fs.existsSync(manifestPath) || !fs.statSync(manifestPath).isFile()) return null;
  const rootReal = fs.realpathSync(root);
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  if (!Array.isArray(manifest.bodies) || manifest.bodies.length === 0) throw new Error("foundation manifest bodies missing");
  return Buffer.concat(manifest.bodies.flatMap(row => [foundationBody(rootReal, row), Buffer.from("\n\n")]));
}
function foundationRelative(row) {
  const relative = row && row.path;
  if (typeof relative !== "string" || !relative || path.isAbsolute(relative) || relative.includes("\\") || relative.split("/").some(p => !p || p === "." || p === "..")) {
    throw new Error(`unsafe foundation path: ${String(relative)}`);
  }
  return relative;
}
function foundationBody(rootReal, row) {
  const relative = foundationRelative(row);
  const target = fs.realpathSync(path.join(rootReal, ...relative.split("/")));
  if (target !== rootReal && !target.startsWith(rootReal + path.sep)) throw new Error(`foundation path escapes deployment: ${relative}`);
  if (!fs.statSync(target).isFile()) throw new Error(`foundation body unavailable: ${relative}`);
  const body = fs.readFileSync(target);
  const expected = row.sha256;
  const actual = crypto.createHash("sha256").update(body).digest("hex");
  if (typeof expected !== "string" || !/^[0-9a-f]{64}$/.test(expected) || actual !== expected) throw new Error(`foundation hash mismatch: ${relative}`);
  return body;
}

// A shape capture is observation only: it never certifies context delivery.
const CODEX_SENTINEL = "printf '%s\\n' BACKS_CODEX_HOOK_SENTINEL_V1";
function shapeOf(value, depth = 0) {
  if (typeof value === "string") return {type: "string", bytes: Buffer.byteLength(value), sha256: crypto.createHash("sha256").update(value.slice(0, 262144)).digest("hex")};
  if (value === null || typeof value !== "object") return {type: value === null ? "null" : typeof value};
  if (depth >= 3) return {type: Array.isArray(value) ? "array" : "object"};
  if (Array.isArray(value)) return {type: "array", length: value.length, items: value.slice(0, 8).map(v => shapeOf(v, depth + 1))};
  const safe = new Set(["output", "stdout", "stderr", "content", "text", "type", "exit_code", "session_id"]);
  return Object.fromEntries(Object.keys(value).slice(0, 16).map((k, i) => [safe.has(k) ? k : `field_${i}`, shapeOf(value[k], depth + 1)]));
}
function observeCodexTool(payload) {
  if (payload.tool_name !== "Bash" || payload.tool_input?.command !== CODEX_SENTINEL || !payload.turn_id || !payload.tool_use_id || !payload.session_id) return;
  const hash = value => crypto.createHash("sha256").update(String(value)).digest("hex");
  const target = path.join(stateDir(), `codex_tool_shape_${hash(payload.session_id)}.json`);
  const evidence = {kind: "tool_payload_shape", session_sha256: hash(payload.session_id), turn_sha256: hash(payload.turn_id), call_sha256: hash(payload.tool_use_id), command_sha256: hash(CODEX_SENTINEL), observed_at: Date.now() / 1000, tool_response: shapeOf(payload.tool_response)};
  try { fs.writeFileSync(target, JSON.stringify(evidence), {flag: "wx", mode: 0o600}); }
  catch (error) { if (error.code !== "EEXIST") process.stderr.write(`BACKS observer unavailable: ${error.code}\n`); }
}

function deliverFloor(cursorProtocol, sessionId, event, options = {}) {
  try {
    const floor = floorContext();
    if (typeof options.deliverContext === "function") {
      options.deliverContext(floor.context);
    } else if (options.emit !== false) {
      const output = cursorProtocol ? {additional_context: floor.context} : {
        hookSpecificOutput: {hookEventName: event, additionalContext: floor.context},
      };
      const data = Buffer.from(JSON.stringify(output) + "\n");
      let offset = 0;
      while (offset < data.length) offset += fs.writeSync(1, data, offset);
    } else {
      return {decision: "allow", additionalContext: floor.context, delivered: false};
    }
    if (floor.pending) return {decision: "allow", delivered: false};
    const receipt = {session_id: sessionId, kind: "context_delivery", bodies: floor.bodies.map(({body, ...entry}) => entry)};
    const target = stateFile(sessionId) + ".load.json";
    const tmp = target + `.${process.pid}.${crypto.randomBytes(6).toString("hex")}.tmp`;
    try {
      fs.writeFileSync(tmp, JSON.stringify(receipt), {mode: 0o600, flag: "wx"});
      fs.renameSync(tmp, target);
    } finally {
      try { fs.unlinkSync(tmp); } catch {}
    }
    writeFloorMarker(sessionId);
    return {decision: "allow", delivered: true};
  } catch (err) {
    process.stderr.write(`aios_gate: grounding unavailable (${err.name}: ${err.message}); allowing\n`);
    return {decision: "allow", delivered: false};
  }
}

function evaluate(payload, options = {}) {
  const kill = String(process.env[KILL_ENV] || "").trim().toLowerCase();
  if (["off", "0", "false", "no"].includes(kill)) return disabledDecision(options);

  return routeEvent(payload, options);
}
function routeEvent(payload, options) {
  const event = String(payload.hook_event_name || "");
  const toolName = String(payload.tool_name || "");
  const cursorProtocol = ["sessionStart", "preToolUse", "postToolUse"].includes(event) || Boolean(payload.cursor_version);
  const rawToolInput = payload.tool_input;
  const toolInput = rawToolInput && typeof rawToolInput === "object" && !Array.isArray(rawToolInput) ? rawToolInput : {};
  const sessionId = sessionIdOf(payload);
  if (event === "Stop") return evaluateStop(payload);
  if (isSessionEvent(event)) {
    return deliverFloor(cursorProtocol, sessionId, event, options);
  }
  if (isPostEvent(event)) return evaluatePost(payload, toolName, toolInput, sessionId);
  if (isPreEvent(event)) return evaluatePre(toolName, toolInput, rawToolInput, sessionId, cursorProtocol, event, options);

  return { decision: "allow" };
}
function evaluateStop(payload) {
  const adapter = path.join(pluginRoot(), "hooks", "codex_stop_continuation.py");
  const root = deployRoot();
  if (!root || !fs.existsSync(adapter)) {
    process.stderr.write("BACKS continuation unavailable: deployed owner or adapter missing\n");
    return {decision: "allow"};
  }
  const result = childProcess.spawnSync(process.env.PYTHON || "python3", [adapter, "stop"], {
    input: JSON.stringify(payload), encoding: "utf8", timeout: 30000, killSignal: "SIGKILL",
    env: {...process.env, BACKS_DEPLOY_ROOT: root, PYTHONPATH: path.join(root, "backend")},
  });
  if (result.stderr) process.stderr.write(result.stderr);
  if (result.error) {
    process.stderr.write(`BACKS continuation unavailable: adapter did not finish (${result.error.code || result.error.message})\n`);
    return {decision: "allow"};
  }
  if (result.status !== 0 || !result.stdout.trim()) return {decision: "allow"};
  try {
    const decision = JSON.parse(result.stdout);
    const data = Buffer.from(JSON.stringify(decision) + "\n");
    let offset = 0;
    while (offset < data.length) offset += fs.writeSync(1, data, offset);
    return decision;
  } catch (error) {
    process.stderr.write(`BACKS continuation unavailable: malformed adapter output (${error.message})\n`);
    return {decision: "allow"};
  }
}
function isSessionEvent(event) {
  return ["SessionStart", "sessionStart", "UserPromptSubmit"].includes(event);
}
function isPostEvent(event) {
  return event === "PostToolUse" || event === "postToolUse";
}
function isPreEvent(event) {
  return event === "PreToolUse" || event === "preToolUse";
}
function disabledDecision(options) {
  if (options.emit !== false) process.stderr.write("aios_gate: disabled by AIOS_GATE; allowing\n");
  return {decision: "allow", reason: "disabled by AIOS_GATE"};
}
function evaluatePost(payload, toolName, toolInput, sessionId) {
  observeCodexTool(payload);
  if (toolName !== "Skill") return {decision: "allow"};
  const skill = invokedSkill(toolInput);
  if (!skill) return {decision: "allow"};
  let pack;
  try { pack = packSkillNames(); }
  catch (err) {
    process.stderr.write(`aios_gate: WARNING skill catalog unreadable or empty, grounding evidence unavailable (${err.name}: ${err.message})\n`);
    return {decision: "allow"};
  }
  if (pack.has(skill)) recordSkillEvidence(skill, sessionId);
  return {decision: "allow"};
}
function recordSkillEvidence(skill, sessionId) {
  writeFloorMarker(sessionId);
  try {
    const digests = {};
    const resolved = resolveNativeOrPackSkill(skill);
    if (resolved) digests[resolved.canonical] = crypto.createHash("sha256").update(fs.readFileSync(resolved.path)).digest("hex");
    writeCoGroundingEvidence(sessionId, digests);
  } catch (err) { process.stderr.write(`aios_gate: WARNING CO evidence write failed (${err.message})\n`); }
}
function evaluatePre(toolName, toolInput, rawToolInput, sessionId, cursorProtocol, event, options) {
  const red = !stateExists(sessionId);
  if (["Bash", "Shell"].includes(toolName)) {
    return red && bashIsMutating(String(toolInput.command || ""))
      ? deliverFloor(cursorProtocol, sessionId, event, options) : {decision: "allow"};
  }
  const mutating = MUTATING_TOOLS.has(toolName) || codexExecInvokesPatch(toolName, rawToolInput);
  return red && mutating ? deliverFloor(cursorProtocol, sessionId, event, options) : {decision: "allow"};
}

function load(argv) {
  try {
    const canonical = canonicalSkillArg(argv[0]);
    if (!canonical) return skillNotFound();
    const resolvedInfo = resolvedSkillOrNull(canonical);
    if (!resolvedInfo) return skillNotFound();
    if (canonical === "optimus") {
      const manifestBody = foundationManifestBodies(deployRoot());
      if (manifestBody !== null) return writeAll(manifestBody);
    }
    return loadPortable(canonical, resolvedInfo, argv[1]);
  } catch (err) {
    process.stderr.write(`aios_gate: load failed (${err.name}: ${err.message})\n`);
    return 1;
  }
}
function loadPortable(canonical, resolvedInfo, sessionArg) {
    const bodies = resolvedInfo.canonical === "optimus" || canonical === "optimus"
      ? foundationBodies() : [readBody(resolvedInfo)];
    const body = bodies.map(entry => entry.body).join("\n\n");
    const sessionId = sessionIdOf({}, sessionArg);
    const digests = Object.fromEntries(bodies.map(entry => [entry.canonical, entry.sha256]));
    const data = Buffer.from(body);
    writeAll(data);
    writeFloorMarker(sessionId);
    const invocationPath = path.join(coStateDir(), `backs_ground_${stateComponent(sessionId)}.hashes.json`);
    const temporary = invocationPath + `.${process.pid}.tmp`;
    try {
      fs.writeFileSync(temporary, JSON.stringify(digests), {mode: 0o600, flag: "wx"});
      fs.renameSync(temporary, invocationPath);
    } finally { try { fs.unlinkSync(temporary); } catch {} }
    return 0;
}
function resolvedSkillOrNull(canonical) {
  return resolveNativeOrPackSkill(canonical);
}
function writeAll(data) {
  let offset = 0;
  while (offset < data.length) offset += fs.writeSync(1, data, offset);
  return 0;
}
function canonicalSkillArg(skillArg) {
  if (!skillArg) return null;
  if (skillArg.includes(":")) {
    if (!skillArg.startsWith("backs-aios:")) return null;
    skillArg = skillArg.slice("backs-aios:".length);
  }
  return /^[a-z0-9]+([_-][a-z0-9]+)*$/.test(skillArg) ? skillArg : null;
}
function skillNotFound() {
  process.stderr.write("aios_gate: skill not found\n");
  return 2;
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
