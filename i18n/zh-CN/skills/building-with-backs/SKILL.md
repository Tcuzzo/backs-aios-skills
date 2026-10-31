---
name: building-with-backs
description: "构建或修复 BACKS 项目、解决目录或工作副本歧义，或把已授权改动从 IDE 推进到实际运行时时使用。"
license: MIT
---

# Building with BACKS

This skill closes a recurring failure: a good patch in the wrong checkout or a
green test that never reaches the operator's app. The destination is the human's
requested product and path. Discover the target before writing.

加入现有 [BACKS Build Flow](../backs-build-flow/SKILL.md) 任务包；直接调用时只建立
一次。保持一位集成负责人，复用既有 operator essence 与上下文。遵守 `task_mode`，
将 [bounded-loops](../bounded-loops/SKILL.md) 的截止时间和剩余额度贯穿工作者、
模型与交接。解析新路径不会重启预算，也不授权部署。

1. **Resolve the destination.** Use the exact path named by the human. If none was
   named, inspect the active workspace, recent project references, and repository
   map. Do not substitute a nearby clone merely because it has a matching name.
   从本技能目录运行
   `python scripts/resolve_target.py --repo <path> --target <file-or-directory>`；
   add `--expected-root <path>` when the human named the checkout. The command
   returns nonzero for a missing target root, a path outside that root, or a
   checkout mismatch or missing Git revision. A new target file may not exist
   yet; its parent must. For a specifically named non-Git project, add
   `--allow-non-git` and record that no revision is available.
2. **Pin the starting truth.** Record the resolved root, branch or detached HEAD,
   `base_sha`、当前 `candidate_sha`、工作区状态、请求目标、应用/服务入口和检查。
   提交过程中固定原始基线，明确更新候选身份并重新检查待提交路径。
   Preserve unrelated edits. If another checkout is newer, compare revisions and
   actual working trees before choosing; "newest" is a measured claim.
3. **Map the route.** Trace user action to entry point, implementation, data,
   outputs, and deployment seam. Name the existing owner of the behavior and
   any dependent consumers. Use `repo-map`, `architecture-engineer`, and
   `root-cause-first` when those seams are uncertain.
4. **Build in the resolved place.** Give parallel readers distinct questions and
   writers non-overlapping files or isolated worktrees. Keep one integration
   owner. 写能关闭整类缺陷的最小改动；在当前工作流内用 `repair-loop` 处理缺陷。
   选择或明确要求完整 `elite-build` 时遵循它，复用有效阶段而不重新启动。
   评审或诊断只返回发现，不编辑。
5. **证明真实路径。** 遵循当前封存 RED → 最小修复 → 精准 lint/类型/测试检查 →
   clean-code-gauntlet 循环。根据固定的汇总候选差异确定范围，使用仓库真实命令，
   如实说明缺失或 N/A 检查。保留作者隔离评审和必需的完整受影响测试集落地检查。
   在请求范围内检查实际应用/CLI 界面和运行日志，记录部署源的确切版本/哈希及
   观察行为，指出无法实际验证的内容。
6. **Promote through the project's own route.** Read its deployment instructions
   and approval rules from that repository. Never transplant a deployment
   command from another project. Re-run the target check before installation
   and verify the running process uses the installed code afterward.

If the destination remains ambiguous, keep read-only investigation moving and
ask for the missing path only after checking available evidence. Never claim a
cross-host installation merely because files were copied; verify discovery in
each host or mark it unverified.

额度耗尽时，以 **STILL-BUILDING** 建立检查点，保留已验证目标、候选版本、未决
证据和准确下一步。保留原始任务限制；完成不消耗已尽额度的有用已授权工作。
本地检查不能替代请求所需的交付证据。
