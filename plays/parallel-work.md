# Play: Parallel Work

How to fan work across agents without them trampling each other. The rule that pays
for everything else: one write spine, many readers.

## When to run

- A task splits into research, scanning, testing, or grading that can run at once.
- More than one agent will touch the same repository in the same window.
- You are tempted to let two agents write code in parallel. Read this first.

## Shared task and limits

Apply this play inside the current [BACKS Build Flow](../skills/backs-build-flow/SKILL.md)
task packet. Keep one integration owner, the requested `task_mode`, pinned base
and candidate revisions, operator essence, and current evidence. Reuse applicable
loaded skill bodies; this play adds its domain gates without restarting the task.

[bounded-loops](../skills/bounded-loops/SKILL.md) owns the original deadline and
remaining allowances across retries, workers, models, reviews, and handoffs.
Never reset them for a nested play. On exhaustion, checkpoint **STILL-BUILDING**
with the candidate, evidence, unmet gates, and next action. Continue useful
authorized work only within its remaining allowance; no missing gate becomes a pass.

## The chain

1. [leap-protocol](../skills/leap-protocol/SKILL.md) — decompose the work into balls
   with goals, specs, and hard file scopes BEFORE any agent spawns. Give each lane
   the current packet, pinned base/candidate, RED seals, and allocated remaining
   allowance. A lane's limit cannot extend the parent mission deadline or totals.
2. Spawn readers, not writers — fan out subagents ONLY for read-heavy work with few
   cross-dependencies: research, test-running, security scans, grading. Never for
   interdependent code authoring.
3. Isolate every lane — each parallel agent gets its OWN worktree (a separate
   checkout of the same repo). Conflicts then surface at merge as real merge
   conflicts, never as silent overwrites that lose data with no warning.
4. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — every lane runs
   its quality gauntlet inside its permitted worktree/isolation before landing.
   Use [sniper-testing](../skills/sniper-testing/SKILL.md) first for actual repo
   lint/type/test commands scoped to the pinned aggregate candidate diff; name
   missing or N/A checks. Reuse a valid receipt for exactly the same candidate and
   check scope; never reuse another lane's green for different bytes. Missing
   test coverage gets a separate supplemental file, preserving sealed originals.
5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — the reviewing agent gets a
   CLEAN context, never the author's. Shared context rots and self-agrees.
6. Merge one lane at a time, in a dedicated merge workspace, test-gated by exit code.
   The integration owner verifies the combined candidate, affected consumers, and
   required full affected-suite landing gate; independent lane passes alone do not
   prove their composition. Delivery claims require the real target evidence.

## Coordination rules

- ONE agent writes code per workspace, in one coherent context. Parallel writers
  make conflicting implicit decisions that no merge can reconcile.
- Declare per-agent file ownership up front. Each agent edits ONLY its named files.
- Coordinate through a tracker (issues, tickets) — never a shared checklist file in
  the working tree. That file is itself a merge-conflict surface and causes two
  agents to grab the same task.
- Each subagent returns a distilled summary (key facts, decisions, open items, a
  page or two), never its full transcript.
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

**Weight:** heavy by design — leap decomposition, a gauntlet per lane, and a clean-context tribunal; the spend pays only when the work is big enough to split, which is the only time to run this play.
