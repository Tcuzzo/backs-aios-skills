# Agent Builds

如何构建一个能自主行动的 agent 或服务。核心思想：确定性的原语（primitive，
即不靠模型、结果可预测的基础函数）承担重活；模型只在"非推理不可"的地方推理。
全靠 LLM、零原语的设计，是无效设计。

## 什么时候用

构建任何 agent、bot、worker 或长期运行的服务——凡是握着工具、访问网络、
或在无人盯着每一步的情况下自己采取行动的东西。

## 链路

1. [intent-compiler](../skills/intent-compiler/SKILL.md) —— 把需求完整读懂；
   任务和它的边界来自这个人自己说的话。
2. [understanding-gates](../skills/understanding-gates/SKILL.md) —— 在设计阶段，
   先点名领域原语（DOMAIN PRIMITIVES）：每个核心能力都是确定性、离线、
   fail-closed（出错即拒绝）的函数。LLM 的位置只留给真正的推理。
3. [red-first](../skills/red-first/SKILL.md) —— 动手构建之前，先为每个带类型
   契约的 IO 边界提交会失败的契约测试。
4. 按下面的守则构建。每个循环都套上
   [bounded-loops](../skills/bounded-loops/SKILL.md)：预算、检查点、
   退避（backoff）、响亮的急停开关——绝不做狂轰滥炸式的重试。
5. [sniper-testing](../skills/sniper-testing/SKILL.md) —— 只允许 mock 出站
   传输层——路由、prompt 组装、解析逻辑一律不许 mock。
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) —— agent 的
   工具处理器和决策函数要跑完整个关卡：风险分低于你的上限，然后对决策路径
   跑变异测试，直到零幸存。翻转一个比较符还能活下来的分支逻辑，
   等于从来没被测过。
7. [blind-tribunal](../skills/blind-tribunal/SKILL.md) —— 上线前由跨模型家族
   的评审放行。构建者绝不给自己的活打分。

## 守则（构建必须满足的条件）

- 每个 IO 边界都声明类型契约（输入 → 输出），并且 FAIL CLOSED——输入不对
  就抛错或拒绝。绝不 fail-open（出错却放行），绝不吞掉错误。
- 每条网络接缝都可"录像带"式测试：把出站调用包在录制/回放层后面，
  让测试套件离线跑在固定样本（fixtures）上。
- 所有出站流量都要过一份默认拒绝的主机名白名单。未知主机直接抛错，
  绝不悄悄连上去。
- 把 agent 建模为带类型的事件流/状态机，带有确定性的签核状态
  （draft → review → ready → done），由 agent 自己算出来——这是原语，
  不是给人添堵。任何动作都不许跳过它的状态。
- 只有真正破坏性或不可逆的动作（花钱、删除、无法撤回的对外发送）才需要
  在执行前对照已提交的状态做确认。绝不拦无害或只读的动作，也绝不拦人——
  见 [decision-bar](../skills/decision-bar/SKILL.md)。
- 把持久状态（目标、决策、台账）写到上下文窗口之外的磁盘上，并重新读取。
  长跑任务绝不信任上下文里的记忆。
- 附带一份 agent 每次任务前都会加载的操作文档——就近文件优先、限制大小——
  承载那些永远必须遵守的规则。
- 工具失败要向推理槽返回结构化错误，供它自我纠正。被吞掉的工具错误
  就是 bug。
- 最小权限：agent 只带任务需要的那几个工具——没有随手可用的文件系统
  或网络权限。

## 硬门槛

- 零原语 = 无效设计；回到第 2 步。
- 任何 fail-open 的边界、静默回退或被吞掉的错误，都拦下交付。
- 决策路径上有变异体幸存，拦下交付。
- 跨家族评审必须通过；构建者永远不当评审。

## 好搭档

- [root-cause-first](../skills/root-cause-first/SKILL.md) —— agent 行为异常时用
- [session-handoff](../skills/session-handoff/SKILL.md) —— 把持久状态做对
