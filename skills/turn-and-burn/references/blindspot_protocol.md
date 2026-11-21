# The blind-spot evidence contract

This is the long form of the contract that
[turn-and-burn](../SKILL.md) points at. Read it when a blindspot answer is about
to be written, when a verdict is disputed, or when you are deciding whether a
green result is real.

## Why this exists

An agent asked "what could this plan miss?" will always produce something. The
failure is not silence — it is a confident sentence with no evidence behind it.
A blindspot answer is only worth acting on when the reader can check it.

So every blindspot answer in this pack is a **verdict with evidence**, not a
paragraph. Two verdicts exist:

- **+1** — the claim holds. Every required predicate has valid, current evidence.
- **-1** — the claim does not hold, or cannot be shown to hold. The reason names
  the predicate that failed.

There is no "probably". A missing predicate is a -1 with a reason.

## The six rules

1. **+1 requires every required predicate, with current evidence.** Missing,
   stale, incomplete, duplicate or malformed evidence leaves the verdict at -1,
   and the reason names the predicate that failed.
2. **Admission, execution and observation are three different facts.** Being
   allowed to run is not running. Running is not observed completion. A stage
   that never reached observation is never reported as done.
3. **A builder cannot author its own authoritative positive verification.** The
   builder may supply evidence; the authoritative +1 comes from the check that
   observed the thing, or from an independent reviewer.
4. **Independent review runs on frozen inputs, in separate scratch.** Isolation
   is claimed only when the runtime enforces it and it was demonstrated — never
   asserted because the reviewer was told to be independent.
5. **Repeated confidence without new evidence triggers a bounded, decisive
   investigation.** One probe that can tell the live causes apart, then -1 with
   the reason, or an escalation. Never a third repetition of the same conclusion.
6. **Use the organs the host already ships.** A red test, an independent
   reviewer, a real side effect to assert, a bounded loop with a checkpoint. Any
   mechanism the host cannot enforce stays marked **unvalidated until
   demonstrated** until a live receipt shows it holding.

## The evidence record

Every verdict carries one. Keep it small, and keep it checkable.

```yaml
blindspot: <the one-sentence claim under test>
verdict: +1 | -1
predicate_failed: <name of the predicate, only when verdict is -1>
evidence:
  - kind: test | command | file | receipt | review
    ref: <path, command line, or receipt id>
    observed_at: <timestamp>
    fresh: true | false
    author: builder | observer | independent-reviewer
isolation:
  frozen_inputs: true | false
  separate_scratch: true | false
  enforced_by: <the mechanism that enforces it>
status: validated | unvalidated until demonstrated
```

The fields that make a verdict load-bearing:

- **`fresh`** — evidence that predates the change it judges is stale, and stale
  evidence is a -1, not a caveat.
- **`author`** — evidence written by the same execution that made the change is
  supporting material, never an authoritative +1.
- **`enforced_by`** — isolation you cannot name a mechanism for is isolation you
  do not have.
- **`status`** — a mechanism that has never been shown holding on this host stays
  `unvalidated until demonstrated`.

## The verdict function

```text
verdict(claim, required_predicates, evidence, author) -> (+1 | -1, reason)

  for each predicate p in required_predicates:
      bound = evidence bound to p
      if bound is missing:
          return (-1, "predicate " + p + " has no evidence")
      if bound is stale or incomplete or duplicate or malformed:
          return (-1, "predicate " + p + " has " + bound.problem)
      if p requires observation and bound.kind != observed:
          return (-1, "predicate " + p + " was never observed")
      if p requires independence and bound.author == author:
          return (-1, "predicate " + p + " was verified by its own author")

  if claim was already asserted with the same evidence:
      return (-1, "no new evidence — run one decisive probe")

  return (+1, "")
```

Two properties of this shape are the point. The verdict cannot be softened: there
is no branch that returns a qualified yes. And the reason is always the name of
the predicate that failed, so the next probe is chosen, not guessed.

## Acceptance scenarios

**Passes (+1).** A build claims the new endpoint writes a row. The red test was
committed first, the builder did not touch it, the test runs against the real
database and reads the row back, the review of that run happened in a separate
session with the author's context withheld, and the run is on the human's own
surface. Every predicate has current evidence from a non-author observer, and
the isolation is enforced by the runtime, not by a promise. Verdict: +1.

**Fails (-1), and the reason names the predicate.** The same build, but the
reviewer was told to be independent and the host cannot start a session without
the author's conversation. The isolation predicate has no evidence behind it, so
the verdict is -1 with the reason "predicate isolation has no evidence", and the
fix is to run the review on a host that can isolate, or to report that it could
not be isolated.

**Fails (-1) on staleness.** The proof is a green test run before the last
change to the code under test. The evidence is old, so the verdict is -1 with
the reason "predicate proof has stale evidence". Re-run it, then answer again.

**Fails (-1) on a missing observation.** The plan's stage was admitted and
executed, but nobody watched it finish. "Executed" is not "observed", so the
observation predicate fails and the verdict is -1.

**Fails (-1) on repetition.** The same conclusion was reported twice with no new
evidence between the two reports. The third report is not a confirmation; it is
the signal to stop and run one decisive probe that can separate the live causes.

**Fails (-1) on a mocked proof.** The test mocks the exact seam that was
supposed to be proven. The evidence is malformed by construction — a mock of the
thing under test proves nothing — so the verdict is -1 and the repair is a real
side effect: a file on disk, a row read back from the real database, a real
payload in a real DOM.

## How to get this behavior on your host

The contract is portable. These are the organs that make it real rather than
aspirational, and every one of them is something the pack expects you to bring
or point at.

- **A red contract test.** Write it, commit it, prove it fails for the reason
  you claim, and let the builder make it green without touching it. See
  [red-first](../../red-first/SKILL.md).
- **A real side effect to assert.** A file, a database row, a real payload. If
  the test can pass while the capability is broken, it is not a proof. See
  [sniper-testing](../../sniper-testing/SKILL.md).
- **A way to start a fresh session.** Independence is a property of the
  runtime, not of an instruction. If your host cannot, the verdict is -1 and the
  report says so.
- **A bounded loop with a checkpoint.** Retries, workers, review rounds and
  handoffs share one budget. On exhaustion, checkpoint and escalate — never
  continue silently.
- **A place to file lessons.** A lessons file the next session reads before it
  plans. Without one, the same mistake is paid for twice.
- **A surface to prove on.** The human's own screen or command. A proxy probe
  while the real surface is broken is a false green.

## Red flags

- A +1 with no evidence, or evidence that is only the author's word.
- A -1 with no reason, or a reason that names a symptom instead of a predicate.
- A stage reported done because the previous stage was done.
- A review claiming isolation it never demonstrated.
- The same conclusion reached again with no new evidence.
- A proof that mocks the seam it claims to prove.
- A verdict that was softened to "looks good" because the deadline was close.

Each red flag is a -1 waiting to happen. The fix is always the same: go get the
evidence, or say plainly that it is missing.
