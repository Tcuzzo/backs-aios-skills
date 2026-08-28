# BACKS AIOS Skills

**其他语言版本：** [English](../../README.md) · [Español](../es/README.md) · [Português (BR)](../pt-BR/README.md) · [Français](../fr/README.md) · [Deutsch](../de/README.md) · [हिन्दी](../hi/README.md)

> 本页是简体中文镜像，以英文原版为准：[English（canonical）](../../README.md)。

一套从真实运行中的 agent 平台提炼出来的 agent harness（约束和驱动 agent 的
执行框架），拆成 27 个可移植的技能和 8 套有名字的战术，重写成任何 agent
都能加载的纯 markdown。

## 使命

这个包是为那些原本会被高价挡在门外的人准备的——不是平台工程师的程序员、
设计师和创造者。harness 和这些技能就是平衡器：它们托住那些用不起最大模型
的人，让模型档次变得不那么重要。这就是这个包下的注：装在强 harness 里的
小模型，能赢过放养的大模型。你不需要懂 harness 是怎么造出来的——
说出触发词，纪律就会启动。

## 理念

三条信念贯穿这个包里的每一个文件。

**编程实现，而不是提示词祈求。** 这个包背后的 agent 说话直白、拒绝坏操作，
是因为这些性质被工程化进了 harness，成了结构性规则——hook、关卡、测试——
而不是写在 prompt 里的建议。一条要靠 agent 记住的规则，恰恰会在 agent
最忙的时候失效。所以真正要紧的规则，都在忘不掉的地方强制执行：
在 harness 里，不在模型的记忆里。

**机器不思考——机器蒸馏。** 不给模型任何真实材料，它就压缩空气——
产出一个自信的错误答案。给同一个模型正确的上下文，它就答对了。
我们所说的推理，其实是对上下文的蒸馏：模型把拿到的东西压缩成一个答案。
没有调研的推理就是幻觉。这就是技能存在的原因。技能是 agent 在思考某件事时
"带着思考"的上下文——它把 agent 从高层理解一路带到专业深度，
让蒸馏有真材实料可蒸。

**只在推理是唯一可行工具的地方推理。** 一切确定性的东西归 harness——
关卡、测试、hook、预算。模型的推理只花在配得上它成本的地方：判断、设计、
读懂意图。正是这种分工让这个包起到模型平衡器的作用：harness 干重活，
模型档次就不再决定结果。

## 快速上手

### 方式一 —— Claude Code 插件

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

然后输入 `/optimus` 启动地板。技能加载完毕，战术命令可用，
接地 hook 默认开启（急停开关：`AIOS_GATE=off`）。

### 方式二 —— 手动

把 `skills/` 下的文件夹丢进你 agent 的技能目录，然后说触发词。
各家 agent 的路径——Claude Code、任何 Agent Skills 运行时、OpenClaw、
Hermes、裸 API 循环——见 [INSTALL.md](INSTALL.md)。

| 你想要… | 就说… |
| --- | --- |
| 有东西坏了 | "repair loop"（或说"修复循环"） |
| 构建一个功能 | `/elite-build`（插件）或读 `plays/elite-build.md`（手动） |
| 这质量够上线吗？ | "clean code gauntlet"（或说"代码关卡"） |
| 盲审我的活 | "blind tribunal"（或说"盲评法庭"） |
| 我迷路了——下一步干嘛？ | "wayfinder"（或说"寻路"） |
| 需求是一段模糊的大白话 | "prose is the spec"（或说"话就是规格"） |

## 它怎么运作

- **技能（Skills）** 是单项纪律。每个技能的描述里有触发词，正文有编号
  步骤、会判负的硬规则，以及它搭配的技能链接。一个技能一个文件：
  `skills/<name>/SKILL.md`。
- **战术（Plays）** 是有名字的组合拳。一套战术按固定顺序触发多个技能，
  并列出拦下落地的硬门槛。一套战术一个文件：`plays/<name>.md`。每套战术的
  线框图里都标着一位 **Lord of the Loop**——驱动迭代直到落地门槛转绿的
  循环负责人；这个角色的定义见 [NAMING.md](NAMING.md#lord-of-the-loop)。
- **命令（Commands）** 是插件安装的斜杠入口——每条命令加载一套战术或
  一个技能并执行。每条命令在 `commands/` 里一个文件。
- **命名规范**——为什么技能是名词短语、命令是动词、地板是法律——
  见 [NAMING.md](NAMING.md)。
- **Effort 标记**——每个技能一行的成本承诺（free / light / heavy），加上
  每套战术结尾的 Weight 行，其读法在 [NAMING.md](NAMING.md#effort-标记) 里解读。

## 技能清单

| 技能 | 它做什么 |
| --- | --- |
| [absorb](skills/absorb/SKILL.md) | 吸收现有的开源能力，重新工程化为原生技能，而不是造一个重复轮子。 |
| [blind-eval](skills/blind-eval/SKILL.md) | 隐去作者信息，只凭改动本身的价值评判，然后留下或回滚。只有被证明的提升才落地。 |
| [blind-tribunal](skills/blind-tribunal/SKILL.md) | 来自不同模型家族的盲评陪审员给变更打分，一人一个视角。每条发现都变成一条失败测试。循环到全员放行。 |
| [bounded-loops](skills/bounded-loops/SKILL.md) | 每个循环都带预算上限、检查点和急停开关。让狂轰 API 在结构上不可能发生。 |
| [clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) | 一条确定性的质量线：狙击测试、CRAP 分数（复杂度 x 覆盖率）、有界变异测试，再加一轮轻量品味审查。 |
| [decision-bar](skills/decision-bar/SKILL.md) | 每个决定过同一条杠：只有品味、愿景或破坏性风险才到人面前。其余一律直接执行。 |
| [design-taste](skills/design-taste/SKILL.md) | 交付"看着像设计过、不像生成出来"的视觉作品：设计 token 先行、截图评审、无障碍硬门槛。 |
| [fleet-ladder](skills/fleet-ladder/SKILL.md) | 解析实时模型阶梯：探测谁活着，按顺序回退，阶梯耗尽就大声报错。 |
| [gpu-dispatch](skills/gpu-dispatch/SKILL.md) | 每张 GPU 只驻留一个模型，不溢出到系统内存，整个循环期间保持热身，循环结束才卸载。 |
| [guided-steps](skills/guided-steps/SKILL.md) | 把只有人能做的步骤——控制台、凭据、密钥——一步一步编成脚本，逐个捕获每个值。 |
| [human-calibration](skills/human-calibration/SKILL.md) | 建立这个人如何思考、如何决策、希望被怎样对话的画像，然后让整个构建顺着它走。 |
| [incident-closure](skills/incident-closure/SKILL.md) | "修好它"意味着完整收口——有证据的根因、失败测试、转绿、线上实证——绝不把选项菜单甩回给人。 |
| [intent-compiler](skills/intent-compiler/SKILL.md) | 把人的自然语言——方言、比喻、简称——当作完整规格来读，然后整体执行。每种方言都是合法语法；这个技能把文化当作有内在逻辑的上下文来读，绝不当作刻板印象。 |
| [invariant-floor](skills/invariant-floor/SKILL.md) | 每个自主变更落地前必须满足的编号法律。整个包站立的地板。 |
| [leap-protocol](skills/leap-protocol/SKILL.md) | 把大工程拆成可独立认领的球，铺给隔离 worktree 里的并行构建者，通过唯一的写入主脊收拢。 |
| [live-research](skills/live-research/SKILL.md) | 并行的调研 agent 去读活的源头——README、文档、真实代码——让推理扎根于真实存在的东西，不是记忆。 |
| [model-fusion](skills/model-fusion/SKILL.md) | 一组模型并行起草，独立裁判挑选，赢家再对照最初的意图验证。 |
| [optimus](skills/optimus/SKILL.md) | harness 没加载就不许写代码。一个确定性 hook 拦住所有会改动东西的工具，直到 agent 读完规则。 |
| [human-voice](skills/human-voice/SKILL.md) | 无学位门槛：如果读懂它需要一个学位，就重写。剥掉机器腔的同时保住完整的想法。 |
| [red-first](skills/red-first/SKILL.md) | 构建开始前先提交一条被证明会失败的测试。构建者不许碰它。评审核实它从没动过。 |
| [repair-loop](skills/repair-loop/SKILL.md) | 完整的修复循环：扎根地板、复现、红测试、修掉整个类、在真实路径上验证、独立评审、落地。 |
| [repo-map](skills/repo-map/SKILL.md) | 改代码前，先画清仓库的真实结构、入口、配置和运行路径。 |
| [root-cause-first](skills/root-cause-first/SKILL.md) | 没调查就没修复。按需复现、在边界埋探针、把数据一路往回追到源头。 |
| [seam-engineering](skills/seam-engineering/SKILL.md) | 在共享原语处一次修掉整个缺陷类，横扫所有同类，再落一个能抓住下一个惯犯的守卫。 |
| [session-handoff](skills/session-handoff/SKILL.md) | 把一个会话压缩成一个平面文件，让全新的 agent 能冷读并接着干。密钥已脱敏。 |
| [sniper-testing](skills/sniper-testing/SKILL.md) | 只跑覆盖你改动部分的测试。干掉 mock 剧场——能力已坏、测试却通过的戏。 |
| [understanding-gates](skills/understanding-gates/SKILL.md) | 给设计、计划、构建、测试、交付各设一道关，判定为通过/返工/否决，确保构建始终对得上需求。 |
| [wayfinder](skills/wayfinder/SKILL.md) | 迷路时画一张通往目的地的决策地图，而不是把问题甩给人。 |

## 战术清单

| 战术 | 它跑什么 |
| --- | --- |
| [elite-build](plays/elite-build.md) | 任何构建、修复或升级的主战术：读懂意图、给计划设关、先证明红、构建、精准测试、盲评、带线上实证落地。 |
| [agent-builds](plays/agent-builds.md) | 构建 agent 和服务：确定性原语干重活；模型只在"非推理不可"的地方推理。 |
| [web-app-builds](plays/web-app-builds.md) | 结构干净、供应链有防御的 web 应用和网站——依赖卫生就是战术本身，不是事后补课。 |
| [design-taste](plays/design-taste.md) | 看着像设计过、不像生成出来的 UI：品味定夺与实现分开、token 先行、给 agent 眼睛、无障碍把关。 |
| [grading-verification](plays/grading-verification.md) | 对抗式评审：绿色的结果是主张，不是证明。评审进攻，地板无法被糊弄。 |
| [parallel-work](plays/parallel-work.md) | 把工作铺给多个 agent 而不互相踩踏：一条写入主脊，多个读者。 |
| [security-delivery](plays/security-delivery.md) | 任何会被客户或另一台机器运行的东西的出厂关。安全靠构造，不靠记性。 |
| [bughunt](plays/bughunt.md) | 有边界的并行猎虫：画好地图、铺开猎手、对抗式核验每条发现、关死整条接缝。 |

## 最佳拍档

这些技能是 **BACKS AIOS** 的可移植层。BACKS AIOS 是
[Tcuzzo](https://github.com/Tcuzzo) 构建的 agent 平台——一个以图索引、
以关卡强制执行的系统，纪律握在 harness 手里，不在模型手里。完整系统——
它的记忆设计、模型行为画像、代码图谱——不在这个包里。但这些技能在任何
agent 上都能独立成立：Claude Code、OpenClaw、Hermes、Codex、Cursor，
或一个裸 API 循环。你的 agent 自主性越大，这块地板就越值回票价。

## 致谢

组合与转写：[Tcuzzo](https://github.com/Tcuzzo)。部分技能嫁接了已发表的
公开工作，带有脚手架致谢；这些致谢在文内标注，并汇总于
[NOTICE.md](../../NOTICE.md)。许可证：[MIT](../../LICENSE)。欢迎贡献——
请保持致谢完整。

> 说明：LICENSE、NOTICE.md、CITATION.cff 以及 `commands/`、`hooks/`
> 保持英文原文，不做翻译——它们是法律文本、事实性引用和可执行接线。
