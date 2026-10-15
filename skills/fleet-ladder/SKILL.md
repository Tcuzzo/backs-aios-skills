---
name: "fleet-ladder"
description: "Use before any work is handed to a model (building, grading, or a bounded worker job), when a provider is down and you need the fallback order, or when the rung is frontier/design/reason and must honor research-before-heavy-lift. Resolves the LIVE model ladder from deploy yaml only: probe what is up, pick by explicit fallback order by capability and availability, gate frontier research seams, fail loud when exhausted. Trigger words: fleet, ladder, dispatch, fallback, model down, provider down, which model, availability, builder seat, frontier research, research seams, rung policy, thinking floor, token efficiency, research before builder, capability, oauth, api, quota, essence, checkpoint."
license: "MIT"
---

# Fleet Ladder
**Effort:** light — one cached live probe of the rung before any dispatch. Removes: dispatches to dead providers, model names hardcoded at call sites, frontier heavy-lift without realtime research, and the seat-itself-as-authority mistake.

Never hand-build a provider call, and never hardcode a model name at a call site.
One resolver owns the question "which model does this job right now?" — and it
answers from live truth (probe + provider status), not from a config file's
opinion. Capability and availability drive the choice; model identity records
provenance, never authority.

## When to run it

- Before ANY dispatch to a model: build, grade, review, or bounded worker job.
- When a provider is down and you need to know what falls back to what.
- The moment you catch yourself typing a model name into code or a prompt template.
- Before any frontier / design / reason heavy lift — load rung policy and research seams first.
- At every fallback step: record why (provider error, quota exceeded, transport
  refused), checkpoint the dispatch, and carry the full required context + tools.

## Source of truth (READ — never fork)

Resolution lives only in deploy ladder files. Skills teach agents to **honor**
them; Patch owns yaml edits.

| File | Absolute path (deploy parent) |
|------|-------------------------------|
| Fleet ladder | `<placeholder-mount>/backs_deploy/JarvisAI/config/fleet_ladder.yaml` |
| GPU nodes | `<placeholder-mount>/backs_deploy/JarvisAI/config/gpu_nodes.yaml` |

**NEVER** hardcode model IDs in skill text, prompts, or call sites as source of truth.
You may name **roles** in prose (`builder`, `grader`, `worker`, `frontier` / planner),
and you may name **capabilities** the job needs (long context, vision, code, reason).
Resolution = ladder + gpu_nodes files only. Patch owns yaml; Skills own these rails.

## The steps

1. **Declare the role AND the capability the job needs.** Every job asks for a
   role — `builder`, `grader`, or `worker` — and a capability (the kind of work it
   must do). The ladder maps roles to ordered model candidates and ranks candidates
   by capability fit plus live availability.
   - `builder`: implements and repairs.
   - `grader`: independent review — the authoring execution that built is
     disqualified; the grader runs in a fresh, author-disjoint session that did
     not see the builder's conversation or inherit its context.
   - `worker`: bounded, well-specified jobs. Cheaper rungs are fine here.
   - Capability is matched to the task from a list the ladder reads (long
     context, vision, code-gen, reason, tool-use, ...). A candidate that does
     not carry the capability is refused, even if it is the first rung.
2. **Read the ladder from deploy config.** Load `fleet_ladder.yaml` (+ `gpu_nodes.yaml`
   for local survival / organ placement). One file lists, per role, the candidates in
   explicit fallback order: strongest first, down to local GPU survival when clouds are dark.
   To change or add a model, **Patch edits that file** — never skill text, never call sites.
3. **Probe live before you trust.** A config listing is a claim, not truth. Probe the
   provider before dispatching to a rung — models-endpoint or a one-token request.
   Cache the probe for a sane window; do not hammer providers. A routing route is
   distinguished from a working inference: a probe that just replies is not a
   working candidate for a heavy task unless the ladder says so.
4. **Walk down, loudly.** Dispatch to the best AVAILABLE rung whose capability
   matches the task. On transport failure (provider down, oauth token expired,
   api error, quota exceeded), report loudly, checkpoint the dispatch with the
   reason, then try the next rung. Never skip silently. Carry the full required
   context and tools through every fallback step — never silently narrow.
5. **Exhaustion fails loud.** If every rung is down, raise a clear error naming what
   was tried: provider, role, capability, why each rung was refused, and the
   recorded cost / time / output budget of the run that hit the wall.
6. **Log provenance.** Append every dispatch: role, model chosen, rungs skipped and why,
   capability matched, quota budget consumed, and the run-time actuals. Provenance is
   recorded as fact — not as authority and not as a guarantee that a rung is still
   the right one next time. Shared quota is a measured account/route fact: it is
   not assumed because model names match across runs.

## Rung policy (honor builder seat + frontier research)

Encode on the ladder (Patch yaml). This skill **reads** those keys; it does not
invent a parallel policy. The builder's live identity is whatever the ladder
declares (typically `roles.builder.candidates[0]` plus identity / notes /
transport fields). Agents resolve the seat from the yaml — model IDs are never
pasted into skill forks.

### Builder seat
- The builder identity is the live value the ladder returns after Patch lands
  the operator order. The seat is read from yaml; it is not pinned here.
- The builder's run record carries `--builder <identity>` and `builder_family`
  where the portable runner supports them — these are runner-side fields, not
  universal flags. Skills teach how the **resolver** uses the recorded
  authoring execution: it disqualifies that exact execution and any session
  that inherited the builder's conversation or context out loud before any
  dispatch, and it reads `builder_family` for the same purpose when present.
  Provenance, not a blanket model, rung, family, or vendor gate.
- Agents resolve the seat from the yaml identity / notes / transport fields —
  do not paste model IDs into skill forks, and do not assume a runner that
  does not carry `--builder` will produce one.

### Frontier / design / reason — HARD research gate
Before any heavy design, solve, or reason lift on a rung that is marked
frontier (or that requires research seams), agents MUST:

1. Inspect the candidate card in `fleet_ladder.yaml` for flags such as:
   - `research_seams: true` / `requires_research_seams: true`
   - `frontier: true` / identity containing frontier / planner duty notes
   - `web_search` **not** set to disabled for that rung (frontier must keep search ON)
2. If any of those fire: run **realtime** research seams **before** the heavy lift:
   - internet / web search
   - GitHub
   - Reddit
   - scientific papers (arxiv / primary papers)
3. Pair with [live-research](../live-research/SKILL.md) for repo-grounded facts; do not
   treat model memory as the research seam.
4. **Never disable `web_search` on frontier / research-required rungs.** Mechanical
   Ollama-compat `web_search="disabled"` args are for non-frontier cloud-compat seats only —
   do not copy them onto frontier cards.
5. Failure to research = **invalid frontier use**. Prefer cheaper builder seats for
   mechanical build when research is not warranted.

### GPU / survival
Read `gpu_nodes.yaml` for local GPU organs. Local survival rungs stay on the
ladder; do not delete the local rail when clouds are preferred. The GPU
dispatch law (one model per card, no spill to system RAM, warm for the whole
loop, unload only at loop end) governs these organs — it is preserved here, not
re-invented.

## Research → token efficiency + thinking floor

**Purpose of the research seam (token efficiency):** gather frontier specs /
prior art **BEFORE** heavy builder lift so the builder's tokens spend on the
**correct scope** — not rediscovery. Research-first is the efficiency lever;
chopping prompts is not.

### Thinking scale (FLOOR = medium)
- Scale range: **ultra ↔ medium only**.
- **FLOOR = medium** — never drop below medium (no "low" / "minimal" thinking as a save-tokens move).
- **Autonomic primitives:** agents may scale thinking **UP** (toward ultra) or
  **DOWN** (toward medium) based on task hardness — never below the floor.
- Efficiency = research-first + right rung + thinking-floor discipline — **not** truncation.

### Explicit ban — no truncation hacks
**FORBIDDEN** as a thinking / token-efficiency control:
- truncating / chopping prompts, context, or history "to save tokens"
- fake efficiency via context amputation
Token efficiency comes from: research seams → correct cheap-builder specs →
right ladder rung → thinking floor discipline.

### Route token budgets (capability + host + auth, not provider name)
Route the budget by what the job needs and what the host can carry, not by a
provider label:
- **Sparse routes** (low token budget): short, bounded asks. Long envelopes,
  spec authorship, heavy builds, and long-envelope grading do not go here.
- **Heavy-lift routes**: large context, deep reasoning, long envelopes. These
  carry larger budgets — route design, spec, build, and long-envelope work here.
- Local GPU organs are NOT banned — the GPU dispatch law still governs them.
  Record the budget map in ledgers + ops manual so every session reads it from
  the harness, not from session memory.

### Expected ladder keys (Patch-owned yaml — Skills READ only)
Hermetic names for Patch tip / FOLLOW-ON (land into `config/fleet_ladder.yaml`;
do **not** invent a second SoT):

| Key | Expected shape / value | Notes |
|-----|------------------------|-------|
| `thinking_floor` | `medium` | Global or per-role/rung; never resolve below this |
| `thinking_scale` | `ultra` ↔ `medium` (ordered) | Autonomic up/down within this band only |
| `research_seams` | list or map | Maps research → cheap-builder / frontier specs before heavy lift |
| `requires_research_seams` | `true` on frontier / design / reason rungs | Existing HARD gate (deploy may still GAP until land) |
| `capabilities` | per-rung list | Capability tags each rung carries (long context, vision, code, reason, ...) |

If keys are **absent** on live deploy: skill still teaches this policy and
boards **GAP** for Patch. Never hardcode model IDs; resolve seats via ladder +
`gpu_nodes.yaml` only.

## Hard rules — break one and the skill failed

- **No model name at a call site.** Code asks for a role and a capability; the
  ladder answers with a model. Grep for model-name literals — each one is a bug.
- **No model IDs as skill source of truth.** Point at `fleet_ladder.yaml` + `gpu_nodes.yaml`.
- **The live probe outranks the config.** Checked-and-it-answers is settled;
  a stale list is not. A listing in the catalog is provenance; live
  availability is what dispatches.
- **The grader seat did not see the builder's authoring execution.** When the
  portable runner records the builder's authoring identity on the run
  (`--builder`, `builder_family`), the resolver disqualifies that exact
  execution and any session that inherited the builder's conversation or
  context out loud before any dispatch — provenance, not a blanket model,
  rung, family, or vendor gate. The exclusion is the authoring execution; a
  same model, rung, or family reviewer in a fresh, author-disjoint context is
  allowed where the configured runtime permits.
- **Frontier research-before-lift is HARD** when the rung marks frontier / research_seams.
- **Bounded probing.** Probes are cheap, cached, and backoff-aware.
- **No silent fallback.** Every step down the ladder is visible in the log and
  report, with the reason (provider error, quota, oauth expired, transport
  refused) and a checkpoint carrying the full required context + tools.
- **Thinking FLOOR = medium.** Scale ultra↔medium only; autonomic up/down; never below medium.
- **No truncation hacks** as token efficiency (no chopping context/history to "save tokens").
- **Route token budgets by capability + host + auth**, not by provider label.
- **Ground in the BACKS harness, never session or model memory.** BACKS is
  model- and context-agnostic with robust memory lanes — the harness carries
  the knowledge, not the model's head. Essence files (per-model know-thyself)
  load at the dispatch site, not from session chat.
- **Patch owns yaml; Skills own rails.** Do not edit `fleet_ladder.yaml` from this skill.

## Unresolved runtime mismatches (surface, never silently fix or bypass)

A few historical runtime pieces still ride alongside the matrix above. They
must be surfaced by name, never silently asserted fixed and never bypassed by
this skill:

- A legacy identity filter (model-name-only or family-only) on top of the
  capability + `--builder` policy is **not fixed** by this rewrite. If it sits
  underneath the resolver, the resolver still follows the matrix; the legacy
  filter becomes a separate ticket. Patch owns that ticket.
- An old role-prescription block on a previous version of this skill (named
  seat assignments, dated operator rulings pinned to a moment in time) is
  retired here. If the deploy ladder still reads from those legacy blocks,
  that is a GAP for Patch — do not paste the old assignments into this file
  and do not use them as authority. Read the live yaml.

## Works well with

- [live-research](../live-research/SKILL.md) — realtime seams before frontier heavy lift.
- [model-fusion](../model-fusion/SKILL.md) — panel/judge resolve through this ladder.
- [blind-tribunal](../blind-tribunal/SKILL.md) — jurors graded by capability and
  availability; ladder picks live ones; the builder's identity is refused out loud.
- [bounded-loops](../bounded-loops/SKILL.md) — probe cadence, backoff, kill-switches.
- [optimus](../optimus/SKILL.md) — harness boot loads this skill when dispatch is in play.
- [wayfinder](../wayfinder/SKILL.md) — chart route; frontier tickets still honor research gate.
