---
name: secure-delivery
description: The ship gate for anything a customer or another machine will run — secrets, egress, lethal trifecta, taint, sandbox.
argument-hint: the repo, agent, or app about to ship
---

Load the bundled `plays/security-delivery.md` using `${CLAUDE_PLUGIN_ROOT}/plays/security-delivery.md` in Claude Code or `${CURSOR_PLUGIN_ROOT}/plays/security-delivery.md` in Cursor, then execute it, whole, on: $ARGUMENTS

Order: secret gate (verified-only scan) → egress lockdown (deny by default, canonicalize hostnames before allowlist match) → break the lethal trifecta (private data, untrusted content, external comms — at least one always missing) → taint tracking on untrusted input → sandbox run before ship.

Hard gate: one confirmed-live credential, one open egress path, or one execution path holding all three trifecta legs fails the delivery. No exception.
