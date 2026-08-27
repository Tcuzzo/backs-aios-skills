# Naming — how this pack names things, and why

Names in this pack are load-bearing. An agent picks a skill by matching the task
against the name and description, so a name that says the wrong thing routes work to
the wrong discipline. The convention below keeps routing honest.

## The three kinds of names

- **Skills are noun-phrase disciplines.** A skill is the context an agent loads to
  reason with — a body of rules, not an action. So it is named like a discipline:
  `red-first`, `seam-engineering`, `sniper-testing`. You load a discipline; you do
  not "run" one.
- **Commands are imperatives.** A command is an action with a start and an end, so
  its name is a verb, or the name of the play or skill it fires: boot, build, hunt,
  grade, tribunal.
- **The invariant floor is law.** `invariant-floor` is the one skill every other
  skill inherits. It is named for what it is, the floor, because every hard rule
  in the pack stands on it, and no skill may land a change below it.

## The shipped commands

| Command | Fires |
| --- | --- |
| `/agent-build` | `plays/agent-builds.md` |
| `/bughunt` | `plays/bughunt.md` |
| `/design-taste` | `plays/design-taste.md` |
| `/elite-build` | `plays/elite-build.md` |
| `/grade` | `plays/grading-verification.md` |
| `/optimus` | `skills/optimus/SKILL.md` |
| `/parallel-work` | `plays/parallel-work.md` |
| `/secure-delivery` | `plays/security-delivery.md` |
| `/tribunal` | `skills/blind-tribunal/SKILL.md` |
| `/web-build` | `plays/web-app-builds.md` |

`design-taste` existing as skill, play, and command is deliberate — one discipline,
three entry forms: the skill is the context, the play is the recipe, the command is
the trigger. Unambiguous because the command fires the play; the play links the skill.

## Where each kind of information lives

Each layer answers a different question, and nothing is duplicated:

- **The name says the mechanism.** `blind-tribunal` tells you how it works before
  you open the file: jurors, blind to the author.
- **The description carries the trigger words.** The runtime matches your words
  against descriptions, so the description holds every phrase a human would say
  when they need the skill — including old names (see below).
- **The body carries the rules.** Steps, hard rules that fail the skill, and the
  skills it pairs with. The body is the discipline; the name and description are
  only its address.

## Renames never break

When a skill is renamed, its old name moves into the description as a trigger word,
so every habit and every doc that used the old name still routes correctly:

- **optimus** keeps its name outright — it is the boot brand, the one proper name in
  the pack, and the command you type first (`/optimus`).
- **"yoke"** survives as a trigger word on `human-calibration` — say either, and the
  same discipline loads.

A rename that breaks an existing trigger is a regression, not a cleanup.

## Effort stamps

Every skill carries one **Effort:** line under its title, answering two questions:
what does running it SPEND, and what wasted effort does it REMOVE? Three tiers:

- **free** — pure discipline: no extra model calls, no extra tooling runs. Some
  free skills cut net cost outright, and their stamps say so.
- **light** — one extra pass: a subagent, a validator run, a probe, a test-first write.
- **heavy** — multiple models or agents, or real compute (mutation runs, juror
  panels). A heavy stamp must also say WHEN the spend pays.

Honesty law: the stamp is a claim the skill body must back — a tribunal stamped
free is a lie. The "Removes:" clause names the specific waste the skill deletes
(killed rework, killed rogue landings, killed full-suite reruns), never a generic
"saves time". Each play ends with one **Weight:** line summing its chain the same way.

## Lord of the Loop

Every play's wireframe marks a **Lord of the Loop** — the loop owner. One hand
drives the whole iteration: it dispatches lanes, judges what comes back, and loops
findings around until the landing gate is green. A lane never lands its own work;
the Lord lands it.

## Per-skill rationale

| Name | Why this name |
| --- | --- |
| absorb | The discipline of taking an external capability in and re-engineering it as native, instead of duplicating it. |
| blind-eval | Evaluation with authorship hidden — the blindness is the mechanism. |
| blind-tribunal | A panel of jurors, blind to the author, from different model families. Tribunal = panel plus verdict. |
| bounded-loops | The property enforced: every loop carries a bound — budget, checkpoint, kill-switch. |
| clean-code-gauntlet | A gauntlet is a series of hard checks; clean code is what survives it. |
| decision-bar | One bar every decision is measured against before it may reach the human. |
| design-taste | The discipline of taste in visual work — gated and checked, not left to vibes. |
| fleet-ladder | The model fleet resolved as a fallback ladder, climbed in order. |
| gpu-dispatch | The dispatch law for GPU work: one model per card, warm through the loop. |
| guided-steps | Steps only a human can do, guided one stage at a time. |
| human-calibration | Calibrating the build to the human it serves. (Was "yoke" — the old name survives as a trigger word.) |
| incident-closure | An incident is closed fully, root cause to live proof, never triaged back to the human. |
| intent-compiler | Compiles natural language into an executable directive. The prose is the source; the directive is the output. |
| invariant-floor | The floor of numbered laws every change must clear. Law, not guidance. |
| leap-protocol | The protocol for leaping big work across parallel builders and landing it through one spine. |
| live-research | Research against live sources (docs and code as they are now), not model memory. |
| model-fusion | Many models draft, one independent judge picks — fusion of outputs, not a vote. |
| optimus | The boot brand, kept as a proper name. It boots the floor; every session starts here. |
| human-voice | Named for what it enforces: the agent writes the way a person talks, and hard ideas still arrive whole. |
| red-first | The failing (red) test comes first, committed before the build starts. |
| repair-loop | The full fix loop, named for its shape: ground, reproduce, fix, verify, land. |
| repo-map | Named for its artifact: one map file of the repo's shape, read map-first before any raw tree walk. |
| root-cause-first | The order of operations is the rule: cause before fix, always. |
| seam-engineering | Fixes land at the seam (the shared primitive), never as scattered point patches. |
| session-handoff | Named for its artifact: one handoff file a cold session can continue from. |
| sniper-testing | One shot, one target: run only the tests that cover what you touched. |
| understanding-gates | Gates on each build stage that check understanding, not just syntax. |
| wayfinder | Finds the way when lost, instead of parking a question on the human. |
