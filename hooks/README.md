# Grounding loader

The existing Node and Python hooks deliver the actual Optimus, Yoke and Build Flow bodies,
plus the proven native harness when available. They do not refuse tools.

Claude/Codex hook events use `hookSpecificOutput.additionalContext`; Cursor uses
`additional_context`. OpenCode uses its system-context transform to merge the
floor into the leading system block. The tool callbacks preserve availability.

Session start, resume and compaction reload context without erasing earned
receipts. If a matched tool arrives without a session marker, the native hook
loads the floor automatically. Read-only tools remain unchanged.

Build Flow routes optional operator-essence assessment; the deterministic hook does
not scan operator history or invoke an insights model.

## Evidence

The floor marker and its `.load.json` companion are written after delivery. The
receipt binds the session, source paths and SHA-256 of each emitted body. It is
context-delivery evidence, separate from the CO Skill-event state and hashes.
An unavailable body produces a diagnostic without a false loaded marker.

## Explicit loading

```bash
node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
```

The Python alternative is `hooks/aios_gate.py`. Pass the active session ID as the
last argument when the host hook and shell may supply different identities. In
Codex this is `"$CODEX_SESSION_ID"`. `--rearm <session_id>` requests another load;
it does not impose a permission check. Unknown skills and explicit-loader errors
exit nonzero. Hook failures warn and leave tools available.

The operator's existing `AIOS_GATE=off` switch (also `0`, `false`, `no`) still
turns automatic loading off with a diagnostic. No new approval or switch is
required to work.

## Bounded Codex Stop continuation

`Stop` is registered with the same hook and delegates to
`codex_stop_continuation.py`, which imports the deployed DurableRunStore. A
build flow explicitly binds one run with `python hooks/codex_stop_continuation.py
bind-task-packet RUN_ID < task-packet.json`. The packet carries the
session/workspace/scope,
checkpoint, absolute deadline, cumulative call/cost use and ceilings, and stall
state. Rebinding may advance progress and cumulative use; it cannot refill or
change the original identity and limits.

Each native `turn_id` is a distinct callback identity; replay of the same turn
is idempotent. The adapter consumes the previous pending callback when the next
checkpoint is bound, retains `ProgressBudget` signature history, and separately
bounds callbacks by the provider-call allowance remaining at first bind. Unknown
cost stays unknown while known call and deadline ceilings remain enforced. The
bound run read/modify/write is protected by a per-run process lock.

Only an unfinished, progressing, unexpired run in that same session and working
directory returns native `{decision:"block"}`. Completion, operator stop,
cancellation, expiry, stall, exhaustion, duplicates, ambiguity, and malformed
state all allow Stop and persist or emit the truthful reason. The continuation
prompt names only the bound run, checkpoint, next action, and limits; transcript
content is never copied into it. The adapter does not call a provider or create
a worker. The Python and Node host hooks both delegate to this same adapter.
