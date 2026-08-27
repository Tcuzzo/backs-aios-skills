# Install — bolt the pack onto a real agent

The pack is folders of markdown. Each skill is `skills/<name>/SKILL.md`. Each play is
`plays/<name>.md`. No binaries, no server, no build step. Installing means putting the
markdown where your agent looks for skills.

The frontmatter is deliberately the minimal 3-key subset — `name`, `description`,
`license` — of the open Agent Skills convention (agentskills.io). The spec requires only
`name` and `description`, and compliant runtimes ignore keys they do not recognize. So
the pack loads natively wherever the convention loads, and reads as plain markdown
everywhere else.

## 1. Claude Code

Claude Code discovers skills from two folders (confirmed against the official docs,
2026-08): personal `~/.claude/skills/<name>/SKILL.md` (every project on your machine)
and project `.claude/skills/` (rides with one repo).

Personal, one line:

    git clone https://github.com/Tcuzzo/backs-aios-skills.git ~/backs-aios-skills && ln -s ~/backs-aios-skills/skills/* ~/.claude/skills/

Project: `cp -r ~/backs-aios-skills/skills/* .claude/skills/`

Symlink if you want pack updates to flow through; copy if you want the version pinned
(or if symlinks give your runtime trouble). Start a new session. A skill fires when the
task matches its `description` — say the trigger words and the agent loads the file.
Plays are not skills: keep them in the clone and tell the agent to read one
(`read ~/backs-aios-skills/plays/elite-build.md`) at session start, or paste your
default play into the project's CLAUDE.md.

## 2. Any Agent Skills runtime (the open convention)

The convention is adopted well beyond Claude — OpenAI Codex, Gemini CLI, Cursor,
VS Code and more (per the spec ecosystem, 2026-08). The rules that matter here: the
file is named exactly `SKILL.md`; the directory name equals the frontmatter `name`;
only `name` + `description` are required. This pack satisfies all three. Install =
copy `skills/*` into wherever your runtime keeps skills (Cursor uses
`.cursor/skills/`, for example). We did not verify every runtime's folder — check
your platform docs for the exact path.

## 3. OpenClaw, Hermes, other agent frameworks

Confirmed against their current docs (2026-08):

- **OpenClaw** discovers any `SKILL.md` under its configured skill roots. Copy
  `skills/*` into your workspace `skills/` folder, or into the shared global
  `~/.openclaw/skills` folder. The `openclaw skills` CLI manages installs and updates.
- **Hermes (Nous Research)** keeps one folder per skill in `~/.hermes/skills/`, and
  loads a skill's SKILL.md into the system prompt when the task activates it. Copy
  `skills/*` there.

Any other framework — the generic pattern, no code needed:

1. Mount or paste each `SKILL.md` as tool-invokable context (a document tool, a prompt
   library entry, a retrieval store). Keep the `description` line intact — its trigger
   words are the invocation contract.
2. Load one play (`plays/*.md`) as system context for the session. A play names the
   skills it fires, in order; the agent then pulls each skill by name.
3. Verify the framework's current install mechanism in its own docs before trusting
   this file — mechanisms change fast; we only state what we confirmed above.

## 4. Bare API loop (no framework)

You are the harness. On each loop:

1. Put `skills/invariant-floor/SKILL.md` in the system prompt, always. That is the
   floor every change must clear.
2. Pick the play that matches the ask — build → `plays/elite-build.md`, bug →
   `plays/bughunt.md`, grading → `plays/grading-verification.md` — and append it.
3. Match the user's words against each skill's `description` trigger words. Never
   inject the whole pack — inject the one to three skills that match. The pack is
   token-lean; keep it that way.
4. Re-inject on every context reset. A rule that fell out of context is not loaded.

## First session

    You:   read ~/.claude/skills/harness-boot/SKILL.md and boot. This session follows it.
    You:   task — checkout total is wrong when a coupon and a gift card stack.
    Agent: [boots: loads invariant-floor, picks plays/bughunt.md, names the skills it will fire]
    You:   go.
    Agent: [the play drives: reproduce, red test, fix the class, verify live, blind grade, land]
