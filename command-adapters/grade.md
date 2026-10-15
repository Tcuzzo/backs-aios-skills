---
name: grade
description: Adversarially grade a built change — red proof, no mock theater, capability-resolved non-author verdict. A green result is a claim, not proof.
argument-hint: the change, diff, or claim to grade
---

Load the bundled `plays/grading-verification.md` using `${CLAUDE_PLUGIN_ROOT}/plays/grading-verification.md` in Claude Code or `${CURSOR_PLUGIN_ROOT}/plays/grading-verification.md` in Cursor, then execute it, whole, on: $ARGUMENTS

Order: red-first check (prove the suite failed before the fix existed) → sniper-testing audit (no mock theater on the changed seam) → independent grade by a non-author grader, chosen live by capability and availability from the configured rung matrix (the authoring execution that built is recorded as provenance and disqualified; a same model, rung, or family reviewer in a fresh, author-disjoint session is permitted where the configured runtime allows) → blind-tribunal for consequential changes → clean-code-gauntlet re-run by the grader.

Hard gate: PASS requires red-before-green evidence and a passing verdict from a non-author grader. A suite that was never red, or a builder grading itself, is an automatic FAIL.
