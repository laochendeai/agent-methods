# Trust Gate / Project Onboarding Governance 方法

很多仓库第一次进入时只有一句模糊提醒：

- 这是你信任的目录吗
- 小心这里可能有脚本
- 如果不放心先看看文件

这类提醒的问题是：

- 没有显式状态，系统不知道用户现在处于 onboarding 还是已经完成
- 没有风险盘点，用户看不到这个仓库到底声明了哪些高风险能力
- 没有记忆粒度，系统不知道应该按 session、目录还是项目持久化
- 没有和后续 permission flow 分层，结果第一次确认和每次工具授权混在一起

Claude code 值得迁移的，不是某句 trust 文案，而是这组原则：

> 第一次进入仓库时的 trust gate，应该是一个有状态、有风险披露、有记忆粒度、且和后续 permission flow 分层的固定治理流程。

## 1. 先拆清 onboarding 和 trust gate

这两件事不是一回事。

### onboarding

关注的是：

- 用户是否已经进入了一个真实项目上下文
- 工作区是否已经准备好最小协作骨架
- 例如是否已有仓库、是否已有 `CLAUDE.md`

### trust gate

关注的是：

- 这个目录是否值得信任
- 进入后会暴露哪些能力和风险
- 用户是否愿意接受这些风险再继续

一句话：

> onboarding 解决“是不是已经准备开始协作”，trust gate 解决“是不是可以信任这个目录并继续运行代理”。

## 2. onboarding 应该是显式状态机

源码里 onboarding 不是永远弹一次提示，而是：

- 定义明确步骤
- 每个步骤有 `isComplete`
- 每个步骤有 `isCompletable`
- 每个步骤有 `isEnabled`

这说明一个可迁移的方法：

1. 先把 onboarding 步骤建模成数据，而不是写死在 UI 文案里
2. 用当前目录真实状态决定哪些步骤启用
3. 只有启用且可完成的步骤全部完成，才算 onboarding 完成

这样的好处是：

- 空目录和已有仓库不会收到同一套提示
- 可以针对不同项目类型裁剪步骤
- 系统能清楚判断该显示什么，而不是反复弹统一弹窗

## 3. onboarding 触发必须有记忆和上限

源码里还有两个很重要的约束：

- 完成状态会缓存
- 展示次数有上限

这背后的治理方法是：

> onboarding 不是 nagging 机制，而是有限次数的引导机制。

推荐至少具备：

- `hasCompletedProjectOnboarding`
- `projectOnboardingSeenCount`
- `shouldShowProjectOnboarding()`

并明确：

- 完成后不再重复展示
- 展示超过上限后默认不再打扰
- demo / 非真实项目环境可以直接跳过

一句话：

> onboarding 的目标是帮助进入状态，不是永久占用入口。

## 4. trust gate 不能只问“你信任吗”，必须先盘点风险面

Claude 的 trust dialog 并不是只问一句 “Do you trust this folder?”。

它会先检查项目里是否声明了高风险能力，例如：

- MCP servers
- hooks
- bash allow 规则
- 来自 commands、skills、plugins 的 bash 执行能力
- `apiKeyHelper`
- AWS 认证辅助命令
- GCP 认证辅助命令
- `otelHeadersHelper`
- 非安全白名单内的环境变量

这说明：

> trust gate 的输入不是用户主观感觉，而是当前仓库声明出来的真实 capability surface。

如果一个仓库配置了这些能力，却仍然只展示泛化提示，用户实际上并不知道自己接受了什么。

## 5. 风险披露要按来源解释，而不是只给总量

源码在做风险盘点时，不只是判断“有没有”，还会追踪这些能力来自哪个配置源。

例如：

- `.claude/settings.json`
- `.claude/settings.local.json`

这背后的方法很重要：

> 风险提示不该只说“存在 bash 权限”，还应回答“它来自哪里”。

这会直接影响用户判断：

- 是项目规则的一部分
- 还是本地私有覆盖
- 是不是某个插件或技能引入的额外能力

推荐至少在 trust summary 里回答：

1. 哪类能力被声明了
2. 每类能力来自哪些配置源
3. 哪些能力意味着执行外部命令、访问凭据或接入外部服务

## 6. trust memory 必须按作用域保存

源码里 trust 接受结果不是统一写死成一个全局布尔值。

它明确区分：

- 当前目录如果是 home 目录，只在 session 里记住
- 当前目录如果是具体项目，则按项目配置持久化

这说明：

> trust memory 的粒度应和风险边界一致，而不是“一次接受，全局永久信任”。

推荐最小作用域至少分成：

- session scope：只适合临时、高层目录或非项目上下文
- project scope：针对具体仓库目录持久化

不要轻易做成：

- 全局永久信任所有目录
- 用一个用户级开关覆盖所有新项目

## 7. trust gate 需要明确 skip、reuse、retrigger 规则

一个可复用的方法至少要写清三类判断：

### skip

适合跳过的情况：

- 当前目录已明确接受 trust
- 当前会话已接受高层目录 trust
- 当前是 demo 或不应触发真实 onboarding 的环境

### reuse

适合复用已存在信任状态的情况：

- 同一项目目录再次进入
- 同一 session 内重复回到已接受的高层目录

### retrigger

源码直接体现了“按目录粒度重新判断”的思路。
在通用治理上，推荐把下面情况视作重新触发信号：

- 进入了新的项目目录
- capability surface 发生显著扩张
- 从只读项目变成声明 hooks、bash、MCP 或凭据辅助的项目

这里最后两条是治理上的推荐延伸：

> 一旦仓库新增高风险能力，旧 trust 决策不应被默认视作永远覆盖未来状态。

## 8. trust gate 不是后续 permission flow 的替代品

这层最容易被设计错。

首次接受 trust，并不意味着之后所有工具调用都自动放行。

源码里后续权限流仍然会继续：

- 记录是 hook 批准、user 批准还是 classifier 批准
- 记录是否是永久更新
- 持久化具体 permission updates
- 保留和 `toolUseContext`、`assistantMessage` 关联的审计信息

这说明：

> trust gate 只建立“可以进入这个仓库继续运行”的基本信任，不替代后续具体工具授权。

更合理的分层是：

- trust gate：仓库级初始信任确认
- permission flow：具体操作级授权、拒绝与持久化

## 9. trust gate 应该留下审计和分析信号

源码在 trust dialog 显示和接受时都会打点，并附带风险面信息。

这说明系统不只要问用户要不要继续，还要能回答：

- trust dialog 为什么被展示
- 当时有哪些高风险能力
- 用户是否接受
- 这是 home scope 还是 project scope

一句话：

> 没有审计信号的 trust gate，后续很难分析误授权和风险教育是否有效。

## 10. 推荐的最小 trust/onboarding contract

一个够用的最小模型可以长这样：

```yaml
trust_onboarding:
  onboarding:
    steps:
      - key: workspace
      - key: project_rules
    seen_limit: 4
    complete_flag: has_completed_project_onboarding
  trust_gate:
    disclose:
      - hooks
      - mcp_servers
      - bash_permissions
      - command_bash_execution
      - credential_helpers
      - cloud_auth_helpers
      - dangerous_env_vars
    memory_scope:
      home: session
      project: persisted
  permission_flow:
    keep_separate_from_trust_gate: true
    log_approval_source: true
    persist_granular_updates: true
```

重点不是字段长相，而是：

- onboarding 有显式步骤和完成条件
- trust gate 按 capability surface 披露风险
- trust memory 按作用域保存
- 后续 permission flow 保持独立

## 11. 推荐的最小检查清单

一个仓库准备补 trust/onboarding governance 时，至少先回答：

1. onboarding 和 trust gate 是否明确分成两层？
2. onboarding 步骤是否是显式状态，而不是硬编码提示？
3. trust gate 是否基于真实能力面盘点风险？
4. 风险提示是否能指出来源文件或来源层？
5. trust acceptance 是按 session、目录还是项目保存？
6. 哪些情况应该 skip、reuse、retrigger？
7. trust gate 和后续 permission flow 是否严格分层？
8. trust dialog 的展示和接受是否有审计信号？

本仓库提供可直接改造的清单模板：

- `templates/project/trust-onboarding-checklist.md`

## 12. 设计规则

- onboarding 和 trust gate 必须分层，不要合成一个模糊欢迎弹窗
- onboarding 必须有显式步骤、完成条件和展示上限
- trust gate 必须基于真实 capability surface 披露风险
- 风险提示应尽量指出来源，而不是只给抽象警告
- trust memory 必须按作用域保存，避免全局永久信任
- trust gate 不得替代后续具体 permission flow
- 权限批准来源和持久化更新应继续保留审计能力

## 13. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/trust-onboarding-governance.md`
- `skills/trust-onboarding-governance/`
- `templates/project/trust-onboarding-checklist.md`

这样以后再遇到“为什么第一次进入仓库时只弹一句话、为什么用户不知道项目里声明了哪些危险能力、为什么信任状态一旦接受就全局永久生效、为什么首次信任和后续工具授权搅在一起”时，就可以按同一套 trust/onboarding governance 方法处理。
