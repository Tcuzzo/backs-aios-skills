# BACKS IDE provider control

`backs-provider` controls the next local Claude Code session. Installation does
not select a provider, edit Claude settings, load a model or start a listener.
Existing chats retain their configuration until restarted normally.

| Action | Result |
| --- | --- |
| `claude` | Restore the saved native Claude configuration |
| `ollama` | Check and select the configured Ollama cloud profile |
| `minimax` | Check and select the configured MiniMax profile |
| `needle`, `kev`, `jev`, `fleet` | Select the gateway's **Automatic** picker |
| `status` | Report saved configuration; this is not inference proof |
| `models`, `doctor` | Inspect/check the selected provider |
| `serve --config FILE` | Run an owned portable Anthropic gateway until interrupted |

`jev` remains a compatibility command alias. Kev System One is the local typed
runtime; it is not OpenRouter's Jev service. The gateway records which runtime
actually supplied evidence. Neither component executes tools or grants authority.

## Install into an ordinary project

```bash
bash install-provider.sh /path/to/project
python3 scripts/install_typed_decision.py
```

The first command installs the launcher, credential helpers and provider skill.
A native BACKS backend is optional. Existing native projects retain their normal
credential resolver. Ordinary projects use configured environment credentials or
explicit credential-file variables; credentials are never copied into profiles.
The second command installs pinned Needle weights/CPU engine, Kev checkpoints
and measured dependencies in an
isolated user-local release. This measured runtime supports Linux x86_64 and
Python 3.12. Windows packs carry the source assets; native Windows CPU inference
has not been verified. Other existing host capabilities remain available.

## Native gateway

```bash
backs-provider needle
```

The configured gateway's `/api/system/needle_engineer_rungs` supplies discovery;
`BACKS_ANTHROPIC_GATEWAY_URL` overrides its URL. In a native checkout the existing
in-process resolver remains available. Activation selects `backs/claude-auto`,
so each Automatic request reaches routing instead of freezing a concrete model.
Explicit provider switches are operator actions; installation never performs one.

## Portable gateway

The packaged `provider/portable.example.json` is the default runtime configuration.
Use `--config FILE` to supply explicit overrides.
Without an `upstream` override, the gateway reads the existing Claude settings,
endpoint, selected model and credential helper. An optional `routes` object maps
`plan`, `build` and `work` to explicitly configured provider routes. With no such
mapping, all capabilities retain the already selected host provider/model.
An endpoint override uses that route's explicit credential binding
(`api_key_env`, `auth_token_env`, or `api_key_helper`); it never inherits the
previous endpoint's credential or forwards the host's incoming key to it.
Named credential variables resolve from the process environment.

```bash
backs-provider serve --port 0
```

The process prints its owned PID and actual port. It starts no system service and
makes no host configuration changes. To use it in a new Claude process, explicitly
point that process at the printed endpoint and choose `backs/claude-auto`.
`--host` and `--port` accept the operator's binding choice. SIGINT/SIGTERM settle
only this gateway and its owned inference workers.

Automatic requests run CPU Needle similarity and Kev typed decisions through
shared native/plugin policy with one configured eight-second decision budget.
Only the current human task enters routing; separate host reminder blocks and
tool results stay in the original upstream payload without becoming the task. A cold, busy, unavailable or uncertain component
produces an honest fallback receipt; it does not block the configured provider.
An explicit model request bypasses routing and remains explicit. Messages,
thinking/tool blocks, tool results, token-count requests and streaming responses
use the Anthropic interface. This is the Claude Code consumer; it does not claim
to implement Codex's Responses API.

Receipts record actual provider/model/transport, decision evidence and fallback
reason. They exclude prompts and credentials. The upstream provider still charges
its usual inference quota. Local routing does not turn a paid provider into a
free one.

## Validation

```bash
python3 -m pytest -q tests/test_provider_backend_absent.py tests/test_portable_gateway.py
```

The live runtime tests use real files, real local HTTP and real CPU checkpoints.
Only the paid provider's HTTP transport is replaced in protocol fixtures. Actual
host proof is recorded separately from fixture results.
