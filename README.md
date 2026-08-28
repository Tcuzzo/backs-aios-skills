# BACKS AIOS Skills

**Read this in:** [Español](i18n/es/README.md) · [Português (BR)](i18n/pt-BR/README.md) · [Français](i18n/fr/README.md) · [Deutsch](i18n/de/README.md) · [हिन्दी](i18n/hi/README.md) · [简体中文](i18n/zh-CN/README.md)

An agent harness distilled into 28 portable skills, 8 named plays, and 10 command
entry points, taken from a running agent platform and rebuilt as plain markdown any
agent can load.

Prefer pictures? Start with the [Visual guide](docs/FLOWCHARTS.md) for the complete
skill map and the boot, build, repair, grading, parallel-work, and decision loops.

## Mission

This pack exists for the people who would otherwise be priced out of elite agent
results — coders, designers, and builders who are not platform engineers. The harness
and the skills are the equalizer: they carry the humans who cannot afford the biggest
models, and they make the model tier matter less. That is the bet this pack makes: a
small model inside a strong harness can beat a big model running loose. You do not
need to know how the harness was built to use it — you say the trigger words, and the
discipline fires.

## Philosophy

Three beliefs run through every file in this pack.

**Programmed, not prompted.** The agent behind this pack communicates plainly and
refuses bad moves because those properties are engineered into the harness as
structural rules (hooks, gates, tests), not suggested in a prompt. A rule an agent
must remember fails exactly when the agent is busiest. So the rules that matter are
enforced where forgetting is impossible: in the harness, not in the model's memory.

**Machines do not think — they distill.** Give a model nothing real to work from and
it compresses thin air — a confident wrong answer. Give the same model the right
context and it gets it right. What we call reasoning is distillation over
context: the model compresses what it was given into an answer. Reasoning without
research is hallucination. That is why skills exist. A skill is the context an agent
reasons WITH while reasoning ABOUT a thing — it carries the agent from high-level
understanding down to subject-matter depth, so the distillation has something real to
distill.

**Reason only where reasoning is the only tool that works.** Everything deterministic
belongs to the harness — gates, tests, hooks, budgets. The model's reasoning is spent
only where it earns its cost: judgment, design, reading intent. That split is what
makes the pack model-equalizing: the harness does the heavy lifting, so the model
tier stops deciding the outcome.

## Quick start

### Option 1 — every local coding agent

    git clone https://github.com/Tcuzzo/backs-aios-skills.git ~/backs-aios-skills
    cd ~/backs-aios-skills && ./install.sh --target all

This registers the pack for Codex, Cursor, OpenCode, and Claude Code without
rewriting any skill body. It also installs host-native commands for Claude Code and
OpenCode plus command-skill adapters for Codex and portable Agent Skills runtimes.
Windows uses `install.ps1 -Target all`.

### Option 2 — Claude Code plugin

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

Then type `/optimus` to boot the floor. The skills load, the play commands become
available, and the grounding hook ships enabled (kill-switch: `AIOS_GATE=off`).

### Option 3 — one host or a portable Agent Skills root

Use `./install.sh --target codex|cursor|opencode|claude|portable`, then say the
trigger words. Exact discovery paths, project-local installs, Windows commands,
and update steps are in [INSTALL.md](INSTALL.md).

| When you want... | Say... |
| --- | --- |
| Something broke | "repair loop" |
| Build a feature | `/elite-build` (plugin) or read `plays/elite-build.md` (manual) |
| Is this good enough to ship? | "clean code gauntlet" |
| Check my work, blind | "blind tribunal" |
| I'm lost — what next? | "wayfinder" |
| The ask is vague prose | "prose is the spec" |

## How it works

- **Skills** are single disciplines. Each one has trigger words in its description,
  numbered steps, hard rules that fail the skill, and links to the skills it pairs
  with. One file each: `skills/<name>/SKILL.md`.
- **Plays** are named combos. A play fires skills in a set order and lists the hard
  gates that block a landing. One file each: `plays/<name>.md`. Every play's
  wireframe marks a **Lord of the Loop** — the loop owner who drives iteration
  until the landing gate is green; the role is defined in
  [NAMING.md](NAMING.md#lord-of-the-loop).
- **Commands** are the 10 action entries that load a play or skill and run it. Claude
  Code, Cursor, and OpenCode receive native slash commands from `command-adapters/`. Codex
  and Agent Skills runtimes receive the equivalent progressive adapters from
  the eight command-named folders in `skills/`, because Codex plugins ingest skills
  rather than command files. `optimus` and `design-taste` already serve both roles.
- **Native manifests** preserve each host's richest supported surface:
  `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and
  `.cursor-plugin/plugin.json`. OpenCode reads the canonical skills and native
  commands directly from its user configuration roots.
- **The naming convention** (why skills are noun phrases, commands are verbs, and
  the floor is law) is in [NAMING.md](NAMING.md).
- **Effort stamps** — every skill's one-line cost claim (free / light / heavy) and
  every play's closing Weight line are decoded in [NAMING.md](NAMING.md#effort-stamps).
- **Visual guide** — the complete skill map and core loops are in
  [FLOWCHARTS.md](docs/FLOWCHARTS.md), with text versions for terminals and screen
  readers.

## Performance

Real numbers, measured on one Linux dev box — spawn cost varies by machine, so
treat the shape, not the digits. Armed, the grounding hook costs about
28ms per tool call on Node (39ms in Python); a read-only Bash call pays about
32ms. Even the `AIOS_GATE=off` kill-switch pays ~35ms, because spawning the hook
process is most of the cost. True zero hook overhead means disabling the hook in
`/hooks` or disabling the plugin — the env var cannot get you there.

The always-on token cost is the skill descriptions: about 4.1k tokens per
session. Full skill bodies load only when a skill is invoked. The cost map is
already in the pack: every skill's Effort stamp and every play's Weight line say
what a discipline spends before you fire it.

On a plain repo the big lever is [repo-map](skills/repo-map/SKILL.md): with no
index, agents re-derive the repo's shape every session. Pay the walk once, then
read the map. The rest is argument, not measurement — but we will make it
plainly: the discipline removes more latency than the harness adds, because the
real latency is wasted iteration, not a 30ms hook.

## The skills

| Skill | What it does |
| --- | --- |
| [absorb](skills/absorb/SKILL.md) | Adopt an existing open-source capability and re-engineer it as a native skill, instead of building a duplicate. |
| [blind-eval](skills/blind-eval/SKILL.md) | Judge a change on its merits with authorship hidden, then keep or revert. Only proven uplift lands. |
| [blind-tribunal](skills/blind-tribunal/SKILL.md) | Blind jurors from different model families grade the change, one lens each. Every finding becomes a failing test. Loop until all pass. |
| [bounded-loops](skills/bounded-loops/SKILL.md) | Budget ceilings, checkpoints, and kill-switches on every loop. Makes hammering an API structurally impossible. |
| [clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) | A deterministic quality bar: sniper tests, the CRAP score (complexity x coverage), bounded mutation testing, then a light taste review. |
| [decision-bar](skills/decision-bar/SKILL.md) | One bar for every decision: only taste, vision, or destructive risk reach the human. Everything else executes. |
| [design-taste](skills/design-taste/SKILL.md) | Ship visual work that looks designed, not generated: design tokens first, screenshot critique, a hard accessibility gate. |
| [fleet-ladder](skills/fleet-ladder/SKILL.md) | Resolve the live model ladder: probe what is up, fall back in order, fail loud when the ladder is exhausted. |
| [gpu-dispatch](skills/gpu-dispatch/SKILL.md) | One model per GPU, no spill to system RAM, keep the card warm through the loop, unload at loop end. |
| [guided-steps](skills/guided-steps/SKILL.md) | Script the steps only a human can do (dashboards, credentials, secrets) stage by stage, capturing each value. |
| [human-calibration](skills/human-calibration/SKILL.md) | Build a profile of how this human thinks, decides, and wants to be spoken to, then steer the whole build through it. |
| [incident-closure](skills/incident-closure/SKILL.md) | "Fix it" means a full close (root cause with evidence, failing test, green, live proof), never a menu of options back at the human. |
| [intent-compiler](skills/intent-compiler/SKILL.md) | Read a human's natural language (dialect, metaphor, shorthand) as a full spec, then execute it whole. Every dialect is a valid grammar; the skill reads culture as context with its own internal logic, never as stereotype. |
| [invariant-floor](skills/invariant-floor/SKILL.md) | The numbered laws every autonomous change must satisfy before it lands. The floor the whole pack stands on. |
| [leap-protocol](skills/leap-protocol/SKILL.md) | Split big work into independently ownable balls, fan them to parallel builders in isolated worktrees, reconcile through one write spine. |
| [live-research](skills/live-research/SKILL.md) | A parallel research agent reads the live source (READMEs, docs, actual code) so reasoning grounds in what is really there, not memory. |
| [model-fusion](skills/model-fusion/SKILL.md) | A panel of models drafts in parallel, an independent judge picks, the winner is validated against the original intent. |
| [optimus](skills/optimus/SKILL.md) | No code until the harness is loaded. A deterministic hook blocks mutating tools until the agent has read the rules. |
| [human-voice](skills/human-voice/SKILL.md) | The no-degree bar: if reading it needs a degree, rewrite it. Keeps the full idea while it strips the machine tells. |
| [red-first](skills/red-first/SKILL.md) | Commit a proven-failing test before the build starts. The builder may not touch it. A grader verifies it never moved. |
| [repair-loop](skills/repair-loop/SKILL.md) | The full fix loop: ground in the floor, reproduce, red test, fix the class, verify on the real path, independent grade, land. |
| [repo-map](skills/repo-map/SKILL.md) | Walk the tree once, write one CODE_MAP.md at the repo root, and read the map before walking raw. The repo's shape is derived once, not every session. |
| [root-cause-first](skills/root-cause-first/SKILL.md) | No fixes without investigation. Reproduce on demand, instrument boundaries, trace the data backward to the source. |
| [seam-engineering](skills/seam-engineering/SKILL.md) | Fix the flaw class once at its shared primitive, sweep every sibling, land a guard that catches the next offender. |
| [session-handoff](skills/session-handoff/SKILL.md) | Compact a session into one flat file a brand-new agent can read cold and continue from. Secrets redacted. |
| [sniper-testing](skills/sniper-testing/SKILL.md) | Run only the tests that cover what you touched. Kill mock theater — tests that pass while the capability is broken. |
| [understanding-gates](skills/understanding-gates/SKILL.md) | Gate Design, Plan, Build, Test, and Ship with approve/revise/reject verdicts, so the build still matches the ask. |
| [wayfinder](skills/wayfinder/SKILL.md) | When lost, chart a decision map to the destination instead of parking a question on the human. |

## The plays

| Play | What it runs |
| --- | --- |
| [elite-build](plays/elite-build.md) | The master play for any build, fix, or uplift: read the intent, gate the plan, prove it red, build, test tight, grade blind, land live-proven. |
| [agent-builds](plays/agent-builds.md) | Building agents and services: deterministic primitives do the heavy lifting; the model reasons only where reasoning is the only thing that works. |
| [web-app-builds](plays/web-app-builds.md) | Web apps and sites with clean structure and a defended supply chain — dependency hygiene is the play, not an afterthought. |
| [design-taste](plays/design-taste.md) | UI that looks designed, not generated: split taste-making from implementation, set tokens first, give the agent eyes, gate on accessibility. |
| [grading-verification](plays/grading-verification.md) | Adversarial grading: a green result is a claim, not proof. The grader attacks, and the floor cannot be gamed. |
| [parallel-work](plays/parallel-work.md) | Fan work across agents without them trampling each other: one write spine, many readers. |
| [security-delivery](plays/security-delivery.md) | The ship gate for anything a customer or another machine will run. Safe by construction, not by memory. |
| [bughunt](plays/bughunt.md) | A bounded, parallel bug hunt: chart the map, fan out finders, verify every finding adversarially, close whole seams. |

## Works best with

These skills are the portable layer of **BACKS AIOS**, an agent platform built by
[Tcuzzo](https://github.com/Tcuzzo) — a graph-indexed, gate-enforced system where the
harness, not the model, holds the discipline. The full system (its memory design, its
model-behavior profiles, its code graph) is not in this pack. The skills still stand
alone on any agent: Claude Code, OpenClaw, Hermes, Codex, Cursor, or a bare API loop.
The bigger your agent's autonomy, the more the floor pays for itself.

## Credit

Composition and conversion by [Tcuzzo](https://github.com/Tcuzzo). Some skills carry
scaffold credits for the published work they graft; those are noted inline and
collected in [NOTICE.md](NOTICE.md). Licensed [MIT](LICENSE). Contributions are
welcome — keep the credits intact.
