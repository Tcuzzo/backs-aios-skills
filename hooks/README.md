# The grounding gate

The pack's floor, made structural: a rule an agent must remember fails exactly
when the agent is busiest — so this gate is programmed, not prompted.

The gate runs in one of three modes depending on the host:

1. **Native hook mode** — Claude Code (`hooks/hooks.json`) and Cursor
   (`hooks/cursor-hooks.json`) call `hooks/aios_gate.js` through their native
   pre/post tool lifecycle events.
2. **OpenCode adapter mode** — OpenCode loads
   `~/.config/opencode/plugins/backs-aios.js`, an ESM adapter that registers
   `tool.execute.before` and `tool.execute.after` callbacks and calls the same
   shared JavaScript gate evaluator. It does not edit `opencode.json`.
3. **Explicit loader mode** — Codex and any host without a native skill event arm
   by running the gate script directly, for example:
   ```bash
   node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
   ```
   Python alternate:
   ```bash
   python3 "$HOME/.local/share/backs-aios/current/hooks/aios_gate.py" --load backs-aios:optimus
   ```

The script has two behavior-identical implementations: `aios_gate.js` (Node, the
default in `hooks.json` and `cursor-hooks.json`) and `aios_gate.py` (Python, the
alternate). Node is the default because Claude Code itself runs on Node — so Node
is guaranteed present wherever the plugin installs; Python is not. Same state
files, same deny JSON, same mutating-verb pattern, same kill-switch.

To swap a native hook config to Python, change each command line in `hooks.json`
in one move:

    sed -i 's|node "${CLAUDE_PLUGIN_ROOT}/hooks/aios_gate.js"|python3 "${CLAUDE_PLUGIN_ROOT}/hooks/aios_gate.py"|' hooks/hooks.json

## Native hook mode

- Every session starts RED.
- While RED, the gate denies the file-edit tools (`Edit`, `Write`,
  `NotebookEdit`, `MultiEdit`) and the primary mutating shell verbs run through
  `Bash`, with one plain line:
  `Load the floor first — run /optimus. Set AIOS_GATE=off to disable.`
- Read-only tools (read, grep, search, fetch) always pass. The agent grounds
  itself freely while RED.
- Invoking any pack skill or command via the Skill tool flips the session
  GREEN (`PostToolUse` / `postToolUse` on `Skill` writes a session-scoped state
  file under `~/.aios/state/`). From then on, edits pass.

Claude Code uses `hooks/hooks.json` and its `PreToolUse` / `PostToolUse` JSON.
Cursor uses `hooks/cursor-hooks.json` and its native `preToolUse` / `postToolUse`
JSON. Both configs call the same script, which emits the response shape required
by the event it received.

## The boundary — what it blocks, what it never blocks

While RED the gate covers the file-edit tools and these shell verbs at a
command position: `git commit` / `git push`, `rm`, `mv` or `tee` onto a
tracked-looking path (anything outside `/tmp` and `/dev`), `sed -i`,
`npm` / `pip` / `cargo install`, `systemctl` / `service ... restart`,
`chmod` / `chown`, and `>` redirection into a non-`/tmp` path.

It deliberately never blocks:

- read-only tools — read, grep, glob, search, fetch;
- read-only shell — `ls`, `cat`, `grep`, `git status` / `diff` / `log`,
  `echo` without redirection, and any command matching no mutating verb.

This is a positive-pattern grounding gate, not a sandbox: deny fires only on a
positive match, so an exotic mutation may slip past the pattern, but grounding
work is never blocked. Do not claim matcher parity across hosts or complete
mutation coverage.

## Why it exists

The pack's method is "load the floor before you work." Left as advisory text,
agents skip it under pressure and edit from instinct. The gate turns the advice
into a deterministic check that runs before every mutating tool call. It forces
grounding — it is not a sandbox and not an approval gate.

## Kill-switch

`AIOS_GATE=off` (also `0`, `false`, `no`) disables the gate entirely. The
capability defaults ON; the switch is loud, reversible, and the only escape.

## Error semantics

- **Native hook mode and OpenCode adapter mode:** parsing or runtime errors warn
  loudly and allow the call. A broken hook must never brick a session.
- **Explicit loader mode:** `--load` and `--rearm` errors are loud and exit
  nonzero. Unknown skills return nonzero and do not arm. The kill switch
  (`AIOS_GATE=off`) remains a loud allow.

Do not claim that all errors fail open. Hook-mode and adapter-mode errors are
allowed; explicit-loader errors are not.

## Re-arm per job

Native session-start events rearm the emitting host. A new job, handoff, context
reset, or compaction does NOT automatically rearm unless the host emits a real
sessionStart event. To demand a fresh floor load across those boundaries, use the
explicit gate loader:

```bash
node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --rearm <session_id>
```

Python alternate:

```bash
python3 "$HOME/.local/share/backs-aios/current/hooks/aios_gate.py" --rearm <session_id>
```

Both runtimes share the same state files, so either re-arms the session.
Without an id it resolves the session through the supported environment identity
first, then falls back to the parent PID.
