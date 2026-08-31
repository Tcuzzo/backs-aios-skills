# Install BACKS AIOS

BACKS AIOS ships one canonical set of 28 Agent Skills, 8 named plays, and 10 command
entry points with native packaging for Claude Code, Codex, Cursor, and OpenCode.
There is no build step and no runtime dependency for the skills themselves.

## Fast path: register every local coding agent

Clone once, then run the installer from the clone:

```bash
git clone https://github.com/Tcuzzo/backs-aios-skills.git ~/backs-aios-skills
cd ~/backs-aios-skills
./install.sh --target all
```

Windows PowerShell:

```powershell
git clone https://github.com/Tcuzzo/backs-aios-skills.git "$HOME\backs-aios-skills"
Set-Location "$HOME\backs-aios-skills"
.\install.ps1 -Target all
```

The Unix installer creates update-friendly symlinks by default; use `--copy` for
positively marked pinned copies. The PowerShell installer creates pinned copies.
Both refuse to overwrite user-owned skills, commands, or plugins. Managed command
adapters and managed copies are marked and may be refreshed safely.
Run a new agent session after installation, then invoke `optimus`.

Supported `--target` / `-Target` values:

| Target | Registration path | What loads it |
| --- | --- | --- |
| `codex` | `~/.codex/skills/<name>/SKILL.md` | Codex CLI, app, and IDE extension; 28 skills + 8 command-skill adapters; arming requires the explicit gate loader — no native Codex skill lifecycle |
| `cursor` | `~/.cursor/plugins/local/backs-aios` | Cursor IDE and Cursor CLI (`agent`); full plugin with skills, commands, and native hook |
| `opencode` | `~/.config/opencode/skills/<name>/SKILL.md` + `commands/*.md` + `~/.config/opencode/plugins/backs-aios.js` | OpenCode terminal and desktop, including all 10 slash commands and the ESM adapter that calls the shared JavaScript gate evaluator |
| `claude` | `~/.claude/skills/<name>/SKILL.md` | Claude Code loads all 36 skills directly; no duplicate legacy commands and no hook; the marketplace plugin adds the hook |
| `portable` | `~/.agents/skills/<name>/SKILL.md` | Agent Skills runtimes, including the 8 play adapters and 2 canonical command equivalents |
| `all` | Every native and portable path above | Claude Code, Codex, Cursor, OpenCode, and Agent Skills runtimes |

Use a translated mirror with `--locale de`, `es`, `fr`, `hi`, `pt-BR`, or
`zh-CN`. Cursor's full plugin remains English because its commands and hook use
stable English invocation keys; skill-only targets use the selected language.

## Claude Code: full plugin

The full Claude Code plugin carries all 28 skills, all 10 slash commands, and the
grounding hook:

```text
/plugin marketplace add Tcuzzo/backs-aios-skills
/plugin install backs-aios
```

Start a fresh Claude Code session and run `/optimus`. The hook starts each session
RED, leaves all read-only tools alone, and blocks mutating agent tools until a pack
skill loads. `AIOS_GATE=off` is the human-owned, loud kill-switch.

Use `./install.sh --target claude` for the same skills without duplicate commands
and without the plugin hook. Use the marketplace plugin when you also want the
grounding hook and namespaced plugin lifecycle.

## Codex: plugin or plain skills

The richer local plugin development flow can point a Codex marketplace entry at this clone and run:

```bash
codex plugin add backs-aios@<marketplace-name>
```

The marketplace name belongs to the local catalog that references the clone; it is not hardcoded by this repository.

For a direct GitHub clone, the portable route is:

```bash
./install.sh --target codex
```

Codex discovers the 28 canonical skill folders plus 8 command adapters on the next
thread. `optimus` and `design-taste` already exist as canonical skills, so all 10
command capabilities are invocable without duplicate adapters. Codex plugins do not
ingest `command-adapters/`; invoke the matching namespaced skill (for example,
`backs-aios:elite-build`).

Codex has no native skill/hook lifecycle in this pack. To arm a Codex session, run
the explicit gate loader against the managed runtime root:

```bash
node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
```

Python alternate:

```bash
python3 "$HOME/.local/share/backs-aios/current/hooks/aios_gate.py" --load backs-aios:optimus
```

The `--load` call prints the skill body and atomically arms the same session marker.
Unknown skills return nonzero and do not arm. There is no `codex --load` CLI flag.

## Cursor IDE and terminal

Cursor supports skills, commands, and hooks in a `.cursor-plugin` bundle. Register
the full bundle with:

```bash
./install.sh --target cursor
```

This creates `~/.cursor/plugins/local/backs-aios` as a symlink to the clone. Restart
Cursor or run **Developer: Reload Window**. In Cursor CLI, start a new `agent`
session. The 28 skills appear in skill discovery, the 10 commands appear in `/`,
and `hooks/cursor-hooks.json` drives the same grounding gate through Cursor's native
lowercase event protocol.

When the GitHub repository is listed in a Cursor marketplace, install it from
**Customize → Plugins** instead of the local-development path.

## OpenCode terminal and desktop

OpenCode discovers one `SKILL.md` per folder and native command markdown from
`~/.config/opencode/commands/`:

```bash
./install.sh --target opencode
```

The installer registers all 10 commands and the ESM adapter at
`~/.config/opencode/plugins/backs-aios.js` (a symlink by default; pinned copies
with `--copy`), and renders play paths against the managed runtime root at
`~/.local/share/backs-aios/current`. The adapter uses
OpenCode's official `tool.execute.before` and `tool.execute.after` callbacks and
calls the shared JavaScript gate evaluator. It does not edit `opencode.json`.
Start a new OpenCode session, then run `/optimus`. OpenCode loads the selected
skill or play on demand.

## Project-local installation

For cloud agents, remote workers, containers, or a team repository, commit the
skills with the project instead of relying on your home directory:

```bash
mkdir -p .agents/skills
cp -R ~/backs-aios-skills/skills/* .agents/skills/
```

Both Cursor and OpenCode discover `.agents/skills`. Cursor also accepts
`.cursor/skills`; OpenCode also accepts `.opencode/skills`; Claude Code accepts
`.claude/skills`; and Codex accepts `.codex/skills`.

## Bare API loops and other coding agents

If a harness does not implement Agent Skills, mount each `SKILL.md` as on-demand
context:

1. Always load `skills/invariant-floor/SKILL.md`.
2. Load one matching play from `plays/`.
3. Match the request against skill descriptions and load only the one to three
   relevant skill bodies.
4. Reload after every context reset.

Do not inject all skill bodies at once. Discovery metadata is cheap; full bodies
are deliberately progressive.

## Update

Symlink installation:

```bash
cd ~/backs-aios-skills
git pull --ff-only
```

Pinned copies (Unix `./install.sh --copy` and PowerShell) intentionally do not
overwrite existing user-owned or unmarked files. Identical reruns are OK; a valid
prior managed copy may be refreshed; user-owned/unmarked paths remain untouched
as conflicts. Move the old installed copy aside, then rerun the installer, or
install the new release in a fresh directory and switch after inspection.

For Claude Code marketplace installs, update through `/plugin`. For a Codex local
plugin cache, reinstall from its configured marketplace and start a new thread.

Cursor marketplace refreshes must be verified because an update can report success
while retaining the previous commit. Refresh, then compare its `gitRef` with GitHub's
current `main`:

```bash
agent plugin marketplace update backs-aios
agent plugin marketplace list --format json
git ls-remote https://github.com/Tcuzzo/backs-aios-skills refs/heads/main
```

If `gitRef` does not equal the SHA from `git ls-remote`, rebuild only that reversible
marketplace pointer; an existing local plugin symlink remains available throughout:

```bash
agent plugin marketplace remove backs-aios
agent plugin marketplace add https://github.com/Tcuzzo/backs-aios-skills
agent plugin marketplace list --format json
```

Restart the host session after any marketplace or plugin refresh. OpenCode also loads
configuration once per process, so quit and start a fresh OpenCode process after its
command files or ESM adapter change.

## Verify discovery

- **Claude Code:** `/plugin list`, then `/optimus` in a fresh session.
- **Codex:** `codex plugin list` for plugin mode, then confirm
  `backs-aios:optimus` and `backs-aios:elite-build` in a fresh thread. For the
  explicit gate loader, run:
  ```bash
  node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
  ```
  and confirm the skill body is printed and the call exits 0. Unknown skills exit
  nonzero.
- **Cursor:** Customize → Plugins/Skills, then `/optimus` in the IDE or `agent` CLI.
- **OpenCode:** `opencode debug skill`, `opencode debug config`, then `/optimus` in a
  fresh session; the resolved config must contain all 10 command names, and the
  adapter file must exist at `~/.config/opencode/plugins/backs-aios.js`.

The canonical format is `skills/<name>/SKILL.md`. Every `name` is lowercase
kebab-case, matches its directory, and carries a 1–1024 character description.
