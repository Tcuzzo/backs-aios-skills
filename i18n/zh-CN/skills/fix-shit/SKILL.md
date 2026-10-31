---
name: fix-shit
description: "当操作者报告损坏行为、要求 fix shit 或停止吞错，或要求完成顽固缺陷修复时使用。"
license: MIT
---

# Fix Shit

在当前 [BACKS Build Flow](../backs-build-flow/SKILL.md) 任务内，将本技能作为
`root-cause-first` 和 `repair-loop` 的快速入口。保留同一集成负责人、operator
 essence、`task_mode`、候选身份和证据；不重新加载有效任务包或启动另一生命周期。
直接调用只建立一次任务包。[bounded-loops](../bounded-loops/SKILL.md) 的调用方
剩余预算和截止时间适用于每次复现、修复、模型回退和评审，本技能绝不重置它们
或隐藏失败信号。

1. 说明用户遇到的损坏行为及其出现的确切界面。
2. 从真实路径构建可重复的红色信号。追踪输入和每个边界，找到实际行为偏离
   预期的位置。构建者改变接缝前，用 [red-first](../red-first/SKILL.md) 封存
   原始失败契约。诊断任务返回该证据。
3. 确定根因和损坏接缝的所有调用方。在日志或操作者状态中保留原始错误；
   回退可以保护应用，但不能把失败变成虚假成功。
4. 已授权修复时，在当前流程中用 [repair-loop](../repair-loop/SKILL.md)：最小的
   整类修复、根据固定汇总候选差异限定真实 lint/类型/测试命令，再执行
   clean-code-gauntlet 的质量与变异检查。保留封存原件；新缺口另加补充测试。
   复用已验证阶段，不重复它们。
5. 完成所请求交付必需的作者隔离评审（author-disjoint）、受影响测试集落地关卡和真实应用路径检查。
   同时验证预期结果和显式失败状态。缺少评审能力属于运行时缺口，绝不是自授的独立通过。
6. 将候选版本和证据返回集成负责人。只有必需评审和真实交付证据齐全才报告 PROVEN；
   否则以 STILL-BUILDING 建立检查点，说明确切剩余红项和下一步。预算耗尽应保留
   工作和限制；有用且未受阻的工作也只能在剩余额度内继续。

If the error is intermittent, capture timing and a bounded reproduction rate;
do not infer a cause from one green rerun. For code-location ambiguity, start
with `building-with-backs` and its target check.


## 证据与独立评审

调查已发布的可执行文件、软件包或请求的运行时行为时，在分析有用的情况下调用 [rea-investigation](../rea-investigation/SKILL.md) 和单独安装的 `reverse-engineer-anything` 技能；对受支持的原生目标使用现有 Ghidra 提供程序。静态证据不能证明实时行为；不得悄悄安装缺失的提供程序。采用开源能力时调用 [absorb](../absorb/SKILL.md)。通过 [fleet-ladder](../fleet-ladder/SKILL.md) 按角色和能力选择，不硬编码模型名称。需要评审团时遵循 [blind-tribunal](../blind-tribunal/SKILL.md)：与作者分离的新执行审查去除作者信息的冻结材料。缺少解析器、评审者或证据时报告运行时缺口。
