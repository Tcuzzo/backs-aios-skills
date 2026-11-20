"use strict";
/* RED follow-ups to the once-per-session contract, from the blind grade of 2026-11-19.
 *
 * The skip must never stop grounding from reaching a session that needs it:
 * 1. A host that delivers through its own callback (the OpenCode adapter merges
 *    the floor into a per-request system block) must get the content on every
 *    call. Only a hook that prints its output may skip.
 * 2. "--rearm <session>" requests another load: the next session event delivers.
 * 3. A session start whose source is anything but "startup" (resume, fork,
 *    compact, clear) delivers again: nothing proves an injected block survives
 *    into a restored transcript.
 * Real files and real hook processes only. Nothing is mocked.
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
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "aios-once-more-"));
  const home = path.join(root, "home");
  const deploy = path.join(root, "deploy");
  fs.mkdirSync(home, {recursive: true});
  for (const [rel, text] of [
    ["backend/prompts/BACKS_CODEX_HARNESS.md", "# harness body\n"],
    ["skills/optimus/SKILL.md", "# optimus body\n"],
    ["skills/human-calibration/SKILL.md", "# calibration body\n"],
    ["skills/backs-build-flow/SKILL.md", "# build flow body\n"],
  ]) {
    const file = path.join(deploy, rel);
    fs.mkdirSync(path.dirname(file), {recursive: true});
    fs.writeFileSync(file, text);
  }
  const env = {...process.env, HOME: home, BACKS_DEPLOY_ROOT: deploy};
  delete env.AIOS_GATE;
  delete env.BACKS_AI_ROOT;
  return {root, env};
}

function hookPath(rt) {
  return path.join(ROOT, "hooks", RUNTIMES[rt].file);
}

function fire(f, rt, event, session, extra = {}) {
  const result = spawnSync(RUNTIMES[rt].cmd, [hookPath(rt)], {
    env: f.env, input: JSON.stringify({hook_event_name: event, session_id: session, ...extra}),
  });
  assert.equal(result.status, 0, result.stderr.toString());
  return result.stdout.toString().split(MARK).length - 1;
}

test("a host delivery callback gets the content on every call in one session", t => {
  const f = fixture();
  t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
  const script = `
    const {evaluate} = require(${JSON.stringify(hookPath("js"))});
    let calls = 0;
    for (let i = 0; i < 3; i++) {
      evaluate({session_id: "s-host", hook_event_name: "SessionStart"},
        {emit: false, deliverContext(context) { if (context.includes(${JSON.stringify(MARK)})) calls++; }});
    }
    process.stdout.write(String(calls));`;
  const result = spawnSync(process.execPath, ["-e", script], {env: f.env});
  assert.equal(result.status, 0, result.stderr.toString());
  assert.equal(result.stdout.toString(), "3", "a per-request host lost the grounding after the first call");
});

for (const rt of Object.keys(RUNTIMES)) {
  test(`${rt}: --rearm makes the next session event deliver again`, t => {
    const f = fixture();
    t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
    assert.equal(fire(f, rt, "SessionStart", "s-rearm", {source: "startup"}), 1);
    const rearm = spawnSync(RUNTIMES[rt].cmd, [hookPath(rt), "--rearm", "s-rearm"], {env: f.env});
    assert.equal(rearm.status, 0, rearm.stderr.toString());
    assert.equal(fire(f, rt, "UserPromptSubmit", "s-rearm", {prompt: "go"}), 1,
      "--rearm requested another load, but nothing was delivered");
  });

  test(`${rt}: a resumed or forked session start delivers again`, t => {
    const f = fixture();
    t.after(() => fs.rmSync(f.root, {recursive: true, force: true}));
    assert.equal(fire(f, rt, "SessionStart", "s-resume", {source: "startup"}), 1);
    for (const source of ["resume", "fork"]) {
      assert.equal(fire(f, rt, "SessionStart", "s-resume", {source}), 1,
        `source ${source}: nothing proves the earlier block survived`);
    }
    assert.equal(fire(f, rt, "UserPromptSubmit", "s-resume", {prompt: "go"}), 0,
      "a plain user turn after delivery must still send nothing");
  });
}
