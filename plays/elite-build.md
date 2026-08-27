# Elite Build — the master play

The default play for any "build X", "fix X", or "uplift X" ask. The human states the
goal once; this play assembles the whole environment so they never re-explain the
baseline. Read the intent, load the human, gate the plan, prove it red, build, test
tight, measure, grade blind, land.

## When to run

Any build, fix, or uplift with real stakes. A trivial one-line edit may skip straight
to [sniper-testing](../skills/sniper-testing/SKILL.md) and land.

## The chain

0. [optimus](../skills/optimus/SKILL.md) — boot the harness before
   anything edits. The floor loads first, every session, every time.
1. [intent-compiler](../skills/intent-compiler/SKILL.md) — read the ask as the
   spec, whole. Deduce intent before surfacing any ship or option decision. Never
   present an option menu when a clear solve exists — solve it.
2. [human-calibration](../skills/human-calibration/SKILL.md) — load the human's validated
   profile and apply it. Never re-interrogate a human you already know.
3. [understanding-gates](../skills/understanding-gates/SKILL.md) — Design → Plan →
   Build → Test → Ship, each stage gated. Before any design: read what exists via
   [live-research](../skills/live-research/SKILL.md), reuse what is written, map the
   whole topology. The answer is usually already written.
4. [wayfinder](../skills/wayfinder/SKILL.md) — when lost at any step, chart the route
   from evidence. Never park on the human a question that evidence can answer.
5. [red-first](../skills/red-first/SKILL.md) — write the failing contract test and
   commit it BEFORE any builder runs. The builder may not touch that test.
6. Build. Fan out parallel lanes by default — never serialize what can run at once.
   Each lane gets its own scratch branch or worktree. Solo, one session? One lane IS
   the fan-out — build on a scratch branch and continue. (A worktree is a second
   checkout of the same repo in another folder, so two builders never touch the same
   files.) Resolve builders through [fleet-ladder](../skills/fleet-ladder/SKILL.md);
   combine drafts with [model-fusion](../skills/model-fusion/SKILL.md). For a bug,
   run the [repair-loop](../skills/repair-loop/SKILL.md) and close the CLASS at the
   shared seam per [seam-engineering](../skills/seam-engineering/SKILL.md).
7. [sniper-testing](../skills/sniper-testing/SKILL.md) — scoped runs only while
   iterating; the one full touched-module pass waits for the landing (step 10).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — measure before
   landing: sniper suite, complexity-times-coverage risk score under your ceiling,
   then mutation testing to zero survivors. Measure the code; never eyeball it.
9. [blind-eval](../skills/blind-eval/SKILL.md), then
   [blind-tribunal](../skills/blind-tribunal/SKILL.md) — an author-redacted envelope
   goes to graders from a different model family than the builder. The builder never
   grades its own work. Every juror finding becomes a new red test; re-convene until
   every juror passes. Solo rig? Degrade per blind-tribunal's Solo rig rule — and
   name the weakened gate in the landing report.
10. Land — merge cleanly, run ONE full pass over the touched modules' suites, restart
    the real service, and prove the behavior on the human's own surface (the page
    they load, the command they run) — never a proxy probe. Then report.

## Hard gates (any one red blocks the landing)

- The failing test was committed before the build and is untouched — the grader
  verifies the test-file diff is empty.
- Builder is never grader, and the grader is a different model family.
- Every surfaced finding is closed, or adjudicated "not a bug" with recorded
  evidence. Never silently deferred. Whole-seam closure — the seam is the shared
  spot in the code where this class of bug lives — or no landing.
- Live proof on the human's real surface. Green tests with broken capability is
  failure, not success.
- Report in two words — PROVEN or STILL-BUILDING — in
  [plain-speech](../skills/plain-speech/SKILL.md). Proven means landed, plus
  independently graded, plus demonstrated live.
- Commit only this change's own files — never another session's in-flight work.

## Works well with

- [optimus](../skills/optimus/SKILL.md) — re-boot the floor after a compaction or restart
- [invariant-floor](../skills/invariant-floor/SKILL.md) — the locked floor every landing must meet
- [decision-bar](../skills/decision-bar/SKILL.md) — what reaches the human vs. what executes
- [bounded-loops](../skills/bounded-loops/SKILL.md) — budgets and kill-switches on long runs
- [session-handoff](../skills/session-handoff/SKILL.md) — seal state before stopping
