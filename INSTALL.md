# Install BACKS AIOS

BACKS AIOS ships one canonical set of 28 Agent Skills plus native packaging for
Claude Code, Codex, and Cursor. OpenCode loads the same skills directly. There is
no build step and no runtime dependency for the skills themselves.

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

The Unix installer creates update-friendly symlinks. The PowerShell installer
creates pinned copies. Both refuse to overwrite an existing skill or plugin.
Run a new agent session after installation, then invoke `optimus`.

Supported `--target` / `-Target` values:

| Target | Registration path | What loads it |
| --- | --- | --- |
| `codex` | `~/.codex/skills/<name>/SKILL.md` | Codex CLI, app, and IDE extension |
| `cursor` | `~/.cursor/plugins/local/backs-aios` | Cursor IDE and Cursor CLI (`agent`) |
| `opencode` | `~/.config/opencode/skills/<name>/SKILL.md` | OpenCode terminal and desktop |
| `claude` | `~/.claude/skills/<name>/SKILL.md` | Claude Code skill-only/manual mode |
| `portable` | `~/.agents/skills/<name>/SKILL.md` | Agent Skills runtimes, including Cursor and OpenCode |
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

Use `./install.sh --target claude` only when you want skills without the plugin's
commands and hook.

## Codex: plugin or plain skills

This repository includes `.codex-plugin/plugin.json` for Codex plugin catalogs.
For a direct GitHub clone, the portable route is:

```bash
./install.sh --target codex
```

Codex discovers the 28 skill folders on the next thread. The richer local plugin
development flow can point a Codex marketplace entry at this clone and run:

```bash
codex plugin add backs-aios@<marketplace-name>
```

The marketplace name belongs to the local catalog that references the clone; it
is not hardcoded by this repository.

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

OpenCode discovers one `SKILL.md` per folder from
`~/.config/opencode/skills/` and `~/.agents/skills/`:

```bash
./install.sh --target opencode
```

Start a new OpenCode session. Use the native `skill` tool or `/optimus`; OpenCode
loads skill bodies on demand and keeps their relative links intact.

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

Pinned PowerShell copies intentionally do not overwrite existing files. Move the
old installed copy aside, then rerun `install.ps1`, or install the new release in a
fresh directory and switch after inspection.

For Claude Code marketplace installs, update through `/plugin`. For a Codex local
plugin cache, reinstall from its configured marketplace and start a new thread.

## Verify discovery

- **Claude Code:** `/plugin list`, then `/optimus` in a fresh session.
- **Codex:** `codex plugin list` for plugin mode, or confirm the skills in a fresh thread.
- **Cursor:** Customize → Plugins/Skills, then `/optimus` in the IDE or `agent` CLI.
- **OpenCode:** inspect the `skill` tool's available list or run `/optimus`.

The canonical format is `skills/<name>/SKILL.md`. Every `name` is lowercase
kebab-case, matches its directory, and carries a 1–1024 character description.
