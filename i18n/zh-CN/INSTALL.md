# 安装 —— 把这个包拧到真实的 agent 上

> **v0.7 portable installer:** Claude Code、Codex、Cursor、OpenCode 和通用 agent 的当前一键注册方式：`./install.sh --target all --locale zh-CN`。脚本不会覆盖已有路径；PowerShell 用户运行 `./install.ps1`。完整的当前路径矩阵见[规范安装指南](../../INSTALL.md)。

这个包就是几个装满 markdown 的文件夹。每个技能是 `skills/<name>/SKILL.md`，
每套战术是 `plays/<name>.md`。没有二进制、没有服务器、没有构建步骤。
安装 = 把 markdown 放到你的 agent 找技能的地方。

frontmatter（文件头部的元数据块）刻意只用最小的 3 键子集——`name`、
`description`、`license`——遵循开放的 Agent Skills 规范（agentskills.io）。
该规范只要求 `name` 和 `description`，合规的运行时会忽略不认识的键。
所以凡是这套规范能加载的地方，这个包都能原生加载；其他任何地方，
它就是普通的 markdown。

## 1. Claude Code 插件（推荐）

在 Claude Code 里敲两条命令：

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

一次装齐所有东西：技能加载完毕，斜杠命令可用（输入 `/optimus` 启动地板），
接地 hook 默认开启——它会拦住所有会改动东西的工具，直到 harness 加载完成。
急停开关在你手里：在环境变量里设 `AIOS_GATE=off` 即可大大方方地关掉它。
市场仓库有更新时，走 `/plugin` 更新。

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
2. 挑匹配需求的战术——构建 → `plays/elite-build.md`，bug →
   `plays/bughunt.md`，评审 → `plays/grading-verification.md`——追加进去。
3. 拿用户的话去匹配各技能 `description` 里的触发词。绝不注入整个包——
   只注入匹配上的那一到三个技能。这个包很省 token；保持住。
4. 每次上下文重置都重新注入。掉出上下文的规则等于没加载。

## 第一个会话

插件安装：输入 `/optimus`，把任务交给它。手动安装：

    你：    读 ~/.claude/skills/optimus/SKILL.md 并启动。本会话遵循它。
    你：    任务——优惠券和礼品卡叠加时，结账总价算错了。
    Agent： [启动：加载 invariant-floor，选中 plays/bughunt.md，点名它要触发的技能]
    你：    开干。
    Agent： [战术驱动：复现、红测试、修掉整个类、线上验证、盲评、落地]
