# Play: Bughunt

A bounded, parallel bug hunt. Chart the hunt as a map, fan finders across it, verify
every finding adversarially, and close whole seams — never single symptoms.

## When to run

- An audit, sweep, or hunt across many seams — not one reported bug (use the
  repair loop for that).
- A backlog of findings needs to be attacked in parallel without drift or trampling.

## The chain

1. [wayfinder](../skills/wayfinder/SKILL.md) — chart the hunt FIRST as one map with
   a node per seam or finding. Finders claim nodes atomically from the frontier;
   closing a node writes the next node's question. Invent nothing off-map.
2. [leap-protocol](../skills/leap-protocol/SKILL.md) — every node is one ball: goal,
   spec, hard file scope, bounded rounds, tri-state result. Related balls ride one
   dependency-ordered slice with exactly ONE writer.
3. [root-cause-first](../skills/root-cause-first/SKILL.md) — reproduce the bug and
   review the root-cause evidence BEFORE any code changes. No mutation on a guess.
4. [repair-loop](../skills/repair-loop/SKILL.md) — the inner discipline of every
   ball: [red-first](../skills/red-first/SKILL.md) failing test committed before the
   fix, [sniper-testing](../skills/sniper-testing/SKILL.md) scoped runs during
   iteration, one full touched-module pass at landing.
5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — every finding is attacked
   adversarially: a grader that did not author it attacks refuse-by-default, jurors
   judge an author-redacted envelope. The builder never grades its own work.
6. [seam-engineering](../skills/seam-engineering/SKILL.md) — close the CLASS at
   the shared seam, never the single symptom.
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — closure proof:
   the fixed branch must DIE under mutation. A closure whose mutant survives is
   unproven, and the finding stays open.

## A ball closes

A ball closes only through [leap-protocol](../skills/leap-protocol/SKILL.md)'s
Score gate — source truth, keep-or-revert, blind review, live proof, provenance;
missing evidence never defaults to pass. Hunt-specific terminal states: every
finding ends FIXED or REFUTED-WITH-EVIDENCE.

## Rules of the hunt

- Lower your confidence. Reground from the ledger and the node's attempt history,
  never from your own memory. Relaunch means re-claim from the frontier; hand off
  through [session-handoff](../skills/session-handoff/SKILL.md).
- Stream progress in a human voice as you go. Unknown stays unknown — it never
  becomes "pass".
- Once candidate bytes, commands, tests, and verdict are frozen, landing is a
  deterministic replay. No model call re-decides an already-decided command.
- Respect the box: measure resources before spawning, bound concurrency, reap dead
  lanes, stop LOUD after a second death on the same node, throttle every external
  call. The kill-switch stops new claims — never a mutation mid-flight.
- Name each slice's waste and measure before/after. Take an efficiency win only
  when a comparator proves zero capability loss; over-bloat is a defect too.
- Report in two words: PROVEN or STILL-BUILDING.

## Hard gates — any one fails the play

- A mutation made before reproduced root-cause evidence was reviewed.
- A builder grading its own finding.
- A finding closed while a mutant survives on the fixed branch.
- A full-suite run mid-hunt — sniper the finding's own seam only.
- Mock theater in a closure test: it silently re-opens the bug while the ledger
  claims it is shut.
- A finding parked instead of fixed or refuted with evidence.

**Weight:** free hunt discipline at the core; the heavy spend is triple — leap fan-out, the adversarial tribunal, and mutation closure proof — it pays when a whole backlog closes in parallel with every closure proven under mutation.
