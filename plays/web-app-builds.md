# Web App Builds

How to build a web app or site with clean structure and a defended supply chain.
Most web-build damage comes in through dependencies and boundaries, not through
your own logic — so hygiene is the play, not an afterthought.

## When to run

Building or extending any web app, site, API, or delivered repo that someone else
will install and run.

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

1. Use the intent and operator essence established through Build Flow before
   choosing a stack or structure; apply the whole request and current corrections.
2. [understanding-gates](../skills/understanding-gates/SKILL.md) — design the
   structure first: one documented entrypoint, an explicit dependency manifest,
   and a committed lockfile. No ad-hoc file sprawl.
3. Dependency hygiene (do this BEFORE any install):
   - Validate every referenced package against the registry: it exists, it
     predates your project, its publisher has history. AI-hallucinated package
     names are squatting bait — measured research shows about 43% of hallucinated
     names recur across identical re-runs (Spracklen et al. (2025), USENIX
     Security 25), so attackers can pre-register them.
   - Hash-pin everything from a compiled lockfile (e.g. `pip install
     --require-hashes`, `npm ci --ignore-scripts`); refuse any integrity mismatch.
   - Block install-time lifecycle scripts by default. A package that only works by
     running a postinstall script is a red flag.
   - Pin every CI workflow dependency to a full 40-character commit SHA, never a
     mutable version tag.
   - Minimize the count: every dependency is a reviewed decision, not a reflex.
     Prefer the standard library or the platform primitive.
4. [red-first](../skills/red-first/SKILL.md) — failing contract tests for routes,
   loaders, and validation paths before building them.
5. Build to the doctrine below. For any UI surface, run the
   [design-taste](../skills/design-taste/SKILL.md) method — tokens first,
   accessibility as a hard gate.
6. [sniper-testing](../skills/sniper-testing/SKILL.md) — use the repository's real
   lint/type/test commands scoped from the pinned aggregate candidate diff; report
   gaps and justified N/A checks. Never mock your own validation or serialization:
   a mocked web boundary ships an app that accepts what it should reject.
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — route handlers,
   data loaders, and form/validation paths pass before deploy; run mutation over
   the validation and auth predicates within the shared budget; meaningful
   survivors block deployment. Add any missing regression in a separate file,
   preserving the sealed original RED. A boundary check
   whose flipped comparison still passes the suite is an open door on a public
   surface.
8. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — independent juror panel
   before the deploy, every juror chosen live by capability and availability
   from the configured rung matrix (the authoring execution that built is
   recorded as provenance and excluded; the reviewer uses a fresh
   author-disjoint session). Each substantiated finding gets a separate RED and
   bounded repair inside this task. Re-convene within the remaining budget;
   every required juror must pass. Preserve the full affected-suite landing gate
   and verify the authorized delivery on the real app surface.

## The doctrine (what the build must satisfy)

- No secrets in source: read credentials from environment or a secret store. A
  committed key fails the build.
- Output handling is context-aware: parameterized queries for SQL, and the correct
  encoding before any value reaches shell, database, or DOM. Never
  string-concatenate untrusted input.
- Emit a machine-readable SBOM, a software bill of materials (e.g. CycloneDX),
  so the recipient can audit the full dependency tree.
- Keep the build reproducible: pinned toolchain versions, deterministic install,
  and no EXTERNAL network access during the test run (local loopback services
  like databases and fixtures are fine and expected).

## Hard gates

- An unvalidated or unpinned dependency blocks the install.
- A committed secret blocks the build.
- Mutation survivors in validation or auth predicates block the deploy.
- External network access during tests blocks the landing (loopback is fine).

## Works well with

- [seam-engineering](../skills/seam-engineering/SKILL.md) — fix a boundary flaw as a class
- [bounded-loops](../skills/bounded-loops/SKILL.md) — rate-limit-aware outbound calls

**Weight:** free hygiene discipline through the build; the heavy spend is mutation over the validation and auth predicates plus the tribunal — it pays on every public surface, where one flipped comparison is an open door.
