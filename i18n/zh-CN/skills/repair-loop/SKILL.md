---
name: repair-loop
description: 修 bug、关掉上报的问题、或者端到端升级一条接缝时用它。跑完整的修复循环——扎根地板、在实况真相上复现、红色契约测试、在接缝处修掉整类、在真实路径上验证、独立评分、落地——并且一直迭代到全部成真。Trigger words: repair loop, dev mode, fix this, uplift, close the seam, dev build. 中文触发词：修复循环、修一下、把问题关掉、闭合接缝、升级、开发模式。
license: MIT
---

# Repair Loop

任何修复、关单或升级的默认循环。它是一种行为，不是审批机器：给人加的关卡为零、摩擦为零。它约束的是 agent，用一套纪律让"绿了但坏着"在结构上就难以出厂。

## 先加载，再谈设计或编辑

1. [invariant-floor](../invariant-floor/SKILL.md) — 干活之前先读你的规则集。
2. [human-calibration](../human-calibration/SKILL.md) — 应用这个人的画像；绝不重新审问对方。
3. [understanding-gates](../understanding-gates/SKILL.md) — 诊断规划器：Design → Plan → Build → Test → Ship。
4. [wayfinder](../wayfinder/SKILL.md) — 迷路时画出路线；绝不把问题扔给人搁着。
5. 请求如果是散文或比喻的形式，先跑 [intent-compiler](../intent-compiler/SKILL.md)，再对推导出的指令循环。

## 循环

1. **扎根地板。** 碰代码之前先加载规则和项目自己的真相（文档、源码、跟踪器）。凭对规则的记忆干的活不算数。
2. **在实况真相上复现。** 亲眼看到失败，在人真正使用的那条路径上——不是代理探针，也不是听信 bug 报告的一面之词。复现不了，就没有修复。
3. **红色契约测试。** 写一条捕捉这个缺陷的失败测试，修复之前先 commit。证明它真的是红的。修复让它变绿；修复绝不编辑测试。见 [red-first](../red-first/SKILL.md)。
4. **在接缝处修掉整类** — 而不是一个症状一块补丁。完整公式在 [seam-engineering](../seam-engineering/SKILL.md)。
5. **在真实路径上验证。** 信任但要核实。能力要在人自己的界面上证明——他敲字的 UI、他跑的命令——绝不靠一条 mock 了接缝的绿色测试。每个说法（"另一个分支已经落了""那个服务挂了"）都先对照实况真相查证再行动。
6. **给修复量个尺。** 循环中途，只跑覆盖你触碰的接缝的测试——见 [sniper-testing](../sniper-testing/SKILL.md)。然后对改动的代码跑 [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)：限定范围的测试、复杂度对覆盖率的评分、有界的变异测试。有变异体在你的修复下存活，说明测试根本没够到你改的分支——假绿；继续迭代。
7. **独立评分。** 一位没写这次改动的评分者——最好是与构建者不同家族的模型——必须放行。构建者绝不给自己的活打分。见 [blind-tribunal](../blind-tribunal/SKILL.md)。
8. **检查并发工作。** 变更共享状态之前，核实其他会话的进行中工作已被保全（在某个分支或 commit 上）。绝不 commit 或清理不属于你的工作。
9. **落地。** 落地时对触及模块的测试套件跑一次完整通过，然后 commit。这条接缝上循环揪出的每个发现都要关掉——或者对每个发现记录一个明确的、有证据的"不是 bug"裁决。"修了大的、其余延后"永远不许落地。

## 迭代到成真

一条尚未满足的规则不会停下循环——它驱动循环。升级模型或档位、清掉阻碍、重试，直到上面每一步都成真、改动落地。"差不多行了"不是一种状态。同一条接缝真的卡死两次，就记下确切的阻碍证据，转去下一个没被卡住的部分——绝不无声地空磨。

## 硬性规则 — 任何一条都会让这个技能失败

- 没在实况真相上复现就发出的修复。
- 修完才写的测试，或被修复改过的测试。
- 补了症状，而那一类还在接缝处敞着。
- 靠代理探针宣称绿了，而人自己的路径还坏着。
- 构建者给自己的改动打了分。
- 落地时无声搁置了某个已浮出的发现。
- 循环停在"差不多行了"，而不是升级再战。

## 汇报

两个词——**PROVEN** 或 **STILL-BUILDING**——外加用大白话说清意图，以及摆在人面前的那个唯一决定（如果有）。只有品味、愿景或破坏性风险的问题才去找人；见 [decision-bar](../decision-bar/SKILL.md)。

## 搭配使用

- [incident-closure](../incident-closure/SKILL.md) — 人报了故障时，这个循环跑在一次完整闭环里。
- [red-first](../red-first/SKILL.md) · [seam-engineering](../seam-engineering/SKILL.md) · [sniper-testing](../sniper-testing/SKILL.md)
- [blind-tribunal](../blind-tribunal/SKILL.md) · [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
