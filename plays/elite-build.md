# Elite Build — the master play

The default play for any "build X", "fix X", or "uplift X" ask. The human states the
goal once; this play assembles the whole environment so they never re-explain the
baseline. Read the intent, load the human, burn the roster, gate the plan, prove it
red, build, test tight, measure, grade blind, land.

## When to run

Any build, fix, or uplift with real stakes. A trivial one-line edit may skip straight
to [sniper-testing](../skills/sniper-testing/SKILL.md) and land.

The loop, at a glance:

```
+--------------------------------------------+
| 0 optimus  boot the floor first            |
+--------------------------------------------+
| 1 intent-compiler  the ask is the spec     |
+--------------------------------------------+
| 2 human-calibration  load the profile      |
+--------------------------------------------+
| 3 turn-and-burn  load essence + lessons    |
|   know-thyself + cross-session memory --   |
|   so this build never repeats a paid-     |
|   for mistake                            |
+--------------------------------------------+
| 4 understanding-gates + live-research --   |
|   read first, then gate Design -> Ship     |
+--------------------------------------------+
| 5 architecture-engineer  boundary check    |
|   on every diff (declared vs runtime,      |
|   dependency direction, ADR-worthy moves)  |
+--------------------------------------------+
| 6 wayfinder  lost? chart the route         |
+--------------------------------------------+
| 7 red-first  failing test committed first  |<--------------------------+
+--------------------------------------------+  finding -> new red test  |
| 8 build  fleet-ladder + model-fusion;      |   +---------------------+ |
|   bugs: repair-loop + seam-engineering     |   |  LORD OF THE LOOP   |-+
+--------------------------------------------+   | one hand drives the |
| 9 sniper-testing  scoped runs only         |   | loop: dispatch,     |
+--------------------------------------------+   | judge, loop back    |
| 10 clean-code-gauntlet  measure + mutate   |   | until the gate is   |
+--------------------------------------------+   | green. a lane never |
| 11 blind-eval, then blind-tribunal         |-->| lands its own work. |
+--------------------------------------------+   +---------------------+
          |
          | every juror passes
          v
+--------------------------------------------+
| 12 LANDING GATE -- all green or no land:   |
|    red test untouched . builder != grader  |
|    every finding closed . one full pass .  |
|    live proof on the human's own surface . |
|    own files only . two-word report        |
+--------------------------------------------+
```

## The chain

0. [optimus](../skills/optimus/SKILL.md) — boot the harness before
   anything edits. The floor loads first, every session, every time.
1. [intent-compiler](../skills/intent-compiler/SKILL.md) — read the ask as the
   spec, whole. Deduce intent before surfacing any ship or option decision. Never
   present an option menu when a clear solve exists — solve it.
2. [human-calibration](../skills/human-calibration/SKILL.md) — load the human's validated
   profile and apply it. Never re-interrogate a human you already know.
3. [turn-and-burn](../skills/turn-and-burn/SKILL.md) — burn the roster before
   the build. Load each model's essence (know-thyself), read
   `docs/BACKS_LESSONS_LEARNED.md` + `memory/MEMORY.md` (cross-session memory),
   and absorb any missing skill the mission surfaced. Local prompts must be
   capability-aware: every lane consults essence + lessons so the same mistake
   is not paid for twice. This is the operator's "stop redundant failures
   across the board" floor.
4. [understanding-gates](../skills/understanding-gates/SKILL.md) — Design → Plan →
   Build → Test → Ship, each stage gated. Before any design: read what exists via
   [live-research](../skills/live-research/SKILL.md), reuse what is written, map the
   whole topology. The answer is usually already written.
5. [architecture-engineer](../skills/architecture-engineer/SKILL.md) — for any
   diff that touches a module boundary, dependency direction, or shared seam,
   run the structural review recipe (fixed point, declared vs runtime, local
   rule check, structural review, severity + smallest fix, ADR when durable).
   Cite the local rule or concrete failure mode behind every violation. Never
   bypass the authority surface classifier.
6. [wayfinder](../skills/wayfinder/SKILL.md) — when lost at any step, chart the route
   from evidence. Never park on the human a question that evidence can answer.
7. [red-first](../skills/red-first/SKILL.md) — write the failing contract test and
   commit it BEFORE any builder runs. The builder may not touch that test.
8. Build. Fan out parallel lanes by default — never serialize what can run at once.
   Each lane gets its own scratch branch or worktree. Solo, one session? One lane IS
   the fan-out — build on a scratch branch and continue. (A worktree is a second
   checkout of the same repo in another folder, so two builders never touch the same
   files.) Resolve builders through [fleet-ladder](../skills/fleet-ladder/SKILL.md);
   combine drafts with [model-fusion](../skills/model-fusion/SKILL.md). For a bug,
   run the [repair-loop](../skills/repair-loop/SKILL.md) and close the CLASS at the
   shared seam per [seam-engineering](../skills/seam-engineering/SKILL.md).
9. [sniper-testing](../skills/sniper-testing/SKILL.md) — scoped runs only while
   iterating; the one full touched-module pass waits for the landing (step 12).
10. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — measure before
    landing: sniper suite, complexity-times-coverage risk score under your ceiling,
    then mutation testing to zero survivors. Measure the code; never eyeball it.
11. [blind-eval](../skills/blind-eval/SKILL.md), then
    [blind-tribunal](../skills/blind-tribunal/SKILL.md) — an author-redacted envelope
    goes to graders from a different model family than the builder. The builder never
    grades its own work. Every juror finding becomes a new red test; re-convene until
    every juror passes. Solo rig? Degrade per blind-tribunal's Solo rig rule — and
    name the weakened gate in the landing report.
12. Land: merge cleanly, run ONE full pass over the touched modules' suites, restart
    the real service, and prove the behavior on the human's own surface (the page
    they load, the command they run) — never a proxy probe. Then report.

## Hard gates (any one red blocks the landing)

- The failing test was committed before the build and is untouched — the grader
  verifies the test-file diff is empty.
- Builder is never grader, and the grader is a different model family.
- Every surfaced finding is closed, or adjudicated "not a bug" with recorded
  evidence. Never silently deferred. Whole-seam closure (the seam is the shared
  spot in the code where this class of bug lives) or no landing.
- The burn ritual (step 3) was honored — essence + lessons were consulted
  before the build. The mission's absorb pass landed any missing skill the
  build surfaced.
- Live proof on the human's real surface. Green tests with broken capability is
  failure, not success.
- Report in two words, PROVEN or STILL-BUILDING, in
  [human-voice](../skills/human-voice/SKILL.md). Proven means landed, plus
  independently graded, plus demonstrated live.
- Commit only this change's own files — never another session's in-flight work.

## Works well with

- [optimus](../skills/optimus/SKILL.md) — re-boot the floor after a compaction or restart
- [turn-and-burn](../skills/turn-and-burn/SKILL.md) — the burn ritual; pair this play with it on every mission
- [architecture-engineer](../skills/architecture-engineer/SKILL.md) — the boundary check; pair on any seam-touching change
- [seam-engineering](../skills/seam-engineering/SKILL.md) — close the CLASS at the seam; partner to architecture-engineer
- [invariant-floor](../skills/invariant-floor/SKILL.md) — the locked floor every landing must meet
- [decision-bar](../skills/decision-bar/SKILL.md) — what reaches the human vs. what executes
- [bounded-loops](../skills/bounded-loops/SKILL.md) — budgets and kill-switches on long runs
- [session-handoff](../skills/session-handoff/SKILL.md) — seal state before stopping

**Weight:** the full stack — free discipline, light gates, and three heavy steps (model fusion, the gauntlet, the tribunal); the heavy spend pays on anything that ships, which is exactly what this play is for.


## Fleet ladder rung policy

Build/dispatch step uses [fleet-ladder](../skills/fleet-ladder/SKILL.md): read deploy
`config/fleet_ladder.yaml` + `config/gpu_nodes.yaml`, honor the live builder seat, and
HARD-gate frontier research-before-lift (web + GitHub + Reddit + papers; never disable
web_search on those rungs). Patch owns yaml; skill rails only.

Thinking / tokens: [fleet-ladder](../skills/fleet-ladder/SKILL.md) ??? research seams first (`token_efficiency` ??? cheap_builder_specs), thinking_floor=medium (ultra???medium only), no truncation hacks.
