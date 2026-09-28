---
name: design-taste
description: Build UI that looks designed, not generated — tokens first, screenshot-critic loop, 8-axis taste rubric, accessibility gate.
argument-hint: the screen, page, or component to design
---

Load the bundled `plays/design-taste.md` using `${CLAUDE_PLUGIN_ROOT}/plays/design-taste.md` in Claude Code or `${CURSOR_PLUGIN_ROOT}/plays/design-taste.md` in Cursor, then execute it, whole, on: $ARGUMENTS

Order: intent-compiler (name WHICH taste the ask wants) → human-calibration → emit the three-tier design-token file BEFORE any component → build with tokens as a hard constraint (no raw hex, pixels, or font families in components) → screenshot → critic loop → 8-axis taste rubric.

Hard gate: every rubric axis scores at least 2 and the WCAG 2.2 accessibility check passes — or the loop continues; it does not ship.
