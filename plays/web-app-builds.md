# Web App Builds

How to build a web app or site with clean structure and a defended supply chain.
Most web-build damage comes in through dependencies and boundaries, not through
your own logic — so hygiene is the play, not an afterthought.

## When to run

Building or extending any web app, site, API, or delivered repo that someone else
will install and run.

The build, at a glance:

```
+--------------------------------------------+
| 1 intent-compiler  read the ask whole      |
+--------------------------------------------+
| 2 understanding-gates  structure first:    |
|   one entrypoint, manifest, lockfile       |
+--------------------------------------------+
| 3 dependency hygiene  validate + hash-pin  |
|   every dep, no install scripts, pin CI    |
+--------------------------------------------+
| 4 red-first  contract tests for routes,    |<--------------------------+
|   loaders, validation -- committed first   |  finding -> a new red     |
+--------------------------------------------+  test -> fix ->           |
| 5 build to the doctrine; any UI runs       |  re-convene               |
|   the design-taste method                  |                           |
+--------------------------------------------+   +---------------------+ |
| 6 sniper-testing  never mock your own      |   |  LORD OF THE LOOP   |-+
|   validation or serialization              |   | one hand drives the |
+--------------------------------------------+   | loop: dispatch,     |
| 7 clean-code-gauntlet  mutate validation   |   | judge, loop back    |
|   + auth predicates until none survive     |   | until the gate is   |
+--------------------------------------------+   | green. a lane never |
| 8 blind-tribunal  cross-family grade       |-->| lands its own work. |
+--------------------------------------------+   +---------------------+
          |
          | every juror passes
          v
+--------------------------------------------+
| LANDING GATE -- all green or no deploy:    |
| no unpinned dep . no committed secret .    |
| zero mutation survivors in validation +    |
| auth predicates . no external network      |
| during tests (loopback is fine)            |
+--------------------------------------------+
```

## The chain

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — read the ask whole
   before choosing a stack or a structure.
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
6. [sniper-testing](../skills/sniper-testing/SKILL.md) — never mock your own
   validation or serialization: a mocked web boundary ships an app that accepts
   what it should reject.
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — route handlers,
   data loaders, and form/validation paths pass before deploy; run mutation over
   the validation and auth predicates until nothing survives. A boundary check
   whose flipped comparison still passes the suite is an open door on a public
   surface.
8. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — cross-family grade before
   the deploy. Every juror finding becomes a new red test; re-convene until
   every juror passes.

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
