---
name: "sniper-testing"
description: "任何修复或构建循环期间用它，以及在相信任何一个绿色测试之前。只跑覆盖你所改动内容的测试，并干掉 mock 剧场——那种能力已经坏了、测试还在通过的戏。Trigger words: sniper testing, scoped tests, test scope, mock theater, fake green, full suite, test bloat. 中文触发词：狙击测试、只跑相关测试、测试范围、mock 剧场、假绿、全量测试、测试膨胀。"
license: "MIT"
---

# Sniper Testing
**Effort:** free — 纯纪律，不额外跑任何东西；它删掉迭代期间的全量套件重跑，净成本直接下降。消除：测试膨胀（为一点小 diff 跑整套测试），以及你原本会在其上盖楼的 mock 剧场假绿。

## 为什么有这个技能

两种失败模式烧掉了大部分测试时间。测试膨胀：为一点小改动跑整个套件。mock 剧场：真实能力已经物理性坏掉，测试却在通过。这个技能把两个都干掉。

## 规则 1 — diff 划定范围，不是乐观情绪

在修复 / 构建的迭代循环里，禁止跑完整测试套件。

1. 跑 `git diff --name-only HEAD`，看清你到底碰了哪些文件。
2. 把每个碰过的文件映射到直接覆盖它的测试文件
   （例如 `src/payments/refund.py` → `tests/test_refund.py`）。
3. 先说出你的具体测试目标，然后只跑那些文件
   （Python：`pytest tests/test_refund.py`；
   JS：`npx vitest run tests/refund.test.js`；
   Go：`go test ./payments/ -run TestRefund`）。
4. 已经通过的测试不重跑，除非你的下一个改动碰到了它覆盖的代码。范围由 diff 划定——不由乐观划定，也不由恐惧划定。
5. 落地时——commit 关卡——对每个被碰模块的套件跑一次完整通过。这唯一的一趟恰好把间接耦合抓一次。迭代速度和一次扎实的落地，都是工作的一部分。

## 规则 2 — 干掉 mock 剧场

能力测试必须断言一个真实的、物理的副作用：

- "生成了视频" → 磁盘上真的有一个文件，大小 > 0 字节。
- "存了记忆" → 那一行能从真实的本地数据库里读回来。
- "渲染了组件" → 页面上真的存在一个 DOM 元素。

不许 mock 数据库。不许 mock 文件系统。不许 mock 本地网络套接字。

唯一合法的 mock 是付费的外部传输叶子——打向计费第三方 API 的那次 HTTP 调用。即便如此，测试也必须穿过它周围所有的真实逻辑：构造请求、路由、解析响应。mock 电线，绝不 mock 大脑。

## 先审计，再信任

依赖任何测试之前，先读它。如果它是 mock 剧场——靠 mock 变绿、没有任何物理断言——就删掉 mock，把测试重写成断言真实副作用。一条不可能失败的测试比没有测试更糟：它给谎言盖章，而你会在谎言上盖楼。

## 硬性规则（破一条，技能即失败）

- 迭代期间不许跑全量套件。
- 没有真实副作用断言，不许宣称绿了。
- 能力测试里，付费外部传输叶子之外不许有任何 mock。
- 没对被碰模块跑那唯一一次完整通过，不许落地。

## 搭配使用

- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — 狙击范围喂给它的第一道关卡
- [red-first](../red-first/SKILL.md) — 修复之前先写那条失败测试
- [seam-engineering](../seam-engineering/SKILL.md) — 修掉一类，再用限定范围的测试扫尾
