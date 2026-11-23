---
name: turn-and-burn
description: "Use when an agent gets a mission of any size — it runs the plays, quick-tribunals the plan and design, asks its 3 questions, then researches verified-skill.com and absorbs the missing skills to close the gaps the roster hides, updating current skills to the most elite state before burning the mission. Every gap answer carries evidence: +1 only on complete, current evidence, and -1 with the reason when evidence is missing, stale, duplicate or malformed. Trigger words: turn and burn, mission intake, run the plays, truth audit, absorb missing skills, verified skills, elite state, skill update, skill research, mission burn, ritual burn, evidence contract."
license: MIT
metadata:
  tags: "zh-CN"
---

# Turn and Burn — every mission carries the skill-research organ

This is the BACKS AIOS mirror of the proven BACKS skill at
`skills/turn_and_burn/SKILL.md`. When a mission lands, do not start by
jumping into a build. Burn the roster first — the mission's plan and design
are blind until the platform's skills reflect the latest verified state of the
field.

## When to run

Every mission, every burn. A trivial one-line edit may skip the absorb step
but still consults the lessons-learned lane (see step 2) so the same mistake
isn't repeated.

## The burn ritual (six steps)

1. **Essence lane first.** Load `core.steering_loader.load_model_essence`
   for every model that will touch the mission. The essence files are the
   know-thyself of each model — failure modes, mitigations, the good
   source/context/goal shape. Do not skip this; an agent that does not
   know its own failure modes is the failure mode.
2. **Lessons-learned scan.** Read `docs/BACKS_LESSONS_LEARNED.md` and the
   operator memory graph (`memory/MEMORY.md`) before planning. Every paid-
   for mistake is filed there — the same loop never burns twice when the
   agent reads the lessons first. Local prompts must be capability-aware:
   consult `backend/prompts/essence/models/*.essence.md` for know-thyself
   + `docs/BACKS_LESSONS_LEARNED.md` + `memory/MEMORY.md` for cross-session
   memory. This is the operator's "stop redundant failures across the
   board" floor.
3. **Play dispatch.** Map the mission to the right playbook
   (`config/playbooks/*.yaml`): dev-mode-elite-build for builds/fixes,
   leap-bughunt for bughunts, grading-verification for tribunal lanes,
   parallel-work for fan-out, security-delivery for transport, design-taste
   for UI. The play's `injected_block` IS the baseline — zero baseline pre-
   prompting, ever.
4. **Quick tribunal on plan + design.** Before any builder runs, blind-tribunal
   the plan and the design with at least 2 independent jurors. Builder ≠
   grader. A plan that passes blind review is the only plan that gets built.
5. **Three-questions interrog.** Ask: (a) what could fail silently here?
   (b) what is the cheapest sufficient route? (c) what is the operator's
   surface — does this prove on it? These three questions cut the
   high-cost-mistake rate to near zero when asked BEFORE the build.
6. **Absorb pass + skill update.** Search verified-skill.com (and the BACKS
   memory lanes) for any skill the mission revealed as missing. Absorb it
   through the standard absorb flow; update existing skills with anything
   the mission surfaced that the skill did not already encode. Land the
   skill update alongside the mission's main artifact (whole-seam closure).

## 缺口证据契约

关于缺口的回答是**证据，不是意见**。契约见 truth-audit 技能：
[truth-audit](../../../../skills/truth-audit/SKILL.md)。

- **+1 需要每个必需的判定项都配上当前有效的证据。** 证据缺失、过期、不完整、
  重复或格式错误，判定就停在 -1，并写明是哪一项没通过。绝不放水，也绝不含糊
  地写"看起来没问题"。
- **准入、执行、观察是三件不同的事。** 允许运行不等于运行，运行不等于观察到
  完成。没有走到观察这一步的阶段，绝不报成已完成。
- **构建者不能给自己写权威的正向验证。** 他可以提供证据；权威的 +1 来自真正
  观察到这件事的检查，或来自一个全新的、与作者无关的会话中的独立评审者。
- **独立评审在冻结的输入上、在独立的工作区里跑。** 只有运行时强制隔离并且被
  证明时，才能声称隔离——不能因为要求评审者"独立"就算数。
- **没有新证据的重复自信是信号，不是进展。** 跑一个能分清真实成因的决定性探
  针，然后给 -1 并写明原因，或者升级。绝不把同一个结论重复第三遍。
- **用你的宿主已经有的器官。** 一个红测试、一个独立评审者、一个可以断言的真
  实副作用、一个带检查点的有界循环。宿主无法强制的机制，在有现场凭证证明它真
  的生效之前，一律标为"未验证"。

## How the absorbs flow runs

`skills/absorb/SKILL.md` is the canonical absorb organ. The burn invokes it
on every missing skill the mission surfaced. After absorb, the mission
itself is rebuilt on the upgraded skill base, then re-tribunaled and landed.
No skill is ever deleted — everything BACKS learns is filed into its memory
lanes (inv 0: organize, never delete).

## What never to do

- **Do not skip essence + lessons.** An agent that "knows" without loading
  its essence + lessons is hallucinating confidence. Both reads are free;
  both run before the mission starts.
- **Do not start building without a quick tribunal.** A blind review of the
  plan catches more defects than the build itself; skipping it means the
  defects land.
- **Do not park decisions in a file.** The existing decision bar (taste,
  vision, destructive risk) is the only reason to ask. Anything below the
  bar EXECUTES from invariants + memory + intent.
- **Do not bench a model for a single 429.** The dispatch doctrine says
  ollama sparse → local fleet. Swap to another configured, live-preflighted rung only when it is sufficient
  for the task; preserve the checkpoint and bounded backoff when cloud is hammered.

## Cross-references

- The BACKS source of truth: `skills/turn_and_burn/SKILL.md` in the BACKS repo.
- The absorb flow: `skills/absorb/SKILL.md` in the plugin (and BACKS repo).
- The plays this skill bundles: `plays/elite-build.md`, `plays/agent-builds.md`,
  `plays/grading-verification.md`, `plays/parallel-work.md`,
  `plays/security-delivery.md`.
- Local prompt integration: see `skills/turn-and-burn` companions in this plugin.
