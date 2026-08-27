# Design Taste

构建"看着像设计过、不像生成出来"的 UI 的战术。千篇一律的 UI 是流程
（WORKFLOW）bug，不是模型 bug：把品味定夺和代码实现分开，先定死
设计 token（design token，即统一管理颜色、字号、间距的设计变量），
给 agent 一双眼睛，最后用无障碍标准把关。

## 什么时候用

任何会被人看到的屏幕、页面、组件、仪表盘或视觉交付物。第一个屏幕
会给之后所有屏幕定标准——动手前先跑这套。

## 链路

1. [intent-compiler](../skills/intent-compiler/SKILL.md) —— 从这个人自己的话
   里推断出他要的是哪一种品味，动笔前用一行话把你的解读说出来。
2. [human-calibration](../skills/human-calibration/SKILL.md) —— 把解读锚定在
   这个人的记录和真正研究过的参考上，绝不靠人群标签瞎猜。
3. 先产出三层设计 token 文件，再写任何组件——完整的 token 规范和
   禁用默认值清单见 [design-taste](../skills/design-taste/SKILL.md)。
4. 把 token 文件当硬约束注入后再写组件。组件里绝不硬编码裸的十六进制
   色值、像素值或字体族。
5. 按 [design-taste](../skills/design-taste/SKILL.md) 跑"截图 → 评审"循环，
   评审模型通过 [fleet-ladder](../skills/fleet-ladder/SKILL.md) 实时解析。
6. 按 [design-taste](../skills/design-taste/SKILL.md) 给 8 轴品味量表打分。
7. 按 [design-taste](../skills/design-taste/SKILL.md) 执行 WCAG 2.2
   无障碍硬门槛。
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) —— 只跑
   像素背后的代码：token 解析器、主题切换、对比度计算器、状态 reducer
   必须通过，变异体零幸存。对比度检查里一个翻转的比较符，交付出去的
   就是一块漂亮却用不了的屏幕。关卡从不给品味打分——量表和无障碍门槛
   才是视觉裁判。测试里渲染真实 DOM；mock 出来的渲染，
   证明不了人眼看到什么。

## 硬门槛（战术专属——技能自身的硬规则叠加生效）

- 评审必须和构建者来自不同的模型家族，通过 fleet ladder 实时解析——
  绝不写死模型 id（一个已退役的写死 id，会悄悄弄死整个评审环节）。

## 好搭档

- [blind-tribunal](../skills/blind-tribunal/SKILL.md) —— 给整个交付物打分
- [sniper-testing](../skills/sniper-testing/SKILL.md) —— 圈定组件测试范围
