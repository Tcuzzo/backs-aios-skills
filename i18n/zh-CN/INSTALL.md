# 安装 —— 把这个包拧到真实的 agent 上

> **Portable installer:** Claude Code、Codex、Cursor、OpenCode 和通用 agent 的当前一键注册方式：`./install.sh --target all --locale zh-CN`。脚本不会覆盖已有路径；PowerShell 用户运行 `./install.ps1`。完整的当前路径矩阵见[规范安装指南](../../INSTALL.md)。

本包包含 62 个规范技能文件夹（54 个非命令本地化技能、8 个命令包装）、8 套战术
和 15 个命令适配器。技能正文是 `skills/<name>/SKILL.md`，战术是 `plays/<name>.md`。
安装器先复制规范文件夹内容，再覆盖本地化正文，保留参考资料和辅助脚本。
仅复制 `i18n/zh-CN/skills/` 可能遗漏辅助内容；翻译安装请使用上面的 `--locale zh-CN`。

技能 frontmatter 包含 `name`、`description` 和 `license`；部分原生技能还有绑定
元数据。开放 Agent Skills 规范（agentskills.io）要求 `name` 和 `description`。
请核对宿主当前加载器及规范安装指南；不要把所有原生元数据视为每个运行时都具备
的可执行绑定。

## 1. Claude Code 插件（推荐）

在 Claude Code 里敲两条命令：

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

安装会提供技能、斜杠命令和上下文加载 hook。`/optimus` 建立底线和 Build Flow。
Hook 将实际 **Optimus + Yoke + Build Flow** 正文交付给宿主上下文，不阻断工具。
会话启动或压缩时重载所需正文，不撤销已完成 grounding。匹配的改动工具发现标记
缺失时自动加载。正文缺失或不可读会给出可见诊断，工具仍可用，也不产生虚假回执。
上下文加载回执与实际 Skill 事件证据不同。`--rearm <session_id>` 请求再次加载，
不锁住会话。操作者仍拥有可逆停用开关 `AIOS_GATE=off`。通过 `/plugin` 更新。

不提供上下文 hook 的宿主可使用受支持加载器：

```bash
node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
```

Codex shell 将活动 `CODEX_SESSION_ID` 作为最后一个参数。也可用对应的 Python
加载器 `aios_gate.py`。未知技能返回非零，不编造加载证据。

## 2. Claude Code，手动安装

Claude Code 还会从两个文件夹发现技能（已对照官方文档确认，2026-08）：
个人级 `~/.claude/skills/<name>/SKILL.md`（你机器上的每个项目都能用）
和项目级 `.claude/skills/`（跟着单个仓库走）。

个人级，一行搞定：

    git clone https://github.com/Tcuzzo/backs-aios-skills.git ~/backs-aios-skills && ln -s ~/backs-aios-skills/skills/* ~/.claude/skills/

项目级：`cp -r ~/backs-aios-skills/skills/* .claude/skills/`

想跟着包一起更新就用软链接；想钉死版本（或你的运行时对软链接不友好）
就用复制。开一个新会话。当任务匹配到某个技能的 `description` 时，
技能就会触发——说出触发词，agent 就加载那个文件。手动路径下，
战术不是技能：把它们留在 clone 里，在会话开始时让 agent 读一份
（`read ~/backs-aios-skills/plays/elite-build.md`），或把你的默认战术
贴进项目的 CLAUDE.md。

## 3. 任何 Agent Skills 运行时（开放规范）

这套规范的采用远不止 Claude——OpenAI Codex、Gemini CLI、Cursor、
VS Code 等等（按规范生态，2026-08）。这里要紧的规则：文件必须叫
`SKILL.md`；目录名等于 frontmatter 里的 `name`；必填的只有 `name` +
`description`。这个包三条全满足。安装 = 把 `skills/*` 复制到你的运行时
放技能的地方（比如 Cursor 用 `.cursor/skills/`）。我们没有逐一验证
每个运行时的文件夹——确切路径请查你的平台文档。

## 4. OpenClaw、Hermes 及其他 agent 框架

已对照各自当前文档确认（2026-08）：

- **OpenClaw** 会发现其配置的技能根目录下的任何 `SKILL.md`。把 `skills/*`
  复制进你工作区的 `skills/` 文件夹，或全局共享的 `~/.openclaw/skills`
  文件夹。`openclaw skills` 命令行负责安装和更新。
- **Hermes（Nous Research）** 在 `~/.hermes/skills/` 里一个技能一个文件夹，
  任务激活时把该技能的 SKILL.md 加载进系统 prompt。把 `skills/*` 复制过去。

其他任何框架——通用套路，不用写代码：

1. 把每个 `SKILL.md` 挂载或贴入为工具可调用的上下文（文档工具、prompt
   库条目、检索库）。保持 `description` 那一行原样——它的触发词就是
   调用契约。
2. 加载一套战术（`plays/*.md`）作为会话的系统上下文。战术会按顺序点名
   它要触发的技能；agent 再按名字逐个拉取。
3. 在相信本文件之前，先到框架自己的文档里核实它当前的安装机制——
   机制变得很快；我们只陈述上面确认过的内容。

## 5. 裸 API 循环（无框架）

你自己就是 harness。每一轮循环：

1. 把 `skills/invariant-floor/SKILL.md` 放进系统 prompt，永远放。
   那是每个变更都必须跨过的地板。
2. 用 `skills/backs-build-flow/SKILL.md` 建立一位任务负责人、模式、目标、验收
   检查与共享预算。需要或明确要求时再加入对应战术；不是每个小改动都启动完整
   elite-build。
3. 拿用户的话去匹配各技能 `description` 里的触发词。绝不注入整个包——
   只注入匹配上的那一到三个技能。这个包很省 token；保持住。
4. 上下文重置后，重载下一步缺失的实际正文。保留当前任务包、RED 封条、基线/
   候选和剩余预算；新上下文不是新任务。

## 第一个会话

插件安装：输入 `/optimus`，把任务交给它。手动安装：

    你：    读 ~/.claude/skills/optimus/SKILL.md 并启动。本会话遵循它。
    你：    任务——优惠券和礼品卡叠加时，结账总价算错了。
    Agent： [载入实际底线和 Build Flow，验证目标，建立一个有界任务包]
    Agent： [复现、封存 RED、整类修复、限定 lint/类型/测试及 gauntlet，再完成已授权评审与交付]
