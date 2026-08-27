---
name: optimus
description: 任何 agent 会话、任务或循环开始时用它——写任何代码之前。harness 优先的启动：先加载不变量地板和这个任务需要的技能，让 agent 先读规则再干活；内含接地关卡 hook 模式，在 harness 加载之前拦下所有会改动东西的工具。Trigger words: optimus, harness-boot, harness first, load the harness, boot the floor, grounding gate, read the floor, no code without harness, session start, boot sequence. 中文触发词：先上 harness、加载 harness、启动地板、接地关卡、先读规则、没上 harness 不写代码、会话启动。
license: MIT
---

# Harness Boot
**Effort:** light — 每个会话一次启动流程，加载地板和本次任务的技能，外加一个运行零成本的确定性 hook。消除：不接地的编辑——规则还没读就动手的改动，以及读完规则后随之而来的那场重做。

一条规则：**harness 没加载，就没有代码、没有任务。**harness（约束和驱动 agent 的执行框架）= 本包的不变量地板，加上覆盖当前任务的那些技能。每个会话、每个运行时、每一次。为什么：一条要靠 agent"记得"的规则，恰恰会在 agent 最忙的时候失效——所以加载规则是第一个动作，而且用 hook 把它做成结构性的，而不是劝告性的。

## 什么时候跑

每个会话、任务、使命和循环的开头。上下文重置或交接之后再来一次。加载一次 harness 然后滑行一个星期，不叫加载 harness。

## 启动序列

1. **加载不变量地板。** 碰任何东西之前先读 [invariant-floor](../invariant-floor/SKILL.md)。整个会话都站在这块地板上。
2. **加载这个任务的地图。** 说得出哪些文件、哪些规则、哪些包内技能管辖这项具体工作。说不出来，你就还没准备好动手编辑。
3. **加载人类画像**（[human-calibration](../human-calibration/SKILL.md)），凡是任务触及某个人的品味、界面或工作流。
4. **实时调用任务需要的技能——就在本会话里。** 只被点名、没被调用的技能等于没发生。"凭对某技能的记忆"干活不算调用它。
5. 然后才可以：写代码、跑改动性命令、变更任何东西。

## 接地关卡模式

用一个确定性的**工具调用前 hook**——agent 运行时在每次工具调用前执行的小脚本——把第 4 步做成结构性的：

- 每个会话以**红灯（RED）**开始。
- 红灯期间，只读工具（read、grep、search、fetch）一律放行。agent 可以自由接地。
- 红灯期间，hook **拦截改动性工具**（edit、write、delete）和主要的改动性 shell 动词（commit、push、rm、install、服务重启、就地编辑）。
- 调用任何一个 harness 技能就把会话**翻成绿灯（GREEN）**（由工具调用后 hook 捕获）。之后 agent 才可以动手。
- **重新武装：**每次会话启动都重置回红灯。长会话按任务或按动作重新武装，让过期的绿灯永远带不进未接地的工作。

hook 本身的设计规则：

- **确定性且免费。** 不调模型、不走网络、无依赖。状态是每会话一个小文件，原子写入。
- **它逼的是接地，不是沙箱。** 只匹配主要的改动性动词；放过两用包装器和复制类工具，别让接地命令自己被困住。
- **失败即放行，但要大声。** hook 崩了绝不能砖掉会话——也绝不能无声放行。把错误打在人看得见的地方。
- **绝不困死一个会话。** 会话身份未知就放行，附一行大声警告。一个永远翻不成绿灯的会话，绝不能被红灯锁死。
- **一个由人掌握的总开关**（一个环境变量），默认开启，关闭时大声记录。关卡只约束 agent，从不约束人。绝不加第二道关卡。

通用 hook（伪代码，约 25 行）：

```python
HARNESS_SKILLS = {"optimus", "repair-loop", "invariant-floor"}  # your pack set
MUTATING_TOOLS = {"Edit", "Write", "Delete"}
MUTATING_SHELL = r"^\s*(sudo\s+)?(git (commit|push|reset|checkout)|rm|pip install|" \
                 r"npm install|systemctl (restart|stop)|sed .*-i)"

def handle(event, session_id, tool, args):
    if kill_switch_off():                    # human-owned env var, e.g. HARNESS_GATE=off
        return ALLOW                         # disabled loudly, never silently
    if not session_id:
        warn("no session id — allowing; the gate never traps a session")
        return ALLOW
    if event == "SessionStart":
        set_state(session_id, "RED")         # every session re-arms to RED
        return ALLOW
    if event == "PostToolUse":
        if tool == "Skill" and args.get("skill") in HARNESS_SKILLS:
            set_state(session_id, "GREEN")   # harness invoked -> agent may act
        return ALLOW
    if event == "PreToolUse":
        mutating = tool in MUTATING_TOOLS or (
            tool == "Bash" and matches(MUTATING_SHELL, args.get("command", "")))
        if not mutating or get_state(session_id) == "GREEN":
            return ALLOW                     # read-only always passes
        return BLOCK("RED: invoke a harness skill first, then act")
    return ALLOW
```

## 硬性规则（什么会让这个技能失败）

- harness 加载之前的任何改动。
- 报告里点名了某个技能，会话里却从没调用过它。
- 一个会拦只读工具、会把会话锁死在红灯、或者无声失败的 hook。
- 第二道关卡，或任何加在人身上的新摩擦。总开关永远归人。

## 搭配使用

- [invariant-floor](../invariant-floor/SKILL.md) — 启动最先加载的那块地板。
- [human-calibration](../human-calibration/SKILL.md) — 启动序列里的画像那一步。
- [repair-loop](../repair-loop/SKILL.md) — 启动之后，修复任务跑的东西。
- [bounded-loops](../bounded-loops/SKILL.md) — 启动开出的每个循环的预算。
- [wayfinder](../wayfinder/SKILL.md) — 启动时发现你不认路，就用它。
