# Web App Builds

如何构建结构干净、供应链有防御的 web 应用或网站。web 构建的多数伤害
是从依赖和边界进来的，不是从你自己的逻辑——所以卫生就是战术本身，
不是事后补课。

## 什么时候用

构建或扩展任何会被别人安装并运行的 web 应用、网站、API 或交付仓库。

## 链路

1. [intent-compiler](../skills/intent-compiler/SKILL.md) —— 选技术栈或结构
   之前，先把需求完整读懂。
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
6. [sniper-testing](../skills/sniper-testing/SKILL.md) —— 绝不 mock 你自己
   的校验或序列化：被 mock 掉的 web 边界，交付出去的是一个该拒收却
   照单全收的应用。
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) —— 路由
   处理器、数据加载器、表单/校验路径过关才许部署；对校验和鉴权谓词跑
   变异测试，直到无一幸存。翻转比较符、套件却照过的边界检查，
   就是公网表面上敞开的一扇门。
8. [blind-tribunal](../skills/blind-tribunal/SKILL.md) —— 部署前跨家族评审。

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
