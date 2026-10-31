# Play: Grading & Verification

The adversarial grading play. Its one belief: a green result is a claim, not proof.
The grader attacks, and the floor is built so it cannot be gamed. Model identity is
provenance, not authority — the grader is the EXECUTION that did not author the
candidate, chosen live by capability and availability from the configured rung
matrix; independence requires a fresh author-disjoint execution.

## When to run

- Any built change asks to land — code, config, docs, an agent's output.
- A suite claims green and nobody watched it fail first.
- One seat built the work and an honest, blind verdict on it is owed.
- A previous grade ran in the builder's authoring session or inherited the
  builder's conversation — a fresh, author-disjoint context is owed.

## Shared task and limits

Apply this play inside the current [BACKS Build Flow](../skills/backs-build-flow/SKILL.md)
task packet. Keep one integration owner, the requested `task_mode`, pinned base
and candidate revisions, operator essence, and current evidence. Reuse applicable
loaded skill bodies; this play adds its domain gates without restarting the task.

[bounded-loops](../skills/bounded-loops/SKILL.md) owns the original deadline and
remaining allowances across retries, workers, models, reviews, and handoffs.
Never reset them for a nested play. On exhaustion, checkpoint **STILL-BUILDING**
with the candidate, evidence, unmet gates, and next action. Continue useful
authorized work only within its remaining allowance; no missing gate becomes a pass.

## The chain

1. [red-first](../skills/red-first/SKILL.md) — confirm the suite failed with a
   non-zero exit BEFORE the fix existed. A suite that was never red proves nothing.
   The failing test is committed and the builder may not touch it; the exact
   bytes of that test file are the contract.
2. [sniper-testing](../skills/sniper-testing/SKILL.md) — verify the builder used
   the repository's real lint/type/test commands scoped to the pinned aggregate
   candidate diff, and ran no mock theater on the seam it changed. Verify explicit
   N/A reasons and missing checks. Freeze candidate identity for this review.
3. Independent grade — pick the grader seat live: it is the seat that did not
   build, selected by capability and availability from the configured rung
   matrix (task → capability → rung → live probe). Record the authoring
   execution where the runner supports provenance. A fresh, author-disjoint
   session may review using any capable configured route. What is barred: a grade
   run in a session that saw the builder's conversation or inherited its
   context.
4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — for consequential changes,
   convene jurors on an author-redacted envelope in a fresh session with no
   inherited conversation. Return substantiated findings to the integration owner
   for a separate supplemental RED and bounded repair; the original RED remains
   sealed. Re-convene on the revised frozen candidate within the same remaining
   budget. Every required juror must pass before landing.
5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — the grader re-runs
   the gauntlet itself (coverage-vs-complexity, bounded mutation testing). Never
   trust the builder's report of its own numbers.

Honor review mode's immutable target. Run checks that create caches, mutate code,
or exercise services only in permitted isolation; mutation testing must never
rewrite the frozen source. Missing isolation or runtime support is an evidence
gap, not permission to patch while reviewing. Preserve the required full
affected-suite landing evidence and report local checks separately from real
surface or delivery proof.

## The two-sided proof (both, or no pass)

- **Fail-to-pass:** the tests that were red are now green — the fix is proven
  on the exact test file committed at the red baseline. Evidence: the diff of
  that test file is empty between red commit and landing.
- **Pass-to-pass:** everything that was green is still green — no regression.
  Evidence: the regression cluster at the touched modules stays no worse than
  the baseline run.
- A run that only ADDS passing tests satisfies neither. Run both hermetically.

## Fake-green guards (any one is the tell)

- An exit-code escape hatch — a harness that exits clean no matter what happened.
- Hardcoded or memorized outputs standing in for computed ones.
- Deleted, skipped, or weakened tests.
- Any edited grader, timer, or scorer. An edited harness that goes green IS the tell.
- A surviving mutant under a green suite. The mutant is proof the assertions never
  reached that branch — fake green by definition.

## De-bias the judge

The judge-mechanics floor lives in [blind-eval](../skills/blind-eval/SKILL.md)'s
"De-bias the judge" section — apply it whole.

## Hard gates — any one fails the play

- The grader ran in the builder's authoring execution or inherited the builder's conversation. A fresh author-disjoint session is the floor.
- The suite cannot be shown red before the fix.
- The blind-tribunal envelope was graded by a session that saw the author's
  conversation or by a juror that inherited context — it must be a fresh,
  author-disjoint session.
- Fail-to-pass or pass-to-pass is missing from the graded run.
- Any fake-green tell above is present.
- The grader trusted the builder's own report instead of re-running the checks.

**Note on runtime gaps.** Select capable reviewers through the configured
ladder and exclude the authoring execution. Surface any runtime restriction
that blocks a capable reviewer; never silently assert the gap fixed or bypass it.

**Weight:** free red and sniper checks up front; the heavy spend is the tribunal
plus the grader re-running the gauntlet itself — it pays on any change that asks
to land, because one fake green costs more than every grade combined.
