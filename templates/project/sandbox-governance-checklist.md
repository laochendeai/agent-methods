# Sandbox Governance Checklist

这不是运行时实现文件，而是给项目设计 sandbox restriction profile、managed-only 边界和 doctor/override 流程时的最小清单。

## Restriction Dimensions

先列出是否分别建模：

- filesystem
- network
- dependency checks
- override mode
- violation handling

## Permission vs Sandbox Conversion

逐项确认：

1. permission rules 如何转换成 sandbox runtime config
2. 哪些规则只表达意图
3. 哪些字段是 runtime 真正执行的限制

## Path Semantics

至少写清：

1. permission-rule 风格路径如何解析
2. sandbox.filesystem.* 风格路径如何解析
3. `/path`、`//path`、`~/path`、相对路径各自语义
4. 哪些常见误配会导致越界或误拦截

## Managed-Only Restrictions

逐项确认：

1. 哪些 domain / path 只能由 managed policy 放行
2. 为什么这些项值得 only-managed
3. 哪些普通项目级差异不应升级成 only-managed

## Restriction Modes

至少定义：

- strict sandbox mode
- allow unsandboxed fallback
- policy lock

并写清：

- 当前模式如何切换
- 谁能切换
- 被 policy 锁住时如何提示

## Dependency Checks

至少回答：

1. 当前平台是否支持 sandbox
2. 关键依赖有哪些
3. 缺失时哪些是 warning，哪些是 error
4. 用户下一步该安装什么

## Violation Handling

逐项确认：

1. 高风险违规如何阻断
2. 可恢复违规是否允许 fallback
3. 哪些噪音型违规允许单独忽略
4. 是否会保留日志或状态解释

## Debug / Override Entry

至少保证：

- 用户能看到当前 sandbox 状态
- 用户能看到当前依赖状态
- 用户能看到是否被 policy lock
- 用户能进入 override / debug 路径

## Repository Rule Snippet

可直接改造成项目 `CLAUDE.md` 的最小规则：

- Sandbox must be modeled as a restriction profile, not a single boolean switch.
- Permission rules and sandbox runtime config must remain separate layers.
- Path semantics must be documented explicitly for each sandbox-related surface.
- Managed-only allowances should be reserved for high-trust boundaries.
- Strict mode, fallback mode, and policy lock must be expressed separately.
- Sandbox doctor and override flows must explain missing dependencies and active restrictions in user-facing terms.
