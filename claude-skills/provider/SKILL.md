---
name: provider
description: Configure Claude, Ollama, MiniMax, or Needle/Kev Automatic routing through the configured gateway for the next local Claude Code terminal or VS Code session.
argument-hint: "[claude|ollama|minimax|needle|kev|jev|fleet|status|models [ollama|minimax|needle]|doctor [ollama|minimax|needle]|update]"
disable-model-invocation: true
allowed-tools: Bash
---

Validate arguments against this exact grammar before running anything:

- No argument means `status`.
- One argument: `claude`, `ollama`, `minimax`, `needle`, `kev`, `jev`, `fleet`, `status`, `models`, `doctor`, or `update`.
- Two arguments: `models ollama`, `models minimax`, `models needle`, `doctor ollama`, `doctor minimax`, or `doctor needle` only.
- `kev`, `jev` and `fleet` are aliases of the Needle IDE provider-router slot (same live resolve).
- Reject everything else, especially internal credential actions. Do not interpolate arbitrary text into a shell.

Execute the installed launcher with only the validated literal arguments:

```bash
"$HOME/.local/bin/backs-provider" status
```

Replace `status` above only with a validated action and optional literal provider.
The launcher supplies the saved BACKS project and Python interpreter used by the IDE credential helper.

- `needle` / `kev` / `jev` / `fleet` query the configured native or portable gateway via `GET /api/system/needle_engineer_rungs` (or in-process `resolve_engineer_rungs`). Writes the IDE profile to the BACKS Anthropic-format gateway (`ANTHROPIC_BASE_URL` points at BACKS) with discovery ON. Selects `backs/claude-auto`; concrete provider/model decisions remain in the configured runtime. Installation never changes the current provider. The `jev` command is a compatibility alias, not a claim that Kev is Jev.
- `minimax` resolves `MINIMAX_API_KEY` through the existing BACKS environment, tests real streaming tool use and a tool-result round trip, then switches the whole lineup. Checks use MiniMax inference quota; a failed check must not be called success.
- `ollama` checks its installed credential helper and makes minimal real Messages API requests to selected models before saving the complete profile. These checks use Ollama inference quota.
- `claude` restores the original provider configuration across either alternate provider, not an authentication guarantee. Never change the OAuth credential store.
- `status` reports saved configuration and saved preflight results, not the running model's transport.
- `models` and `doctor` use the saved alternate provider, or Ollama when none is active. An explicit `minimax`, `ollama`, or `needle` argument selects which one to inspect.
- MiniMax's model list comes from its documented compatibility list, not account entitlement discovery. Needle `models` lists the configured gateway discovery rows; native gateways use `resolve_engineer_rungs`.
- `doctor` tests without changing settings. Needle doctor checks gateway discovery only, not inference.
- `update` refreshes provider code, profiles, helpers, and this skill through the existing validated updater. It does not replace the primary BACKS runtime.

Start a new local Claude Code process after switching. In VS Code, run Developer: Reload Window, then open a NEW LOCAL Claude Code chat. An existing session is not hot-switched.

Never run `__key` or `__minimax_key`, print credentials, read a key file aloud, or copy `.env` values.

For an ordinary project without a BACKS backend, see `docs/PROVIDERS.md`. The explicit terminal command `backs-provider serve --config FILE` runs the portable Claude Messages consumer; it does not activate a provider or start a permanent service. Do not interpolate arbitrary `/provider` arguments into this command.
