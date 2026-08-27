# Play: Grading & Verification

The adversarial grading play. Its one belief: a green result is a claim, not proof.
The grader attacks, and the floor is built so it cannot be gamed.

## When to run

- Any built change asks to land — code, config, docs, an agent's output.
- A suite claims green and nobody watched it fail first.
- One model built the work and you need an honest verdict on it.

The grade, at a glance:

```
+--------------------------------------------+
| 1 red-first  confirm the suite failed --   |<--------------------------+
|   non-zero exit -- BEFORE the fix existed  |  each finding -> a new    |
+--------------------------------------------+  red test -> fix ->       |
| 2 sniper-testing  scoped runs verified;    |  re-convene               |
|   no mock theater on the changed seam      |                           |
+--------------------------------------------+   +---------------------+ |
| 3 cross-family grade -- a model from a     |   |  LORD OF THE LOOP   |-+
|   DIFFERENT family than the builder        |   | one hand drives the |
+--------------------------------------------+   | loop: dispatch,     |
| 4 blind-tribunal  jurors judge an          |-->| judge, loop back    |
|   author-redacted envelope                 |   | until the gate is   |
+--------------------------------------------+   | green. a lane never |
| 5 clean-code-gauntlet  the grader re-runs  |   | lands its own work. |
|   it -- never trust the builder's numbers  |   +---------------------+
+--------------------------------------------+
          |
          | all jurors pass
          v
+--------------------------------------------+
| LANDING GATE -- the two-sided proof:       |
| fail-to-pass AND pass-to-pass, run         |
| hermetically . no fake-green tell .        |
| builder + grader families differ . the     |
| grader re-ran the checks itself            |
+--------------------------------------------+
```

## The chain

1. [red-first](../skills/red-first/SKILL.md) — confirm the suite failed with a
   non-zero exit BEFORE the fix existed. A suite that was never red proves nothing.
2. [sniper-testing](../skills/sniper-testing/SKILL.md) — verify the builder used
   scoped tests during iteration and ran no mock theater on the seam it changed.
3. Cross-family grade — hand the work to a model from a DIFFERENT family than the
   builder. Same-family grading measurably inflates win-rates — graders favor their
   own kin; a different instance of the same family is not enough.
4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — for consequential changes,
   convene jurors on an author-redacted envelope. Every finding becomes a new red
   test, and the tribunal re-convenes until all jurors pass it.
5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — the grader re-runs
   the gauntlet itself (coverage-vs-complexity, bounded mutation testing). Never
   trust the builder's report of its own numbers.

## The two-sided proof (both, or no pass)

- **Fail-to-pass:** the tests that were red are now green — the fix is proven.
- **Pass-to-pass:** everything that was green is still green — no regression.
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

- Builder and grader share a model family.
- The suite cannot be shown red before the fix.
- Fail-to-pass or pass-to-pass is missing from the graded run.
- Any fake-green tell above is present.
- The grader trusted the builder's own report instead of re-running the checks.

**Weight:** free red and sniper checks up front; the heavy spend is the tribunal plus the grader re-running the gauntlet itself — it pays on any change that asks to land, because one fake green costs more than every grade combined.
