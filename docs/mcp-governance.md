# MCP Governance / Connector Policy 方法

`MCP` 不是“再接一个外部工具”这么简单，而是一层需要单独治理的连接器系统。

如果这一层只有“会不会连上”的视角，仓库后面通常会出现四类问题：

- 同一个外部能力从多个来源重复接入，名字不同但实际指向同一连接
- 某些高风险连接器被当成普通工具面看待，没有单独门禁
- server 根本不支持某项能力，却仍然把相关入口暴露给模型
- 用户、项目、插件、平台策略彼此打架，最后没人说得清谁该生效

真正值得迁移的不是某个具体 `MCP` runtime，而是这一套判断：

> 连接器从哪里来，谁优先，谁能暴露，谁必须额外审查，冲突时如何决策。

## 1. 先把 MCP 当成“连接器治理”问题

在方法层，`MCP` 更接近 connector surface，而不是单一工具协议。

它至少同时涉及：

- 来源治理
- 去重治理
- 能力暴露治理
- 风险分级治理
- 连接状态治理

所以不要只问“支不支持 MCP”，要先问：

1. 这些 server 从哪里进来？
2. 哪些来源表达了更高意图？
3. 哪些 server 可以默认加载？
4. 哪些能力允许被模型看到？
5. 哪些连接器需要额外 allowlist 或人工确认？

## 2. 连接器来源必须分层

成熟系统里，`MCP` server 往往不会只来自一个地方。

常见来源至少包括：

- 平台 / enterprise / managed policy
- 用户或项目手写配置
- 插件动态注入的 server
- Web UI / connector 平台同步下来的远程连接器
- agent 或 task 运行时临时追加的 server

这几层如果不分层，只靠“最后 merge 的对象长什么样”，就无法解释优先级。

### 推荐的最小来源分层

1. `policy / managed`
   负责组织级底线与 allowlist / denylist。
2. `manual`
   代表用户或项目明确声明的连接器意图。
3. `dynamic plugin`
   代表能力包或插件自动带入的连接器。
4. `synced connector`
   代表网页端或外部系统同步下来的连接器。
5. `runtime additive`
   代表某个 agent / task 仅在当前运行中需要的附加连接器。

一句话：

> 先写清来源，再谈启用；不分来源，优先级永远会乱。

## 3. 优先级应该围绕“意图强度”定义

优先级不要按“谁最后加载”决定，更好的原则是按意图强度：

- `policy / managed` 决定底线
- `manual` 通常比插件和同步连接器优先
- `plugin` 自动补能力，但不应压过用户显式配置
- `synced connector` 不应覆盖用户已经手写的等价连接
- `runtime additive` 只能在当前运行范围内生效，不能静默改长期配置

其中最重要的一条是：

> 手写配置通常比自动注入更能代表真实意图。

## 4. 去重不能只看名字，必须看签名

连接器去重如果只按名称，很容易漏掉这类情况：

- 名字不同，但 command 完全相同
- 名字不同，但 URL 实际指向同一远程服务
- 一个是插件注入，一个是手写配置，本质却是同一 server

所以最小去重模型应该基于“连接签名”而不是展示名。

### 推荐的最小签名规则

- `stdio` server：按 `command + args` 生成签名
- `remote` server：按归一化后的 `url` 生成签名
- 名字仅用于展示和引用，不用于判断是不是同一连接

### 推荐的去重优先级

- 手写配置优先于插件注入
- 手写配置优先于同步连接器
- 同层插件冲突时，固定“先加载者赢”或其他稳定顺序
- 被显式禁用的手写配置，不应该继续抑制其他来源的等价连接

一句话：

> 名字负责可读性，签名负责真相。

## 5. 把 gate 拆开，不要用一个开关承载全部风险

连接器治理最容易退化的地方，是把所有判断都塞进“enabled / disabled”。

更稳妥的做法是把 gate 分成不同职责：

### Policy Gate

- 负责组织级允许 / 禁止边界
- 可以按名称、命令、URL 或来源判断
- `deny` 优先级应高于 `allow`

### Source Gate

- 负责判断某种来源在当前环境是否允许生效
- 例如只允许 managed server，或限制插件来源

### Risk / Allowlist Gate

- 负责高风险连接器的额外门禁
- 例如 channel 型 server、开发态 connector、未知 marketplace 来源

### Capability Gate

- 负责判断 server 宣称支持哪些能力
- 没有 `resources` 能力，就不该暴露资源读取入口
- 没有 prompts / skills / notifications 能力，就不该显示对应表面

### State Gate

- 负责判断连接当前是否真的可用
- 至少包括：enabled、connected、authenticated、healthy

不要把这几层混成一句“这个 server 开了没”。

## 6. 为什么 channel server 必须单独治理

不是所有 `MCP` server 风险都一样。

像 Telegram、Discord、iMessage 这种 channel server，和普通“查文档 / 查工单”的 connector 有一个本质差异：

- 它们不是单向取数
- 它们可能参与对话注入
- 它们可能参与审批回路
- 一旦被攻破，风险面不是单个工具调用，而是整条交互链

所以 channel server 不应只复用普通 `MCP` 启用流程，还应该额外具备：

- 单独 allowlist
- 明确 capability 声明
- 单独的 permission relay 开关
- 和普通 server 分开的告警与审计

一句话：

> channel server 的风险更像“远程交互面”，不是普通工具面。

## 7. 能力暴露必须按 capability 细分

成熟的 `MCP` 系统不应该默认认为每个 server 都同时拥有工具、资源、prompt、skill。

更合理的暴露原则是：

- `tools`
  只有连接成功并且 server 实际返回工具清单时才暴露
- `resources`
  只有声明支持 `resources` 时才暴露资源读取表面
- `prompts`
  只有 server 实际提供 prompt 类入口时才暴露
- `skills`
  只有你的运行时明确支持把某类 `MCP` 能力映射成 skill 时才暴露
- `notifications / permission relay`
  只有显式 capability 存在时才启用，不要靠隐式约定

这层规则的核心不是“功能更全”，而是：

> 只暴露 server 真正具备且当前允许暴露的能力。

## 8. 最小暴露矩阵建议

给项目写 `MCP` 规则时，至少要有一张最小矩阵：

| Surface | 暴露前提 | 常见风险 |
| --- | --- | --- |
| Tools | server 已连接且工具清单可用 | 误把失效 server 当可调用工具 |
| Resources | 显式声明 `resources` 能力 | 模型尝试读取根本不支持的资源 |
| Prompts | server 提供 prompt 表面 | UI 或运行时出现假入口 |
| Skills | 运行时支持该映射且 server 可用 | 把 prompt / skill 混在一起 |
| Channel relay | allowlist + 显式 capability + 风险开关 | 把高风险交互面当普通连接器 |

## 9. 推荐的最小检查清单

一个仓库引入新连接器前，至少检查：

1. 来源是什么？
2. 更高优先级来源是否已经提供了等价连接？
3. 连接签名是什么？
4. 它属于普通 server 还是高风险 channel server？
5. 它实际支持哪些 surface？
6. 被禁用、失联、未鉴权时，UI 和模型是否都能看到正确状态？
7. 冲突时，日志或诊断输出能不能解释为什么被抑制或被拦截？

本仓库提供可直接改造的清单模板：

- `templates/project/mcp-governance-checklist.md`

## 10. 设计规则

- 先定义来源分层，再写 merge 逻辑
- 去重按签名，不按名字
- 高风险 channel server 单独治理，不和普通 server 混用同一门禁
- capability 决定暴露面，不要暴露不存在的能力
- policy gate、allowlist gate、state gate 负责不同问题，不要混成一个总开关
- 手写配置表达更强意图时，应优先于自动注入
- 诊断输出必须能解释“为什么没加载 / 为什么被抑制 / 为什么没暴露”

## 11. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/mcp-governance.md`
- `skills/mcp-governance/`
- `templates/project/mcp-governance-checklist.md`

这样以后再遇到“要不要接这个 connector、谁该覆盖谁、为什么某个 server 不该暴露给模型”时，就不必重新靠聊天解释一遍。
