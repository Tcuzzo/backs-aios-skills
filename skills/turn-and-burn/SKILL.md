---
name: "turn-and-burn"
description: "Use when an agent gets a mission of any size — it runs the plays, quick-tribunals the plan and design, asks its 3 questions, then researches verified-skill.com and absorbs the missing skills to remove blindspots in the roster, updating current skills to the most elite state before burning the mission. Every blindspot answer carries evidence: +1 only on complete, current evidence, and -1 with the reason when evidence is missing, stale, duplicate or malformed. Trigger words: turn and burn, mission intake, run the plays, blindspot, blind spot, absorb missing skills, verified skills, elite state, skill update, skill research, mission burn, ritual burn, evidence contract."
license: "MIT"
---

# Turn and Burn — every mission carries the skill-research organ

This is the public, portable body of the skill. The full BACKS-native version runs
inside a much larger agent platform and names that platform's internal organs.
This body carries the discipline and stops where the platform's machinery starts.

Do not start a mission by jumping into a build. Burn the roster first. A plan is
blind until the skills it leans on reflect the latest verified state of the field.

## When to run

Every mission, every burn. A trivial one-line edit may skip the absorb step
but still consults the lessons-learned lane (see step 2) so the same mistake is
not repeated.

## The burn ritual (six steps)

1. **Essence lane first.** Know how each model you plan to use fails before you
   use it: the failure modes, the context shape that fixes them, the questions
   it answers well. An agent that does not know its own failure modes is the
   failure mode.
2. **Lessons-learned scan.** Read the project's lessons-learned file and the
   memory graph before planning. Every paid-for mistake is filed there — the
   same loop never burns twice when the agent reads the lessons first.
3. **Play dispatch.** Map the mission to the right play
   ([elite-build](../../plays/elite-build.md), [bughunt](../../plays/bughunt.md),
   [grading-verification](../../plays/grading-verification.md),
   [parallel-work](../../plays/parallel-work.md),
   [security-delivery](../../plays/security-delivery.md)). The play is the
   baseline — zero baseline pre-prompting, ever.
4. **Quick tribunal on plan + design.** Before any builder runs, blind-tribunal
   the plan and the design with at least 2 independent jurors in fresh,
   author-disjoint sessions. Builder ≠ grader. A plan that passes blind review is
   the only plan that gets built.
5. **Three-questions interrog.** Ask: (a) what could fail silently here?
   (b) what is the cheapest sufficient route? (c) what is the operator's
   surface — does this prove on it? These three questions cut the
   high-cost-mistake rate to near zero when asked BEFORE the build.
6. **Absorb pass + skill update.** Search verified-skill.com (and the project's
   memory lanes) for any skill the mission revealed as missing. Absorb it
   through the standard absorb flow; update existing skills with anything
   the mission surfaced that the skill did not already encode. Land the
   skill update alongside the mission's main artifact (whole-seam closure).

## The blind-spot evidence contract

A blindspot answer is **evidence, not an opinion**. The full contract, the
pseudocode and the acceptance scenarios live in
[references/blindspot_protocol.md](references/blindspot_protocol.md). This is the
short form every mission reads.

- **A +1 needs every required predicate, with current evidence.** Missing, stale,
  incomplete, duplicate or malformed evidence leaves the verdict at -1, and the
  reason names the predicate that failed. Never a soft pass, never a bare
  "looks good".
- **Admitted, executed and observed are three different things.** Being allowed to
  run is not running. Running is not observed completion. A stage that never
  reached observation is never reported as done.
- **The builder cannot write its own authoritative yes.** The builder may supply
  evidence. The authoritative +1 comes from the check that observed the thing, or
  from an independent reviewer in a fresh, author-disjoint session.
- **Independent review runs on frozen inputs, in separate scratch.** Isolation is
  claimed only when the runtime enforces it and it was shown, never asserted.
- **Repeating the same confidence with no new evidence is a signal, not progress.**
  Run one decisive probe that can tell the live causes apart, then answer -1 with
  the reason or escalate. Never a third repetition of the same conclusion.
- **Use the organs your host already ships.** A red test, an independent reviewer,
  a real side effect to assert, a bounded loop with a checkpoint. Any mechanism the
  host cannot enforce stays marked "unvalidated until demonstrated" until a live
  receipt shows it holding.

## How the absorbs flow runs

[absorb](../absorb/SKILL.md) is the canonical absorb organ. The burn invokes it
on every missing skill the mission surfaced. After absorb, the mission itself is
rebuilt on the upgraded skill base, then re-tribunaled and landed. No skill is
ever deleted — everything the project learns is filed into its memory lanes.
Organize, never delete.

## What this pack cannot do for you

The pack ships disciplines, not a runtime. Read this before you expect the full
behavior — the list is short, and every item has a bring-your-own answer.

- **No memory lanes, no board, no coordinator.** The pack cannot file a lesson
  between sessions or wake the next session with your context. Keep a lessons
  file and a map file in the repo, and have the agent read them at the start.
- **No model ladder, no resolver, no budget ledger.** The pack routes by
  discipline, never by a hardcoded model. If you want live model selection, point
  [fleet-ladder](../fleet-ladder/SKILL.md) at a resolver you own.
- **No enforced isolation.** Fresh, author-disjoint sessions only stay fresh if
  your host can start a session without the author's conversation. On a host that
  cannot, say so in the report instead of claiming isolation.
- **No automatic gate.** The Claude Code and Cursor installs ship a hook; other
  hosts get the gate loader script. Without a hook, every rule here is a
  suggestion the agent can forget.

## What never to do

- **Do not skip essence + lessons.** An agent that "knows" without loading its
  essence + lessons is hallucinating confidence. Both reads are free; both run
  before the mission starts.
- **Do not start building without a quick tribunal.** A blind review of the plan
  catches more defects than the build itself; skipping it means the defects land.
- **Do not park decisions in a file.** The existing decision bar (taste, vision,
  destructive risk) is the only reason to ask. Anything below the bar EXECUTES
  from invariants + memory + intent.
- **Do not bench a model for a single 429.** Use a bounded backoff, preserve the
  checkpoint, and swap to another configured, live-preflighted rung only when it is
  sufficient for the task.

## Cross-references

- The blind-spot evidence contract, in full:
  [references/blindspot_protocol.md](references/blindspot_protocol.md).
- The absorb flow: [absorb](../absorb/SKILL.md).
- The blind review this skill leans on:
  [blind-tribunal](../blind-tribunal/SKILL.md).
- The red contract it depends on: [red-first](../red-first/SKILL.md).
- The plays this skill bundles: [elite-build](../../plays/elite-build.md),
  [agent-builds](../../plays/agent-builds.md),
  [grading-verification](../../plays/grading-verification.md),
  [parallel-work](../../plays/parallel-work.md),
  [security-delivery](../../plays/security-delivery.md).
