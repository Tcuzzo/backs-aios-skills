---
name: provider
description: Switch the entire Claude Code provider lineup between native Claude OAuth and the BACKS Ollama model pool, inspect status, show resolved fallbacks, or update BACKS.
argument-hint: "[claude|ollama|status|models|update]"
disable-model-invocation: true
allowed-tools: Bash(python3 *)
---

Treat `$ARGUMENTS` as exactly one provider action: `claude`, `ollama`, `status`, `models`, or `update`.
If it is empty, use `status`. Reject any other value.

Execute the BACKS provider controller:

```bash
python3 "$HOME/.local/share/backs-aios/current/provider/backs_provider.py" "$ARGUMENTS"
```

Semantics:

- `ollama` discovers the current Ollama catalog and resolves the whole Claude model-family lineup from ordered role preferences in one atomic settings transaction.
- `claude` restores only BACKS-managed provider settings and returns Claude Code to the user's existing Anthropic/Claude OAuth path. Never log out, inspect, print, copy, or modify Claude OAuth credentials.
- `status` reports the active provider and selected role mappings without exposing custom/private endpoint hostnames.
- `models` shows the currently discovered Ollama selections and ordered fallbacks. It does not change provider state.
- `update` fast-forwards the managed BACKS source from GitHub, reruns installation, and executes provider safety tests.

Do not perform per-model provider switching here. `/provider` is the control plane for the whole lineup.
Never print `OLLAMA_API_KEY`, Claude credentials, key-file contents, or secret-bearing environment values.
