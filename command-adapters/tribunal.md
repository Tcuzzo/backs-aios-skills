---
name: tribunal
description: Convene the blind tribunal on the current diff — eight cross-family jurors, one lens each, routed by tier, author-redacted envelope, loop until all pass.
argument-hint: optional scope (defaults to the current diff)
---

Load the bundled `skills/blind-tribunal/SKILL.md` using `${CLAUDE_PLUGIN_ROOT}/skills/blind-tribunal/SKILL.md` in Claude Code or `${CURSOR_PLUGIN_ROOT}/skills/blind-tribunal/SKILL.md` in Cursor, then convene it on the current diff (or on: $ARGUMENTS).

Order: build the author-redacted envelope carrying whole files → seat eight jurors from a different family than the builder, one lens each, routed by tier (defect, proportion, operator_consequence, reversibility, state_continuity, resource_economy, boundary_condition, telemetry) → collect strict verdicts → turn every finding into a new failing test → fix → re-convene.

Hard gate: the change lands only when every juror passes. A solo-family rig must say so out loud in the report — never silently pretend the cross-family gate held.
