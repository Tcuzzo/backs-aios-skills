---
name: "optimus"
description: "开始或续接需要 BACKS harness 与相关任务技能的智能体会话、任务或自主循环时使用。"
license: "MIT"
---

# Harness Boot
**Effort:** light — 每个会话一次启动流程，加载地板和本次任务的技能，外加一个运行零成本的确定性 hook。消除：不接地的编辑——规则还没读就动手的改动，以及读完规则后随之而来的那场重做。

一条规则：**harness 没加载，就没有代码、没有任务。**harness（约束和驱动 agent 的执行框架）= 本包的不变量地板，加上覆盖当前任务的那些技能。每个会话、每个运行时、每一次。为什么：一条要靠 agent"记得"的规则，恰恰会在 agent 最忙的时候失效——所以加载规则是第一个动作，而且用 hook 把它做成结构性的，而不是劝告性的。

## 什么时候运行

会话或新任务开始时运行；上下文重置或交接后重新验证。内层重试复用当前 grounding
和同一任务包。重载缺失或变化的正文，不为每次迭代重启完整生命周期。

## 启动序列

1. **加载不变量底线。** 动手前读取 [invariant-floor](../invariant-floor/SKILL.md)，
   整个会话建立在这份底线上。
2. **应用 [Build Flow](../backs-build-flow/SKILL.md)。** 它负责任务模式、开工条件、
   技能选择、带限定范围 lint 与测试的有界 RED/GREEN、gauntlet 证据和交付。
   复用已验证任务包，只收集下一项具体行动所缺的事实。专业技能返回同一负责人。
3. **按需应用人类上下文**（[human-calibration](../human-calibration/SKILL.md)）。
   [operator-essence](../operator-essence/SKILL.md) 负责有证据的认知文件以及文件缺失
   时的洞察梳理，不开启第二轮档案流程。
4. **加载会话。** 会话 hook 交付实际的 Optimus、Yoke 和 Build Flow 正文，以及
   可用时已经证明的原生 harness。上下文压缩后重载这些正文，不撤销已经完成的
   grounding。改动工具缺少标记时触发加载，绝不拒绝工具。没有上下文 hook 的宿主可用：
   ```bash
   node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
   ```
   Codex shell 将活动的 `CODEX_SESSION_ID` 作为最后一个参数。也可使用对应的
   Python `aios_gate.py` 加载器。未知技能返回非零，不编造回执。
5. **应用下一步需要的技能。** 说明每项的目的、输出和退出条件。只点名未调用等于
   没发生。复用当前上下文仍可用的实际正文；记忆中的摘要或文件哈希不能替代正文。
6. 然后才写代码、运行修改命令或改变任何内容。

## 自动 grounding

现有 hook 读取基础文件，通过宿主上下文交付正文，并且只在交付后记录来源哈希。
上下文加载回执与实际 Skill 事件证据不同；加载指针或计算文件哈希不算调用该技能。

- 会话启动和上下文压缩重载底线，不收回工具。
- 会话标记缺失时，在下一次匹配的工具调用自动加载。
- 正文缺失或不可读时给出可见诊断，不产生虚假回执；操作者和智能体保留工具。
- `--rearm <session_id>` 请求再次加载，绝不锁住会话。
- `AIOS_GATE=off` 仍是操作者现有的可逆停用开关。
- Hook 在本地确定性运行，不新增模型调用或网络依赖。

## 硬性规则（任一项导致失败）

- Harness 加载前进行修改。
- 报告声称使用了本会话中未调用的技能。
- 用会话记忆、模型先验或“我记得”替代 BACKS harness。BACKS 不依赖模型或上下文，
  并有可靠的记忆通道；知识由 harness 的记忆文件、剧本、账本和梯级 YAML 承载，
  不在模型脑中（操作者裁定 2026-09-26）。
- Hook 拒绝任何工具、撤销已完成 grounding，或报告并未发生的加载。
- 新增第二道关卡或对人增加摩擦。停用开关仍归操作者。

## 搭配使用

- [invariant-floor](../invariant-floor/SKILL.md) — 启动最先加载的那块地板。
- [human-calibration](../human-calibration/SKILL.md) — 启动序列里的画像那一步。
- [repair-loop](../repair-loop/SKILL.md) — 启动之后，修复任务跑的东西。
- [bounded-loops](../bounded-loops/SKILL.md) — 启动开出的每个循环的预算。
- [wayfinder](../wayfinder/SKILL.md) — 启动时发现你不认路，就用它。


## Fleet ladder 梯级政策（简要指引）

任何模型派发或前沿设计/推理升级前，调用 [fleet-ladder](../fleet-ladder/SKILL.md)。
它要求读取 `config/fleet_ladder.yaml` 和 `config/gpu_nodes.yaml`（部署路径），遵守
实际可用的构建席位，并在梯级标记 frontier / `research_seams` 时强制开展实时研究
（web、GitHub、Reddit 和论文）。不要硬编码模型 ID；YAML 由 Patch 负责。
参考：`observe/SECURITY_OPERATOR_BUILDER_SEAT_ORDER_20260926.md`。

遵守 [fleet-ladder](../fleet-ladder/SKILL.md)：在支持时采用 medium 或更高的推理
基线，重任务前先研究，不截断上下文。
