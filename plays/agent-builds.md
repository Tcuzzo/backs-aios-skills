# Agent Builds

How to build an agent or service that acts on its own. The core idea: deterministic
primitives do the heavy lifting; the model reasons only where reasoning is the only
thing that works. A design that is all-LLM with zero primitives is invalid.

## When to run

Building any agent, bot, worker, or long-running service — anything that holds
tools, calls networks, or takes actions without a human watching every step.

## The chain

1. [prose-is-the-spec](../skills/prose-is-the-spec/SKILL.md) — read the ask whole;
   the mission and its limits come from the human's own words.
2. [understanding-gates](../skills/understanding-gates/SKILL.md) — at the design
   stage, name the DOMAIN PRIMITIVES first: every core capability is a
   deterministic, offline, fail-closed function. Reserve the LLM slot for genuine
   reasoning only.
3. [red-first](../skills/red-first/SKILL.md) — commit failing contract tests for
   each typed IO boundary before building it.
4. Build to the doctrine below. Keep every loop inside
   [bounded-loops](../skills/bounded-loops/SKILL.md): budgets, checkpoints,
   backoff, and a loud kill-switch — never a hammering retry.
5. [sniper-testing](../skills/sniper-testing/SKILL.md) — only the outbound
   transport may be mocked — never routing, prompt-building, or parsing.
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — the agent's tool
   handlers and decision functions pass the gauntlet: risk score under your
   ceiling, then mutation over the decision paths to zero survivors. Branch logic
   that survives a flipped comparison was never really tested.
7. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — cross-family graders pass
   the agent before it ships. The builder never grades its own work.

## The doctrine (what the build must satisfy)

- Every IO boundary declares a typed contract (inputs → outputs) and FAILS CLOSED —
  raise or deny on bad input. Never fail open, never swallow an error.
- Every network seam is cassette-testable: wrap outbound calls behind a
  record/replay seam so the suite runs offline against fixtures.
- All egress passes an explicit deny-by-default hostname allowlist. An unknown host
  raises; it never silently connects.
- Model the agent as a typed event stream / state machine with deterministic
  sign-off states (draft → review → ready → done) the agent computes for itself —
  a primitive, not human friction. No action may skip its state.
- Confirm ONLY genuinely destructive or irreversible actions (spend, delete, an
  external send that cannot be undone) against committed state before firing.
  Never gate a benign or read-only action, and never gate the human — see
  [ask-me-bar](../skills/ask-me-bar/SKILL.md).
- Persist durable state (objectives, decisions, ledger) on disk OUTSIDE the context
  window and re-read it. Never trust in-context memory across a long run.
- Ship an operating doc the agent loads before every task — nearest file wins,
  size-capped — carrying the must-always-apply rules.
- Tool failures return a structured error to the reasoning slot for
  self-correction. A swallowed tool error is a bug.
- Least privilege: the agent carries exactly the tools its mission needs — no
  ambient filesystem or network authority.

## Hard gates

- Zero primitives = invalid design; go back to step 2.
- Any fail-open boundary, silent fallback, or swallowed error blocks the ship.
- Mutation survivors in decision paths block the ship.
- Cross-family grade must pass; builder is never the grader.

## Works well with

- [root-cause-first](../skills/root-cause-first/SKILL.md) — when the agent misbehaves
- [session-handoff](../skills/session-handoff/SKILL.md) — durable state done right
