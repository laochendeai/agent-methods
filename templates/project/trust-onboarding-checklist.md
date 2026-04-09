# Trust Onboarding Checklist

这不是运行时实现文件，而是给项目设计首次进入仓库时的 onboarding、trust gate 和信任记忆边界时的最小清单。

## Onboarding vs Trust

先分别写清：

- onboarding 负责什么
- trust gate 负责什么
- 哪些内容属于后续 permission flow，而不属于首次 trust

## Onboarding State

至少定义：

1. onboarding steps
2. 每个 step 的完成条件
3. 每个 step 的启用条件
4. 完成标记如何保存
5. seen count 和展示上限

## Capability Surface Disclosure

逐项确认首次进入时是否需要披露：

- hooks
- MCP servers
- bash permissions
- commands / skills / plugins 带来的 bash 执行
- credential helpers
- cloud auth helpers
- dangerous env vars

## Source-Aware Risk Summary

至少写清：

1. 每类高风险能力来自哪个配置源
2. 项目配置和本地配置如何区分
3. 哪些来源属于插件、技能或项目规则

## Trust Memory Scope

至少定义：

- session scope
- project scope

并写清：

1. home / 高层目录是否只在 session 内记忆
2. 项目目录是否持久化
3. 是否存在全局信任，为什么

## Skip / Reuse / Retrigger

逐项确认：

1. 什么时候直接跳过
2. 什么时候复用已有 trust
3. 什么时候重新触发
4. 风险面扩张时是否要求重新确认

## Permission Flow Boundary

至少保证：

- trust gate 不替代工具级授权
- 后续 permission flow 仍然记录 approval source
- 具体 permission updates 仍然可持久化和审计

## Audit Signals

至少保证系统可回答：

- trust dialog 何时展示
- 展示时有哪些高风险能力
- 用户是否接受
- 这是 session 还是 project 作用域

## Repository Rule Snippet

可直接改造成项目 `CLAUDE.md` 的最小规则：

- Onboarding and trust gate must be modeled as separate flows.
- First-entry trust prompts must disclose the repository's actual capability surface.
- Trust acceptance must be scoped to session or project, not silently promoted to global permanent trust.
- Trust gate must not replace later tool-level permission checks.
- Approval source, persistence, and audit signals must remain available after onboarding is complete.
