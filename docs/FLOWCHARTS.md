# BACKS AIOS visual guide

These diagrams show how the pack moves from a human request to verified delivery.
They are maps, not extra rules. The linked skill and play files remain the source of
truth.

Mermaid renders directly on GitHub and in many IDEs. Every chart also has a **Text
version** for terminals, screen readers, and Markdown viewers without Mermaid.
Shapes carry meaning so the guide never depends on color:

- rounded box: start or finish;
- rectangle: action or skill;
- diamond: decision or gate;
- double-sided box: named play.

## Quick links

**Skills:** [absorb](../skills/absorb/SKILL.md) ·
[blind-eval](../skills/blind-eval/SKILL.md) ·
[blind-tribunal](../skills/blind-tribunal/SKILL.md) ·
[bounded-loops](../skills/bounded-loops/SKILL.md) ·
[clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) ·
[decision-bar](../skills/decision-bar/SKILL.md) ·
[design-taste](../skills/design-taste/SKILL.md) ·
[fleet-ladder](../skills/fleet-ladder/SKILL.md) ·
[gpu-dispatch](../skills/gpu-dispatch/SKILL.md) ·
[guided-steps](../skills/guided-steps/SKILL.md) ·
[human-calibration](../skills/human-calibration/SKILL.md) ·
[human-voice](../skills/human-voice/SKILL.md) ·
[incident-closure](../skills/incident-closure/SKILL.md) ·
[intent-compiler](../skills/intent-compiler/SKILL.md) ·
[invariant-floor](../skills/invariant-floor/SKILL.md) ·
[leap-protocol](../skills/leap-protocol/SKILL.md) ·
[live-research](../skills/live-research/SKILL.md) ·
[model-fusion](../skills/model-fusion/SKILL.md) ·
[optimus](../skills/optimus/SKILL.md) ·
[red-first](../skills/red-first/SKILL.md) ·
[repair-loop](../skills/repair-loop/SKILL.md) ·
[repo-map](../skills/repo-map/SKILL.md) ·
[root-cause-first](../skills/root-cause-first/SKILL.md) ·
[seam-engineering](../skills/seam-engineering/SKILL.md) ·
[session-handoff](../skills/session-handoff/SKILL.md) ·
[sniper-testing](../skills/sniper-testing/SKILL.md) ·
[understanding-gates](../skills/understanding-gates/SKILL.md) ·
[wayfinder](../skills/wayfinder/SKILL.md)

**Plays:** [elite-build](../plays/elite-build.md) ·
[agent-builds](../plays/agent-builds.md) ·
[web-app-builds](../plays/web-app-builds.md) ·
[design-taste](../plays/design-taste.md) ·
[grading-verification](../plays/grading-verification.md) ·
[parallel-work](../plays/parallel-work.md) ·
[security-delivery](../plays/security-delivery.md) ·
[bughunt](../plays/bughunt.md)

## 1. Pick the play

Start with the shape of the work. A play is a tested combination of skills; it does
not replace the individual skill files.

```mermaid
flowchart LR
  accTitle: Choose the BACKS AIOS play that matches the work
  accDescr: A request routes to one of eight named plays for general builds, agents, web apps, visual design, grading, parallel work, security, or bug hunting.

  Start([Human request]) --> Route{What kind of work is it?}
  Route -->|General build or fix| Elite[[elite-build]]
  Route -->|Agent or service| Agent[[agent-builds]]
  Route -->|Web app, site, or API| Web[[web-app-builds]]
  Route -->|Visual surface| Taste[[design-taste]]
  Route -->|Independent proof| Grade[[grading-verification]]
  Route -->|Several safe lanes| Parallel[[parallel-work]]
  Route -->|Customer-facing delivery| Security[[security-delivery]]
  Route -->|Find and close defects| Hunt[[bughunt]]

  Elite --> Floor[All plays stand on the invariant floor]
  Agent --> Floor
  Web --> Floor
  Taste --> Floor
  Grade --> Floor
  Parallel --> Floor
  Security --> Floor
  Hunt --> Floor
```

<details>
<summary>Text version</summary>

```text
Human request
  ├─ general build or fix ───────────> elite-build
  ├─ agent or autonomous service ────> agent-builds
  ├─ web app, site, or API ──────────> web-app-builds
  ├─ visual surface ─────────────────> design-taste
  ├─ independent proof ──────────────> grading-verification
  ├─ several safe lanes ─────────────> parallel-work
  ├─ customer-facing delivery ───────> security-delivery
  └─ defect hunt ────────────────────> bughunt

Every route stands on invariant-floor.
```

</details>

## 2. How all 28 skills fit together

The pack has four layers. Grounding learns the real job. Delivery turns that
understanding into a change. Scale coordinates models and lanes. Proof decides whether
the result may land.

```mermaid
flowchart TB
  accTitle: Complete map of all twenty-eight BACKS AIOS skills
  accDescr: Four connected layers show the grounding, delivery, scale, and proof skills that carry a request from session boot to live closure.

  subgraph Grounding["Grounding: know the job before acting"]
    direction LR
    Optimus[optimus] --> Floor[invariant-floor] --> Repo[repo-map]
    Repo --> Research[live-research] --> Intent[intent-compiler]
    Intent --> Human[human-calibration] --> Voice[human-voice]
    Intent --> Way[wayfinder]
    Human --> Decision[decision-bar]
  end

  subgraph Delivery["Delivery: build or repair the real seam"]
    direction LR
    Gates[understanding-gates] --> Red[red-first]
    Red --> Root[root-cause-first] --> Repair[repair-loop]
    Repair --> Seam[seam-engineering] --> Sniper[sniper-testing]
    Sniper --> Gauntlet[clean-code-gauntlet]
    Prior[absorb] --> Red
    Intent --> Visual[design-taste]
  end

  subgraph Scale["Scale: coordinate without losing control"]
    direction LR
    Bound[bounded-loops] --> Fleet[fleet-ladder] --> GPU[gpu-dispatch]
    Bound --> Leap[leap-protocol] --> Fusion[model-fusion]
    Leap --> Handoff[session-handoff]
  end

  subgraph Proof["Proof: decide, deliver, and close"]
    direction LR
    Eval[blind-eval] --> Tribunal[blind-tribunal]
    Tribunal --> Close[incident-closure]
    HumanSteps[guided-steps] --> Close
  end

  Intent --> Gates
  Decision --> Gates
  Gates --> Bound
  Gauntlet --> Eval
  Visual --> Eval
  Fusion --> Tribunal
  Handoff --> Tribunal
  Close --> Done([Live-proven result])
```

<details>
<summary>Text version</summary>

```text
GROUND
  optimus -> invariant-floor -> repo-map -> live-research -> intent-compiler
  intent-compiler -> human-calibration -> human-voice -> decision-bar
  intent-compiler -> wayfinder

DELIVER
  understanding-gates -> red-first -> root-cause-first -> repair-loop
  repair-loop -> seam-engineering -> sniper-testing -> clean-code-gauntlet
  absorb -> red-first
  intent-compiler -> design-taste

SCALE
  bounded-loops -> fleet-ladder -> gpu-dispatch
  bounded-loops -> leap-protocol -> model-fusion
  leap-protocol -> session-handoff

PROVE
  blind-eval -> blind-tribunal -> incident-closure -> live-proven result
  guided-steps supports incident-closure when a human-only step is real.
```

</details>

## 3. Session boot and grounding loop

The hook does not decide what the agent may build. It only prevents an ungrounded
agent from mutating files before it loads the floor.

```mermaid
flowchart TD
  accTitle: Session boot and deterministic grounding gate
  accDescr: Each session starts red, permits research, becomes green after a pack skill loads, and rearms when a new session, reset, or job begins.

  Start([Session starts or resets]) --> Red[Gate state: RED]
  Red --> Read[Read-only research stays available]
  Read --> Boot[Invoke optimus]
  Boot --> Floor[Load invariant-floor]
  Floor --> Map[Read repo-map and live source]
  Map --> Match[Load the skills matching this job]
  Match --> Green[Post-tool hook sets state: GREEN]
  Green --> Work[Mutating tools may run]
  Work --> New{New job, handoff, or context reset?}
  New -->|No| Work
  New -->|Yes| Red
  Red --> Mutate{Mutation attempted before grounding?}
  Mutate -->|Yes| Block[Block and point to optimus]
  Block --> Boot
  Mutate -->|No, research only| Read
```

<details>
<summary>Text version</summary>

```text
Session start/reset -> RED
RED -> research is allowed -> optimus -> invariant-floor -> repo map/live source
     -> matching skills load -> GREEN -> mutations may run
New job, handoff, or reset -> RED again
Mutation while RED -> blocked with a direct pointer to optimus
```

</details>

## 4. Elite build loop

Every stage checks against the human's original words. A failed stage goes through the
repair loop and returns to the same gate; it never skips forward.

```mermaid
flowchart TD
  accTitle: Elite build loop from original request to live proof
  accDescr: The original request moves through design, plan, build, test, independent grade, and ship gates, with every failure returning through repair to the same gate.

  Ask([Original request]) --> Intent[intent-compiler]
  Intent --> Calibrate[human-calibration when needed]
  Calibrate --> Stage["Run the current stage:<br/>Design → Plan → red-first and Build<br/>→ sniper Test → independent Grade → Ship"]
  Stage --> Gate{Current stage passes?}
  Gate -->|No| Repair[repair-loop names and fixes the failures]
  Repair --> Rerun[Rerun the same failed stage]
  Rerun --> Stage
  Gate -->|Yes| More{Another stage remains?}
  More -->|Yes| Advance[Advance exactly one stage]
  Advance --> Stage
  More -->|No| Quality[clean-code-gauntlet and final fact check]
  Quality --> Live[Prove it on the real surface]
  Live --> Land([Land and report])
```

<details>
<summary>Text version</summary>

```text
Original request -> intent -> human calibration (when needed)
  -> Design gate -> Plan gate -> red-first contract -> Build gate
  -> real-seam tests -> Test gate -> clean-code gauntlet
  -> independent grade -> Ship gate -> live proof -> land

Any failed gate -> repair-loop -> rerun the SAME gate.
```

</details>

## 5. Repair and bug-hunt loop

The loop closes a flaw class, not just the first symptom. Bug hunts repeat the same
loop independently for each verified finding.

```mermaid
flowchart TD
  accTitle: Root-cause repair and bug-hunt loop
  accDescr: A symptom is reproduced and traced to its source, protected by a red test, fixed at the shared primitive, swept across siblings, tested live, and independently graded until it passes.

  Symptom([Observed symptom]) --> Map[repo-map and live-research]
  Map --> Reproduce[Reproduce on demand]
  Reproduce --> Trace[root-cause-first]
  Trace --> Hypothesis[One falsifiable hypothesis]
  Hypothesis --> Red[red-first test proves the failure]
  Red --> Primitive[seam-engineering at the shared primitive]
  Primitive --> Sweep[Horizontal sweep of sibling paths]
  Sweep --> Sniper[sniper-testing]
  Sniper --> Live[Run the real operator path]
  Live --> Grade[blind grade]
  Grade --> Pass{Finding closed?}
  Pass -->|No| Trace
  Pass -->|Yes| More{More verified findings?}
  More -->|Yes| Reproduce
  More -->|No| Close([incident-closure])
```

<details>
<summary>Text version</summary>

```text
Symptom -> map/live source -> reproduce -> trace backward -> one hypothesis
  -> failing test -> shared-primitive fix -> sibling sweep -> sniper tests
  -> real path -> blind grade

Grade fails -> trace again
More verified findings -> run the loop again
No findings remain -> incident-closure
```

</details>

## 6. Understanding gates loop

The five stage gates all use the same anchor and verdict bands. “Approve” means the
stage may continue; only the real surface can prove the whole job done.

```mermaid
flowchart LR
  accTitle: Five understanding gates and their repair verdicts
  accDescr: Design, plan, build, test, and ship are each scored against the original request; revise repairs and reruns the same gate, while reject returns one stage.

  Anchor([Original request is the anchor]) --> Design[Design gate]
  Design --> Plan[Plan gate] --> Build[Build gate] --> Test[Test gate] --> Ship[Ship gate]
  Ship --> Live([Real-surface proof])

  Design --> Verdict{Verdict}
  Plan --> Verdict
  Build --> Verdict
  Test --> Verdict
  Ship --> Verdict
  Verdict -->|Approve: 80 and above| Continue[Continue to the next stage]
  Verdict -->|Revise: 60 to 79| Repair[Name failures, repair, rerun same gate]
  Verdict -->|Reject: below 60| Back[Return one stage]
  Repair --> Verdict
  Back --> Anchor
```

<details>
<summary>Text version</summary>

```text
Original request anchors every check.
Design -> Plan -> Build -> Test -> Ship -> real-surface proof

Approve (80+)  -> continue
Revise (60-79) -> name failures, repair, rerun the same gate
Reject (<60)   -> return one stage
```

</details>

## 7. Parallel work and model routing loop

Parallelism begins only after the work is split into independently ownable slices.
There is one write spine, so reconciliation remains deterministic.

```mermaid
flowchart TD
  accTitle: Safe parallel work and model routing loop
  accDescr: A mapped goal is split into bounded slices, routed through available models and GPUs, built in isolated worktrees, tested and independently reviewed per lane before one-at-a-time merge through the write spine.

  Goal([Mapped goal]) --> Split[leap-protocol creates scoped slices]
  Split --> Bound[bounded-loops sets cost, time, and retry limits]
  Bound --> Route[fleet-ladder probes available models]
  Route --> GPU[gpu-dispatch assigns one model per GPU when local]
  GPU --> Lanes[Isolated worktrees: one writer per slice]
  Lanes --> Readers[Parallel readers: research, tests, and grading]
  Readers --> LaneTest[Per-lane sniper tests and gauntlet]
  LaneTest --> LanePass{Lane passes?}
  LanePass -->|No| LaneRepair[Repair inside the same bounded lane]
  LaneRepair --> LaneTest
  LanePass -->|Yes| Tribunal[blind-tribunal in a clean context, per lane]
  Tribunal --> ReviewPass{Independent review passes?}
  ReviewPass -->|No| LaneRepair
  ReviewPass -->|Yes| Spine[Merge one lane at a time into the write spine]
  Spine --> MergePass{Merge tests and stat verification pass?}
  MergePass -->|No| LaneRepair
  MergePass -->|Yes| More{More lanes remain?}
  More -->|Yes| Lanes
  More -->|No| Handoff[session-handoff records the proven state]
```

<details>
<summary>Text version</summary>

```text
Mapped goal -> leap-protocol slices -> bounded budgets -> fleet-ladder
  -> gpu-dispatch when local -> isolated worktrees
  -> one writer per slice + parallel readers
  -> per-lane tests/gauntlet -> blind tribunal in a clean context
  -> merge one lane at a time into the write spine

Lane fails -> repair in that lane
Independent review fails -> repair and retest that lane
Merge test or stat verification fails -> repair and retest that lane
All lanes merged and verified -> session-handoff
```

</details>

## 8. Independent grade, human decision, and closure

The builder never grades its own work. Most findings are repaired automatically. Only
taste, vision, or destructive/data-loss risk belongs to the human.

```mermaid
flowchart TD
  accTitle: Independent grading, decision routing, and incident closure
  accDescr: An author-redacted change is graded by another model family, findings become failing tests, ordinary repairs execute automatically, and only true human decisions interrupt the loop before live closure.

  Change([Built change]) --> Redact[Remove authorship from the review envelope]
  Redact --> Eval[blind-eval]
  Eval --> Consequence{Consequential change?}
  Consequence -->|Yes| Tribunal[blind-tribunal with separate lenses]
  Consequence -->|No| Findings{Any verified finding?}
  Tribunal --> Findings
  Findings -->|Yes| Test[Turn each finding into a failing test]
  Test --> Decision{Taste, vision, or destructive risk?}
  Decision -->|No| Repair[repair-loop executes]
  Decision -->|Yes| Human[decision-bar sends one clear choice to the human]
  Human --> Repair
  Repair --> Eval
  Findings -->|No| Live[Live operator-path proof]
  Live --> Guided{Human-only dashboard or credential step?}
  Guided -->|Yes| Steps[guided-steps walks the human through it]
  Guided -->|No| Close[incident-closure]
  Steps --> Close
  Close --> Done([Land with evidence])
```

<details>
<summary>Text version</summary>

```text
Built change -> redact author -> blind evaluation
Consequential change -> blind tribunal
Verified finding -> failing test -> decision-bar
  ordinary repair -> execute automatically -> regrade
  taste, vision, or destructive risk -> ask the human once -> repair -> regrade
No findings -> live path proof
Human-only setup -> guided-steps
Then -> incident-closure -> land with evidence
```

</details>

## Read the diagrams in practice

1. Pick the closest play in chart 1.
2. Boot chart 3 before any mutation.
3. Follow the build loop or repair loop for the work.
4. Use the gate, parallel, and grading charts only when their decision points appear.
5. Open the linked skill whenever a node fires. A diagram label is a pointer, not an
   invocation.
