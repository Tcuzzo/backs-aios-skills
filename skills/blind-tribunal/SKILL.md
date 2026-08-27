---
name: blind-tribunal
description: Use when an autonomous change needs an independent grade before landing and no human is in the loop. Convenes blind, cross-family jurors — one lens each — over an author-redacted envelope of whole files; every finding becomes a new failing test; loop until every juror passes. Trigger words: blind tribunal, tribunal, jurors, cross-family grade, convene, blind grade, independent grade, grade before landing.
license: MIT
---

# Blind Tribunal

The grading loop that lets the human walk away without the agent going rogue.
A panel of jurors reviews the change blind, with authorship stripped. Every
finding becomes a new failing test. The loop repeats until every juror passes.
Nothing lands on the builder's word alone.

## When to run it

- Before landing any autonomous change no human will review.
- Any high-blast-radius change: security-shaped, data-touching, authority-adjacent.
- When one grader is not enough and you want independent lenses on the same artifact.

## The seats

Three jurors. Each is a model from a DIFFERENT family than the builder.
Each holds exactly ONE lens — a juror asked to check everything checks nothing well.

| Juror | Lens | The question it asks |
| --- | --- | --- |
| Defect | defect hunting | What actually breaks? Escapes, edge cases, broken contracts. |
| Proportion | right-sizing | Is this the right size? Over-built, or a bandaid on a symptom? |
| Consequence | human impact | If this is wrong, what happens to the person who depends on it? |

**Solo rig.** When only one model family is available, degrade EXPLICITLY: a
fresh context or session that never saw the author's conversation acts as the
blind grader, or the human reviews the redacted envelope. The report must name
the weakened gate — "graded same-family-blind, not cross-family" — never
silently pretend the cross-family gate held.

## The envelope

Jurors never see the repo, the builder, or the conversation. They see one envelope:

- **Whole current files** for every file the change touched, plus its test files.
  Never bare diff hunks — a hunk hides the surrounding contract and induces false findings.
- **The review contract**: the change's intent in one line, and the pass criteria.
- **Zero authorship.** No names, no model ids, no commit authors, no chat history.
  If identity leaks through, the envelope build fails loud — never grade un-blind.
- **No prose about the old behavior.** Describing what the code "used to do" plants
  phantom defects. The files speak for themselves.

## The verdict

Strict machine-parseable JSON, one object, no prose:

```json
{"verdict": "pass" | "refuse",
 "findings": [{"severity": "blocker|major|minor|info",
               "claim": "...", "evidence": "..."}]}
```

- A juror that ANSWERED badly — garbage, non-JSON, refusal text — counts as
  **refuse**; a juror that NEVER answered (transport failure, unreachable) is a
  **hold**: re-seat it via [fleet-ladder](../fleet-ladder/SKILL.md), never a
  silent pass. One shot per answering juror per round — no retries.
- A bare pass with zero findings and no evidence is a **low-information vote**.
  It counts, but never as the only proof — two bare passes do not outrank one
  detailed refuse. A strong pass names what it checked.

## The loop

1. Red first: commit the failing contract test BEFORE the fix is built, and record
   that commit. The builder may not touch the test ([red-first](../red-first/SKILL.md)).
2. Build to green.
3. Build the envelope from the CURRENT files.
4. Seat the three jurors — different families than the builder
   ([fleet-ladder](../fleet-ladder/SKILL.md) resolves what is live).
5. Each juror also verifies, not just reads: the new tests pass; the regression
   suite is no worse than baseline; and a fake-green check — a test that SHOULD
   fail (the bug re-introduced) does fail. A fake green is a refuse.
6. On any refuse: EVERY finding — blocker, major, and minor — becomes a NEW
   failing test that fails for the finding's real reason. Fix it. Rebuild the
   envelope on the revised files. Re-convene ALL jurors. A verdict on stale files
   is no verdict.
7. Land only on unanimous pass. Minor findings raised in the final round are
   closed too, never deferred — "fixed the blockers, minors later" is the exact
   leak this skill exists to stop. A finding ends FIXED or refuted with recorded
   evidence, never parked.

## Hard rules — any one broken voids the grade

- The builder never grades its own work: not the same instance, not the same family.
- **A juror refusal is only as good as the envelope.** Before writing a test from
  a finding, verify the finding against the actual files. A finding about code the
  envelope never carried means fix the envelope, not the code.
- Measure convergence on NEW findings per round, not the raw total. New findings
  flat or growing two rounds running: stop and escalate to the human. Never grind.
- Never weaken or edit the failing tests to reach a pass. Jurors verify the test
  files are unchanged since the red commit.
- A unanimous pass opens the gate; it is not the finish. Land, then prove the
  capability live on the real surface. Green without live proof is not done.

## Works well with

- [red-first](../red-first/SKILL.md) — the failing contract, committed before the builder runs.
- [sniper-testing](../sniper-testing/SKILL.md) — real side-effects, scoped runs, no mock theater.
- [seam-engineering](../seam-engineering/SKILL.md) — fix the class, sweep siblings, land a guard.
- [repair-loop](../repair-loop/SKILL.md) — the build loop this tribunal grades.
- [blind-eval](../blind-eval/SKILL.md) — the lighter keep-or-revert gate when the question is taste, not defects.

> Scaffold credit: Matt Pocock, grill-me / grilling (mattpocock/skills, MIT). The
> cross-family blind adversarial tribunal design is BACKS AIOS.
