# BACKS AIOS Skills

A battle-tested agent harness, distilled into portable skills. This pack carries the
laws, the gates, and the plays that keep an autonomous agent honest: a numbered
invariant floor, deterministic hooks that block ungrounded edits, blind cross-family
grading, red-first tamper-proof testing, and named combo plays that chain it all.
It stops an agent from going rogue. It kills useless iteration. It makes long,
multi-hour autonomous sessions safe to leave alone — when a move breaks a law of the
floor, the move fails loudly instead of the agent hallucinating past it. Reasoning is
spent only where reasoning is the only tool that works; everything else is a rule the
harness enforces.

## Who this is for

Not just engineers. Coders, designers, and builders can bolt these on and run them by
keyword. Each skill reads as plain markdown. You do not need to know how the harness
was built to use it — you say the trigger words, the discipline fires.

## How it works

- **Skills** are single disciplines. Each one has trigger words in its description,
  numbered steps, hard rules that fail the skill, and links to the skills it pairs
  with. One file each: `skills/<name>/SKILL.md`.
- **Plays** are named combos. A play fires skills in a set order and lists the hard
  gates that block a landing. One file each: `plays/<name>.md`.

**30-second quick start:** drop the `skills/` folders into your agent's skill
directory. Open a play — start with [elite-build](plays/elite-build.md). Say the
keywords ("red first", "blind tribunal", "repair loop") and the matching skill loads.
Per-agent install paths are in [INSTALL.md](INSTALL.md).

| When you want... | Say... |
| --- | --- |
| Something broke | "repair loop" |
| Build a feature | read [plays/elite-build.md](plays/elite-build.md) first |
| Is this good enough to ship? | "clean code gauntlet" |
| Check my work, blind | "blind tribunal" |
| I'm lost — what next? | "wayfinder" |
| The ask is vague prose | "prose is the spec" |

## The skills

| Skill | What it does |
| --- | --- |
| [absorb](skills/absorb/SKILL.md) | Adopt an existing open-source capability and re-engineer it as a native skill, instead of building a duplicate. |
| [ask-me-bar](skills/ask-me-bar/SKILL.md) | One bar for every decision: only taste, vision, or destructive risk reach the human. Everything else executes. |
| [blind-eval](skills/blind-eval/SKILL.md) | Judge a change on its merits with authorship hidden, then keep or revert. Only proven uplift lands. |
| [blind-tribunal](skills/blind-tribunal/SKILL.md) | Blind jurors from different model families grade the change, one lens each. Every finding becomes a failing test. Loop until all pass. |
| [bounded-loops](skills/bounded-loops/SKILL.md) | Budget ceilings, checkpoints, and kill-switches on every loop. Makes hammering an API structurally impossible. |
| [clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) | A deterministic quality bar: sniper tests, the CRAP score (complexity x coverage), bounded mutation testing, then a light taste review. |
| [design-taste](skills/design-taste/SKILL.md) | Ship visual work that looks designed, not generated: design tokens first, screenshot critique, a hard accessibility gate. |
| [fleet-ladder](skills/fleet-ladder/SKILL.md) | Resolve the live model ladder: probe what is up, fall back in order, fail loud when the ladder is exhausted. |
| [full-close](skills/full-close/SKILL.md) | "Fix it" means a full close — root cause with evidence, failing test, green, live proof — never a menu of options back at the human. |
| [gpu-dispatch](skills/gpu-dispatch/SKILL.md) | One model per GPU, no spill to system RAM, keep the card warm through the loop, unload at loop end. |
| [harness-boot](skills/harness-boot/SKILL.md) | No code until the harness is loaded. A deterministic hook blocks mutating tools until the agent has read the rules. |
| [human-steps-wizard](skills/human-steps-wizard/SKILL.md) | Script the steps only a human can do — dashboards, credentials, secrets — stage by stage, capturing each value. |
| [invariant-floor](skills/invariant-floor/SKILL.md) | The numbered laws every autonomous change must satisfy before it lands. The floor the whole pack stands on. |
| [know-your-human](skills/know-your-human/SKILL.md) | Build a profile of how this human thinks, decides, and wants to be spoken to, then steer the whole build through it. |
| [leap-protocol](skills/leap-protocol/SKILL.md) | Split big work into independently ownable balls, fan them to parallel builders in isolated worktrees, reconcile through one write spine. |
| [live-research](skills/live-research/SKILL.md) | A parallel research agent reads the live source — READMEs, docs, actual code — so reasoning grounds in what is really there, not memory. |
| [model-fusion](skills/model-fusion/SKILL.md) | A panel of models drafts in parallel, an independent judge picks, the winner is validated against the original intent. |
| [plain-speech](skills/plain-speech/SKILL.md) | Short sentences, one idea each, active voice, 8th-grade level — on every human-facing message. |
| [prose-is-the-spec](skills/prose-is-the-spec/SKILL.md) | Translate a human's natural prose — slang, metaphor, shorthand — into a stated technical directive, then execute it whole. |
| [red-first](skills/red-first/SKILL.md) | Commit a proven-failing test before the build starts. The builder may not touch it. A grader verifies it never moved. |
| [repair-loop](skills/repair-loop/SKILL.md) | The full fix loop: ground in the floor, reproduce, red test, fix the class, verify on the real path, independent grade, land. |
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
harness, not the model, holds the discipline. The full system — its memory design, its
model-behavior profiles, its code graph — is not in this pack. The skills still stand
alone on any agent: Claude Code, OpenClaw, Hermes, Codex, Cursor, or a bare API loop.
The bigger your agent's autonomy, the more the floor pays for itself.

## Credit

Composition and conversion by [Tcuzzo](https://github.com/Tcuzzo). Some skills carry
scaffold credits for the published work they graft; those are noted inline and
collected in [NOTICE.md](NOTICE.md). Licensed [MIT](LICENSE). Contributions are
welcome — keep the credits intact.
