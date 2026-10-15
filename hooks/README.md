# Grounding loader

The existing Node and Python hooks deliver the actual Optimus and Yoke bodies,
plus the proven native harness when available. They do not refuse tools.

Claude/Codex hook events use `hookSpecificOutput.additionalContext`; Cursor uses
`additional_context`. OpenCode uses its system-context transform to merge the
floor into the leading system block. The tool callbacks preserve availability.

Session start, resume and compaction reload context without erasing earned
receipts. If a matched tool arrives without a session marker, the native hook
loads the floor automatically. Read-only tools remain unchanged.

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
