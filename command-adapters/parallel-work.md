---
name: parallel-work
description: Fan work across parallel agents safely — one write spine, many readers, isolated worktrees, per-lane gauntlets.
argument-hint: the work to decompose and fan out
---

Load the bundled `plays/parallel-work.md` using `${CLAUDE_PLUGIN_ROOT}/plays/parallel-work.md` in Claude Code or `${CURSOR_PLUGIN_ROOT}/plays/parallel-work.md` in Cursor, then execute it, whole, on: $ARGUMENTS

Order: leap-protocol decomposition (balls with goals, specs, hard file scopes) BEFORE any agent spawns → fan out readers only (research, scans, tests, grading) → one writer per slice, each lane in its own worktree → per-lane clean-code-gauntlet → blind-tribunal on the merged result.

Hard gate: no two writers on the same files, ever — and no lane lands on another lane's green; each lane proves its own work before the single write spine merges it.
