---
name: design-taste
description: 在构建任何视觉产物之前使用——网站、应用、仪表盘、控制台、演示稿——让它带着真正的品味出厂，而不是一股 AI 默认味。Trigger words: design, UI, taste, design tokens, design system, accessibility, WCAG, screenshot critique, dark mode, restyle. 中文触发词：设计、界面、品味、设计 token、设计系统、无障碍、截图评审、深色模式、改版。
license: MIT
---

# Design Taste——token 先行、睁眼构建、无障碍硬门
**Effort:** light — 写任何组件之前先出一份 token 文件，每个渲染出的界面再加一轮“截图 → 视觉评审”。消除：把千篇一律的 AI 默认样式再出厂一遍——改样式的返工和出厂后的无障碍补课。

千篇一律的 UI 是流程 bug，不是模型 bug。用结构解决它：把需求描述当规格读，写任何组件之前先定死设计 token，点名封禁那些默认套路，用截图循环给构建者装上眼睛，无障碍设成硬门——不过不发。

## 什么时候用

- 任何"帮我做个 / 设计个……"、最终要渲染成像素的请求。
- 搭前端脚手架或做面向客户的交付物之前。
- 现有界面看着平庸，需要一个具体、站得住脚的方向时。

## 步骤

1. **把需求描述当规格读。** 人话里的比喻、节奏感、点名的年代、艺术家或地点，都是
   具体的设计约束，不是点缀。完整的读题纪律见：[intent-compiler](../intent-compiler/SKILL.md)。
2. **选一个有根据的方向。** 挑一个*主参照*（真实存在的设计系统或组件库，定下结构
   基线）和一个*点睛参照*（把它的签名盖在上面）。两者都必须真实、当代、有可验证的
   品味特征。凭空编的"气质"直接判负。
3. **先出 token。** 写任何组件之前，先写一份机器可读的三层设计 token 文件
   （primitive → semantic → component；W3C token 格式，`$value` + `$type`）。预先
   定死：感知均匀的色阶（Oklch——一个"等步长看起来就等距"的色彩空间）、非默认字体上
   的真实字号阶梯、一个间距增量（4px 基准 → 4/8/12/16/24/32/48/64）、圆角阶梯、
   层高阶梯、命名的动效 token（进入 / 滚动 / 状态切换各配时长 + 缓动；尊重
   `prefers-reduced-motion`）。深色和浅色是一等公民，且都从同一套 semantic token 解析。
4. **点名封禁默认套路。** 禁令比形容词管用：不用条件反射式的默认字体（Inter/Roboto）、
   不用紫色渐变、不用居中 hero、不用三等宽卡片排、不用灰字白底一大块。每个项目再加
   自己的封禁清单。
5. **戴着镣铐构建。** 组件只消费 token。组件内部硬编码的裸 hex、px、字体族就是缺陷。
6. **闭合截图 → 视觉评审循环。** 凡是渲染出来的东西：在无头浏览器里按移动端和桌面端
   宽度渲染、截图、让视觉模型打分——然后分轮修（批评 → 结构修复 → 审计 → 打磨），
   绝不一把梭。评审者是裁判：用与构建者不同家族的模型、按命名的轴打分、绝不打一个
   整体分。评审模型在调用时从配置解析——写死的模型 id 总有一天退役，会把整个循环
   一起带走。
7. **打 8 轴品味评分。** 每轴 0–3 分，且每一轴都必须 ≥ 2：token 遵循度 · 布局/层级 ·
   排印 · 色彩/对比 · 动效 · 深浅一致性 · 无障碍 · "像被设计过吗"直觉检查（"这看着
   是设计出来的，还是万物的平均值？"）。任何一轴低于 2 = 没完成。
8. **执行无障碍硬门（WCAG 2.2）。** 指针目标 ≥ 24×24 CSS px。可见焦点指示 ≥ 2px
   边缘、对比 ≥ 3:1。文本对比正文 ≥ 4.5:1、大字与 UI 组件 ≥ 3:1。键盘全程可达。
   两套主题下都验对比。这是门，不是建议：不过 = 不发。
9. **测像素背后的代码。** token 解析器、主题切换、对比度计算器、状态 reducer 都要在
   真实渲染的 DOM 上跑真实测试——对比检查里一个写反的比较，就会发出一张漂亮却悄悄
   无障碍失效的界面。测试审代码；评分表和 WCAG 门审品味。

## 硬规则——踩中任何一条即失败

- token 文件还不存在就写了组件。
- 组件内出现裸 hex / px / 字体族。
- 封禁清单上的任何一项出现在产出里。
- 渲染物跳过截图 → 评审循环。
- 构建者评自己的视觉产出，或用一个整体分替代分轴打分。
- 出厂时任何评分轴低于 2，或任何 WCAG 2.2 检查不过。
- 一个无法落到真实、可验证参照上的品味方向。

## 搭配使用

- [intent-compiler](../intent-compiler/SKILL.md)——完整的读题纪律。
- [blind-eval](../blind-eval/SKILL.md)——问题是品味时的保留或回滚。
- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)——加固像素背后的代码。
- [blind-tribunal](../blind-tribunal/SKILL.md)——合入前的跨家族评审。

> Scaffold credit: W3C Design Tokens Community Group (token format); WCAG 2.2, W3C
> (accessibility gate); UICrit, UIST 2024 (axis-scored UI critique); AI Jason, &
> JackJack. (2025). superdesign: AI design agent [Computer software]. GitHub.
> https://github.com/superdesigndev/superdesign (AGPL-3.0; dual-licensed with a
> commercial enterprise license) — forbid-the-defaults. The composition and hard
> rules here are BACKS AIOS.
