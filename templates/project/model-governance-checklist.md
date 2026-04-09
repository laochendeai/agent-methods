# Model Governance Checklist

这不是运行时实现文件，而是给项目设计 model identity、provider routing、allowlist、capability policy 和 deprecation 机制时的最小清单。

## Model Identity

至少确认：

- [ ] 是否区分 provider
- [ ] 是否区分 alias / family / version-prefix / exact id
- [ ] 是否能记录 selector value 和 resolved id
- [ ] 是否能单独描述 capabilities

## Selection Precedence

至少写清：

- [ ] session override
- [ ] startup flag
- [ ] environment variable
- [ ] settings
- [ ] built-in default

## Provider Routing

逐项确认：

- [ ] provider 是否会影响默认模型
- [ ] provider 是否会影响模型可用性
- [ ] provider 是否会影响 deprecation 判断
- [ ] provider 是否会影响 capability 支持矩阵

## Allowlist Policy

至少确认：

- [ ] 是否支持 family alias
- [ ] 是否支持 version prefix
- [ ] 是否支持 exact id
- [ ] 更具体规则是否能收窄 family wildcard
- [ ] 空 allowlist、缺失 allowlist、未知 selector 各自意味着什么

## Capability Policy

逐项确认：

- [ ] capability 是否支持 discovery
- [ ] 是否有 cache file 或 cache strategy
- [ ] refresh 触发条件是什么
- [ ] 哪些环境不应刷新
- [ ] provider lag 时是否允许 override

## Deprecation And Upgrade

至少回答：

- [ ] deprecation 是否带 provider 语义
- [ ] 是否有明确 retirement date
- [ ] 是否会在仍可用但即将退役时提示
- [ ] 是否存在明确 upgrade path
- [ ] 只有真正可达时才提示 upgrade 吗

## Explainability

系统至少应能回答：

- [ ] 当前 provider 是什么
- [ ] 当前 selector 属于哪一类
- [ ] 当前 resolved model 是什么
- [ ] allowlist 为什么允许或拒绝
- [ ] capability 来自缓存、发现还是 override
- [ ] 当前模型是否已弃用或可升级

## Repository Rule Snippet

可直接改造成项目 `CLAUDE.md` 里的最小规则：

- Model selection must be documented as provider-aware policy, not a single string field.
- Selector semantics must distinguish alias, family, version-prefix, and exact id.
- Model selection precedence must be explicit before adding more defaults.
- Capability support must allow cache and override boundaries, not only hardcoded assumptions.
- Deprecation and upgrade signals must remain provider-aware and explainable.
