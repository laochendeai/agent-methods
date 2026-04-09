# MCP Governance Checklist

这不是运行时配置文件，而是给项目梳理 `MCP` 连接器治理时的最小清单。

## Source Inventory

先列出每个 connector 的来源：

- managed / policy
- user manual config
- project manual config
- plugin / capability pack
- synced connector
- runtime additive

## Precedence Rules

先写清谁优先：

- policy 决定底线
- manual config 高于自动注入
- plugin 不覆盖等价 manual config
- synced connector 不覆盖等价 manual config
- runtime additive 只在当前运行范围内生效

## Dedup Signature

不要只按名字去重，至少定义：

- `stdio` 按 `command + args`
- `remote` 按归一化后的 `url`

## Gate Split

分别检查：

1. policy gate
2. source gate
3. risk / allowlist gate
4. capability gate
5. state gate

## Channel Server Review

如果某个 server 会参与消息注入、通知或审批 relay，单独回答：

- 是否有单独 allowlist
- 是否要求显式 capability 声明
- 是否需要单独审计或告警

## Surface Exposure Matrix

对每个 connector，写清哪些 surface 可以暴露：

- tools
- resources
- prompts
- skills
- notifications / permission relay

## Diagnostic Questions

出现“为什么没生效”时，先查：

1. 来源是什么
2. 是否被更高优先级来源压住
3. 是否被签名级去重抑制
4. 是否被 policy / allowlist 拦截
5. 是否缺 capability
6. 是否只是未连接 / 未鉴权 / disabled

## Repository Rule Snippet

可直接改造成项目 `CLAUDE.md` 里的最小规则：

- MCP connectors must be tracked by source, not treated as a flat list.
- Connector deduplication must use connection signatures, not display names.
- Manual config takes precedence over automatic connector injection.
- High-risk channel servers require separate allowlist and capability review.
- Tools, resources, prompts, and relay surfaces are exposed only when the server actually supports them.
- MCP diagnostics must explain suppression, blocking, and missing exposure in user-facing terms.
