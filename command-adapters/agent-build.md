---
name: agent-build
description: Build an agent, bot, worker, or autonomous service — deterministic primitives first, typed IO, bounded loops.
argument-hint: the agent or service to build
---

Load the bundled `plays/agent-builds.md` using `${CLAUDE_PLUGIN_ROOT}/plays/agent-builds.md` in Claude Code or `${CURSOR_PLUGIN_ROOT}/plays/agent-builds.md` in Cursor, then execute it, whole, on: $ARGUMENTS

Order: intent-compiler → understanding-gates (name the domain primitives; the LLM slot is for genuine reasoning only) → red-first contracts on every typed IO boundary → build inside bounded-loops → sniper-testing → blind grade.

Hard gate: no landing while any core capability is an LLM call where a deterministic primitive would do, or any loop lacks a budget, checkpoint, and loud kill-switch.
