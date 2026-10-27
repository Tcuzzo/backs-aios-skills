---
name: "fleet-dispatch"
description: "当包内同伴发送 \"invoke skill fleet-dispatch\"，或本智能体需要为自己的工作调度自己的舰队梯级时使用。调用本地舰队解析器，读取 FLEET_RECEIPT，并连同来源证明一起返回答案。与模型无关：顺序由梯子决定。 Trigger words: fleet-dispatch, fleet rung, dispatch, role agent, role bot, invoke skill, fleet ladder. 中文触发词：舰队调度、舰队梯级、调用技能."
license: "MIT"
---

# 舰队调度

读取并执行完整的规范说明。解析角色与规格，调用本地舰队解析器，并把答案与 FLEET_RECEIPT 一起返回。绝不硬编码模型名称，绝不绕过解析器；一切严格遵循英文原文。

[Canonical skill](../../../../skills/fleet-dispatch/SKILL.md)
