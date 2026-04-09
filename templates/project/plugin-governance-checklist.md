# Plugin Governance Checklist

这不是运行时实现文件，而是给项目设计 plugin lifecycle、marketplace trust 和 dependency policy 时的最小清单。

## Lifecycle States

至少定义这些状态是否存在：

- `available`
- `installed`
- `enabled`
- `loaded`
- `demoted`
- `disabled`
- `updated_pending_restart`
- `removed`
- `delisted_flagged`

## Install vs Enable

逐项确认：

1. 安装状态是否和启用状态分开存储
2. 哪些状态是全局的
3. 哪些状态是项目级或会话级的
4. 用户是否能解释“装了但没生效”的原因

## Manifest Layers

明确：

1. plugin manifest 负责哪些字段
2. marketplace manifest / entry 负责哪些字段
3. 哪些字段绝不能混放
4. validation 是否会给出明确警告或错误

## Validation Guard

至少检查：

- schema validity
- unknown or misplaced fields
- path traversal
- directory base misunderstandings
- duplicate or conflicting metadata

## Dependency Model

逐项确认：

1. dependency 是否按 capability presence guarantee 理解
2. install-time 是否做 closure / cycle / not-found 检查
3. load-time 是否做 demotion
4. reverse dependents 是否可被解释

## Marketplace Trust Boundary

逐项确认：

1. cross-marketplace auto-install 是否默认阻断
2. 是否存在 allowlist 或显式 trust 机制
3. 用户手动预装的跨市场依赖如何处理
4. 是否避免 transitive trust 无限传播

## Policy Block

至少回答：

1. org policy 是否可以直接 block plugin
2. block 是否影响 install、enable 和 UI filter
3. user disable 和 policy block 是否明确区分

## Startup Reconciliation

启动期至少确认：

1. enabled plugins 是否真的 installed
2. installed metadata 和 settings 是否一致
3. 缺失 plugin 是否需要自动补装或显式报错
4. 本次会话哪些 loaded，哪些 demoted，哪些 blocked

## Update Model

至少定义：

- autoupdate trigger
- marketplace refresh behavior
- plugin update behavior
- pending restart visibility
- failure fallback

## Delist Cleanup

逐项确认：

1. 市场下架后是否需要自动处理
2. 哪些 scope 可以自动卸载
3. managed-only installation 是否应留给管理员处理
4. 是否保留 flagged 状态避免重复处理

## Repository Rule Snippet

可直接改造成项目 `CLAUDE.md` 里的最小规则：

- Plugins must be governed as lifecycle assets, not one-shot downloads.
- Installed state and enabled state must remain distinct.
- Plugin manifest and marketplace metadata must remain separate.
- Cross-marketplace dependency trust must be explicit, not implicit.
- Load-time demotion must stay visible instead of silently mutating user intent.
- Update, restart, and delist cleanup rules must be documented before the plugin system scales.
