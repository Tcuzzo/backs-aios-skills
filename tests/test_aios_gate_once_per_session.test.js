"use strict";
/* RED contract: the grounding bodies reach a session ONCE, not once per hook event.
 *
 * Live failure (2026-11-19): a fleet Codex job's first turn carried the same
 * 28,827-character "BACKS wake-load" block twice (identical text, same turn):
 * once from SessionStart and again from UserPromptSubmit. Both events run the
 * gate hook, and its floor delivery wrote a delivery receipt for the session
 * but never read it before sending the bodies again. A second copy of the
 * plugin (two installs) doubles it again, because every install reads the same
 * ~/.aios/state.
 *
 * Wanted: when this session already received exactly this content (same
 * content hash), a later SessionStart or UserPromptSubmit sends nothing and
 * writes ONE stderr line saying so. New content, a new session, or a SessionStart
 * that replaced the history (source "compact" or "clear") sends it again.
 *
 * Both shipped runtimes (hooks/aios_gate.js and its twin hooks/aios_gate.py)
 * carry the same flaw and must both pass, including a JS install and a Python
 * install sharing one session. Real files only: separate plugin install
 * folders, a real deploy tree with real skill bodies, one shared HOME. Nothing
 * is mocked.
 */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const {spawnSync} = require("node:child_process");

const ROOT = path.resolve(__dirname, "..");
const RUNTIMES = {
  js: {file: "aios_gate.js", cmd: process.execPath},
  py: {file: "aios_gate.py", cmd: "python3"},
};
const MARK = "## BACKS loaded: harness";

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "aios-once-"));
  const home = path.join(root, "home");
  const deploy = path.join(root, "deploy");
  fs.mkdirSync(home, {recursive: true});
  const write = (rel, text) => {
    const file = path.join(deploy, rel);
    fs.mkdirSync(path.dirname(file), {recursive: true});
    fs.writeFileSync(file, text);
  };
  // No config/foundation_manifest.json: this is the full-bodies path that doubled live.
  write("backend/prompts/BACKS_CODEX_HARNESS.md", "# harness body\n");
  write("skills/optimus/SKILL.md", "# optimus body\n");
  write("skills/human-calibration/SKILL.md", "# calibration body\n");
  write("skills/backs-build-flow/SKILL.md", "# build flow body\n");
  const install = (name, runtime) => {
    const hook = path.join(root, name, "hooks", RUNTIMES[runtime].file);
    fs.mkdirSync(path.dirname(hook), {recursive: true});
    fs.copyFileSync(path.join(ROOT, "hooks", RUNTIMES[runtime].file), hook);
    return {hook, cmd: RUNTIMES[runtime].cmd};
  };
  return {root, home, deploy, install};
}

function fire(f, inst, event, session, extra = {}) {
  const env = {...process.env, HOME: f.home, BACKS_DEPLOY_ROOT: f.deploy};
  delete env.AIOS_GATE;
  delete env.BACKS_AI_ROOT;
  const result = spawnSync(inst.cmd, [inst.hook], {
    env, input: JSON.stringify({hook_event_name: event, session_id: session, ...extra}),
  });
  assert.equal(result.status, 0, result.stderr.toString());
  return {stdout: result.stdout.toString(), stderr: result.stderr.toString()};
}

function delivered(out) {
  return out.stdout.split(MARK).length - 1;
}

for (const rt of Object.keys(RUNTIMES)) {
  test(`${rt}: session start delivers, the next user turn sends nothing and says so once`, t => {
    const f = fixture();
    t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
    const a = f.install("install-a", rt);
    const first = fire(f, a, "SessionStart", "s-one", {source: "startup"});
    assert.equal(delivered(first), 1, "session start must deliver the bodies");
    const second = fire(f, a, "UserPromptSubmit", "s-one", {prompt: "go"});
    assert.equal(second.stdout, "", "the same content was sent twice in one session");
    const lines = second.stderr.split("\n").filter(Boolean);
    assert.equal(lines.length, 1, `want exactly one log line, got: ${JSON.stringify(lines)}`);
    assert.match(lines[0], /already delivered/i);
  });

  test(`${rt}: two installs fire both events, the grounding is delivered once in total`, t => {
    const f = fixture();
    t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
    const a = f.install("install-a", rt);
    const b = f.install("install-b", rt);
    const outs = [
      fire(f, a, "SessionStart", "s-two", {source: "startup"}),
      fire(f, b, "SessionStart", "s-two", {source: "startup"}),
      fire(f, b, "UserPromptSubmit", "s-two", {prompt: "go"}),
      fire(f, a, "UserPromptSubmit", "s-two", {prompt: "go"}),
    ];
    assert.equal(outs.reduce((n, o) => n + delivered(o), 0), 1,
      outs.map(o => delivered(o)).join(","));
  });

  test(`${rt}: changed content is delivered again in the same session`, t => {
    const f = fixture();
    t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
    const a = f.install("install-a", rt);
    fire(f, a, "SessionStart", "s-change", {source: "startup"});
    fs.writeFileSync(path.join(f.deploy, "skills/optimus/SKILL.md"), "# optimus body v2\n");
    const again = fire(f, a, "UserPromptSubmit", "s-change", {prompt: "go"});
    assert.equal(delivered(again), 1, "a new body hash must be delivered");
    assert.match(again.stdout, /optimus body v2/);
  });

  test(`${rt}: a different session gets its own delivery`, t => {
    const f = fixture();
    t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
    fire(f, f.install("install-a", rt), "SessionStart", "s-first", {source: "startup"});
    const other = fire(f, f.install("install-b", rt), "SessionStart", "s-second", {source: "startup"});
    assert.equal(delivered(other), 1);
  });

  test(`${rt}: a session start that replaced the history delivers again`, t => {
    const f = fixture();
    t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
    const a = f.install("install-a", rt);
    fire(f, a, "SessionStart", "s-compact", {source: "startup"});
    for (const source of ["compact", "clear"]) {
      const out = fire(f, a, "SessionStart", "s-compact", {source});
      assert.equal(delivered(out), 1, `source ${source} lost the history; it must be re-sent`);
    }
  });
}

test("a JS install and a Python install share one session: delivered once in total", t => {
  const f = fixture();
  t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
  const js = f.install("install-js", "js");
  const py = f.install("install-py", "py");
  const outs = [
    fire(f, js, "SessionStart", "s-mixed", {source: "startup"}),
    fire(f, py, "SessionStart", "s-mixed", {source: "startup"}),
    fire(f, py, "UserPromptSubmit", "s-mixed", {prompt: "go"}),
    fire(f, js, "UserPromptSubmit", "s-mixed", {prompt: "go"}),
  ];
  assert.equal(outs.reduce((n, o) => n + delivered(o), 0), 1,
    outs.map(o => delivered(o)).join(","));
});
