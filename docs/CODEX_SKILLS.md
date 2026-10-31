# BACKS AIOS in Codex

This pack has two Codex delivery paths. The managed plain skills at
`~/.codex/skills/<name>/SKILL.md` work in Codex CLI, the desktop app, and the
IDE extension. The local Codex plugin adds a namespaced skill bundle and a
grounding hook in the desktop app. The plugin is built from the public skill
pack's skills, playbooks and hook files; it does not copy BACKS production code or runtime
data.

## The behavior Codex should follow

The managed instruction block in `config/codex/AGENTS.md` is installed into
`~/.codex/AGENTS.md` by the refresh command. Codex reads this global file at the
start of a new task. It tells Codex to load `optimus` and `invariant-floor`
before changing code, then to load the skills relevant to the task. The plugin
supplies the skill bodies; the instruction file makes the intended routing
explicit. Build Flow owns the current task, bounded RED/GREEN, scoped lint/type/tests,
quality evidence and delivery. Operator Essence supplies a private, evidence-backed
awareness slice, with one insight bootstrap when missing. A model can still miss an instruction, so verify the actual skill
body or hook output in the task rather than treating installation as proof of
invocation.

The local manifest declares `./hooks/hooks.json`, which invokes the existing grounding loader on
session start and selected tool events. Codex desktop requires the operator to
review and trust that hook definition before it will run. The hook reports
loading evidence and errors; it must never refuse tools. If the hook is not
trusted or unavailable, the plain skills and global instruction file still
work. The explicit fallback is:

```powershell
node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
```

Run the fallback in the active Codex session and pass `CODEX_SESSION_ID` as
the final argument when shell and host session IDs differ. Do not report a
hook as active just because the file exists.

## One refresh command for the local machine

Run this from a clean, released public-pack checkout after reviewing its
changes:

```powershell
python tools/refresh_codex_local.py --update-source
```

The command fast-forwards the public checkout, runs `install.ps1 -Target all`
to refresh Codex, Cursor, Claude Code, OpenCode, portable Agent Skills, and the
managed runtime, then updates a personal local Codex plugin under
`~/.codex/plugins/backs-aios`. It merges one entry into
`~/.agents/plugins/marketplace.json` and a bounded managed block into
`~/.codex/AGENTS.md`, preserving unrelated entries and instructions. The
Codex plugin copy includes only `plugin.json`, canonical `skills/`, `plays/`, three
grounding-hook files, and `LICENSE`. Compatibility aliases are omitted from this
bundle to prevent duplicate discovery; loose skill paths remain compatible. An existing unmarked plugin directory or conflicting
BACKS AIOS marketplace entry causes a visible error and stays untouched.

The selected `--home` is passed only to the child installer environment; it does
not change the caller's environment. This command does not rewrite Claude settings
JSON or Codex config TOML.

The command prints JSON with the source commit, bundle SHA-256, changed flags,
and whether a desktop restart or new Codex task is needed. It refuses to sync
a dirty checkout by default, so unattended runs cannot publish incomplete
local edits. `--allow-dirty` and `--skip-host-install` exist only for isolated
development tests; do not use them for scheduled refresh. A failed source
pull, installer, or plugin merge is an error, not a successful update.

To make refresh recurring, schedule this same command against the public-pack
checkout with a Codex heartbeat. The heartbeat should run on the local host,
stay quiet when the source commit and installed bundle hash are unchanged,
and notify only on an update, a failed refresh, or a required app restart.
This updates files automatically; a running Codex task retains its existing
context. Start a new task after changed skills, and restart the desktop app
when the local plugin or catalog changed.

## Install and verify the Codex desktop plugin

The checkout includes a root `plugin.json`, but no repo marketplace catalog:
pointing a marketplace at the checkout would cache unrelated source files.
The refresh command creates an allowlisted plugin copy and a personal catalog
so the plugin is available across repositories. Restart the
ChatGPT desktop app, open **Plugins Directory**, choose the local marketplace,
and install **BACKS AIOS**. Review and trust its hook when Codex asks. In a
fresh task, confirm `backs-aios:optimus` and `backs-aios:repair-loop` appear
in skill discovery, then invoke `optimus` and inspect its loaded body. Confirm
the plugin's installed copy has the same skill content hash as the public pack.
Check the actual capabilities of the installed CLI before using a plugin
subcommand. Where it is unavailable, use the desktop Plugins Directory and the
plain-skill path. File installation alone does not prove host discovery.

The source files are editable in the public-pack repository. The installed
plain skills are under `~/.codex/skills`; the personal catalog is at
`~/.agents/plugins/marketplace.json`; the managed global instruction block is
in `~/.codex/AGENTS.md`. The desktop app loads a cached plugin copy, so edit
the public source and refresh it, not the cache.

## Public release boundary

The local desktop plugin includes a hook, and current OpenAI packaging rules
do not allow hook bundles in the universal public plugin directory. A public
submission must be a separately built, allowlisted skills-only package with
the hook directory excluded **and** the `extensions.com.openai.hooks` field
removed from its derived manifest. The local source manifest is not a valid
public-directory upload as-is. Its directory listing requires review and
approval; a local marketplace entry is not a public store listing. Do not
claim that VS Code, Cursor, Claude Code, Codex desktop, and the public Plugins
Directory all updated merely because one host's files copied successfully.
Verify each host's discovered skill or command in a new session.

OpenAI references: [plugin packaging and local marketplaces](https://developers.openai.com/plugins/build/plugins),
[plugin skill activation](https://developers.openai.com/plugins/concepts/skills),
and [Codex AGENTS.md loading](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide).
