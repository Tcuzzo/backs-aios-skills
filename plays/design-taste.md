# Design Taste

The play for building any UI that looks designed, not generated. Generic UI is a
WORKFLOW bug, not a model bug: split taste-making from implementation, set exact
design tokens first, give the agent eyes, and gate on accessibility.

## When to run

Any screen, page, component, dashboard, or visual deliverable a human will look at.
The first screen sets the standard for every screen after — run this before it.

The taste loop, at a glance:

```
+--------------------------------------------+
| 1 intent-compiler  WHICH taste do the      |
|   human's words ask for? state the read    |
+--------------------------------------------+
| 2 human-calibration  anchor in the record  |
|   + studied references, never a guess      |
+--------------------------------------------+
| 3 design-taste  emit the three-tier        |
|   token file FIRST, before any component   |
+--------------------------------------------+
| 4 build with the token file as a hard      |<--------------------------+
|   constraint -- no raw hex, px, fonts      |  critique -> fix ->       |
+--------------------------------------------+  re-shoot                 |
| 5 design-taste  screenshot -> critic;      |   +---------------------+ |
|   critic resolved live via fleet-ladder    |-->|  LORD OF THE LOOP   |-+
+--------------------------------------------+   | one hand drives the |
| 6 design-taste  8-axis taste rubric        |   | loop: dispatch,     |
+--------------------------------------------+   | judge, loop back    |
| 7 design-taste  WCAG 2.2 HARD gate         |   | until the gate is   |
+--------------------------------------------+   | green. a lane never |
| 8 clean-code-gauntlet  the code BEHIND     |   | lands its own work. |
|   the pixels; zero surviving mutants       |   +---------------------+
+--------------------------------------------+
          |
          | rubric + WCAG green
          v
+--------------------------------------------+
| LANDING GATE -- all green or no ship:      |
| WCAG 2.2 passes . 8-axis rubric scored .   |
| zero surviving mutants behind the pixels   |
| . critic family != builder family, live-   |
| resolved via fleet-ladder, never pinned    |
+--------------------------------------------+
```

## The chain

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — deduce WHICH taste
   the human's own words ask for, and state the read in one line before writing.
2. [human-calibration](../skills/human-calibration/SKILL.md) — anchor the read in the
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

**Weight:** light through the loop — calibration and the screenshot-critic pass each cost one extra run; the heavy step is the gauntlet on the code behind the pixels — it pays on any screen a human will actually look at.
