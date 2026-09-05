---
name: tribunal
description: Convene the blind tribunal on the current diff — eight cross-family jurors, one lens each, routed by tier, author-redacted envelope, loop until all pass.
argument-hint: optional scope (defaults to the current diff)
---

Load the bundled `skills/blind-tribunal/SKILL.md` using `${CLAUDE_PLUGIN_ROOT}/skills/blind-tribunal/SKILL.md` in Claude Code or `${CURSOR_PLUGIN_ROOT}/skills/blind-tribunal/SKILL.md` in Cursor, then convene it on the current diff (or on: $ARGUMENTS).

Order: build the author-redacted envelope carrying whole files → seat eight jurors from a different family than the builder, one lens each, routed by tier (defect, proportion, operator_consequence, reversibility, state_continuity, resource_economy, boundary_condition, telemetry) → collect strict verdicts → turn every finding into a new failing test → fix → re-convene.

Fast-structural seats (boundary_condition, resource_economy) sit on a free local model FUSED with a cheap cloud verifier that judges the same prompt: the lens passes only when both pass; with every cloud rung down the local verdict stands, flagged UNVERIFIED — never silently "verified". A local model must see the whole artifact: size its context window (`num_ctx` on Ollama; the 4096 default truncates silently) to the prompt and refuse, before sending, what the rung cannot hold. The verifier never comes from the primary's family; an UNVERIFIED seat is a hold (never unanimity, never a pack pass). Harness jurors run read-only (`--sandbox read-only`); every convene carries a `run_id`, writes its summary last, and its receipt binds the exact bytes the jurors read.

Hard gate: the change lands only when every juror passes. A solo-family rig must say so out loud in the report — never silently pretend the cross-family gate held.

Declare the builder on every convene (`--builder <model-or-family>`); the run records `builder_family`, refuses that family on every ladder, and a lens left with no rung holds. Prove the fall-through on the live routing table.

Verdict integrity and evidence, enforced by the organ: a pass carrying a `[blocker]` or `[major]` finding fails closed; a verdict for the wrong lens is a rejected rung and the walk continues; the out directory is owned (stamped) before it is swept, or refused with nothing deleted; one lens failing never discards the verdicts already paid for; mutation evidence names a rewritten file (`changed_paths`); every file the organ writes is 0600; a spilled local model is unloaded only by its last holder; a rung that cannot hold the artifact is skipped before any call. And in the proof harness around it: a survivor is a claim — re-run it by hand; a timeout is not a survivor, a collection error is not a kill, and any verdict path must be able to say INVALID.

The protocol footer names the literal lens (`"lens": "defect"`), never the `<your lens>` placeholder; a rung rejected for a wrong lens or a voided verdict keeps a bounded `raw_tail` on the record; every tier holds at least three rungs with no declared `context_tokens` before its local tail; nothing else writes into the tribunal's repo while it convenes.
