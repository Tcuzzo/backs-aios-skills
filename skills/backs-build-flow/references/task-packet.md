# One execution packet

Keep this record in the task's existing authorized state surface. For a strict
read-only review, return it in the response. A handoff does not widen permissions.

```yaml
objective: requested result and observable acceptance
task_mode: build_fix | read_only_review | investigate | resume_deliver
integration_owner: current writer or coordinator
target: verified repo/worktree/runtime and relevant caller/consumer path
base_sha: verified commit before task changes
candidate_sha: verified current commit; list pending work separately
preserve: unrelated edits, sealed RED files, compatibility requirements
authorization: scope already granted; actual unresolved external boundary
operator_awareness:
  source: private essence path or supplied evidence reference
  status: grounded | provisional | unavailable
  slice: relevant observation, evidence, adaptation, uncertainty
mission:
  mission_id: persistent identity across workers and resumes
  constraints: operator-specified limits and applicable provider constraints
  resources: measured usage or explicitly unavailable
episode:
  episode_id: current bounded-loop identity
  deadline: declared wall-clock boundary
  attempt_allowance: declared attempts or rounds
  attempts_used: measured attempts or rounds spent
  resource_budget: call_ceiling and cost_ceiling (number or null), plus other applicable limits
  resources_used: calls_used and cost_used (measured number or null), plus other usage
  prior_counters: immutable exhausted-episode counters retained across continuation
worker_state:
  status: active | idle | failed | completed
  workers: actual worker/session identifiers and terminal evidence; empty when none
continuation_binding:  # required only when native same-thread Stop continuation is requested
  session_id: exact native Codex session identity
  workspace: absolute active worktree path
  scope: nonempty changed/owned path list
  checkpoint_identity: durable checkpoint or candidate identity
  stall_limit: bounded repeated-progress allowance
  stall_count: measured repeated-progress observations
  progress_signature: current observable progress identity
skills: relevant body/source, purpose, evidence to return, exit condition
evidence:
  red: failing behavior command, revision, output, sealed file hash
  green: scoped lint/type/test commands, revision, results
  quality: measured gauntlet evidence and remaining gates
  delivery: actual artifact/runtime/revision verification
unknowns: decision-relevant gaps and unavailable tooling
next_action: concrete action and owner
```

Do not paste full histories, credentials, or other operators' profiles. A skill
receipt proves delivery of a body, not execution of its method. Revalidate stale
revision/runtime facts rather than rebuilding all context. The receiving worker acknowledges ownership, actual constraints, and the next action.
