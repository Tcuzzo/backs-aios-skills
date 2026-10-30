---
name: fix-shit
description: Diagnose and close a reported failure end to end with a reproducer, root cause, class-level repair, consumer tests, and real-path proof. Use when the operator says fix shit, stop swallowing errors, or finish a stubborn bug.
license: MIT
---

# Fix Shit

Use this as the fast entry point into `root-cause-first` and `repair-loop`.
It is a repair skill, not a permission to hide a failing signal.

1. Name the user's broken behavior and the exact surface where it appears.
2. Build a repeatable red signal from the real path. Trace the input and each
   boundary to find where actual behavior diverges from expected behavior.
3. Identify the root cause and all callers of the broken seam. Preserve the
   original error in logs or the operator-facing state; a fallback may protect
   the app, but it must not turn failure into false success.
4. Make the smallest change that closes the failure class. Add a test that fails
   on the old behavior and covers the seam that failed.
5. Run focused tests, the affected consumers, and the actual app path. Verify
   both the desired result and the explicit failure state. Ask an author-disjoint
   reviewer to inspect the change when available.
6. Report PROVEN or STILL-BUILDING, with the evidence and any remaining red bar.

If the error is intermittent, capture timing and a bounded reproduction rate;
do not infer a cause from one green rerun. For code-location ambiguity, start
with `building-with-backs` and its target check.

## Evidence and independent review

For shipped executables, packages, or requested runtime behavior, invoke
[rea-investigation](../rea-investigation/SKILL.md) and the separately installed `reverse-engineer-anything` skill when its
analysis is useful; use an existing Ghidra provider for supported native targets.
Do not treat static evidence as live behavior or install a missing provider
silently. For adopting an open-source capability, invoke [absorb](../absorb/SKILL.md).
Use [fleet-ladder](../fleet-ladder/SKILL.md) to route by role and capability, never
hardcoded model names. When a tribunal is required, follow
[blind-tribunal](../blind-tribunal/SKILL.md): a fresh author-disjoint execution
reviews an author-redacted frozen packet.
Report any missing resolver, reviewer, or evidence as a runtime gap.
