# Build Flow integration

## Intent

Give BACKS agents enough verified context to act, then carry authorized work
through its requested finish. Integrate Build Flow into Optimus and the existing
REA/Absorb, repair, verification, and delivery paths. Keep one lifecycle owner,
one mission budget, and one canonical definition per discipline.

## Scope and constraints

- Preserve existing command names, context aliases, host events, permissions,
  operator controls, and independent author-disjoint review requirements.
- Keep source aliases compatible and deduplicate them in package discovery;
  do not delete a caller's existing skill entry point.
- Deliver the real Build Flow body through existing Optimus loaders in both
  JavaScript and Python. Record only bodies actually delivered. Add no hook or
  tool-denial mechanism.
- Bound attempts, wall time, and applicable measured resources across workers,
  hypothesis changes, review rounds, and resumption. Budget exhaustion produces
  an exact checkpoint, never green and never an automatic fresh allowance.
- Pin test scope to a base revision and candidate, including owned pending
  changes. Preserve the scope after commits and across handoffs.
- Keep the original sealed RED contract unchanged. New regressions or mutation
  findings get additional tests, not edits that weaken the sealed evidence.
- Use REA for evidence at the relevant source/artifact/runtime boundary; preserve
  the separately installed engine/provider boundary. Discovery returns to the
  adoption owner, and verification returns to that same owner.
- Update canonical skills, active consumers, locale mirrors, host guidance,
  package manifests and docs. Preserve personal data exclusions.
- Publish the verified source to the existing GitHub repository. All-host
  installation and the user's machine settings are a later command request;
  verify packaging/install behavior in isolated homes now.

## Approach

Use a single `backs-build-flow` skill for context readiness, stage transitions,
and completion. Keep `bounded-loops`, `sniper-testing`, and
`clean-code-gauntlet` as the owners of their detailed contracts. Existing entry
skills use short inline stage instructions and link to those owners. This avoids
copying a second lifecycle into every skill and preserves current entry points.

The alternatives were adding another master orchestrator alongside every play,
or replacing existing skill names. The former repeats context; the latter breaks
callers. The implementation choice is shared ownership of policy with compatible
entry points and behavioral tests at the existing loader seam.

## Evidence before changes

Current Optimus loaders deliver Optimus and Yoke, but have no Build Flow body.
Sniper testing uses `git diff --name-only HEAD`, which becomes empty after a
committed fix. Absorb does not call REA; REA can call Absorb and repair-loop,
so reciprocal orchestration needs an explicit return-to-owner contract. Repair
can escalate until true while bounded-loops separately requires budget exits.

## Acceptance

Real JavaScript/Python loader subprocesses deliver each required body once and
bind receipts to those bytes; missing bodies never produce false receipts.
Clean committed changes remain in test scope. Packaged and isolated installed
skills resolve the new workflow without duplicate names or recursive adoption.
Scenario checks preserve an exhausted budget and the sealed RED contract.
The full repository suite, public hygiene, package builds, and an independent
whole-change review must pass before GitHub publication.
