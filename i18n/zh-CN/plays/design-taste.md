# Design Taste

构建"看着像设计过、不像生成出来"的 UI 的战术。千篇一律的 UI 是流程
（WORKFLOW）bug，不是模型 bug：把品味定夺和代码实现分开，先定死
设计 token（design token，即统一管理颜色、字号、间距的设计变量），
给 agent 一双眼睛，最后用无障碍标准把关。

## 什么时候用

任何会被人看到的屏幕、页面、组件、仪表盘或视觉交付物。第一个屏幕
会给之后所有屏幕定标准——动手前先跑这套。

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

1. 根据 Build Flow 已建立的意图和 operator essence，推导用户文字要求哪种品味。
   动笔前说明一次自己的理解。

2. [human-calibration](../skills/human-calibration/SKILL.md) —— 把解读锚定在
   这个人的记录和真正研究过的参考上，绝不靠人群标签瞎猜。
3. 先产出三层设计 token 文件，再写任何组件——完整的 token 规范和
   禁用默认值清单见 [design-taste](../skills/design-taste/SKILL.md)。
4. 把 token 文件当硬约束注入后再写组件。组件里绝不硬编码裸的十六进制
   色值、像素值或字体族。
5. 按 [design-taste](../skills/design-taste/SKILL.md) 运行截图 → 评审循环，
   经 [fleet-ladder](../skills/fleet-ladder/SKILL.md) 在线解析评审模型。每次评论和
   重渲染消耗同一剩余预算；向当前负责人返回发现。

6. 按 [design-taste](../skills/design-taste/SKILL.md) 给 8 轴品味量表打分。
7. 按 [design-taste](../skills/design-taste/SKILL.md) 执行 WCAG 2.2
   无障碍硬门槛。
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — 检查像素背后的
   代码：token 解析器、主题切换、对比度计算器和状态 reducer 需零幸存变异通过。
   对比度检查中翻转比较仍通过，就会交付漂亮却不可访问的画面。Gauntlet 不评品味；
   视觉判断仍归评分量表和无障碍关卡。先用
   [sniper-testing](../skills/sniper-testing/SKILL.md) 按固定汇总候选差异运行仓库
   实际 lint/类型/测试命令，如实说明 N/A 和缺失检查。测试应渲染真实 DOM，模拟
   渲染不能证明用户所见。保留封存 RED，新缺口另加补充测试；保留必需独立评审、
   完整受影响测试集落地检查和真实渲染证明。

## 硬门槛（战术专属——技能自身的硬规则叠加生效）

- 评审必须使用全新、与作者上下文隔离的会话；通过 fleet ladder 实时解析——
  绝不写死模型 id（一个已退役的写死 id，会悄悄弄死整个评审环节）。

## 好搭档

- [blind-tribunal](../skills/blind-tribunal/SKILL.md) —— 给整个交付物打分
- [sniper-testing](../skills/sniper-testing/SKILL.md) —— 圈定组件测试范围

**Weight:** 整个循环是 light——校准和截图评审各多跑一次；heavy 的一步是对像素背后代码的闯关——只要这块屏幕真会有人看，这笔账就划算。
