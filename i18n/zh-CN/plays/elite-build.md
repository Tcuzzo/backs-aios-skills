# Elite Build —— 主战术

明确要求时，或构建、修复、升级需要其组合的设计、构建、质量与评审阶段时，
使用完整战术。用户只说一次目标。范围明确的改动可以只用 BACKS Build Flow
相关方法而不启动整个战术；选择本战术则须保留以下所有适用关卡。

## 一个任务，一位集成负责人

[BACKS Build Flow](../skills/backs-build-flow/SKILL.md) 负责任务包、`task_mode`、
operator essence 和完成状态。复用当前上下文、实际载入技能正文与证据；仅当
阶段输入或候选版本变化时刷新。所有通道保持固定 `base_sha`、当前
`candidate_sha` 和一位集成负责人。调用专业技能不会开启第二生命周期。

[bounded-loops](../skills/bounded-loops/SKILL.md) 负责原始截止时间和剩余任务额度。
研究、构建者、lint/类型/测试检查、变异、评审、回退模型和交接都消耗相同限制。
嵌套战术不得重置它们。耗尽时用 **STILL-BUILDING** 建立检查点，包含候选、证据、
未过关卡和下一步；继续完成不消耗已尽额度的有用已授权工作。预算限制不豁免关卡。

## 链路

0. [optimus](../skills/optimus/SKILL.md) — 每会话建立底线和 Build Flow 一次。
   复用上下文中仍存在的实际正文及其来源回执；单独回执不能替代缺失正文。
   嵌套调用不重启生命周期，也不声称未发生的调用。
1. 使用 Build Flow 已建立的意图和 operator essence。阅读完整请求和当前纠正；
   提出交付或选项决定前先推导指令。证据足以解决的选择直接解决。
2. [human-calibration](../skills/human-calibration/SKILL.md) — 应用任务包中已有的
   已验证档案。载入缺失且适用的上下文；不重新盘问用户或在每个阶段重建同一档案。
3. [turn-and-burn](../skills/turn-and-burn/SKILL.md) — 保留任务的模型名单和计划
   评审要求。可用时查阅各模型的 essence（know-thyself）、
   `docs/BACKS_LESSONS_LEARNED.md` 和 `memory/MEMORY.md`。这些能力/经验记录与
   operator essence 不同。复用当前 burn 证据；必要的 Absorb 工作共享本任务，
   并将结果返回集成负责人。
4. [understanding-gates](../skills/understanding-gates/SKILL.md) — 保留
   Design → Plan → Build → Test → Ship 阶段关卡。用
   [live-research](../skills/live-research/SKILL.md) 检查受影响路径、负责人、
   消费者和交付接缝。证据表明依赖可能改变结果时才继续追踪，不在每次编辑前重复
   全系统调查。Build Flow 的上下文开工条件满足后，开始下一项可执行步骤。
5. [architecture-engineer](../skills/architecture-engineer/SKILL.md) — 差异触及
   模块边界、依赖方向或共享接缝时，应用结构评审和权限界面分类器。每项违规须
   引用本地规则或具体失败模式；持久决定用 ADR 记录。
6. [wayfinder](../skills/wayfinder/SKILL.md) — 以证据绘制确实未决的路径。
   路径已知时不再开始另一轮规划。
7. [red-first](../skills/red-first/SKILL.md) — 构建者运行前，观察并提交真实失败
   契约。记录封条，逐字节保留原始文件。后续发现另建补充测试，不能重写原始 RED。
8. 在负责行为的接缝做最小而完整的改动。独立问题和工作用明确文件归属或隔离
   worktree 并行，保留一位集成负责人和项目并发规则。通过
   [fleet-ladder](../skills/fleet-ladder/SKILL.md) 解析构建者，任务需要时使用
   [model-fusion](../skills/model-fusion/SKILL.md)。缺陷在当前流程内应用
   [repair-loop](../skills/repair-loop/SKILL.md)，并按
   [seam-engineering](../skills/seam-engineering/SKILL.md) 在共享接缝关闭整类问题。
   发现返回本任务，不递归重启战术。
9. [sniper-testing](../skills/sniper-testing/SKILL.md) — 由固定基线到候选的汇总
   差异及自有待提交路径推导范围。运行仓库实际 lint、类型和聚焦测试命令。
   不适用标 N/A 并说明理由，缺少必需工具标为缺口；不任意安装检查器或编造通过。
   迭代期间保持限定范围运行。
10. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — 在当前流程内
    对同一候选执行质量、复杂度/覆盖率和有界变异检查。有意义的幸存者或发现，
    在剩余预算内转入补充 RED 和最小接缝修复。复用有效证据，不以旧裁决覆盖变化
    字节；不启动另一个完整构建生命周期。
11. [blind-eval](../skills/blind-eval/SKILL.md)，再
    [blind-tribunal](../skills/blind-tribunal/SKILL.md) — 向按能力与可用性在线
    选择的评审者提供去作者信息的冻结证据包。评审必须使用全新、与作者隔离的
    执行，不继承构建者对话。记录作者执行来源并排除它。每个证实发现都在相同
    剩余额度内建立独立 RED、修复和复审。所有必需陪审员通过后才落地。
    适用时遵循 tribunal 的 Solo rig 规则；记录实际配置和运行时缺口，不弱化独立性。
12. 完成所请求的状态。重新核实候选身份，完整运行一次受影响模块测试集及项目
    必需检查，保留并发工作，使用项目已授权落地流程。部署时验证已安装/运行的
    代码和用户真实界面。只有请求的交付及实际流程需要时才重启服务。
    本地补丁或评审不悄悄取得发布范围。

## 硬门槛

- 原始 RED 在修复前被观察为失败，并保持逐字节不变；补充契约各有自己的记录
  证据和封条。
- 必需质量、lint/类型/测试及变异关卡在确切候选上通过；有理由的 N/A 和实际
  缺口如实报告。
- 必需评审使用全新且与作者隔离的执行；构建者不自评，也不向评审者提供期望结论。
- 自有接缝上的每个发现已修复或有证据裁定。开放发现明确记录检查点并阻止落地，
  绝不能隐藏。
- 适用的 burn、essence、经验和计划评审要求由当前证据满足。复用证据不代表可以
  跳过必需关卡。
- 能力 **PROVEN** 意味着已落地、独立评审通过，并在用户实际界面证明。否则使用
  [human-voice](../skills/human-voice/SKILL.md) 报告 **STILL-BUILDING** 和准确缺失
  证据。完成所请求的评审或本地补丁，应与线上能力声明分别说明。
- 只提交本任务文件，保留其他会话工作。

## Fleet ladder 政策

实际派发、配置路径、实时探测、回退和评审独立性都使用
[fleet-ladder](../skills/fleet-ladder/SKILL.md)。部署提供时读取
`config/fleet_ladder.yaml` 和 `config/gpu_nodes.yaml`；本包不创建解析器。
保留配置梯级要求的前沿研究先行条件及允许的 web、GitHub、Reddit 和论文来源。
遵循配置的推理下限与 token 效率政策，不硬编码模型 ID，也不截短证据伪造合规。

中断前，用 [session-handoff](../skills/session-handoff/SKILL.md) 保留候选、封条、
证据、截止时间和剩余任务额度。
