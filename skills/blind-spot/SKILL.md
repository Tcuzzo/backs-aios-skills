---
name: blind-spot
description: Use when starting or resuming consequential work, investigating repeated failure or costly friction, reviewing a fix, crossing a handoff or release boundary, or checking completion. Combine current scope, lessons, operator essence, primary research, observable check primitives, fast binary System 1 predicates, and blind adversarial review of frozen scratch inputs. Remain model agnostic and reuse existing delivery owners and safeguards.
license: MIT
---

# Blind Spot

Blind Spot is a bounded evidence doctrine for finding what the current plan, fix, or
completion claim cannot see. It strengthens an existing delivery owner; it does not
start a second lifecycle, choose a model, create an authority gate, or replace the
repository's testing, review, landing, and rollback safeguards.

## The two questions

Ask these at the beginning, after material evidence changes, at handoff, and before
completion:

1. What important fact, dependency, failure mode, or affected person is outside the
   frame I am currently using?
2. What observable result would prove that the work is correct, and what observation
   would force a refusal?

Write both answers as checkable predicates. A persuasive explanation is not evidence.
An absent check is missing evidence, never permission.

## First principles and context

Reconstruct the current scope from source truth and the live task packet. Read the
acceptance criteria, affected producers and consumers, current lessons, known failure
classes, and operator essence. Preserve the operator's intent and the existing owner.
Use primary research when an external technical fact can change the architecture;
record the source, date, bounds, and the exact claim it supports. Separate stable facts,
current observations, assumptions, and advisory judgment. Reuse existing checks and
delivery safeguards before adding a new primitive.

## Bounded evidence loop

1. Freeze the task, inputs, dependency identities, and expected outcome.
2. Name the highest-cost blind spots and turn each into an observable check.
3. Run the cheapest decisive mechanical checks first, with explicit timeouts.
4. Project every required observation into the signed System 1 contract below.
5. Send only frozen, allowlisted scratch inputs to blind adversarial review.
6. Reconcile mechanical and advisory results. Repair a reproduced failure at its owner,
   or retain a loud refusal with the missing evidence and next action.
7. Stop when the declared predicates settle the question or the bounded allowance is
   exhausted. Checkpoint evidence; do not weaken the checks.

The bundled stdlib helpers are the portable reference tools:

- `scripts/observable_probe.py` measures a bounded real subprocess observation.
- `scripts/blind_packet.py` freezes and verifies allowlisted blind-review inputs and
  checks the review runtime's isolation canaries.
- `scripts/signed_gate.py` evaluates strict signed predicates without truthiness or
  multiplication.

## System 1: fast binary decisions

Every predicate verdict is the exact integer `-1` or `+1`. Booleans, zero, null,
floats, strings, and other coercions are invalid. Never use truthiness: `bool(-1)` is
true in Python even though `-1` is refusal. Never multiply verdicts: two refusals must
remain refusal, never flip into authorization.

A predicate carries a unique name, one of the reasons `satisfied`, `failure`,
`missing_evidence`, `stale_input`, or `timeout`, its input digest, evidence age, and a
non-empty authority. The gate returns `+1` only when every required predicate exists,
has an exact matching input digest, is no older than the declared freshness bound, has
a non-empty authority, and carries exact integer `+1` with reason `satisfied`. An empty
required set always returns `-1` with `missing_evidence`.

Mechanical evidence dominates all advisory output. A model may return `-1` to flag a
concern or suggest an additional check. It may never overwrite a mechanical `-1` with
`+1`. An unavailable advisory is recorded loudly and the deterministic plan remains
usable; it is never fabricated as approval.

## Blind adversarial review

Blind review receives a frozen scratch packet containing only explicitly allowlisted
candidate and dependency paths. The canonical manifest binds every relative path,
size, and SHA-256 digest; retain the manifest digest outside the packet and verify it
before accepting a review. Do not include author identity, prior reasoning, unrelated
repository contents, credentials, private topology, or mutable live inputs.

The reviewer is read-only. Run two canaries before trusting its verdict: attempt a
harmless read outside the allowlist and a harmless input write that is restored
byte-for-byte. If either action succeeds, the review runtime is `unisolated` and the
review predicate is `-1`. A review is advisory evidence about the frozen bytes; it
does not replace mechanical tests or grant mutation authority.

## `/rea` engine integration

When the target is a shipped binary, executable, package, firmware image, or packaged
runtime behavior, add a real file/binary observable predicate and invoke the existing
`/rea` investigation bridge. Bind the target's exact path and digest, the question,
the discovery or verification phase, static evidence, runtime observations, limits,
and unknowns. Static findings do not prove runtime behavior. Missing REA tooling or a
provider is a loud unavailable observation, not a reason to invent evidence or install
new dependencies. Return the evidence packet to the current delivery owner.

## Finish and learn

Completion requires every declared mechanical predicate to be fresh and `+1`, every
advisory concern to be repaired or explicitly reconciled without weakening mechanical
refusal, the frozen packet to verify against its externally retained digest, and the
real acceptance surface to show the outcome. Record what the blind spot was, which
primitive exposed it, the owning seam, the repair, and the structural guard that will
catch the next instance. Feed durable lessons through the repository's existing lesson
owner. A candidate, test, or advisory answer is not a landed or operator-proven result.
