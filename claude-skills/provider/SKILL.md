---
name: provider
description: Configure Claude, Ollama, or MiniMax for the next local Claude Code terminal or VS Code session, verify real API requests, list models, or update provider control.
argument-hint: "[claude|ollama|minimax|status|models [ollama|minimax]|doctor [ollama|minimax]|update]"
disable-model-invocation: true
allowed-tools: Bash
---

Validate arguments against this exact grammar before running anything:

- No argument means `status`.
- One argument: `claude`, `ollama`, `minimax`, `status`, `models`, `doctor`, or `update`.
- Two arguments: `models ollama`, `models minimax`, `doctor ollama`, or `doctor minimax` only.
- Reject everything else, especially internal credential actions. Do not interpolate arbitrary text into a shell.

Execute the installed launcher with only the validated literal arguments:

```bash
"$HOME/.local/bin/backs-provider" status
```

Replace `status` above only with a validated action and optional literal provider.
The launcher supplies the saved BACKS project and Python interpreter used by the IDE credential helper.

- `minimax` resolves `MINIMAX_API_KEY` through the existing BACKS environment, tests real streaming tool use and a tool-result round trip, then switches the whole lineup. The shipped profile selects MiniMax-M3 for main, Opus/Sonnet/Haiku aliases, and subagents. Checks use MiniMax inference quota; a failed check must not be called success.
- `ollama` checks its installed credential helper and makes minimal real Messages API requests to selected models before saving the complete profile. These checks use Ollama inference quota.
- `claude` restores the original provider configuration across either alternate provider, not an authentication guarantee. Never change the OAuth credential store.
- `status` reports saved configuration and saved preflight results, not the running model's transport.
- `models` and `doctor` use the saved alternate provider, or Ollama when none is active. An explicit `minimax` or `ollama` argument selects which one to inspect.
- MiniMax's model list comes from its documented compatibility list, not account entitlement discovery. `models` does not test inference or guarantee request-time fallback.
- `doctor` tests the installed helper and real Messages API without changing settings. MiniMax additionally tests streaming and tool-result handling.
- `update` refreshes provider code, profiles, helpers, and this skill through the existing validated updater. It does not replace the primary BACKS runtime.

Start a new local Claude Code process after switching. In VS Code, run Developer: Reload Window, then open a NEW LOCAL Claude Code chat. An existing session is not hot-switched. Updating Claude Code itself or the general skills plugin alone does not update the separate provider-control installation.

The shared Claude Code settings and project overlay cover the CLI and Claude Code VS Code extension, not Copilot, Codex chat, or a cloud/Remote Control subscription session. An unauthenticated chat cannot run this skill; use the terminal launcher instead.

Inherited shell or VS Code Anthropic environment variables may override saved settings. Follow the launcher's warning; never claim a saved profile changed the running process. Never run the MiniMax setup wizard over this managed configuration.

Never run `__key` or `__minimax_key`, print credentials, read a key file aloud, or copy `.env` values. Never change managed organization policy. Preserve unrelated hooks, MCP settings, and user preferences.
