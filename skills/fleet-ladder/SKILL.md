---
name: fleet-ladder
description: Use before any work is handed to a model — building, grading, or a bounded worker job — or when a provider is down and you need the fallback order. Resolves the LIVE model ladder: probe what is actually up, pick the best available by an explicit fallback order, fail loud when the ladder is exhausted. Trigger words: fleet, ladder, dispatch, fallback, model down, provider down, which model, availability.
license: MIT
---

# Fleet Ladder
**Effort:** light — one cached live probe of the rung before any dispatch. Removes: dispatches to dead providers, and model names hardcoded at call sites that break the day the model retires.

Never hand-build a provider call, and never hardcode a model name at a call site.
One resolver owns the question "which model does this job right now?" — and it
answers from live truth, not from a config file's opinion.

## When to run it

- Before ANY dispatch to a model: build, grade, review, or bounded worker job.
- When a provider is down and you need to know what falls back to what.
- The moment you catch yourself typing a model name into code or a prompt template.

## The steps

1. **Declare the role, not the model.** Every job asks for a role — `builder`,
   `grader`, or `worker`. The ladder maps roles to ordered model candidates.
   - `builder`: implements and repairs.
   - `grader`: independent review — structurally never the same model that built.
   - `worker`: bounded, well-specified jobs. Cheaper rungs are fine here.
2. **Read the ladder from config.** One file lists, per role, the candidates in
   explicit fallback order: strongest first, down to your local survival tail
   (whatever you can run on your own hardware when every cloud provider is dark).
   To change or add a model, edit that file — never the code. Starter shape:
   [ladder.example.yaml](ladder.example.yaml) — copy it, swap the placeholders.
3. **Probe live before you trust.** A config listing is a claim, not truth. A stale
   entry lists models that are dead; it also omits models that are alive. Probe the
   provider before dispatching to a rung — a models-endpoint call or a one-token
   request, e.g.:
   `curl -s "$PROVIDER_BASE_URL/v1/models" -H "Authorization: Bearer $API_KEY"`
   (or the same shape against the chat endpoint with `"max_tokens": 1`).
   Cache the probe result for a sane window — do not hammer providers by re-probing
   every call. Refresh the cache only when you actually need fresh truth.
4. **Walk down, loudly.** Dispatch to the best AVAILABLE rung. On transport failure,
   report the failure loudly, then try the next rung. Never skip silently — the
   record must show which rungs failed and why.
5. **Exhaustion fails loud.** If every rung is down, raise a clear error naming what
   was tried. A job that cannot be dispatched never silently succeeds, waits
   forever, or degrades to a made-up answer.
6. **Log provenance.** Append every dispatch to a log: role, model chosen, rungs
   skipped and why. Later you must be able to answer "who actually did this work?"

## Hard rules — break one and the skill failed

- **No model name at a call site.** Code asks for a role; the ladder answers with a
  model. Grep your codebase for model-name literals — each one is a bug.
- **The live probe outranks the config.** If the human says a model exists and the
  config disagrees, probe it. Checked-and-it-answers is settled; a stale list is not.
- **Builder and grader never resolve to the same model** for the same change.
  If the ladder would collapse them onto one model, the grader takes the next
  independent rung — or the job fails loud.
- **Bounded probing.** Probes are cheap, cached, and backoff-aware. A tight retry
  loop against a dead provider is forbidden.
- **No silent fallback.** Every step down the ladder is visible in the log and in
  the report. Degrading quietly is how a broken route dies unnoticed.

## Works well with

- [model-fusion](../model-fusion/SKILL.md) — the panel and judge resolve their models through this ladder.
- [blind-tribunal](../blind-tribunal/SKILL.md) — jurors come from different families; the ladder picks live ones.
- [bounded-loops](../bounded-loops/SKILL.md) — probe cadence, backoff, and kill-switches.
