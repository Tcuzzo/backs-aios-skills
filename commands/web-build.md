---
description: Build or extend a web app, site, or API with clean structure and a defended supply chain.
argument-hint: the app, site, or API to build
---

Load ${CLAUDE_PLUGIN_ROOT}/plays/web-app-builds.md and execute it, whole, on: $ARGUMENTS

Order: intent-compiler → understanding-gates (one entrypoint, explicit manifest, committed lockfile) → dependency hygiene BEFORE any install (registry-verify every package, hash-pin from a lockfile) → build → sniper-testing → security pass → blind grade.

Hard gate: no landing with an unverified or unpinned dependency, and no landing until the tests that were red are green.
