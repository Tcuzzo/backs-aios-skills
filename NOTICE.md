# NOTICE — attribution and scaffold credits

## Authorship

BACKS AIOS Skills was composed and engineered by Tcuzzo (BACKS AIOS).
The selection, composition, hard rules, and harness design in this pack are the
author's own work. Language models were used as tools during construction; they
are not authors, and no model holds authorship credit anywhere in this pack.

This pack is licensed under the MIT License (Copyright (c) 2026 Tcuzzo
(BACKS AIOS)). See LICENSE.

## Scaffold credits (verified)

Each credit below names what was borrowed (the scaffold) and what is this
pack's own (the re-engineering and composition).

- **Matt Pocock — skills (MIT).**
  Pocock, M. (2025-2026). *skills* [Computer software]. GitHub.
  https://github.com/mattpocock/skills (MIT License).
  Scaffold credits, each verified against the live repository listing
  (2026-08-26):
  - `wayfinder` -> our wayfinder keeps his fog-of-war scaffold.
  - `grill-me` / `grilling` -> our blind-tribunal evolved the grill-me idea
    into cross-family blind adversarial grading; the tribunal design is
    BACKS AIOS.
  - `diagnosing-bugs` -> scaffold for our root-cause-first.
  - `handoff` -> scaffold for our session-handoff.
  - `wizard` -> scaffold for our guided-steps.
  - `research` -> scaffold for our live-research.

- **Jesse Vincent (obra) — Superpowers (MIT).**
  Vincent, J. (2025-2026). *Superpowers: An agentic skills framework &
  software development methodology* [Computer software]. GitHub.
  https://github.com/obra/superpowers (MIT License). Credits "Jesse Vincent
  and the team at Prime Radiant." Overlapping disciplines (TDD, systematic
  debugging) were compacted and re-engineered here; the composition is
  BACKS AIOS.

- **CRAP metric — Savoia & Evans (2007).**
  Savoia, A., & Evans, B. (2007). The C.R.A.P. (Change Risk Analysis and
  Predictions) metric and crap4j. Artima Developer.
  https://www.artima.com/weblogs/viewpost.jsp?thread=210575
  Formula: CRAP(m) = comp(m)^2 x (1 - cov(m)/100)^3 + comp(m); threshold 30.

- **Robert C. Martin — Clean Code (2008).**
  Martin, R. C. (2008). *Clean Code: A handbook of agile software
  craftsmanship.* Prentice Hall. ISBN 978-0-13-235088-4. Namesake inspiration
  for the clean-code gauntlet; commercial book — no content reproduced.

- **John Ousterhout — A Philosophy of Software Design (2018).**
  Ousterhout, J. (2018). *A Philosophy of Software Design.* Yosemite Press.
  "Deep modules" is Ousterhout's concept, kept under his name in the
  clean-code gauntlet; commercial book — no content reproduced.

- **Pocock & Martin — Software Fundamentals in the Age of AI (2026).**
  Pocock, M., & Martin, R. C. (2026, August 19). *LIVE: Uncle Bob on Software
  Fundamentals in the Age of AI* [Video]. YouTube.
  https://www.youtube.com/watch?v=zcLPGC-tvgk
  Source of the agentic method in the clean-code gauntlet: the agent CRAP
  band and coverage-first mutation testing.

- **W3C Design Tokens Community Group — token format.**
  W3C Design Tokens Community Group. *Design Tokens Format Module* [Community
  group draft report]. https://tr.designtokens.org/format/
  The tokens-first scaffold in design-taste; specification-and-citation only.

- **W3C — WCAG 2.2 (2023).**
  W3C. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2* [W3C
  Recommendation]. https://www.w3.org/TR/WCAG22/
  The accessibility hard gate in design-taste; standard-and-citation only.

- **UICrit — UI critique dataset (UIST 2024).**
  Duan, P., Cheng, C.-Y., Li, G., Hartmann, B., & Li, Y. (2024). UICrit:
  Enhancing automated design evaluation with a UI critique dataset. In
  *Proceedings of the 37th Annual ACM Symposium on User Interface Software
  and Technology (UIST '24)*. ACM. https://doi.org/10.1145/3654777.3676381
  Scaffold for the axis-scored screenshot critique in design-taste.

- **superdesign — AI design agent (AGPL-3.0).**
  AI Jason, & JackJack. (2025). *superdesign: AI design agent* [Computer
  software]. GitHub. https://github.com/superdesigndev/superdesign
  (AGPL-3.0; dual-licensed with a commercial enterprise license). Scaffold
  for the forbid-the-generic-defaults move in design-taste;
  inspiration-and-citation only, no code reproduced.

- **ASD-STE100, Issue 9 (2025).**
  ASD. (2025). *ASD-STE100, Simplified Technical English, Issue 9*
  [International standard]. https://www.asd-ste100.org/
  Publisher: ASD (AeroSpace, Security and Defence Industries Association of
  Europe), maintained by STEMG. Base register for human-voice, softened;
  inspiration-and-citation only.

- **Andrej Karpathy — autoresearch (MIT).**
  Karpathy, A. (2026). *autoresearch* [Computer software]. GitHub.
  https://github.com/karpathy/autoresearch (MIT License).
  Namesake inspiration; the keep-or-revert discipline is independently
  paralleled in Karpathy's autoresearch (2026). The blind (author-hidden)
  aspect is BACKS AIOS's own design.

- **Anthropic — Agent Skills / SKILL.md format.**
  The SKILL.md convention this pack is compatible with. Announced 2025-10-16
  (https://claude.com/blog/skills); format documentation at
  https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview,
  open standard at https://agentskills.io/, reference repository at
  https://github.com/anthropics/skills.

## References

Research cited inside the skills and plays:

- Spracklen, J., Wijewickrama, R., Sakib, A. H. M. N., Maiti, A., Viswanath,
  B., & Jadliwala, M. (2025). We have a package for you! A comprehensive
  analysis of package hallucinations by code generating LLMs. In *34th USENIX
  Security Symposium (USENIX Security 25)*.
  https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen
  Source of the web-app-builds figure: about 43% of hallucinated package
  names recur across identical re-runs.
- Panickssery, A., Bowman, S. R., & Feng, S. (2024). LLM evaluators recognize
  and favor their own generations. In *Advances in Neural Information
  Processing Systems 37 (NeurIPS 2024)*.
  https://proceedings.neurips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.html
  Establishes self-preference bias in LLM judges — why blind-tribunal hides
  authorship and grades cross-family. The bias is established; its size
  varies by model, so this pack quotes no number for it.

## Prior art

We found no existing public skill pack combining these three disciplines —
agent-harness invariants, a blind multi-model cross-family tribunal, and
red-first tamper-proof contract testing. Conceptually adjacent
verification-first work includes abvx-agent-skills
(markoblogo/abvx-agent-skills, MIT; verification-first gates, no tribunal)
and the temm1e Witness pattern (temm1e-labs/temm1e; a framework, not a skill
pack). This was a brief search, not an exhaustive one: none found, not none
exists.

## Retained attribution

Per the MIT License: the copyright notice and permission notice in LICENSE
shall be included in all copies or substantial portions of this pack. Keep
this NOTICE file, the LICENSE, and the inline scaffold-credit footers in
`skills/*/SKILL.md` intact when redistributing. Never invent a credit; never
strip one.
