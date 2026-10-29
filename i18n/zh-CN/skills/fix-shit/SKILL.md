---
name: fix-shit
description: Diagnose and close a reported failure end to end with a reproducer, root cause, class-level repair, consumer tests, and real-path proof. Use when the operator says fix shit, stop swallowing errors, or finish a stubborn bug.
license: MIT
---

# Fix Shit

Use this as the fast entry point into `root-cause-first` and `repair-loop`.
It is a repair skill, not a permission to hide a failing signal.

1. Name the user's broken behavior and the exact surface where it appears.
2. Build a repeatable red signal from the real path. Trace the input and each
   boundary to find where actual behavior diverges from expected behavior.
3. Identify the root cause and all callers of the broken seam. Preserve the
   original error in logs or the operator-facing state; a fallback may protect
   the app, but it must not turn failure into false success.
4. Make the smallest change that closes the failure class. Add a test that fails
   on the old behavior and covers the seam that failed.
5. Run focused tests, the affected consumers, and the actual app path. Verify
   both the desired result and the explicit failure state. Ask an author-disjoint
   reviewer to inspect the change when available.
6. Report PROVEN or STILL-BUILDING, with the evidence and any remaining red bar.

If the error is intermittent, capture timing and a bounded reproduction rate;
do not infer a cause from one green rerun. For code-location ambiguity, start
with `building-with-backs` and its target check.


## 证据与独立评审

调查已发布的可执行文件、软件包或请求的运行时行为时，在分析有用的情况下调用 [rea-investigation](../rea-investigation/SKILL.md) 和单独安装的 `reverse-engineer-anything` 技能；对受支持的原生目标使用现有 Ghidra 提供程序。静态证据不能证明实时行为；不得悄悄安装缺失的提供程序。采用开源能力时调用 [absorb](../absorb/SKILL.md)。通过 [fleet-ladder](../fleet-ladder/SKILL.md) 按角色和能力选择，不硬编码模型名称。需要评审团时遵循 [blind-tribunal](../blind-tribunal/SKILL.md)：与作者分离的新执行审查去除作者信息的冻结材料；模型家族不能证明会话隔离。缺少解析器、评审者或证据时报告运行时缺口。
