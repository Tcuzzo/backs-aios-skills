---
name: optimus
description: Boot the harness and Build Flow, then apply the skills needed for the current task.
---

Load `skills/optimus/SKILL.md` using
`${CURSOR_PLUGIN_ROOT}/skills/optimus/SKILL.md`
(`${CURSOR_PLUGIN_ROOT}` is the managed runtime root), then run
its boot sequence now.

For hosts without a native context hook, use the explicit loader to deliver the
Optimus, Yoke, and Build Flow bodies:

```bash
node "${CURSOR_PLUGIN_ROOT}/hooks/aios_gate.js" --load backs-aios:optimus
```

Python alternate:

```bash
python3 "${CURSOR_PLUGIN_ROOT}/hooks/aios_gate.py" --load backs-aios:optimus
```

Apply Build Flow's existing task packet and operator essence, readiness to act,
bounded RED/GREEN loop, scoped lint/tests, clean-code gauntlet, and requested delivery.
Reuse current evidence and actual loaded bodies; do not restart nested workflows.

Read the required foundations before editing. The loader records actual delivered
bytes; missing files report a diagnostic without denying tools or inventing a receipt.
A named skill alone is not evidence that its method ran.
