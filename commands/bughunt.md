---
name: bughunt
description: Run a bounded, parallel bug hunt — map the seams, fan finders, verify findings adversarially, close whole seams.
argument-hint: the codebase area or finding backlog to hunt
---

Load the bundled `plays/bughunt.md` using `${CLAUDE_PLUGIN_ROOT}/plays/bughunt.md` in Claude Code or `${CURSOR_PLUGIN_ROOT}/plays/bughunt.md` in Cursor, then execute it, whole, on: $ARGUMENTS

Order: wayfinder charts the hunt as one map (a node per seam) → leap-protocol turns each node into a scoped ball → root-cause-first (reproduce before any code changes) → repair-loop inside every ball (red-first fix, sniper tests) → adversarial verification of each finding.

Hard gate: a seam closes only when EVERY surfaced finding on it is fixed or carries a recorded, evidenced not-a-bug verdict — never a silent deferral. Off-map inventions do not count.
