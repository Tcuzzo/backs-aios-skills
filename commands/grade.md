---
description: Adversarially grade a built change — red proof, no mock theater, cross-family verdict. A green result is a claim, not proof.
argument-hint: the change, diff, or claim to grade
---

Load ${CLAUDE_PLUGIN_ROOT}/plays/grading-verification.md and execute it, whole, on: $ARGUMENTS

Order: red-first check (prove the suite failed before the fix existed) → sniper-testing audit (no mock theater on the changed seam) → cross-family grade by a model that did not author the work → blind-tribunal for consequential changes → clean-code-gauntlet re-run by the grader.

Hard gate: PASS requires red-before-green evidence and a passing verdict from a non-author grader. A suite that was never red, or a builder grading itself, is an automatic FAIL.
