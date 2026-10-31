---
name: "clean-code-gauntlet"
description: "在加固或落地可执行改动时，需要度量复杂度、覆盖率、回归检测强度和独立设计评审时使用。"
license: "MIT"
---

# Clean Code Gauntlet——整洁代码闯关
**Effort:** heavy — 真实算力：覆盖率和复杂度运行，加一轮有界变异测试，最后一个品味模型；把它花在要出厂的改动上。消除：对整个 diff 逐行的人工 review，以及回归藏身其后的假绿测试。

## 为什么有这个

乱代码让 agent 反复空转，而埋在长 prompt 里的规则会在上下文中途褪色——确定性检查永不褪色。所以把 Clean Code 当成**代码必须闯过的关卡**来跑，而不是模型必须记住的散文。

**度量，不 review。** 用工具算出来的数字把关：覆盖率、圈复杂度（一个函数里独立路径的数量）、模块大小、变异击杀数。人和模型只抽查样本——绝不通读整个 diff。

## 关卡链（按顺序跑；每关失败都大声停下）

绑定现有 [Build Flow](../backs-build-flow/SKILL.md) 任务包的 `base_sha`、
`candidate_sha`、集成负责人和 [bounded-loops](../bounded-loops/SKILL.md) 剩余
任务额度。复用仍有效的证据；评审轮次和变异批次不重置预算。

1. **限定范围的 lint、类型和行为检查全绿。** 执行适用的仓库命令，参见
   [sniper-testing](../sniper-testing/SKILL.md)。明确记录不可用或不适用检查，
   不标为通过。基线为红则先修复，不在红色基线上变异或评分。
2. **CRAP 低于阈值**，基于真实覆盖率数据（见下面的关卡）。超标 → 要么把函数重构
   下来，要么覆盖到位。绝不降线。
3. **变异测试：范围内没有未解释的幸存者。** 非等价幸存者是回归缺口。
   另加补充测试文件，逐字节保留 [red-first](../red-first/SKILL.md) 的原始封存
   契约。等价变异的反驳须有证据。工具错误或超时属于无法定论，不算击杀。
4. **轻量品味评审**——模型只评数字管不了的部分。

## 算这些数的工具

| 技术栈 | 工具 |
| --- | --- |
| Python | coverage.py + radon + mutmut |
| JS/TS | c8（或 istanbul）+ Stryker |
| Go | go test -cover + gocyclo + go-mutesting |
| Rust | cargo-tarpaulin + cargo-mutants |
| Java | JaCoCo + PIT |
| 其他 | 任意覆盖率 % + 任意圈复杂度计数器 |

每关一条命令的形状：
- 覆盖率：`coverage run -m pytest <sniper files> && coverage report`（JS/TS：`npx c8 vitest run <files>`）
- 复杂度：`radon cc -s <changed files>`
- 变异：`mutmut run --paths-to-mutate <changed files>`（JS/TS：`npx stryker run --mutate "<glob>"`）

这些仅为示例，不是安装指令或稳定 CLI 保证。使用仓库固定的工具和支持的参数。
仅文档改动应验证链接、结构、分发和行为场景；代码复杂度或变异测试可能不适用。
记录原因，不编造指标。

## CRAP 关卡

```
CRAP(m) = comp(m)^2 * (1 - cov(m)/100)^3 + comp(m)
```

- 覆盖率 100% 时，分数塌缩为复杂度本身。
- 30 是经典的"烂代码"线（复杂度 5、零覆盖就会撞上）。
- 人类每个函数大约扛 4–5 的复杂度。agent 只有在接近 100% 覆盖时才可以带 6–8
  ——那份宽限是用覆盖率买单的。
- 高 CRAP 函数只有两个出口：重构下来，或覆盖到位。**绝不降阈值换通过。**

## 债是谁的——AUTHORED / WORSENED / UNCHANGED

一个绝对分数掩盖了债是谁欠的。使用可比较的实际覆盖率，对照固定的任务前 `base_sha` 拆分每笔复杂度和 CRAP 变化量：

- **AUTHORED（新写的）**——本次改动创建的函数。完整标准照单全收。
- **WORSENED（改差的）**——本次改动弄差的既有函数。差额记在本次改动头上；必须回到
  基线或更好。
- **UNCHANGED（没碰的）**——本次改动从未触碰的既有债务。报告它、立案它，绝不记到
  本次改动头上——也绝不拿它当借口跳过闯关。

## 变异规则（有界，绝不蛮干）

- **绝不动共享工作树。** 在确切已提交 `candidate_sha` 的临时检出里变异。
  目标或测试文件有未提交改动时先建立检查点并完成候选版本，保留原工作区的无关工作。
- **成本靠测量，绝不靠假设。** 先把范围内的测试套件计时一次，在花任何钱之前报出
  预计耗时 = 基线 x 变异体数量。提供一次干跑（dry run）选项。
- **有界且可续跑。** 在剩余任务额度内限制变异体数量和分钟数。预算停止时记录
  未验证变异体，关卡仍未完成。仅在还有额度或获明确扩展后才能续跑。
- **覆盖优先。** 只变异有覆盖的行；没覆盖的行是覆盖缺口，CRAP 关卡已经抓住了。
- **只在范围内。** 只变异 diff 碰过的地方，绝不动整个仓库。
- 真正等价的变异体可以驳回而不必击杀——但驳回理由要写下来，绝不无声跳过。
- **技术栈没有变异测试工具？** 记录限制和实际替代证据。遵循仓库验收政策；
  必需关卡在负责人接受有记录的替代方案前仍未完成。

## 品味评审（最后，且轻）

确定性关卡先行；只有推理是唯一工具的地方才动用模型。评审者是非构建者出身的评分者，按能力与可用性从配置好的梯级矩阵里在线挑出；构建候选的作者执行被取消资格，任何继承了构建者对话或上下文的会话同样被取消资格；评审必须在全新且与作者无关的会话中进行——构建者永远不评自己的活。它只评设计和品味：命名、职责混杂、接口宽度，以及六种坏味道——僵化、脆弱、难移动、多余的复杂、多余的重复、晦涩。算术早已由前面的关卡定案。

评审守住的手艺底线：函数小、只做一件事、参数少、没有 flag 参数、名字诚实；深模块——小接口藏住真逻辑；测试快、独立、可重复、每条只断言一个行为。

## 硬规则（破一条即失败）

- 绝不降阈值、绝不削弱变异集合来强行通过。
- 绝不变异共享工作树；绝不无界地跑。
- 绝不把 UNCHANGED 的债记到本次改动头上。
- 不可能失败的测试是演戏——变异测试正是证明哪些测试是真的的方法。
- 说真实成本——机器时间便宜，回归不便宜。绝不为省一小时装绿。

## 搭配使用

- [sniper-testing](../sniper-testing/SKILL.md)——为第 1 关挑测试范围
- [red-first](../red-first/SKILL.md)——任何构建之前的失败契约
- [blind-eval](../blind-eval/SKILL.md)——问题是品味时的保留或回滚
- [blind-tribunal](../blind-tribunal/SKILL.md)——合入前更完整的评审裁决

> Scaffold credit: Robert C. Martin, *Clean Code* (2008); Alberto Savoia &
> Bob Evans, the CRAP metric (2007); John Ousterhout, deep modules
> (*A Philosophy of Software Design*, 2018); Pocock, M., & Martin, R. C.
> (2026, Aug 19). LIVE: Uncle Bob on Software Fundamentals in the Age of AI
> [Video]. YouTube. https://www.youtube.com/watch?v=zcLPGC-tvgk — source of
> the agent CRAP band and coverage-first mutation. The composition and hard
> rules here are BACKS AIOS.
