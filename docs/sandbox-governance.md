# Sandbox Governance / Restriction Profiles 方法

很多仓库把 sandbox 理解成一个开关：

- 开了就更安全
- 关了就更自由

但真正进入运行时落地后，问题会马上出现：

- 文件和网络限制不是一回事
- permission rule 和 sandbox config 不是同一种语义
- 某些路径在 rule 层和 sandbox 层的解释并不相同
- 托管策略可能要求“只有 managed domain / managed read path 才能放行”
- 用户还需要 doctor、override、依赖检查和状态解释

Claude code 真正值得迁移的，不是某个 sandbox runtime 包，而是这组原则：

> sandbox 不是单一开关，而是一组可解释、可调试、可托管的 restriction profile。

## 1. 先把 sandbox 看成“限制维度”问题

一个成熟的 sandbox 至少包含这些不同维度：

- filesystem
- network
- dependency checks
- override / fallback mode
- violation handling

不要把它们都压缩成一个 `enabled` 字段。

因为这几层解决的是不同问题：

- filesystem：哪些路径能读、能写、不能碰
- network：哪些域名或主机能连
- dependency checks：当前平台能不能真正提供这套隔离
- override / fallback：失败后是否允许进入更宽模式
- violation handling：违规时是阻断、记录、忽略还是回退

一句话：

> sandbox 的关键不是“有或没有”，而是限制边界是否可组合、可解释。

## 2. permission rule 和 sandbox config 不是同一层

源码里一个很重要的点是：

- permission rules 先表达用户可理解的意图
- 然后再转换成 sandbox runtime 真正执行的配置

这说明：

- rule 层更偏策略表达
- sandbox config 层更偏执行落地

不要让用户直接面对底层 runtime 语义，也不要假设 permission 规则天然等于最终 sandbox 行为。

一句话：

> permission rule 负责“想要什么边界”，sandbox config 负责“怎么在运行时把它做出来”。

## 3. path semantics 必须单独写清

这是 sandbox 里最容易误配的一层。

Claude code 源码里明确区分了两种路径语义：

### permission-rule 风格路径

例如：

- `//path`
- `/path`
- `~/path`
- `./path`

其中某些前缀会按 settings 文件目录解释，而不是按传统绝对路径解释。

### sandbox.filesystem.* 风格路径

例如：

- `allowWrite`
- `denyWrite`
- `allowRead`
- `denyRead`

这一层更接近标准文件路径语义。

这说明：

> 同样写成 `/path`，在 rule 层和 sandbox 层可能不是同一个含义。

如果这层不单独沉淀，用户很容易反复遇到：

- 明明写了绝对路径，却被当成 settings-relative
- 明明想约束项目内路径，却实际影响了别的目录

## 4. managed-only 限制适合保护高信任边界

源码里还能看到：

- 某些 network domain 只允许来自 managed policy
- 某些 read path 也只允许来自 managed policy

这背后的方法是：

> 当某个放行能力本身就很敏感时，应允许系统声明“只有托管来源能开这个口子”。

比较适合做 managed-only 的场景：

- 高风险外部域名 allowlist
- 敏感目录读取放行
- 可能直接影响沙箱逃逸面的边界

不适合滥用的场景：

- 所有微小设置都要求 only-managed
- 普通项目级差异也强行升成企业托管

一句话：

> managed-only 用来保护高信任边界，不是把所有设置都升级成企业控制。

## 5. strict mode、fallback 和 policy lock 要分开表达

源码里的 override 设计说明了一个关键边界：

- 严格 sandbox 模式
- 允许 unsandboxed fallback 的模式
- 被更高层 policy 锁死的模式

这三者不是同一个开关。

更合理的最小表达是：

- `strict sandbox mode`
- `allow unsandboxed fallback`
- `locked by policy`

并且要明确：

- 当前模式是谁设置的
- 是否允许本地覆盖
- 被 policy 锁住时如何提示

## 6. dependency check 和 doctor 不是附属 UI

如果 sandbox 真要进入生产使用，doctor 和 dependency check 就不能只是“装饰页”。

源码里能看到：

- 平台支持性检查
- 依赖是否安装
- warning 和 error 分流
- 对缺依赖给出明确安装提示

这说明 sandbox doctor 至少要回答：

1. 当前平台支不支持 sandbox
2. 当前设置是否启用了 sandbox
3. 关键依赖是否缺失
4. 缺失的是 warning 还是 blocking error
5. 用户下一步应该安装什么

一句话：

> sandbox 如果没有 doctor，就等于把运行时隔离问题全部留给用户在失败后猜。

## 7. override / debug 入口必须存在

限制系统最怕的一类问题是：

- 系统说“被拦了”
- 用户却完全不知道是哪里拦的

所以 sandbox 除了执行，还应该提供：

- 当前模式说明
- policy lock 说明
- 依赖状态说明
- override 入口
- debug / status 出口

这层不是为了做复杂 UI，而是为了让限制系统可运维。

一句话：

> 没有 override 和 debug 入口的 sandbox，最后只能靠用户盲试。

## 8. violation handling 要明确，不要默认吞掉

当命令、文件访问或网络访问碰到 sandbox 限制时，系统至少要写清：

- 是直接拒绝
- 记录后拒绝
- 忽略某些违规
- 触发 fallback
- 还是允许用户二次确认

不要让不同类型的 violation 混用同一条静默逻辑。

更合理的做法是：

- 高风险违规：阻断并记录
- 可恢复违规：允许在明确条件下 fallback
- 已知低风险噪音：单独忽略，不污染主诊断面

## 9. 推荐的最小 restriction profile

一个够用的最小模型可以长这样：

```yaml
sandbox_governance:
  filesystem:
    allow_read: []
    deny_read: []
    allow_write:
      - "."
    deny_write: []
  network:
    allowed_domains: []
    denied_domains: []
    allow_managed_domains_only: false
  dependency_check:
    enabled: true
  violation_handling:
    block_on_high_risk: true
    allow_recoverable_fallback: true
  overrides:
    allow_unsandboxed_fallback: false
    lock_by_policy: false
```

重点不是字段长相，而是：

- 限制维度拆开
- managed-only 边界可表达
- fallback 边界可表达
- doctor / dependency 面可接入

## 10. 推荐的最小检查清单

一个仓库准备补 sandbox governance 时，至少先回答：

1. filesystem、network、dependency、override 是否分别建模？
2. permission rules 和 sandbox config 的转换关系是否写清？
3. path semantics 是否区分 permission-rule 风格和 sandbox.filesystem 风格？
4. 哪些放行项只允许来自 managed policy？
5. 当前模式是 strict 还是允许 unsandboxed fallback？
6. doctor 能不能解释平台支持性和缺依赖问题？
7. 当前限制触发后，系统如何处理 violation？

本仓库提供可直接改造的清单模板：

- `templates/project/sandbox-governance-checklist.md`

## 11. 设计规则

- sandbox 要按限制维度建模，不要只用一个开关
- permission rule 和 sandbox runtime config 分层治理
- path semantics 必须单独写清
- managed-only 限制只用于高信任边界
- strict mode、fallback、policy lock 三者分开表达
- doctor、override、debug 是正式能力，不是附属 UI
- violation handling 必须可解释

## 12. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/sandbox-governance.md`
- `skills/sandbox-governance/`
- `templates/project/sandbox-governance-checklist.md`

这样以后再遇到“为什么这个路径规则没按我理解生效、为什么某些域名只能由托管策略放开、为什么 sandbox 打开了却没真正工作、为什么用户被拦却看不到原因”时，就可以按同一套 sandbox governance 方法处理。
