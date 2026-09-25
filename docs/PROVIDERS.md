# Claude Code provider control: Claude, Ollama, MiniMax

This is the existing BACKS `/provider` switch, extended with MiniMax. It uses the same launcher, isolated updater, BACKS environment resolver, and global/project skill links. It does not replace the primary BACKS runtime or reroute the backend orchestration fleet.

## Update an existing provider installation

In a regular terminal, including the VS Code integrated terminal:

```bash
"$HOME/.local/bin/backs-provider" update && "$HOME/.local/bin/backs-provider" minimax
```

In an already authenticated local Claude Code chat:

```text
/provider update
/provider minimax
```

Run those chat commands separately. Then restart the terminal Claude Code process. In VS Code, run **Developer: Reload Window** and open a **new local Claude Code chat**. An existing conversation is not hot-switched.

`claude update`, a VS Code extension update, and a general skills-plugin update are not the provider-control updater. `/provider update` refreshes the checkout, validates its candidate in an isolated test environment, then reruns `install-provider.sh`. The installer updates both skill links and installs the MiniMax helper alongside the existing Ollama helper. It does not run the general `install.sh --target all` installer.

This integrates with the **Claude Code** VS Code extension, not Copilot Chat or Codex chat. A cloud/Remote Control subscription session is not converted to a third-party API session.

## Credentials and first activation

MiniMax must already be configured as `MINIMAX_API_KEY` in the existing BACKS environment or its supported secret resolver (`MINIMAX_API_KEY_FILE` or the `minimax_api_key` credential name). The helper reuses the bound BACKS project and Python interpreter. Do not duplicate the key in Claude settings, another key store, source code, or a chat prompt. Do not run `mmx-cli agent setup` over this managed configuration.

A missing MiniMax credential never falls back to the Ollama key. The default endpoint is `https://api.minimax.io/anthropic`; an explicit `BACKS_MINIMAX_BASE_URL=https://api.minimax.cn/anthropic` selects the official China endpoint. Other hosts, paths, embedded credentials, query strings, and redirects are rejected.

Activation makes two small inference requests per distinct selected MiniMax model: a streamed tool call and a tool-result response. They use the provider's quota. The tool is a fixed local echo with no system actions. A failed request, incomplete stream, wrong tool call, or unsuccessful result prevents settings activation. There is no silent downgrade or automatic retry across providers.

## One command switches the lineup

```text
/provider claude
/provider ollama
/provider minimax
```

The MiniMax profile selects **MiniMax-M3** for the main model, Opus/Sonnet/Haiku aliases, and subagents. Claude Code receives `MiniMax-M3[1m]` and the documented 1,000,000-token auto-compaction window. Probe requests use the raw API model ID without the Claude Code context suffix.

Switches preserve the original Claude baseline across either alternate provider and restore provider-owned settings before applying the next profile. Unrelated hooks, MCP configuration, and user preferences survive. OAuth credentials and the BACKS environment are not edited.

The model preferences, supported alternatives, and context windows live in `provider/profiles/minimax.json`, not in a fixed Python model ladder. They refresh through `/provider update`. `BACKS_MINIMAX_PROFILE` may point to an operator-maintained JSON profile with the same schema. Selected models still require successful inference; listing a model does not prove account access.

## Inspect or verify

```text
/provider status
/provider models minimax
/provider doctor minimax
```

`models` and `doctor` without a provider inspect the saved alternate provider; they default to Ollama when no alternate is active. MiniMax's model list is its documented compatibility list, **not** account discovery. No undocumented catalog endpoint is invented. Listed alternatives are not request-time fallback.

`status` reports saved configuration and the last activation's preflight outcome. It does not inspect the running Claude Code process. `doctor` makes real API checks without changing settings; after activation it checks the saved role selection. It is not proof that the user's IDE has restarted or adopted the profile.

After restarting Claude Code, use its `/status` and `/model` to inspect the actual session. For MiniMax, expect the MiniMax Anthropic endpoint and MiniMax-M3.

## Inherited environment

Shell/VS Code environment variables can override settings. The launcher warns when it detects inherited Anthropic routing/authentication variables. A child command cannot unset a parent process's environment. Clear conflicting exports from the shell that launches Claude Code or VS Code and restart that process; do not print their values. Managed organization policy is never overwritten.

## Validation and limits

```bash
python3 -I -B provider/run_provider_tests.py .
```

The MiniMax tests exercise the actual installed shell helpers, real filesystem snapshots/restoration, CLI dispatch, and real HTTP/SSE against a local fixture server. The production HTTPS allowlist is tested separately. These tests are not a live MiniMax service check or a graphical VS Code session test. Live service checks run during activation/doctor using the operator's existing key; final IDE proof requires the user's restarted local chat.

## Official integration references

- [MiniMax Claude Code setup](https://platform.minimax.io/docs/token-plan/claude-code)
- [MiniMax Anthropic compatibility and supported models](https://platform.minimax.io/docs/api-reference/text-anthropic-api)
- [Claude Code VS Code provider configuration](https://code.claude.com/docs/en/vs-code#use-third-party-providers)
