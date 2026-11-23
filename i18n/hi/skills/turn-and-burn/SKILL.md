---
name: turn-and-burn
description: "Use when an agent gets a mission of any size — it runs the plays, quick-tribunals the plan and design, asks its 3 questions, then researches verified-skill.com and absorbs the missing skills to close the gaps the roster hides, updating current skills to the most elite state before burning the mission. Every gap answer carries evidence: +1 only on complete, current evidence, and -1 with the reason when evidence is missing, stale, duplicate or malformed. Trigger words: turn and burn, mission intake, run the plays, truth audit, absorb missing skills, verified skills, elite state, skill update, skill research, mission burn, ritual burn, evidence contract."
license: MIT
metadata:
  tags: "hi"
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

## अंतराल का सबूत-अनुबंध

अंतराल के बारे में कोई जवाब **सबूत है, राय नहीं।** अनुबंध अंग्रेज़ी में यहाँ है:
[truth-audit](../../../../skills/truth-audit/SKILL.md).

- **+1 के लिए हर ज़रूरी predicate की मौजूदा evidence चाहिए।** जो evidence गायब,
  पुरानी, अधूरी, duplicate या बिगड़ी हुई हो, verdict -1 पर रहता है, और कारण
  बताता है कि कौन-सा predicate fail हुआ। कभी soft pass नहीं, कभी सिर्फ "ठीक
  लगता है" नहीं।
- **Admitted, executed और observed तीन अलग बातें हैं।** चलने की अनुमति चलना नहीं
  है। चलना observed completion नहीं है। जो stage observe तक नहीं पहुँचा, उसे
  कभी पूरा बताया नहीं जाता।
- **Builder अपना खुद का authoritative positive verification नहीं लिख सकता।** वह
  evidence दे सकता है; authoritative +1 उस check से आता है जिसने चीज़ observe
  की, या fresh, author-disjoint session में किसी independent reviewer से।
- **Independent review frozen inputs पर, अलग scratch में चलता है।** Isolation
  तब ही claim की जाती है जब runtime उसे enforce करे और वह दिखाया गया हो —
  इसलिए नहीं कि reviewer से कहा गया कि "independent रहो"।
- **बिना नए evidence के बार-बार same confidence progress नहीं, signal है।** एक
  decisive probe चलाओ जो ज़िंदा causes को अलग कर सके, फिर कारण के साथ -1 या
  escalate करो। उसी नतीजे की तीसरी repetition कभी नहीं।
- **अपने host के पास जो अंग हैं उन्हीं का इस्तेमाल करो।** एक red test, एक
  independent reviewer, assert करने के लिए एक real side effect, checkpoint वाला
  एक bounded loop। जिस mechanism को host enforce नहीं कर सकता, वह "unvalidated
  until demonstrated" रहता है।

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
