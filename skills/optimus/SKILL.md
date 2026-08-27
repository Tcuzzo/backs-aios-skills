---
name: optimus
description: Use when starting any agent session, job, or loop — before writing any code. Harness-first boot: load the invariant floor and the skills the job needs, so the agent reads the rules before it works; includes the grounding-gate hook pattern that blocks mutating tools until the harness is loaded. Trigger words: optimus, harness-boot, harness first, load the harness, boot the floor, grounding gate, read the floor, no code without harness, session start, boot sequence.
license: MIT
---

# Harness Boot
**Effort:** light — one boot pass per session to load the floor and the job's skills, plus a deterministic hook that costs nothing to run. Removes: ungrounded edits — mutations made before the rules were read, and the redo that follows once they are.

One rule: **no code and no job until the harness is loaded.** The harness is the pack's
invariant floor plus the skills that cover this job. Every session, every runtime, every
time. Why: a rule an agent must remember fails exactly when the agent is busiest — so
loading the rules is the first act, and a hook makes it structural instead of advisory.

## When to run

At the start of every session, job, mission, and loop. Again after a context reset or a
handoff. Loading the harness once and coasting for a week is not loading the harness.

## The boot sequence

1. **Load the invariant floor.** Read [invariant-floor](../invariant-floor/SKILL.md)
   before touching anything. This is the floor the whole session stands on.
2. **Load the map for this job.** Name which files, which rules, and which pack skills
   govern this specific work. If you cannot name them, you are not ready to edit.
3. **Load the human profile** ([human-calibration](../human-calibration/SKILL.md)) when the
   job touches a human's taste, surface, or workflow.
4. **Invoke the skills the job needs — in real time, in this session.** A skill named
   but not invoked did not happen. Working "from memory of a skill" is not invoking it.
5. Only then: write code, run mutating commands, or change anything.

## The grounding-gate pattern

Make step 4 structural with a deterministic **pre-tool-use hook** — a small script your
agent runtime calls before every tool call:

- Every session starts **RED**.
- While RED, read-only tools (read, grep, search, fetch) always pass. The agent grounds
  itself freely.
- While RED, the hook **blocks mutating tools** (edit, write, delete) and primary
  mutating shell verbs (commit, push, rm, install, service restart, in-place edits).
- Invoking any harness skill **flips the session GREEN** (caught by a post-tool-use
  hook). Then the agent may act.
- **Re-arm:** state resets to RED at every session start. For long sessions, re-arm per
  job or per action so a stale GREEN never carries into ungrounded work.

Design rules for the hook itself:

- **Deterministic and free.** No model call, no network, no dependencies. State is one
  small file per session, written atomically.
- **It forces grounding, not a sandbox.** Match only primary mutating verbs; leave
  dual-use wrappers and copy tools alone so grounding commands cannot get trapped.
- **Fail open, but loud.** A crashed hook must never brick the session — and must never
  allow silently. Print the error where the human can see it.
- **Never trap a session.** Unknown session identity allows, with one loud warning line.
  A session that can never be flipped GREEN must never be blocked RED.
- **One human-owned kill-switch** (an env var), defaults ON, logs loudly when off. The
  gate binds agents, never the human. Never add a second gate.

Generic hook (pseudocode, ~25 lines):

```python
HARNESS_SKILLS = {"optimus", "repair-loop", "invariant-floor"}  # your pack set
MUTATING_TOOLS = {"Edit", "Write", "Delete"}
MUTATING_SHELL = r"^\s*(sudo\s+)?(git (commit|push|reset|checkout)|rm|pip install|" \
                 r"npm install|systemctl (restart|stop)|sed .*-i)"

def handle(event, session_id, tool, args):
    if kill_switch_off():                    # human-owned env var, e.g. HARNESS_GATE=off
        return ALLOW                         # disabled loudly, never silently
    if not session_id:
        warn("no session id — allowing; the gate never traps a session")
        return ALLOW
    if event == "SessionStart":
        set_state(session_id, "RED")         # every session re-arms to RED
        return ALLOW
    if event == "PostToolUse":
        if tool == "Skill" and args.get("skill") in HARNESS_SKILLS:
            set_state(session_id, "GREEN")   # harness invoked -> agent may act
        return ALLOW
    if event == "PreToolUse":
        mutating = tool in MUTATING_TOOLS or (
            tool == "Bash" and matches(MUTATING_SHELL, args.get("command", "")))
        if not mutating or get_state(session_id) == "GREEN":
            return ALLOW                     # read-only always passes
        return BLOCK("RED: invoke a harness skill first, then act")
    return ALLOW
```

## Hard rules (what fails this skill)

- Any mutation before the harness is loaded.
- A skill named in a report that was never invoked in the session.
- A hook that blocks read-only tools, traps a session in RED, or fails silently.
- A second gate, or any new friction placed on the human. The kill-switch stays theirs.

## Works well with

- [invariant-floor](../invariant-floor/SKILL.md) — the floor boot loads first.
- [human-calibration](../human-calibration/SKILL.md) — the profile step of boot.
- [repair-loop](../repair-loop/SKILL.md) — what a fix job runs after boot.
- [bounded-loops](../bounded-loops/SKILL.md) — budgets for every loop boot starts.
- [wayfinder](../wayfinder/SKILL.md) — when boot shows you do not know the route.
