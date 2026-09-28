---
name: optimus
description: Boot the harness — load the invariant floor and the skills this job needs before any code. Arms the grounding gate green.
---

Load `skills/optimus/SKILL.md` using
`${CURSOR_PLUGIN_ROOT}/skills/optimus/SKILL.md`
(`${CURSOR_PLUGIN_ROOT}` is the managed runtime root), then run
its boot sequence now.

For hosts without a native skill/hook event, arm the session with the explicit gate
loader before you invoke the skill:

```bash
node "${CURSOR_PLUGIN_ROOT}/hooks/aios_gate.js" --load backs-aios:optimus
```

Python alternate:

```bash
python3 "${CURSOR_PLUGIN_ROOT}/hooks/aios_gate.py" --load backs-aios:optimus
```

Order: load the invariant floor → name the map for this job (files, rules, pack
skills that govern it) → load the human profile if the job touches a human's taste
or surface → invoke the skills the job needs, in real time, in this session.

Hard gate: no code, no mutating command, and no job until the boot sequence completes.
A skill named but not invoked did not happen.
