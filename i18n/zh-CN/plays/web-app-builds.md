# Web App Builds

如何构建结构干净、供应链有防御的 web 应用或网站。web 构建的多数伤害
是从依赖和边界进来的，不是从你自己的逻辑——所以卫生就是战术本身，
不是事后补课。

## 什么时候用

构建或扩展任何会被别人安装并运行的 web 应用、网站、API 或交付仓库。

## 共享任务与限制

在当前 [BACKS Build Flow](../skills/backs-build-flow/SKILL.md) 任务包内应用本战术。
保留一位集成负责人、请求的 `task_mode`、固定 `base_sha`、当前 `candidate_sha`、
operator essence 和当前证据。复用适用的已载入技能正文；本战术增加领域关卡，
不重启任务。

[bounded-loops](../skills/bounded-loops/SKILL.md) 负责原始截止时间和剩余额度，
贯穿重试、工作者、模型、评审和交接。嵌套战术不得重置它们。耗尽时建立
**STILL-BUILDING** 检查点，保留候选版本、证据、未过关卡和下一步。
有用且已授权工作仅在剩余额度内继续；缺失关卡不能变成通过。

## 链路

1. 选技术栈或结构前，使用 Build Flow 已建立的意图和 operator essence，遵循完整
   请求和当前纠正。

2. [understanding-gates](../skills/understanding-gates/SKILL.md) —— 先设计
   结构：一个有文档的入口、一份显式的依赖清单、一个已提交的
   lockfile（锁定依赖精确版本的文件）。不许文件随手乱堆。
3. 依赖卫生（装任何东西之前先做）：
   - 每个引用到的包都对着注册表核验：它存在、比你的项目早、发布者有
     历史。AI 幻觉出来的包名是抢注诱饵——实测研究显示，约 43% 的幻觉
     包名会在完全相同的重复运行中反复出现（Spracklen et al. (2025),
     USENIX Security 25），所以攻击者可以提前注册它们。
   - 一切都从编译好的 lockfile 哈希锁定（例如 `pip install
     --require-hashes`、`npm ci --ignore-scripts`）；任何完整性不匹配
     都拒绝。
   - 默认禁掉安装期生命周期脚本。只有跑 postinstall 脚本才能用的包，
     是一面红旗。
   - 每个 CI workflow 依赖都锁到完整的 40 位 commit SHA，
     绝不用可变的版本标签。
   - 数量最小化：每个依赖都是一次经过审视的决定，不是条件反射。
     优先用标准库或平台原语。
4. [red-first](../skills/red-first/SKILL.md) —— 为路由、加载器和校验路径
   先写会失败的契约测试，再去构建它们。
5. 按下面的守则构建。任何 UI 表面都跑
   [design-taste](../skills/design-taste/SKILL.md) 方法——token 先行，
   无障碍是硬门槛。
6. [sniper-testing](../skills/sniper-testing/SKILL.md) — 根据固定汇总候选差异限定
   仓库真实 lint/类型/测试命令，报告缺口和有理由的 N/A。绝不模拟自己的验证或
   序列化；模拟 web 边界会交付接受本应拒绝内容的应用。

7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — 路由处理器、数据
   加载器和表单/验证路径部署前须通过。在共享预算内变异验证与鉴权谓词；有意义的
   幸存者阻止部署。缺失回归另加文件，保留封存的原始 RED。边界比较翻转后套件仍
   通过，就是公开界面上的敞开门。

8. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — 部署前独立陪审。每位评审
   按配置梯级矩阵的能力与可用性在线选择，记录并排除作者执行，使用全新且与作者
   隔离的会话。每个证实发现都在本任务内建立独立 RED 并有界修复。在剩余预算内
   复审，所有必需陪审员均须通过。保留完整受影响测试集落地关卡，并在真实应用
   界面验证已获授权的交付。

## 守则（构建必须满足的条件）

- 源码里没有密钥：凭据从环境变量或密钥仓库读。提交进来的 key，
  让构建失败。
- 输出处理按上下文来：SQL 用参数化查询，值进入 shell、数据库或 DOM
  之前用正确的编码。绝不字符串拼接不可信输入。
- 产出机器可读的 SBOM——软件物料清单（如 CycloneDX）——
  让接收方能审计完整的依赖树。
- 构建可复现：工具链版本锁定、安装过程确定、测试运行期间无外部网络
  访问（本地回环服务——数据库、fixtures——没问题，也是预期内的）。

## 硬门槛

- 未核验或未锁定的依赖，拦下安装。
- 提交进来的密钥，拦下构建。
- 校验或鉴权谓词里有变异体幸存，拦下部署。
- 测试期间的外部网络访问，拦下落地（回环没问题）。

## 好搭档

- [seam-engineering](../skills/seam-engineering/SKILL.md) —— 把边界缺陷当作一个类来修
- [bounded-loops](../skills/bounded-loops/SKILL.md) —— 懂限流的出站调用

**Weight:** 整场构建是 free 的卫生纪律；heavy 开销在对校验和鉴权谓词的变异测试加陪审团——每个公开界面上这笔账都划算，因为一个写反的比较就是一扇敞开的门。
