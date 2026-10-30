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

The grade, at a glance:

```
+--------------------------------------------+
| 1 red-first  confirm the suite failed --   |<--------------------------+
|   non-zero exit -- BEFORE the fix existed  |  each finding -> a new    |
+--------------------------------------------+  red test -> fix ->       |
| 2 sniper-testing  scoped runs verified;    |  re-convene               |
|   no mock theater on the changed seam      |                           |
+--------------------------------------------+   +---------------------+ |
| 3 independent grade  an author-disjoint   |   |  LORD OF THE LOOP   |-+
|   execution, chosen live by capability +   |   | one hand drives the |
|   availability from the configured matrix  |   | loop: dispatch,     |
+--------------------------------------------+   | judge, loop back    |
| 4 blind-tribunal  jurors judge an          |-->| until the gate is   |
|   author-redacted envelope in a fresh      |   | until the gate is   |
|   session, no conversation inherited       |   | green. a lane never |
+--------------------------------------------+   | lands its own work. |
| 5 clean-code-gauntlet  the grader re-runs  |   +---------------------+
|   it -- never trust the builder's numbers  |
+--------------------------------------------+
          |
          | all jurors pass
          v
+--------------------------------------------+
| LANDING GATE -- the two-sided proof:       |
| fail-to-pass AND pass-to-pass, run         |
| hermetically . no fake-green tell . the    |
| grader is the seat that did not build .    |
| the grader re-ran the checks itself        |
+--------------------------------------------+
```

## The chain

1. [red-first](../skills/red-first/SKILL.md) — confirm the suite failed with a
   non-zero exit BEFORE the fix existed. A suite that was never red proves nothing.
   The failing test is committed and the builder may not touch it; the exact
   bytes of that test file are the contract.
2. [sniper-testing](../skills/sniper-testing/SKILL.md) — verify the builder used
   scoped tests during iteration and ran no mock theater on the seam it changed.
3. Independent grade — pick the grader seat live: it is the seat that did not
   build, selected by capability and availability from the configured rung
   matrix (task → capability → rung → live probe). Record the authoring
   execution where the runner supports provenance. A fresh, author-disjoint
   session may review using any capable configured route. What is barred: a grade
   run in a session that saw the builder's conversation or inherited its
   context.
4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — for consequential changes,
   convene jurors on an author-redacted envelope in a fresh session with no
   inherited conversation. Every finding becomes a new failing test, and the
   tribunal re-convenes until all jurors pass it.
5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — the grader re-runs
   the gauntlet itself (coverage-vs-complexity, bounded mutation testing). Never
   trust the builder's report of its own numbers.

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
