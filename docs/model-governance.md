# Model Governance / Provider Routing / Capability Policy 方法

很多仓库在模型配置上，最开始都只有一个字段：

- `model: xxx`

但系统一旦长大，就会立刻遇到这些问题：

- 用户写的是 alias、family、版本前缀，还是完整 model id
- 同一个模型在不同 provider 下是否真的同样可用
- 组织 allowlist 应该按 family 控制，还是按精确版本控制
- 模型能力是硬编码常量，还是应该发现、缓存、刷新
- 某个模型快退役了、或有更高 context 版本了，系统应该怎么提示

如果这些边界不先治理，所谓“模型选择”最后只会退化成：

- 记几个字符串
- 堆几条 if/else
- 用户一旦切 provider 或模型升级，整套行为就开始漂

Claude code 真正值得迁移的，不是它当前支持哪些具体型号，而是这组原则：

> 模型不是一个字符串字段，而是带 identity、provider、allowlist、capability、deprecation 和 upgrade path 的治理对象。

## 1. 先把 model 看成“带语义的 selector”，不是纯字符串

源码里能看到，model selection 至少同时涉及：

- alias
- family alias
- version prefix
- exact model id
- provider-specific resolution

这意味着仓库不该只问：

> 现在 model 字段填了什么？

而应该先问：

1. 这是 alias、family、版本前缀还是 exact id？
2. 解析后会落到哪个 provider 的真实模型？
3. allowlist 对这一层 selector 的约束规则是什么？

一句话：

> model selection 真正选择的不是一个字符串，而是一类有解析规则的 identity。

## 2. 推荐的最小 model identity 模型

一个够用的 model identity 模型，至少应能表达：

- `provider`
- `selector_kind`
- `selector_value`
- `resolved_id`
- `capabilities`

可以这样理解：

- `provider`
  这次运行实际面向哪个 provider
- `selector_kind`
  这是 alias、family、version-prefix 还是 exact id
- `selector_value`
  用户或系统写下的原始选择
- `resolved_id`
  最终实际运行的 model id
- `capabilities`
  这个 resolved model 当前支持什么

如果你的系统现在还只有一个 `model` 字段，也没关系，但方法层至少要把这五层概念分开。

## 3. 选择优先级要明确，不要把所有来源混成一个值

Claude code 在 model 选择上体现出的一个核心思想是：

> 模型选择也有来源优先级。

推荐的默认高到低顺序：

1. 当前 session / 命令内 override
2. 启动参数
3. 环境变量
4. 持久 settings
5. built-in default

这条链的价值在于：

- 当前会话的显式选择能覆盖旧设置
- 启动时的临时指定不必改写长期配置
- 环境变量仍然比持久设置更像当前部署意图
- 最后才回到系统默认

一句话：

> 先定义 model selection precedence，再谈默认模型是什么。

## 4. provider routing 必须进入治理层

源码里最值得迁移的一点，是 provider 不是附件信息，而是 model policy 的组成部分。

至少要区分：

- first-party
- Bedrock
- Vertex
- Foundry
- 其它未来 provider

provider 会影响的东西包括：

- 默认模型
- 可用模型集合
- 某些模型的弃用日期
- 某些能力是否真实存在
- 某些 upgrade path 是否可用

如果系统以后支持多 provider，就不要再假设：

> 一个 model name 到处都成立。

一句话：

> provider routing 决定的不只是请求去哪发，还决定“哪些 model policy 成立”。

## 5. allowlist 不应只支持 exact match

Claude code 在 allowlist 里体现出一个很好的治理思路：

- family alias 可以是 wildcard
- version prefix 可以表达更细的约束
- exact id 可以表达最严格的允许集

而且还有一个关键细节：

> family wildcard 可以被更具体的版本规则收窄。

也就是说：

- 只有 `opus` 时，表示整个 family 都允许
- 同时有 `opus` 和 `opus-4-5` 时，不应仍把 `opus` 当无限 wildcard
- 具体版本约束应优先表达管理员的真实意图

一句话：

> allowlist 要能表达“允许一族”与“只允许其中某些版本”这两种不同治理意图。

## 6. capability policy 不要只靠硬编码

源码里还有一个非常值得迁移的点：

> 模型能力不是永远写死在代码里的，它应该有发现、缓存、刷新和 override 机制。

更稳妥的最小 capability policy 包含：

- capability discovery
- cache file
- refresh policy
- provider-aware override
- stale capability fallback

这样做的好处是：

- 当模型能力变化时，不必每次都等代码升级
- provider 滞后时，可以显式覆盖支持矩阵
- doctor / status 更容易解释“为什么这里不支持”

一句话：

> model capability 更像动态政策缓存，而不是永远不变的 enum。

## 7. capability cache 要按 eligibility 和变化成本设计

不是所有环境都应该无限制刷新 model capability。

Claude code 里体现出的关键判断包括：

- 是否符合当前 provider / user 类型资格
- 是否处于必须减少外部流量的模式
- 新拉下来的能力集是否真的有变化

这背后的方法是：

### eligibility

- 不是所有部署都该访问 capability discovery endpoint
- 不符合资格时应直接跳过

### cost control

- 某些环境需要限制附加外部流量
- 此时能力发现应该主动让位

### unchanged skip

- 如果缓存内容没有变化，就不值得重写磁盘或触发额外流程

一句话：

> capability refresh 不是“尽量多刷”，而是“只在值得的时候刷新”。

## 8. deprecation 应是 provider-aware 的正式信号

模型退役最怕两种情况：

- 系统完全不提示
- 系统只提示一个模糊的“过期了”，但不告诉用户哪天、对哪个 provider 生效

更稳妥的做法是：

- deprecation 信息与 provider 绑定
- 输出用户能理解的 retirement date
- 在 model 仍可用但接近退役时尽早提醒

一句话：

> deprecation 不是错误字符串，而是 provider-aware 生命周期信号。

## 9. override 和 upgrade check 要单独治理

源码里还能看到两个容易被忽略、但方法价值很高的点：

### support override

- 某些 3P provider 的能力支持会落后于 first-party
- 系统需要一层 override 来修正现实可用性

### upgrade check

- 当前 model 不是最大 context
- 用户确实有升级资格
- 系统可以给出明确 upgrade path

这说明：

> model governance 不只负责“选哪个”，也负责“什么时候该改选、更高版本是否可达”。

## 10. status / doctor 应至少能回答这几个问题

模型治理是否成熟，可以看系统能否稳定回答：

1. 当前 provider 是什么？
2. 当前 selector 是 alias、family、版本前缀还是 exact id？
3. 当前 resolved model 是什么？
4. allowlist 是放开的、收窄的，还是完全限制的？
5. 当前 capability 来自静态规则、动态发现还是 override？
6. 当前模型是否已弃用、即将退役，或存在明确 upgrade path？

一句话：

> model policy 不仅要选对，还要解释得出。

## 11. 推荐的最小检查清单

一个仓库准备补这层治理时，至少检查：

1. model identity 是否区分 alias / family / version-prefix / exact id？
2. model selection precedence 是否写清？
3. provider routing 是否进入默认值和 allowlist 判断？
4. allowlist 是否支持 family 与更具体版本规则同时存在？
5. capability 是否有 discovery、cache、refresh 与 override 机制？
6. deprecation 是否带 provider 语义和明确 retirement 提示？
7. upgrade path 是否在合适条件下被显式提示？

本仓库提供可直接改造的最小清单模板：

- `templates/project/model-governance-checklist.md`

## 12. 设计规则

- 不要把 model 当纯字符串字段
- 先定义 selector 语义，再定义具体默认值
- provider routing 必须进入 model policy 判断
- allowlist 不能只支持 exact match
- capability policy 要允许 discovery、cache、refresh 和 override
- deprecation 和 upgrade path 要明确、可解释、provider-aware
- `/status` 和 `doctor` 至少能解释当前 resolved model 和其来源

## 13. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/model-governance.md`
- `skills/model-governance/`
- `templates/project/model-governance-checklist.md`

这样以后再遇到“为什么这个 provider 下默认模型不同、为什么 allowlist 看起来开着但某个版本不能选、为什么模型能力突然不对、为什么现在该升级模型了”时，就可以按同一套 model governance 方法来处理，而不是继续靠散落逻辑兜着跑。
