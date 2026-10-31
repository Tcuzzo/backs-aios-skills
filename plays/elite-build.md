# Elite Build — the master play

Use this full play when explicitly requested or when a build, fix, or uplift needs
its composed design, build, quality, and review stages. The human states the goal
once. A scoped change can use BACKS Build Flow's relevant methods without starting
this entire play; selecting this play preserves every applicable gate below.

## One task, one integration owner

[BACKS Build Flow](../skills/backs-build-flow/SKILL.md) owns the task packet,
`task_mode`, operator essence, and finish. Reuse current context, actual loaded
skill bodies, and evidence; refresh a stage only when its inputs or candidate
change. Keep the pinned `base_sha`, current `candidate_sha`, and one integration
owner across all lanes. Calling a specialist does not start a second lifecycle.

[bounded-loops](../skills/bounded-loops/SKILL.md) owns the original deadline and
remaining mission allowances. Research, builders, lint/type/test checks, mutation,
reviews, fallback models, and handoffs spend those same limits. Never reset them
in a nested play. On exhaustion, checkpoint **STILL-BUILDING** with candidate,
evidence, unmet gates, and the next action; complete useful authorized work that
does not consume the exhausted allowance. A budget limit never waives a gate.

## The chain

0. [optimus](../skills/optimus/SKILL.md) — establish the floor and Build Flow once
   per session. Reuse actual bodies still present in context and their source
   receipts; a receipt alone cannot substitute for a missing body. A nested call
   does not reboot the lifecycle or claim an invocation that never occurred.
1. Use the intent and operator essence established through Build Flow. Read the
   whole request and current corrections; deduce the directive before surfacing
   a ship or option decision. Solve an evidence-resolvable choice directly.
2. [human-calibration](../skills/human-calibration/SKILL.md) — apply the human's
   validated profile already in the task packet. Load missing applicable context;
   never re-interrogate a human or reconstruct the same profile at every stage.
3. [turn-and-burn](../skills/turn-and-burn/SKILL.md) — retain the mission's roster
   and plan-review requirements. Consult each model's essence (know-thyself),
   `docs/BACKS_LESSONS_LEARNED.md`, and `memory/MEMORY.md` when available. These
   capability and lesson records are distinct from operator essence. Reuse the
   current burn evidence; any necessary Absorb work shares this mission and
   returns its result to the integration owner.
4. [understanding-gates](../skills/understanding-gates/SKILL.md) — preserve the
   Design → Plan → Build → Test → Ship stage gates. Use
   [live-research](../skills/live-research/SKILL.md) to inspect the affected path,
   owners, consumers, and delivery seam. Follow additional dependencies when
   evidence says they can change the result; do not repeat a whole-system survey
   before each edit. Begin the next executable step when Build Flow's context
   readiness conditions hold.
5. [architecture-engineer](../skills/architecture-engineer/SKILL.md) — for a diff
   touching a module boundary, dependency direction, or shared seam, apply its
   structural review and authority surface classifier. Cite the local rule or
   concrete failure mode behind each violation; use an ADR for a durable decision.
6. [wayfinder](../skills/wayfinder/SKILL.md) — chart a genuinely unresolved route
   from evidence. Do not start another planning pass when the route is known.
7. [red-first](../skills/red-first/SKILL.md) — observe and commit the real failing
   contract before its builder runs. Record the seal and preserve the original
   file byte-for-byte. A later finding receives a separate supplemental test;
   it cannot rewrite the original RED.
8. Build the smallest complete change at the owning seam. Parallelize independent
   questions and work with explicit file ownership or isolated worktrees; retain
   one integration owner and the project's concurrency rules. Resolve builders
   through [fleet-ladder](../skills/fleet-ladder/SKILL.md), using
   [model-fusion](../skills/model-fusion/SKILL.md) where the mission calls for it.
   For a defect, apply [repair-loop](../skills/repair-loop/SKILL.md) inline and
   close the class at the shared seam per
   [seam-engineering](../skills/seam-engineering/SKILL.md). Return findings to this
   task rather than recursively restarting the play.
9. [sniper-testing](../skills/sniper-testing/SKILL.md) — derive check scope from
   the pinned aggregate base-to-candidate diff plus owned pending paths. Run the
   repository's actual lint, type-check, and focused test commands. Record N/A
   with a reason where inapplicable and missing required tools as gaps; do not
   install arbitrary checkers or invent passes. Keep scoped runs during iteration.
10. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — apply quality,
    complexity/coverage, and bounded mutation checks inline to the same candidate.
    A meaningful survivor or finding returns to a supplemental RED and minimal
    seam fix within the remaining budget. Reuse valid evidence, never a stale
    verdict for changed bytes; do not launch another full build lifecycle.
11. [blind-eval](../skills/blind-eval/SKILL.md), then
    [blind-tribunal](../skills/blind-tribunal/SKILL.md) — provide an author-redacted
    frozen evidence packet to reviewers selected live by capability and
    availability. Review must use fresh author-disjoint executions with no
    inherited builder conversation. Record the authoring execution as provenance
    and exclude it. Every substantiated finding gets a separate RED, fix, and
    re-review within the same remaining allowance. All required jurors must pass
    before landing. Follow the tribunal's Solo rig rule where applicable; record
    the actual configuration and runtime gaps without weakening independence.
12. Complete the requested finish. Recheck candidate identity, run one full
    touched-module suite pass plus required project checks, preserve concurrent
    work, and use the project's authorized landing procedure. For a deployment,
    verify installed/running code and the human's real surface. Restart a service
    only when the requested delivery and actual procedure require it. A local
    patch or review does not silently acquire release scope.

## Hard gates

- The original RED was observed failing before the fix and remains byte-identical;
  supplemental contracts have their own recorded evidence and seals.
- Required quality, lint/type/test, and mutation gates pass on the exact candidate,
  with justified N/A checks and actual gaps reported honestly.
- The required review uses a fresh author-disjoint execution; the builder never
  grades its own work or supplies the reviewer's desired conclusion.
- Every finding on the owned seam is fixed or adjudicated with evidence. An open
  finding is checkpointed explicitly and blocks landing; it is never hidden.
- Applicable burn, essence, lesson, and plan-review requirements are satisfied by
  current evidence. Reusing evidence is not permission to skip a required gate.
- Capability **PROVEN** means landed, independently graded, and demonstrated on
  the human's actual surface. Otherwise report **STILL-BUILDING** and the precise
  missing proof in [human-voice](../skills/human-voice/SKILL.md). State completion
  of a requested review or local patch separately from a live capability claim.
- Commit only this task's files. Preserve another session's work.

## Fleet ladder policy

Use [fleet-ladder](../skills/fleet-ladder/SKILL.md) for actual dispatch, configured
routes, live probes, fallback, and review independence. Read the deployment's
`config/fleet_ladder.yaml` and `config/gpu_nodes.yaml` where provided; the pack does
not create a resolver. Preserve frontier research-before-lift requirements on
configured rungs and their allowed web, GitHub, Reddit, and paper sources. Honor
the configured thinking floor and token-efficiency policy; do not hardcode model
IDs or truncate evidence to manufacture compliance.

Use [session-handoff](../skills/session-handoff/SKILL.md) to preserve candidate,
seals, evidence, deadline, and remaining mission allowances before an interruption.
