---
name: elite-build
description: Run the master build play — intent, human profile, gated stages, red proof, build, sniper tests, blind grade, land.
argument-hint: what to build, fix, or uplift
---

Load the bundled `plays/elite-build.md` using `${CLAUDE_PLUGIN_ROOT}/plays/elite-build.md` in Claude Code or `${CURSOR_PLUGIN_ROOT}/plays/elite-build.md` in Cursor, then execute it, whole, on: $ARGUMENTS

Order: optimus boot → intent-compiler → human-calibration → understanding-gates (Design → Plan → Build → Test → Ship) → red-first contract → build → sniper-testing → clean-code-gauntlet → blind grade.

Hard gate: nothing lands until the red-first contract has been seen failing and now passes, the gauntlet is green, and a grader that did not author the change passes it.
