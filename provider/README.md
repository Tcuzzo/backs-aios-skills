# Provider authentication repair

`backs-provider ollama` is a configuration change for a **new local** Claude Code
process. `/provider ollama` calls the same controller when the current agent can
still execute skills. A broken login needs the terminal command instead.

## Credential handoff

The installer records the workspace and Python interpreter as local metadata.
Both the command and Claude's `apiKeyHelper` use that launcher. The helper no
longer relies on the IDE inheriting an activated terminal virtual environment.
The credential still comes from the existing BACKS `load_runtime_env` and
`env_secret_text` functions. No `.env` key is copied into provider configuration.
Backend import output and exceptions are withheld from the helper output.

Before activation the controller invokes the **installed** helper and makes one
small `/v1/messages` request for each distinct selected model (up to four,
64 output tokens each). These checks use inference quota. A successful catalog
lookup by itself is not authentication/inference validation. Rejected checks
leave existing Claude configuration unchanged. HTTP response bodies and tokens
are not printed, and authenticated redirects are not followed.

## Configuration and rollback

Ollama activation sets empty overrides for stale API/auth/OAuth environment
values and installs the helper at both user and project-local precedence. It
preserves the prior owned values for `backs-provider claude`. The shared project
settings file, hooks, `.env`, primary BACKS deployment, and OAuth credential store
are not rewritten. Explicit managed login restrictions are not bypassed.

Each JSON write uses atomic replacement. Ordinary write failures are rolled
back. Multiple files are **not** a crash-atomic transaction; saved baselines are
written first so an interrupted activation retains recovery information.

`backs-provider status` describes saved configuration, not an active IDE request.
`backs-provider doctor` tests helper + Messages API without changing settings.
The final end-to-end check is a response in a new local Claude Code IDE chat.
A cloud/Remote Control subscription session is not converted to Ollama by a local
configuration change. Native Claude authentication also remains subject to the
account's permissions; restoring configuration is not an OAuth entitlement test.

## Model alternatives

The profile's alternatives are selection fallbacks when catalog models are
absent, not automatic retry after a live model request fails. This repair does
not introduce an OAuth proxy or request-time failover.
