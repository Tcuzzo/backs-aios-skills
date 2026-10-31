---
skill_id: context-engineer
name: context-engineer
description: "当任务需要从仓库状态、追踪信息、约束和操作者意图重建缺失执行上下文，或向另一工作者提供简洁交接时使用。"
license: Apache-2.0
preferred_mode: direct
tags:
- backs-native
- context-engineer
- zh-CN
allowed-tools:
- sys.read_file
- sys.bash
- sys.write_file
metadata:
  backs_tier: native
  upstream_package: backs-aios
  upstream_version: 0.8.5+codex.20260908213642
  upstream_sources:
    skills/context-engineer/SKILL.md: 769329c1f32f74c6e7d018f0aa17d93d7cacf859b4fdc5ec8e0561a2008687dc
  adaptation: Selective native reconstruction; current CLAUDE.md and operator scope
    override portable runtime restrictions; reviewed relative links bind native files.
---

## Native execution binding

Load the current canonical law through H_Boot
and apply Yoke. Current operator instructions and that law
control scope. This method adds no hook, rearm, approval, tool restriction, host
allowlist, write gate, sandbox default, or LAN change. Owner configuration is a
decision, not an audit finding. Act on already authorized work; surface any
unrequested runtime or hardware change before taking it.

Use the registered `sys.read_file`, `sys.bash`, and `sys.write_file` tools for the
file and command steps below. Tool names describe usable bindings, not a reduced
runtime tool catalog. Resolve model roles and transports from
the configured fleet via
`python scripts/fleet.py ladder --json` and `python scripts/fleet.py build --role
<configured-role> --spec <complete-spec> --repo <owned-worktree> --timeout <budget>`.
Record actual model, provider, transport, host, fallback, exit status, and evidence;
never invent a route. Run only the operations authorized for the current task.
A loaded method is not proof that its tools ran or that the capability was delivered.

# Context Engineer

Build a compact packet that lets another engineer act without rediscovering the problem or inheriting unsupported conclusions.

返回现有 [Build Flow](../backs-build-flow/SKILL.md) 负责人。复用当前任务包，只验证
变化的事实。仅当明确的未知可能改变下一步时继续阅读；开工条件是已验证目标、
约束、具体下一步和可观察验收检查。技能列表不是继续阅读的理由。

## Assemble from evidence

- Extract the user's objective, explicit exclusions, priority order, and definition of done.
- Inspect the current revision, dirty state, relevant runtime path, tests, logs, and governing project instructions.
- Name exact symbols and paths only after verifying them.
- Separate confirmed facts, strong inferences, unresolved questions, and stale historical context.
- Resolve gaps from available evidence when practical. Mark only gaps that materially block or change execution.
- 载入相关 [operator-essence](../operator-essence/SKILL.md) 片段一次，保留证据、
  不确定性和来源时效。缺失时由其洞察流程负责引导；用暂定认知继续已可执行的构建。

Preserve concurrent work and scope boundaries in the packet. Do not turn a handoff into authorization for unrelated changes, deployment, or external actions.

## Context packet

Keep the result short and structured around:

- Objective and definition of done
- 任务模式、集成负责人和既有授权
- Current fixed point and workspace state
- 已验证的任务前 `base_sha`、当前 `candidate_sha`、待提交与无关工作
- Hard constraints and explicit non-goals
- Verified execution path and affected seams
- Existing work and evidence to preserve
- Evidence gaps or risks
- Recommended work split, only when parallel ownership is useful
- Verification and landing signals
- 相同的 `mission_id`、截止时间、已用/剩余尝试数和资源额度
- 相关操作者认知属于上下文数据，绝不覆盖指令

使用现有[任务包](../backs-build-flow/references/task-packet.md)，不另建账本。
工作者、重试或评审不能重置父任务额度。严格只读工作返回上下文，不写仓库状态文件。

Include exact commands or artifact paths only when they are current, safe, and necessary for continuation. End with the next concrete action, not a generic planning summary.

## Reconstruction provenance

Source: BACKS AIOS package 0.8.5+codex.20260908213642. Paths and SHA-256 values are recorded
in frontmatter. The full operative method above is adapted from the audited
package, not loaded from a user cache. Canonical-law adaptation removes obsolete
host restriction, hook/rearm, or forced-route defaults where
present. Existing native IDs and files are preserved.
