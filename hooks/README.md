# The grounding gate

The pack's floor, made structural: a rule an agent must remember fails exactly
when the agent is busiest — so this gate is programmed, not prompted.

- Every session starts RED.
- While RED, the gate denies the file-edit tools (`Edit`, `Write`,
  `NotebookEdit`, `MultiEdit`) and the primary mutating shell verbs run through
  `Bash`, with one plain line:
  `Load the floor first — run /optimus. Set AIOS_GATE=off to disable.`
- Read-only tools (read, grep, search, fetch) always pass. The agent grounds
  itself freely while RED.
- Invoking any pack skill or command via the Skill tool flips the session
  GREEN (`PostToolUse` on `Skill` writes a session-scoped state file under
  `~/.claude/state/`). From then on, edits pass.

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

The bias is fail-open: deny fires only on a positive match, so an exotic
mutation may slip past the pattern, but grounding work is never blocked. The
kill-switch (`AIOS_GATE=off`) disables the whole gate, loudly.

## Why it exists

The pack's method is "load the floor before you work." Left as advisory text,
agents skip it under pressure and edit from instinct. The gate turns the advice
into a deterministic check that runs before every mutating tool call. It forces
grounding — it is not a sandbox and not an approval gate.

## Kill-switch

`AIOS_GATE=off` (also `0`, `false`, `no`) disables the gate entirely. The
capability defaults ON; the switch is loud, reversible, and the only escape.

## Fail-open, always

Any script error — malformed payload, unreadable state dir, anything — prints
one warning to stderr and allows the call. A broken gate must never brick a
session.

## Re-arm per job

To demand a fresh floor load for a new job in the same session:

    python3 "${CLAUDE_PLUGIN_ROOT}/hooks/aios_gate.py" --rearm <session_id>

Without an id it falls back to the parent PID, matching the gate's own fallback.
