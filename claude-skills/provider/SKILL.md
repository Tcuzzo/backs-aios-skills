---
name: provider
description: Configure Claude or Ollama for the next local Claude Code session, verify real API requests, list models, or update provider control.
argument-hint: "[claude|ollama|status|models|doctor|update]"
disable-model-invocation: true
allowed-tools: Bash
---

Validate the argument as exactly one of `claude`, `ollama`, `status`, `models`,
`doctor`, or `update`. Empty means `status`. Reject other arguments, especially
internal credential actions. Do not interpolate arbitrary text into a shell.

Execute the installed launcher with that validated literal argument:

```bash
"$HOME/.local/bin/backs-provider" status
```

Replace `status` above only with the validated action. The launcher supplies the
saved BACKS project and Python interpreter used by the IDE credential helper.

- `ollama` checks the installed credential helper and makes minimal real Messages
  API requests to selected models before saving the complete profile. These
  checks use Ollama inference quota. A failing check must not be called success.
- `claude` restores saved provider configuration, not an authentication guarantee.
- `status` reports saved configuration, not the running model's transport.
- `models` lists catalog alternatives; they are not automatic request-time retry.
- `doctor` tests the installed helper and real Messages API without changing settings.
- `update` refreshes provider code without replacing the primary BACKS runtime.

A new local Claude Code process is required after a provider change. This skill
cannot repair an already unauthenticated session or convert a cloud/Remote
Control subscription session to Ollama. Use the terminal launcher in that case.
Never run `__key`, print credentials, read a key file aloud, or copy `.env` values.
Never change managed organization policy or the Claude OAuth credential store.
