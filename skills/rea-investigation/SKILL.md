---
name: rea-investigation
description: Use REA to investigate a shipped executable, package, or observed runtime when its behavior is needed to diagnose or repair a failure.
license: MIT
---

# REA artifact investigation

Use the installed REA engine and its matching standalone skill for investigations
of shipped binaries, packages, or requested runtime behavior. For ordinary source
repositories, use source and tests directly. This bridge does not install REA,
Ghidra, a provider, or an MCP server and does not assert they are available.

1. Resolve the exact target and the question. Read the installed upstream REA
   skill and its relevant references from the host's agent skill directory; avoid
   recursively selecting this bridge. If it is unavailable, say so and continue
   useful investigation through available tools.
2. Use the connected REA tools where available, or the installed REA CLI. For
   native binary analysis, use an existing compatible Ghidra provider where
   supported; report a missing or unavailable provider rather than inventing a
   result or installing dependencies without authorization.
3. Start with read-only static inspection. Record target identity, evidence IDs,
   scope, limits, and unknowns. Static findings do not prove runtime behavior;
   perform live observation only within the user's requested scope and the
   declared tool's execution and mutation boundaries.
4. Carry findings into root-cause-first and repair-loop. For an open-source
   capability adoption, invoke absorb and its license and dependency checks.
   Resolve dispatch by role and capability through the configured fleet-ladder;
   never hardcode model identifiers. For independent assessment, use the
   blind-tribunal's fresh author-disjoint execution and author-redacted packet,
   subject to the capabilities actually provided by the host runtime.

Scaffold: REA by morluto, MIT license, https://github.com/morluto/rea.
The engine, upstream skill, and providers are separate installations.
