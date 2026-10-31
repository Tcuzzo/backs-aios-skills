# 战术：Bughunt

一场有边界的并行猎虫。先把狩猎画成一张地图，派猎手分头铺开，
用对抗方式核验每一条发现，并把整条接缝（seam，即代码里同类 bug
共同居住的位置）关死——绝不只治单个症状。

## 什么时候用

- 横跨多条接缝的审计、扫描或猎杀——不是单个已上报的 bug
  （那个走 repair loop）。
- 一堆积压的发现需要并行进攻，还不能跑偏、不能互相踩踏。

## 共享任务与限制

在当前 [BACKS Build Flow](../skills/backs-build-flow/SKILL.md) 任务包内应用本战术。
保留一位集成负责人、请求的 `task_mode`、固定 `base_sha`、当前 `candidate_sha`、
operator essence 和当前证据。复用适用的已载入技能正文；本战术增加领域关卡，
不重启任务。

[bounded-loops](../skills/bounded-loops/SKILL.md) 负责原始截止时间和剩余额度，
贯穿重试、工作者、模型、评审和交接。嵌套战术不得重置它们。耗尽时建立
**STILL-BUILDING** 检查点，保留候选版本、证据、未过关卡和下一步。
有用且已授权工作仅在剩余额度内继续；缺失关卡不能变成通过。

## 链路

1. [wayfinder](../skills/wayfinder/SKILL.md) —— 先把狩猎画成一张地图：
   每条接缝或每条发现一个节点。猎手从前沿（frontier）原子地认领节点；
   关掉一个节点，就写下下一个节点的问题。地图之外，什么也不许自创。
2. [leap-protocol](../skills/leap-protocol/SKILL.md) —— 每个节点就是一个球
   （ball）：目标、规格、硬性文件范围、有限轮次、三态结果。相关的球排进
   同一条按依赖排序的切片，写入者有且只有一个。
3. [root-cause-first](../skills/root-cause-first/SKILL.md) —— 改任何代码之前，
   先复现 bug、审阅根因证据。靠猜就动代码，不行。
4. [repair-loop](../skills/repair-loop/SKILL.md) — 每个工作包的内层纪律：
   [red-first](../skills/red-first/SKILL.md) 失败测试在修复前提交；
   [sniper-testing](../skills/sniper-testing/SKILL.md) 根据固定汇总候选差异限定
   真实 lint/类型/测试命令，落地时完整运行一次受影响模块测试集。
   原始 RED 不变，新发现另加补充测试。将证据返回调查负责人，不重启战术。

5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) —— 每条发现都要被
   对抗式进攻：一位不是作者的评审以"默认拒绝"的姿态进攻，陪审员评审一份
   抹去作者信息的卷宗。构建者绝不给自己的活打分。
6. [seam-engineering](../skills/seam-engineering/SKILL.md) —— 在共享接缝处
   关掉整个缺陷类（CLASS），绝不只关单个症状。
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) —— 收口证明：
   修好的分支在变异测试下必须死。变异体还活着的收口不算证明，
   这条发现继续挂着。

## 球怎么关

球只能通过 [leap-protocol](../skills/leap-protocol/SKILL.md) 的 Score 关卡
关掉——源头真相、留或回滚、盲审、线上实证、溯源记录；证据缺失绝不默认通过。
狩猎特有的终态：每条发现要么 FIXED（已修复），要么
REFUTED-WITH-EVIDENCE（有证据地驳回）。

额度耗尽时，发现保持开放并建立 STILL-BUILDING 检查点，不能宣称已达到终态
FIXED 或 REFUTED-WITH-EVIDENCE。认领下一个获准节点前，保留尝试历史和剩余任务限制。

## 狩猎守则

- 放低自信。从台账和节点的尝试历史重新校准，绝不靠自己的记忆。
  重启就意味着从前沿重新认领；交接走
  [session-handoff](../skills/session-handoff/SKILL.md)。
- 一边干一边用人话播报进度。未知就是未知——它永远不会变成"通过"。
- 候选字节、命令、测试、判定一旦冻结，落地就是一次确定性重放。
  已经定了的命令，不许再叫模型重新决定。
- 尊重这台机器：起进程前先量资源，限制并发，回收死掉的通道，
  同一节点第二次死掉就大声停下，所有对外调用都要限流。
  急停开关只拦新的认领——绝不打断正在飞的变更。
- 给每个切片的浪费起名字，前后都量。只有比较器证明零能力损失时才收下
  效率优化；过度膨胀同样是缺陷。
- 汇报只用两个词：PROVEN（已证实）或 STILL-BUILDING（仍在构建）。

## 硬门槛——踩中任何一条，整场战术判负

- 根因证据还没复现、还没审阅，就先改了代码。
- 构建者给自己的发现打分。
- 修好的分支上变异体还活着，发现却被关掉了。
- 狩猎中途跑全量测试——只狙击这条发现自己的接缝。
- 收口测试里搞 mock 剧场：台账说 bug 关了，实际它悄悄又开了。
- 悄悄搁置发现，或在未修复、未有证据反驳时将其标为关闭。

**Weight:** 核心是 free 的狩猎纪律；heavy 开销有三重——leap 并行展开、对抗式陪审团、变异收口证明——当整个积压清单并行关闭、每次收口都经变异测试证明时，这笔账就划算。
