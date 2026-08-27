# 战术：Grading & Verification

对抗式评审战术。它只信一件事：绿色的结果是主张，不是证明。
评审要进攻，而地板的设计让它没法被糊弄。

## 什么时候用

- 任何已构建的变更申请落地——代码、配置、文档、某个 agent 的产出。
- 测试套件声称全绿，但没人看着它先失败过。
- 一个模型干了活，你需要对它的一个诚实判定。

整个评审，一图看懂：

```
+--------------------------------------------+
| 1 red-first  confirm the suite failed --   |<--------------------------+
|   non-zero exit -- BEFORE the fix existed  |  each finding -> a new    |
+--------------------------------------------+  red test -> fix ->       |
| 2 sniper-testing  scoped runs verified;    |  re-convene               |
|   no mock theater on the changed seam      |                           |
+--------------------------------------------+   +---------------------+ |
| 3 cross-family grade -- a model from a     |   |  LORD OF THE LOOP   |-+
|   DIFFERENT family than the builder        |   | one hand drives the |
+--------------------------------------------+   | loop: dispatch,     |
| 4 blind-tribunal  jurors judge an          |-->| judge, loop back    |
|   author-redacted envelope                 |   | until the gate is   |
+--------------------------------------------+   | green. a lane never |
| 5 clean-code-gauntlet  the grader re-runs  |   | lands its own work. |
|   it -- never trust the builder's numbers  |   +---------------------+
+--------------------------------------------+
          |
          | all jurors pass
          v
+--------------------------------------------+
| LANDING GATE -- the two-sided proof:       |
| fail-to-pass AND pass-to-pass, run         |
| hermetically . no fake-green tell .        |
| builder + grader families differ . the     |
| grader re-ran the checks itself            |
+--------------------------------------------+
```

图中两个特殊标签：Lord of the Loop = 循环之主，即由一只手驱动整个迭代（派发、评判、循环回炉）、直到落地门槛转绿的循环负责人；LANDING GATE（LAND，落地门槛）= 全部条件转绿才放行落地的最终关卡。

## 链路

1. [red-first](../skills/red-first/SKILL.md) —— 确认在修复存在之前，
   测试套件确实以非零退出码失败过。从没红过的套件，什么也证明不了。
2. [sniper-testing](../skills/sniper-testing/SKILL.md) —— 核实构建者迭代期间
   用的是限定范围的测试，并且没有在它改动的接缝上搞 mock 剧场
   （测试全靠 mock 演出来的通过）。
3. 跨家族评审——把活交给与构建者不同家族的模型。同家族评审会明显抬高
   胜率——评审偏袒自家亲戚；同家族的另一个实例也不够。
4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) —— 重大变更要开庭：
   陪审员评审一份抹去作者信息的卷宗。每条发现都变成一条新的红测试，
   法庭反复开庭，直到所有陪审员都放行。
5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) —— 评审亲自
   重跑关卡（覆盖率对复杂度、有界变异测试）。绝不相信构建者自己报的数字。

## 双向证明（两条都要，缺一不过）

- **Fail-to-pass：**原来红的测试现在绿了——修复得证。
- **Pass-to-pass：**原来绿的全都还绿——没有回归。
- 一次只新增通过测试的运行，两条都不满足。两条都在封闭环境里跑。

## 假绿探测（出现任何一条就是马脚）

- 退出码逃生舱——不管发生什么都干净退出的运行器。
- 硬编码或背下来的输出，顶替计算出来的输出。
- 被删除、被跳过或被削弱的测试。
- 任何被改过的评分器、计时器或打分器。改过的运行器变绿，
  这本身就是马脚。
- 绿色套件下还有幸存的变异体。变异体就是断言从没到过那个分支的证据——
  按定义就是假绿。

## 给裁判去偏

裁判机制的地板在 [blind-eval](../skills/blind-eval/SKILL.md) 的
"De-bias the judge" 一节——整节照做。

## 硬门槛——踩中任何一条，整场战术判负

- 构建者和评审同属一个模型家族。
- 无法展示修复前套件是红的。
- 被评审的运行里缺 fail-to-pass 或缺 pass-to-pass。
- 出现上面任何一条假绿马脚。
- 评审相信了构建者的自述，而不是亲自重跑检查。

**Weight:** 前段是 free 的红测和狙击检查；heavy 开销是陪审团加评审亲自重跑闯关——任何申请落地的改动上这笔账都划算，因为一次假绿的代价超过所有评审加起来。
