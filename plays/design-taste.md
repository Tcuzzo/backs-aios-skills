# Design Taste

The play for building any UI that looks designed, not generated. Generic UI is a
WORKFLOW bug, not a model bug: split taste-making from implementation, set exact
design tokens first, give the agent eyes, and gate on accessibility.

## When to run

Any screen, page, component, dashboard, or visual deliverable a human will look at.
The first screen sets the standard for every screen after — run this before it.

## Shared task and limits

Apply this play inside the current [BACKS Build Flow](../skills/backs-build-flow/SKILL.md)
task packet. Keep one integration owner, the requested `task_mode`, pinned base
and candidate revisions, operator essence, and current evidence. Reuse applicable
loaded skill bodies; this play adds its domain gates without restarting the task.

[bounded-loops](../skills/bounded-loops/SKILL.md) owns the original deadline and
remaining allowances across retries, workers, models, reviews, and handoffs.
Never reset them for a nested play. On exhaustion, checkpoint **STILL-BUILDING**
with the candidate, evidence, unmet gates, and next action. Continue useful
authorized work only within its remaining allowance; no missing gate becomes a pass.

## The chain

1. Use the intent and operator essence established through Build Flow to deduce
   which taste the human's words ask for. State the read once before writing.
2. [human-calibration](../skills/human-calibration/SKILL.md) — anchor the read in the
   human's record and real studied references, never a demographic guess.
3. Emit the three-tier design-token file FIRST, before any component — full token
   spec and banned-defaults list in [design-taste](../skills/design-taste/SKILL.md).
4. Build components with the token file injected as a hard constraint. Never
   hardcode a raw hex, pixel value, or font family inside a component.
5. Run the screenshot → critic loop per
   [design-taste](../skills/design-taste/SKILL.md), resolving the critic model live
   through [fleet-ladder](../skills/fleet-ladder/SKILL.md). Each critique and
   re-render spends the same remaining budget; return findings to the current owner.
6. Score the 8-axis taste rubric per [design-taste](../skills/design-taste/SKILL.md).
7. Enforce the WCAG 2.2 accessibility HARD gate per
   [design-taste](../skills/design-taste/SKILL.md).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — on the code
   BEHIND the pixels only: token resolvers, theme switches, contrast calculators,
   and state reducers pass with zero surviving mutants. A flipped comparison in a
   contrast check ships a beautiful, inaccessible screen. The gauntlet never
   scores taste — the rubric and the accessibility gate stay the visual judges.
   Use [sniper-testing](../skills/sniper-testing/SKILL.md) for actual repo
   lint/type/test commands scoped from the pinned aggregate candidate diff before
   the gauntlet. State N/A or missing checks honestly. Render real DOM in tests;
   a mocked render proves nothing about what the human sees. Preserve sealed RED
   files, add separate supplemental tests for new gaps, and retain the required
   independent review, full affected-suite landing check, and real rendered proof.

## Hard gates (play-specific — the skill's own hard rules apply on top)

- The critic is a non-builder seat resolved live through the fleet ladder by
  capability and availability — never a pinned model id (a retired pin silently
  kills the whole critic).

## Works well with

- [blind-tribunal](../skills/blind-tribunal/SKILL.md) — grade the whole deliverable
- [sniper-testing](../skills/sniper-testing/SKILL.md) — scope the component tests

**Weight:** light through the loop — calibration and the screenshot-critic pass each cost one extra run; the heavy step is the gauntlet on the code behind the pixels — it pays on any screen a human will actually look at.
