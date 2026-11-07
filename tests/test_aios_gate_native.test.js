"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const crypto = require("node:crypto");
const {spawnSync} = require("node:child_process");

const ROOT = path.resolve(__dirname, "..");
const HOOK = path.join(ROOT, "hooks/aios_gate.js");

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "aios-native-"));
  const home = path.join(root, "home");
  const deploy = path.join(root, "deploy");
  fs.mkdirSync(path.join(home, ".claude/state"), {recursive: true});
  fs.mkdirSync(path.join(deploy, "config"), {recursive: true});
  fs.mkdirSync(path.join(deploy, "body"));
  const body = Buffer.from("floor-body\n");
  fs.writeFileSync(path.join(deploy, "body/floor.md"), body);
  const row = {path: "body/floor.md", sha256: crypto.createHash("sha256").update(body).digest("hex")};
  fs.writeFileSync(path.join(deploy, "config/foundation_manifest.json"), JSON.stringify({bodies: [row]}));
  return {root, home, deploy, row};
}

function runHook(f, payload) {
  const env = {...process.env, HOME: f.home, BACKS_DEPLOY_ROOT: f.deploy};
  return spawnSync(process.execPath, [HOOK], {env, input: JSON.stringify(payload)});
}

function writeReceipt(f, session, changes = {}) {
  const receipt = {kind: "foundation_delivery", session_id: session,
    source_root: fs.realpathSync(f.deploy), order: [f.row.path],
    sha256: {[f.row.path]: f.row.sha256}, expires_at: Date.now() / 1000 + 60,
    ...changes};
  const key = crypto.createHash("sha256").update(session).digest("hex");
  fs.writeFileSync(path.join(f.home, ".claude/state", `backs_load_${key}.json`), JSON.stringify(receipt));
}

test("native JS validates whole manifest and never certifies stdout", t => {
  const f = fixture();
  t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
  const env = {...process.env, HOME: f.home, BACKS_DEPLOY_ROOT: f.deploy};
  const good = spawnSync(process.execPath, [HOOK, "--load", "optimus", "native-session"], {env});
  assert.equal(good.status, 0, good.stderr.toString());
  assert.deepEqual(good.stdout, Buffer.from("floor-body\n\n\n"));
  assert.equal(fs.existsSync(path.join(f.home, ".aios/state/aios_floor_native-session.state")), false);
  const manifest = path.join(f.deploy, "config/foundation_manifest.json");
  fs.writeFileSync(manifest, JSON.stringify({bodies: [{...f.row, sha256: "0".repeat(64)}]}));
  const stale = spawnSync(process.execPath, [HOOK, "--load", "optimus", "native-session"], {env});
  assert.notEqual(stale.status, 0);
  assert.equal(stale.stdout.length, 0);
});

test("native JS rejects path escape and refreshes canonical pointer", t => {
  const f = fixture();
  t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
  const env = {...process.env, HOME: f.home, BACKS_DEPLOY_ROOT: f.deploy};
  fs.writeFileSync(path.join(f.root, "outside.md"), "outside\n");
  const manifest = path.join(f.deploy, "config/foundation_manifest.json");
  fs.writeFileSync(manifest, JSON.stringify({bodies: [{path: "../outside.md", sha256: "0".repeat(64)}]}));
  const escaped = spawnSync(process.execPath, [HOOK, "--load", "optimus", "native-session"], {env});
  assert.notEqual(escaped.status, 0);
  assert.match(escaped.stderr.toString(), /unsafe foundation path/);
  fs.writeFileSync(manifest, JSON.stringify({bodies: [f.row]}));
  const payload = JSON.stringify({hook_event_name: "PreToolUse", tool_name: "Write", session_id: "native-session", tool_input: {}});
  const refresh = spawnSync(process.execPath, [HOOK], {env, input: payload});
  assert.equal(refresh.status, 0, refresh.stderr.toString());
  assert.match(JSON.parse(refresh.stdout).hookSpecificOutput.additionalContext, /BACKS FOUNDATION/);
});

test("native JS routes real session, valid receipt, and post-tool observation", t => {
  const f = fixture();
  t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
  const session = "native-session";
  const started = runHook(f, {hook_event_name: "SessionStart", session_id: session});
  assert.equal(started.status, 0, started.stderr.toString());
  assert.match(JSON.parse(started.stdout).hookSpecificOutput.additionalContext, /BACKS FOUNDATION/);

  writeReceipt(f, session);
  const allowed = runHook(f, {hook_event_name: "PreToolUse", tool_name: "Write",
    session_id: session, tool_input: {}});
  assert.equal(allowed.status, 0, allowed.stderr.toString());
  assert.equal(allowed.stdout.length, 0);

  const sentinel = "printf '%s\\n' BACKS_CODEX_HOOK_SENTINEL_V1";
  const observed = runHook(f, {hook_event_name: "PostToolUse", tool_name: "Bash",
    session_id: session, turn_id: "turn", tool_use_id: "call",
    tool_input: {command: sentinel}, tool_response: {stdout: "ok", exit_code: 0}});
  assert.equal(observed.status, 0, observed.stderr.toString());
  const state = path.join(f.home, ".aios/state");
  const shapes = fs.readdirSync(state).filter(name => name.startsWith("codex_tool_shape_"));
  assert.equal(shapes.length, 1);
  assert.equal(JSON.parse(fs.readFileSync(path.join(state, shapes[0]))).kind, "tool_payload_shape");
});

test("native JS refreshes expired and malformed canonical receipts", t => {
  const f = fixture();
  t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
  for (const changes of [{expires_at: 1}, {order: []}, {sha256: {}}]) {
    writeReceipt(f, "native-session", changes);
    const result = runHook(f, {hook_event_name: "preToolUse", tool_name: "Write",
      session_id: "native-session", tool_input: {}});
    assert.equal(result.status, 0, result.stderr.toString());
    assert.match(JSON.parse(result.stdout).additional_context, /BACKS FOUNDATION/);
  }
});
