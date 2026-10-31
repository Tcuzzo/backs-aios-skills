<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/reflex-seam-dark.svg">
  <img alt="反射缝。左侧是确定性运行时，掌管状态、文件、规则和测试。右侧是模型判断内核，掌管推理、策略、可回滚性和优先级。两者之间是一道锯齿状的缝。决策信号从模型穿过缝走向运行时，状态更新再穿回来。未经许可的状态改动会被大声拒绝。" src="../../assets/reflex-seam-light.svg">
</picture>

# BACKS AIOS Skills

先看图？这里有[技能与循环视觉指南](../../docs/FLOWCHARTS.md)。

**其他语言版本：** [English](../../README.md) · [Español](../es/README.md) · [Português (BR)](../pt-BR/README.md) · [Français](../fr/README.md) · [Deutsch](../de/README.md) · [हिन्दी](../hi/README.md)

**模型负责判断。运行时掌管状态、文件和规则——如果模型去动它无权触碰的状态，系统会大声报错，
而不是自己去猜。**

这条线就是 **Reflex Seam**。智能体在下一步前读取实际规则和任务方法。
会话 hook 将 Optimus、Yoke 和 Build Flow 正文交付到宿主上下文；标记缺失时
触发加载，不阻断工具。加载失败给出可见诊断，工具仍可用。只有实际交付后才
记录回执。

两条规则一起过来。**不搞假测试：** 东西已经坏了测试却还是绿的，那就是撒谎，所以这里的测试断言
的是真实的副作用。**写代码的人不给自己打分：** 先写会失败的测试，再由没写这段代码的一方来判定
它是否通过。

> 本页是简体中文镜像，以英文原版为准：[English（canonical）](../../README.md)。

一套从实际智能体平台提炼的 harness：**62 个规范技能文件夹**，其中
**54 个非命令本地化技能**、**8 个命令包装技能文件夹**；另有 **8 套战术**和
**15 个命令适配器**。本简体中文镜像涵盖全部 54 个非命令技能和 8 套战术。
安装器将规范脚本、参考资料及命令包装与翻译正文合并。

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
  并列出拦下落地的硬门槛。一套战术一个文件：`plays/<name>.md`。工作由一位集成负责人在共享任务预算内推进；未过关卡阻止落地，额度耗尽时
  明确建立检查点。负责人的定义见 [NAMING.md](NAMING.md#lord-of-the-loop)。
- **命令（Commands）** 是插件安装的斜杠入口——每条命令加载一套战术或
  一个技能并执行。每条命令在 `command-adapters/` 里一个文件。
- **命名规范**——为什么技能是名词短语、命令是动词、地板是法律——
  见 [NAMING.md](NAMING.md)。
- **Effort 标记**——每个技能一行的成本承诺（free / light / heavy），加上
  每套战术结尾的 Weight 行，其读法在 [NAMING.md](NAMING.md#effort-标记) 里解读。

## 技能清单

| 技能 | 它做什么 |
| --- | --- |
| [absorb](skills/absorb/SKILL.md) | 吸收现有的开源能力，重新工程化为原生技能，而不是造一个重复轮子。 |
| [blind-eval](skills/blind-eval/SKILL.md) | 隐去作者信息，只凭改动本身的价值评判，然后留下或回滚。只有被证明的提升才落地。 |
| [blind-tribunal](skills/blind-tribunal/SKILL.md) | 全新且与作者隔离的陪审员评审去作者信息的冻结工作；发现进入独立 RED，并在同一剩余预算内修复复审。 |
| [bounded-loops](skills/bounded-loops/SKILL.md) | 同一任务的截止时间与剩余额度贯穿所有重试、工作者、模型和交接。 |
| [clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) | 一条确定性的质量线：狙击测试、CRAP 分数（复杂度 x 覆盖率）、有界变异测试，再加一轮轻量品味审查。 |
| [decision-bar](skills/decision-bar/SKILL.md) | 每个决定过同一条杠：只有品味、愿景或破坏性风险才到人面前。其余一律直接执行。 |
| [design-taste](skills/design-taste/SKILL.md) | 交付"看着像设计过、不像生成出来"的视觉作品：设计 token 先行、截图评审、无障碍硬门槛。 |
| [fleet-ladder](skills/fleet-ladder/SKILL.md) | 解析实时模型阶梯：探测谁活着，按顺序回退，阶梯耗尽就大声报错。 |
| [gpu-dispatch](skills/gpu-dispatch/SKILL.md) | 每张 GPU 只驻留一个模型，不溢出到系统内存，整个循环期间保持热身，循环结束才卸载。 |
| [guided-steps](skills/guided-steps/SKILL.md) | 把只有人能做的步骤——控制台、凭据、密钥——一步一步编成脚本，逐个捕获每个值。 |
| [human-calibration](skills/human-calibration/SKILL.md) | 应用有证据的当前操作者认知；当前纠正优先，不重复问卷。 |
| [incident-closure](skills/incident-closure/SKILL.md) | "修好它"意味着完整收口——有证据的根因、失败测试、转绿、线上实证——绝不把选项菜单甩回给人。 |
| [intent-compiler](skills/intent-compiler/SKILL.md) | 依据当前授权和项目证据，将压缩表达的请求转为可执行指令。 |
| [invariant-floor](skills/invariant-floor/SKILL.md) | 每个自主变更落地前必须满足的编号法律。整个包站立的地板。 |
| [leap-protocol](skills/leap-protocol/SKILL.md) | 把大工程拆成可独立认领的球，铺给隔离 worktree 里的并行构建者，通过唯一的写入主脊收拢。 |
| [live-research](skills/live-research/SKILL.md) | 并行的调研 agent 去读活的源头——README、文档、真实代码——让推理扎根于真实存在的东西，不是记忆。 |
| [model-fusion](skills/model-fusion/SKILL.md) | 一组模型并行起草，独立裁判挑选，赢家再对照最初的意图验证。 |
| [optimus](skills/optimus/SKILL.md) | 将实际 Optimus、Yoke 和 Build Flow 正文载入上下文；确定性 hook 不阻断工具。 |
| [human-voice](skills/human-voice/SKILL.md) | 无学位门槛：如果读懂它需要一个学位，就重写。剥掉机器腔的同时保住完整的想法。 |
| [red-first](skills/red-first/SKILL.md) | 构建开始前先提交一条被证明会失败的测试。构建者不许碰它。评审核实它从没动过。 |
| [repair-loop](skills/repair-loop/SKILL.md) | 在当前任务中执行有界 RED → 最小修复 → 限定 lint/类型/测试 → gauntlet → 独立评审及所请求交付。 |
| [repo-map](skills/repo-map/SKILL.md) | 改代码前，先画清仓库的真实结构、入口、配置和运行路径。 |
| [root-cause-first](skills/root-cause-first/SKILL.md) | 没调查就没修复。按需复现、在边界埋探针、把数据一路往回追到源头。 |
| [seam-engineering](skills/seam-engineering/SKILL.md) | 在共享原语处一次修掉整个缺陷类，横扫所有同类，再落一个能抓住下一个惯犯的守卫。 |
| [session-handoff](skills/session-handoff/SKILL.md) | 向下一会话传递同一任务包、基线/候选、RED 封条、证据、截止时间与剩余预算。 |
| [sniper-testing](skills/sniper-testing/SKILL.md) | 按固定基线到当前候选及自有待提交工作确定范围，运行真实 lint/类型/行为检查。 |
| [understanding-gates](skills/understanding-gates/SKILL.md) | 给设计、计划、构建、测试、交付各设一道关，判定为通过/返工/否决，确保构建始终对得上需求。 |
| [wayfinder](skills/wayfinder/SKILL.md) | 迷路时画一张通往目的地的决策地图，而不是把问题甩给人。 |
| [architecture-engineer](skills/architecture-engineer/SKILL.md) | 检查架构漂移、模块边界与依赖方向，将持久决定记录为 ADR。 |
| [backs-build-flow](skills/backs-build-flow/SKILL.md) | 由一个负责人协调上下文到交付，连接相关技能及有界 RED/GREEN、lint/类型/测试与 gauntlet。 |
| [backs-pack-sync](skills/backs-pack-sync/SKILL.md) | 比较私有运行时与公共包覆盖，仅加入另行编写并审阅的公共桥接。 |
| [backs-session-rollover](skills/backs-session-rollover/SKILL.md) | 在上下文压缩与新会话交接中保留原始任务、纠正和已验证工作。 |
| [building-with-backs](skills/building-with-backs/SKILL.md) | 验证确切工作副本与路径，将已授权改动推进到实际运行时。 |
| [cam-iot-inventory](skills/cam-iot-inventory/SKILL.md) | 在实时摄像头/IoT/Wi-Fi 盘点中保持稳定身份与真实证据，不把清单当作画面证明。 |
| [co-health](skills/co-health/SKILL.md) | 观察 harness 与 watchdog 证据，如实报告发现，保留工具和源码。 |
| [conscientious-objector](skills/conscientious-objector/SKILL.md) | 如实返回 harness 与 watchdog 观察，保留操作者与智能体工具。 |
| [context-compiler](skills/context-compiler/SKILL.md) | context-engineer 的兼容别名，使用相同的证据任务包。 |
| [context-engineer](skills/context-engineer/SKILL.md) | 补齐缺失执行上下文，用一个任务包保留已验证目标、下一步和验收检查。 |
| [context_engineer](skills/context_engineer/SKILL.md) | context-engineer 的下划线别名，指令逐字节一致。 |
| [debugging-engineer](skills/debugging-engineer/SKILL.md) | 以可证伪假设和决定性探针调查复杂回归、静默失败与竞态。 |
| [design-critique](skills/design-critique/SKILL.md) | 按真实用户任务、无障碍和视觉一致性评审产品界面，并验证具体修正。 |
| [fix-shit](skills/fix-shit/SKILL.md) | 在当前 Build Flow 中从证据推进到根因、封存 RED、整类修复和真实交付证明。 |
| [fleet-dispatch](skills/fleet-dispatch/SKILL.md) | 按配置的 fleet 角色派发，返回实际路径与来源回执。 |
| [harness-optimizer](skills/harness-optimizer/SKILL.md) | 通过有界基线/候选测量、保留样本与泄漏检查改进 harness。 |
| [karpathy](skills/karpathy/SKILL.md) | 在临时克隆中按用户定义的目标、指标、文件范围和预算做可测量实验。 |
| [operator-essence](skills/operator-essence/SKILL.md) | 一次洞察或后备评估形成含定性与定量证据的私有认知片段，当前请求优先。 |
| [operator-intent-deduction](skills/operator-intent-deduction/SKILL.md) | 从当前请求、已验证事实与有证据的操作者上下文解决未决选择。 |
| [operator_intent_deduction](skills/operator_intent_deduction/SKILL.md) | operator-intent-deduction 的逐字节一致兼容别名。 |
| [osha-bot](skills/osha-bot/SKILL.md) | 观察 harness 与 watchdog 证据，如实报告发现，不收回工具或源码。 |
| [rea-investigation](skills/rea-investigation/SKILL.md) | 用已安装 REA 获取已发布产物或运行时的发现/验证证据，返回调用方。 |
| [reload-vsc-and-verify](skills/reload-vsc-and-verify/SKILL.md) | 检查实际安装拓扑，修复所请求的技能接线并验证 VS Code 重载与发现。 |
| [scrub-plugin-pack-literals](skills/scrub-plugin-pack-literals/SKILL.md) | 通过 dry-run/apply/hook 模式清理公共包中的私有字面量泄漏，并保留结构守卫。 |
| [truth-audit](skills/truth-audit/SKILL.md) | 用只读实时探针核实运行代码、状态与损坏，产出可执行修复或交接规格。 |
| [turn-and-burn](skills/turn-and-burn/SKILL.md) | 整理任务的模型名单、经验与计划/设计评审要求，必要时吸收缺失能力。 |

## Build Flow 与操作者上下文

[backs-build-flow](skills/backs-build-flow/SKILL.md) 用同一任务包承载上下文、职责
和要求的完成状态。目标、约束、下一步和可观察验收检查明确后即开始执行；
专业技能返回负责人，不重启工作流。[operator-essence](skills/operator-essence/SKILL.md)
将当前偏好与定性、定量证据结合。文件缺失或过时，执行一次受支持的洞察流程，
或明确使用报告/历史后备评估；稀少证据标为暂定。它不能替代身份确认、权限或当前请求。

构建/修复执行有界 RED → 最小修复 → 限定 lint/类型/测试 → clean-code-gauntlet
和必需独立评审。原始 RED 保持封存，新缺口另加补充测试。基线到候选的范围、
截止时间和剩余预算贯穿工作者、评审与交接。只读评审不授权编辑；完成本地补丁
与已部署能力达到 **PROVEN** 是不同声明。

## 战术清单

| 战术 | 它跑什么 |
| --- | --- |
| [elite-build](plays/elite-build.md) | 明确选用的完整设计/构建/质量/评审战术；在同一任务与预算中保留所有适用关卡。 |
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

> 说明：LICENSE、NOTICE.md、CITATION.cff 以及 `command-adapters/`、`hooks/`
> 保持英文原文，不做翻译——它们是法律文本、事实性引用和可执行接线。
