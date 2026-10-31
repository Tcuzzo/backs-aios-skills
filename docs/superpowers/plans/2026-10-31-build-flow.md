# Build Flow Integration Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for the integrated change, with one fresh whole-change reviewer. Steps use checkbox syntax for tracking.

**Goal:** Integrate one coherent Build Flow with Optimus and bounded REA/Absorb RED/GREEN work, then publish the verified source.

**Architecture:** One canonical flow owns transitions; existing disciplines own budgets, test scope, and quality checks. Existing loaders deliver the real body and existing aliases remain compatible.

**Tech Stack:** Markdown, Python, JavaScript, Bash/PowerShell installer fixtures, pytest.

**Spec:** `docs/superpowers/specs/2026-10-31-build-flow-design.md`

## Global constraints

- Preserve host schemas, authorization, tool availability, command names, sealed tests, and author-disjoint reviews.
- Keep public content free of private identities, paths, network addresses, and secrets.
- Use existing install/package routes; no changes to the user's machine settings in this source update.

## Review focus

- Missing native Build Flow with an available pack fallback delivers the actual fallback bytes.
- Missing/empty Build Flow produces no false successful grounding receipt.
- A clean committed candidate retains its changed-file test scope.
- New workers and review findings cannot reset an exhausted mission budget.
- REA discovery/verification returns to the existing owner without recursively starting adoption.

## Task 1: Pin loader and package contracts

**Files:** `tests/test_build_flow_integration.py`, `tests/test_floor_autoload.py`.

**Interfaces:** Actual SessionStart, compaction, explicit Optimus load, and isolated package installation.

- [x] Add real-subprocess tests for Build Flow delivery, hashes, single-copy loading, fallback, and missing-body behavior.
- [x] Run the new tests on the current source and record the expected RED failures: 14 failed as expected; baseline suite 313 passed, 10 skipped, 3291 subtests.

## Task 2: Integrate the canonical workflow

**Files:** `skills/backs-build-flow/`, `hooks/aios_gate.js`, `hooks/aios_gate.py`, and the affected canonical skill/play consumers.

**Interfaces:** The workflow packet preserves mode, base/candidate identity, owner, remaining budget, evidence, and next action. REA returns evidence to its caller.

- [x] Add the concise canonical skill and conditional references.
- [x] Make both Optimus loader routes deliver and hash the same foundation bodies.
- [x] Update budget, RED/GREEN, sniper scope, gauntlet, REA/Absorb, and existing consumers; preserve aliases and mandatory checks.
- [x] Run the focused loader/integration tests and fresh workflow scenarios.

## Task 2b: Operator essence and insight feedback

- [x] Add a portable operator-essence skill with a private evidence-backed file, qualitative observations, quantitative denominators, uncertainty, and counterexamples.
- [x] If essence is missing, invoke a supported insight workflow or assess available supplied evidence; label sparse data provisional and continue the authorized task.
- [x] Improve intent-compiler and intent deduction to use a relevant awareness slice without hardcoded operator identity or priorities; synchronize the compatibility alias.
- [x] Preserve the bounded RED/GREEN loop and add real scoped lint/type/test commands before the gauntlet.
- [x] Create and show the operator's private essence file separately from the public plugin.

## Task 3: Update distribution and verify delivery

**Files:** Locale mirrors, host guidance, README/INSTALL/visual docs, release manifests, package tests, and this plan.

**Interfaces:** Existing host discovery and archive builders receive one canonical workflow and compatible aliases.

- [x] Update all affected mirrors and active guidance; bump the existing release version consistently to 0.9.5.
- [x] Verify real package builds and isolated repeated installs preserve unrelated settings and unique discovery.
- [x] Run the full suite and parser checks; obtain a fresh independent review of the exact code candidate.
- [x] Fix proven findings with focused RED/GREEN checks while preserving sealed tests.
- [x] Publish the source and verify the remote revision and CI outcome.

## Verification receipts

### Behavior and distribution

- Pre-task base: `2b05798fe1618faf4513068f7cbb49aceaf71a13`.
- Complete suite on corrected candidate `14b213a2f23c469c56c5711fb9d712605778bd4b`:
  **387 passed, 11 skipped, 3942 subtests passed**, in 85.71 seconds.
- Final code candidate `3009a2e7b5c8b51eb9b7d8c458777af5c8e53fbf` removes one
  redundant Optimus identity condition. The existing loader, foundation, alias and
  committed-scope checks passed again: **38 passed, 6 subtests**, in 10.36 seconds.
- The fresh independent reviewer approved both candidates. The follow-up inspected
  the resolver invariant establishing the one-line cleanup's equivalence.
- Independent packaging review reproduced and closed two defects: omitted locale
  helpers and legacy alias resolution in deduplicated packages. Its actual installed
  consumer tests passed: **32 passed** across both new regression files.
- Locale helper RED: **18 expected failures**, then **18 passed** across all six
  real portable installs and canonical byte/executable-bit comparisons.
- Packaged alias RED: **14 expected failures**, then GREEN. Both real JavaScript
  and Python loaders resolve all three legacy spellings to canonical bodies.
- New essence helper: **16 RED then 16 GREEN**; a separate future-start regression
  reproduced its defect before the fix. Original sealed tests stayed unchanged.
- Claude artifact: **59 unique skills**, one 0.9.5 manifest, no alias directories,
  required references/helpers and all eight plays present. Archive validation checks
  committed bytes, safe paths, CRC, executable bits and absence of personal artifacts.

### Inline quality

- New Python helpers pass Ruff; shipped JavaScript and shell syntax checks pass.
  The repository has no configured Python type-checker gate. Existing unrelated
  lint findings were not relabeled as passing.
- Actual full-suite canonical coverage was 94% for the essence helper and 98% for
  the Git scope helper (line-and-branch combined). These are coverage measurements,
  not a claim that every profile field or host behavior was exercised.
- New helper maximum cyclomatic complexity is 7. Per-function CRAP uses measured
  executable-line coverage; no authored or changed function exceeds 30. The final
  loader cleanup returns its complexity to the pre-task value of 13.
- Comparable baseline coverage is unavailable, so no CRAP improvement is claimed.
  Two unchanged-source functions remain above 30: `_bash_is_mutating` and
  `checked_source`. The canonical `validate_preference` function was not covered
  by the measured suite; its low complexity score does not imply good coverage.
- A bounded scratch-only mutation campaign on `eb760d5` detected all **8 selected
  faults**. Scoped baseline: 41 passed and 6 subtests in 4.321 seconds; estimate for
  eight mutants: 34.569 seconds; mutation subprocess time: 12.701 seconds. One
  invalid test selector was inconclusive, corrected, and rerun before recording
  that mutant as detected. This is not an exhaustive mutation score. Later alias
  and locale corrections are covered by their separate installed-consumer tests.
- Fresh workflow scenarios exercised read-only review, ambiguous metrics, exhausted
  budgets, clean committed scope, red integration, unavailable insights and sealed
  regression handling. This is prompt-level evidence, separate from executable tests.

### Limits and publication

Native PowerShell/Windows installation remains unexecuted locally. Child-process
home propagation and Unix installations ran in disposable directories. No separate
desktop settings were edited, no unsupported insights invocation is claimed, and no
production productivity improvement was measured. The public repository contains
the reusable essence method only; actual operator evidence stays private.

The verified source tree was published as
[`f5292347e75392ce336361fd13560ae0082437a1`](https://github.com/Tcuzzo/backs-aios-skills/commit/f5292347e75392ce336361fd13560ae0082437a1).
The fetched GitHub tree exactly matched the locally verified source, and its
commit-metadata/content hygiene checks passed. The remote
[CI run](https://github.com/Tcuzzo/backs-aios-skills/actions/runs/41185346717)
completed successfully. This final documentation update records that observation.

Owned private-plugin read-back and the personal compatibility entry are separate
account delivery receipts. Public CI does not establish private-plugin activation
or discovery in a running desktop session.
