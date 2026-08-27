# Design Taste

The play for building any UI that looks designed, not generated. Generic UI is a
WORKFLOW bug, not a model bug: split taste-making from implementation, set exact
design tokens first, give the agent eyes, and gate on accessibility.

## When to run

Any screen, page, component, dashboard, or visual deliverable a human will look at.
The first screen sets the standard for every screen after — run this before it.

## The chain

1. [prose-is-the-spec](../skills/prose-is-the-spec/SKILL.md) — deduce WHICH taste
   the human's own words ask for, and state the read in one line before writing.
2. [know-your-human](../skills/know-your-human/SKILL.md) — anchor the read in the
   human's record and real studied references, never a demographic guess.
3. Emit the three-tier design-token file FIRST, before any component — full token
   spec and banned-defaults list in [design-taste](../skills/design-taste/SKILL.md).
4. Build components with the token file injected as a hard constraint. Never
   hardcode a raw hex, pixel value, or font family inside a component.
5. Run the screenshot → critic loop per
   [design-taste](../skills/design-taste/SKILL.md), resolving the critic model live
   through [fleet-ladder](../skills/fleet-ladder/SKILL.md).
6. Score the 8-axis taste rubric per [design-taste](../skills/design-taste/SKILL.md).
7. Enforce the WCAG 2.2 accessibility HARD gate per
   [design-taste](../skills/design-taste/SKILL.md).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — on the code
   BEHIND the pixels only: token resolvers, theme switches, contrast calculators,
   and state reducers pass with zero surviving mutants. A flipped comparison in a
   contrast check ships a beautiful, inaccessible screen. The gauntlet never
   scores taste — the rubric and the accessibility gate stay the visual judges.
   Render real DOM in tests; a mocked render proves nothing about what the human
   sees.

## Hard gates (play-specific — the skill's own hard rules apply on top)

- The critic is a DIFFERENT model family than the builder, resolved live through
  the fleet ladder — never a pinned model id (a retired pin silently kills the
  whole critic).

## Works well with

- [blind-tribunal](../skills/blind-tribunal/SKILL.md) — grade the whole deliverable
- [sniper-testing](../skills/sniper-testing/SKILL.md) — scope the component tests
