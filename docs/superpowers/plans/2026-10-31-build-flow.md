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

- [ ] Add real-subprocess tests for Build Flow delivery, hashes, single-copy loading, fallback, and missing-body behavior.
- [ ] Run the new tests on the current source and record the expected RED failures.

## Task 2: Integrate the canonical workflow

**Files:** `skills/backs-build-flow/`, `hooks/aios_gate.js`, `hooks/aios_gate.py`, and the affected canonical skill/play consumers.

**Interfaces:** The workflow packet preserves mode, base/candidate identity, owner, remaining budget, evidence, and next action. REA returns evidence to its caller.

- [ ] Add the concise canonical skill and conditional references.
- [ ] Make both Optimus loader routes deliver and hash the same foundation bodies.
- [ ] Update budget, RED/GREEN, sniper scope, gauntlet, REA/Absorb, and existing consumers; preserve aliases and mandatory checks.
- [ ] Run the focused loader/integration tests and fresh workflow scenarios.

## Task 3: Update distribution and verify delivery

**Files:** Locale mirrors, host guidance, README/INSTALL/visual docs, release manifests, package tests, and this plan.

**Interfaces:** Existing host discovery and archive builders receive one canonical workflow and compatible aliases.

- [ ] Update all affected mirrors and active guidance; bump the existing release version consistently.
- [ ] Verify real package builds and isolated repeated installs preserve unrelated settings and unique discovery.
- [ ] Run the full suite and parser checks; obtain a fresh independent review of the exact candidate.
- [ ] Fix proven findings with focused RED/GREEN checks, publish the source, and verify the remote revision and CI outcome.
