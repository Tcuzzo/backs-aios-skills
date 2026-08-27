# Elite Build —— 主战术

任何"构建 X""修复 X""升级 X"需求的默认战术。人只把目标说一次；
这套战术把整个环境组装起来，让他永远不用把基线再讲一遍。读懂意图、
加载这个人、给计划设关、先证明红、构建、精准测试、量化度量、盲评、落地。

## 什么时候用

任何有真实风险的构建、修复或升级。琐碎的一行改动可以直接跳到
[sniper-testing](../skills/sniper-testing/SKILL.md) 然后落地。

## 链路

0. [optimus](../skills/optimus/SKILL.md) —— 任何编辑之前先启动 harness
   （约束和驱动 agent 的执行框架）。地板先加载，每个会话，每一次。
1. [intent-compiler](../skills/intent-compiler/SKILL.md) —— 把需求当作完整的
   规格来读。在抛出任何交付或选项决定之前，先推断意图。存在明确解法时
   绝不端出选项菜单——直接解决它。
2. [human-calibration](../skills/human-calibration/SKILL.md) —— 加载这个人
   已验证的画像并照着做。已经认识的人，绝不重新盘问。
3. [understanding-gates](../skills/understanding-gates/SKILL.md) —— 设计 →
   计划 → 构建 → 测试 → 交付，每个阶段设关。设计之前：先通过
   [live-research](../skills/live-research/SKILL.md) 读现有的东西，复用已经
   写下的，画出完整拓扑。答案通常早就写好了。
4. [wayfinder](../skills/wayfinder/SKILL.md) —— 任何一步迷路时，靠证据画出
   路线。证据能回答的问题，绝不甩给人。
5. [red-first](../skills/red-first/SKILL.md) —— 在任何构建者动手之前，写好
   会失败的契约测试并提交。构建者不许碰那个测试。
6. 构建。默认并行铺开多条通道——能同时跑的绝不排队。每条通道有自己的
   临时分支或 worktree。单人单会话？一条通道就是铺开——在临时分支上构建，
   继续。（worktree 是同一个仓库在另一个文件夹里的第二份检出，让两个
   构建者永远碰不到同一批文件。）构建者通过
   [fleet-ladder](../skills/fleet-ladder/SKILL.md) 解析；草稿用
   [model-fusion](../skills/model-fusion/SKILL.md) 融合。遇到 bug，跑
   [repair-loop](../skills/repair-loop/SKILL.md)，并按
   [seam-engineering](../skills/seam-engineering/SKILL.md) 在共享接缝处
   关掉整个缺陷类。
7. [sniper-testing](../skills/sniper-testing/SKILL.md) —— 迭代期间只跑限定
   范围的测试；对触及模块的那一次完整跑，留到落地（第 10 步）。
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) —— 落地前
   先度量：狙击测试套件、复杂度×覆盖率的风险分低于你的上限，然后变异测试
   跑到零幸存。度量代码，绝不靠眼估。
9. [blind-eval](../skills/blind-eval/SKILL.md)，然后
   [blind-tribunal](../skills/blind-tribunal/SKILL.md) —— 一份抹去作者信息
   的卷宗，交给与构建者不同模型家族的评审。构建者绝不给自己的活打分。
   陪审员的每条发现都变成一条新的红测试；重新开庭，直到每位陪审员都放行。
   单机单模型？按 blind-tribunal 的 Solo rig 规则降级——并在落地报告里
   点名被削弱的关卡。
10. 落地——干净合并，对触及模块的测试套件完整跑一遍，重启真实服务，
    并在这个人自己的界面上（他打开的页面、他敲的命令）证明行为成立——
    绝不用代理探针。然后汇报。

## 硬门槛（任何一条红了就拦下落地）

- 失败测试在构建前已提交且没被动过——评审核实测试文件的 diff 为空。
- 构建者永远不当评审，且评审来自不同的模型家族。
- 每条浮出的发现都已关闭，或有记录在案的证据被裁定"不是 bug"。
  绝不静默搁置。整条接缝收口——接缝就是代码里这类 bug 共同居住的位置——
  否则不落地。
- 在这个人的真实界面上有线上实证。测试全绿但能力是坏的，就是失败，
  不是成功。
- 用 [human-voice](../skills/human-voice/SKILL.md) 汇报，只用两个词——
  PROVEN（已证实）或 STILL-BUILDING（仍在构建）。Proven 的意思是：
  已落地，加上独立评审通过，加上线上演示成立。
- 只提交这次改动自己的文件——绝不提交别的会话正在飞的工作。

## 好搭档

- [optimus](../skills/optimus/SKILL.md) —— 上下文压缩或重启后，重新启动地板
- [invariant-floor](../skills/invariant-floor/SKILL.md) —— 每次落地必须满足的锁定地板
- [decision-bar](../skills/decision-bar/SKILL.md) —— 什么该到人面前、什么直接执行
- [bounded-loops](../skills/bounded-loops/SKILL.md) —— 长跑任务的预算和急停开关
- [session-handoff](../skills/session-handoff/SKILL.md) —— 停下之前先封存状态

**Weight:** 全套堆栈——free 纪律、light 关卡，加三步 heavy（模型融合、闯关、陪审团）——heavy 开销在任何要出厂的东西上都划算，而这套战术就是为出厂而生。
