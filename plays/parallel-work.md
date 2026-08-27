# Play: Parallel Work

How to fan work across agents without them trampling each other. The rule that pays
for everything else: one write spine, many readers.

## When to run

- A task splits into research, scanning, testing, or grading that can run at once.
- More than one agent will touch the same repository in the same window.
- You are tempted to let two agents write code in parallel. Read this first.

## The chain

1. [leap-protocol](../skills/leap-protocol/SKILL.md) — decompose the work into balls
   with goals, specs, and hard file scopes BEFORE any agent spawns.
2. Spawn readers, not writers — fan out subagents ONLY for read-heavy work with few
   cross-dependencies: research, test-running, security scans, grading. Never for
   interdependent code authoring.
3. Isolate every lane — each parallel agent gets its OWN worktree (a separate
   checkout of the same repo). Conflicts then surface at merge as real merge
   conflicts, never as silent overwrites that lose data with no warning.
4. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — every lane runs
   its own quality gauntlet inside its own worktree before it asks to land. Dry-run
   first so the lane knows its own cost. No lane lands on another lane's green.
5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — the reviewing agent gets a
   CLEAN context, never the author's. Shared context rots and self-agrees.
6. Merge one lane at a time, in a dedicated merge workspace, test-gated by exit code.

## Coordination rules

- ONE agent writes code per workspace, in one coherent context. Parallel writers
  make conflicting implicit decisions that no merge can reconcile.
- Declare per-agent file ownership up front. Each agent edits ONLY its named files.
- Coordinate through a tracker (issues, tickets) — never a shared checklist file in
  the working tree. That file is itself a merge-conflict surface and causes two
  agents to grab the same task.
- Each subagent returns a distilled summary — key facts, decisions, open items, a
  page or two — never its full transcript.
- Persist the plan, spec, and decisions to disk and re-read them. Long runs compact
  context and silently drop instructions; rules that must always apply live in the
  always-loaded file, nowhere else.

## Merge discipline

- Test-gate EVERY merge by exit code before it lands. A red suite blocks the merge.
  This alone cuts agent-caused breakage by most of it.
- Merge in a dedicated merge workspace, then stat-verify the result: file counts,
  diffstat, each lane's named files present. A merge that silently drops a lane's
  files is the cardinal bad merge — check for it every time.

## Hard gates — any one fails the play

- Two agents writing code in the same workspace at the same time.
- A lane editing outside its declared file scope.
- A merge landed without a green exit code, or without stat-verification.
- A reviewer that shared context with the author.
- A lane landing on another lane's test results, or mocking the seam it changed.
