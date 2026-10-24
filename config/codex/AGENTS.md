<!-- BACKS-AIOS-CODEX-MANAGED:START -->
## BACKS AIOS operating instructions

At the start of each Codex task, load the installed `optimus` and `invariant-floor` skills before changing code. Read their full `SKILL.md` bodies from the active BACKS AIOS plugin or the managed Codex skill directory; do not rely on a remembered summary. Apply `human-calibration` and `yoke` when the task affects the operator's workflow or presentation. Select and load the other BACKS AIOS skills that match the job, including `repo-map` for an unfamiliar repository, `root-cause-first` and `repair-loop` for a reported defect, `red-first` and `sniper-testing` for a fix, and `secure-delivery` for publication.

For an ambiguous request, use `operator-intent-deduction` before handing a decision to the operator and `context-engineer` when compiling task context. Preserve the operator's latest correction over generic process instructions. Keep changes in the intended repository and verify the real path before reporting completion. Never report that a skill or hook ran when only its metadata was discovered. A missing or failed hook is a visible diagnostic, never a reason to hide the failure or block the operator's tools.

When BACKS AIOS files have been refreshed, start a new Codex task to load the new skill list. A running task retains the skill context it already received. The local plugin's lifecycle hooks require Codex's explicit trust review; if not trusted or unavailable, use the installed skills and explicitly load `optimus` with `node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus`. Surface a loader failure instead of pretending it ran.
<!-- BACKS-AIOS-CODEX-MANAGED:END -->
