# 命名 —— 这个包怎么起名，为什么这么起

这个包里的名字是承重墙。agent 靠把任务和名字、描述做匹配来挑技能，
所以一个词不达意的名字会把活派给错的纪律。下面的规范让路由保持诚实。

## 三类名字

- **技能是名词短语式的纪律。** 技能是 agent 加载来"带着思考"的上下文——
  一套规则，不是一个动作。所以它按纪律来命名：`red-first`、
  `seam-engineering`、`sniper-testing`。纪律是拿来加载的，
  不是拿来"跑"的。
- **命令是祈使句。** 命令是有始有终的动作，所以它的名字是动词，
  或它触发的战术/技能之名：boot、build、hunt、grade、tribunal。
- **不变量地板是法律。** `invariant-floor` 是所有其他技能都继承的那一个
  技能。它以它的本质命名——地板——因为包里每条硬规则都站在它上面，
  没有任何技能可以让低于它的变更落地。

## 随包发布的命令

| 命令 | 触发 |
| --- | --- |
| `/agent-build` | `plays/agent-builds.md` |
| `/bughunt` | `plays/bughunt.md` |
| `/design-taste` | `plays/design-taste.md` |
| `/elite-build` | `plays/elite-build.md` |
| `/grade` | `plays/grading-verification.md` |
| `/optimus` | `skills/optimus/SKILL.md` |
| `/parallel-work` | `plays/parallel-work.md` |
| `/secure-delivery` | `plays/security-delivery.md` |
| `/tribunal` | `skills/blind-tribunal/SKILL.md` |
| `/web-build` | `plays/web-app-builds.md` |

`design-taste` 同时作为技能、战术和命令存在，是有意为之——同一门纪律，
三种入口形态：技能是上下文，战术是配方，命令是扳机。不会产生歧义，
因为命令触发战术，战术链接技能。

## 每类信息住在哪

每一层回答不同的问题，没有任何重复：

- **名字说机制。** `blind-tribunal` 在你打开文件之前就告诉你它怎么运作：
  一组陪审员，对作者盲。
- **描述装触发词。** 运行时拿你的话去匹配描述，所以描述里装着一个人
  需要这个技能时会说出的每一种说法——包括旧名字（见下文）。
- **正文装规则。** 步骤、会判负的硬规则、搭配的技能。正文才是纪律；
  名字和描述只是它的门牌号。

## 改名永不断链

技能改名时，旧名字会搬进描述充当触发词，这样每个旧习惯、
每份用旧名字的文档依然能路由正确：

- **optimus** 直接保留本名——它是启动品牌，是包里唯一的专有名词，
  也是你第一个敲的命令（`/optimus`）。
- **"yoke"** 作为触发词活在 `human-calibration` 上——两个名字随便说哪个，
  加载的是同一门纪律。

弄断已有触发词的改名是回归（regression），不是整理。

## 逐技能命名理由

| 名字 | 为什么叫这个 |
| --- | --- |
| absorb | 把外部能力吸收进来、重新工程化为原生的纪律，而不是造重复轮子。 |
| blind-eval | 隐去作者信息的评估——"盲"就是机制本身。 |
| blind-tribunal | 一组对作者盲、来自不同模型家族的陪审员。Tribunal = 陪审团加判决。 |
| bounded-loops | 它强制执行的性质：每个循环都带边界——预算、检查点、急停开关。 |
| clean-code-gauntlet | gauntlet 是一连串硬核考验；clean code 是活着通过的东西。 |
| decision-bar | 每个决定在到人面前之前都要过的同一条杠。 |
| design-taste | 视觉工作里的品味纪律——被把关、被检验，不是凭感觉。 |
| fleet-ladder | 把模型舰队解析成一把回退阶梯，按顺序往上爬。 |
| gpu-dispatch | GPU 工作的调度法：一卡一模型，整个循环保持热身。 |
| guided-steps | 只有人能做的步骤，一步一步带着做。 |
| human-calibration | 把构建校准到它服务的那个人。（曾叫"yoke"——旧名作为触发词保留。） |
| incident-closure | 事故要完整关闭——从根因到线上实证——绝不分诊甩回给人。 |
| intent-compiler | 把自然语言编译成可执行指令。散文是源码；指令是产物。 |
| invariant-floor | 由编号法律构成的地板，每个变更都必须跨过。是法律，不是建议。 |
| leap-protocol | 把大工程跃迁到并行构建者、再从唯一主脊落地的协议。 |
| live-research | 对着活的源头调研——文档和代码的当下状态——不是模型记忆。 |
| model-fusion | 多个模型起草，一个独立裁判挑选——是产出的融合，不是投票。 |
| optimus | 启动品牌，作为专有名词保留。它启动地板；每个会话从这里开始。 |
| human-voice | 以它强制执行的东西命名：agent 用人说话的方式写字，而难的想法依然完整送达。 |
| red-first | 失败（红）测试先行，在构建开始前就提交。 |
| repair-loop | 完整的修复循环，以它的形状命名：扎根、复现、修复、验证、落地。 |
| root-cause-first | 规则就是操作顺序：先有根因，再有修复，永远如此。 |
| seam-engineering | 修复落在接缝——共享原语——上，绝不是散落的点状补丁。 |
| session-handoff | 以它的产物命名：一份冷启动会话也能接着干的交接文件。 |
| sniper-testing | 一枪一个目标：只跑覆盖你改动部分的测试。 |
| understanding-gates | 每个构建阶段上的关卡，检验的是理解，不只是语法。 |
| wayfinder | 迷路时找到路，而不是把问题甩给人。 |
