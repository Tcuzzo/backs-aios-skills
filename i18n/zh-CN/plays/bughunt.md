# 战术：Bughunt

一场有边界的并行猎虫。先把狩猎画成一张地图，派猎手分头铺开，
用对抗方式核验每一条发现，并把整条接缝（seam，即代码里同类 bug
共同居住的位置）关死——绝不只治单个症状。

## 什么时候用

- 横跨多条接缝的审计、扫描或猎杀——不是单个已上报的 bug
  （那个走 repair loop）。
- 一堆积压的发现需要并行进攻，还不能跑偏、不能互相踩踏。

## 链路

1. [wayfinder](../skills/wayfinder/SKILL.md) —— 先把狩猎画成一张地图：
   每条接缝或每条发现一个节点。猎手从前沿（frontier）原子地认领节点；
   关掉一个节点，就写下下一个节点的问题。地图之外，什么也不许自创。
2. [leap-protocol](../skills/leap-protocol/SKILL.md) —— 每个节点就是一个球
   （ball）：目标、规格、硬性文件范围、有限轮次、三态结果。相关的球排进
   同一条按依赖排序的切片，写入者有且只有一个。
3. [root-cause-first](../skills/root-cause-first/SKILL.md) —— 改任何代码之前，
   先复现 bug、审阅根因证据。靠猜就动代码，不行。
4. [repair-loop](../skills/repair-loop/SKILL.md) —— 每个球的内功：
   [red-first](../skills/red-first/SKILL.md) 先提交失败测试再修，
   [sniper-testing](../skills/sniper-testing/SKILL.md) 迭代期间只跑限定范围
   的测试，落地时对触及的模块完整跑一遍。
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
- 一条发现被搁置，而不是被修复或有证据地驳回。
