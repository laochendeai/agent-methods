# Plugin / Capability Pack 方法

当前仓库已经有不少 `skill`、`hook`、规则模板，但还缺一层更高的“能力编组”抽象。

如果没有这一层，仓库很容易出现两种退化：

- 明明是一项完整能力，却被拆成零散 `skill`、`hook`、`MCP`、模板，启停靠人脑记忆
- 新仓库想复用同一组能力时，只能手抄资产清单，无法清楚表达“这是一个整体”

从 Claude code 的 plugin 线索里，真正值得迁移的不是插件市场本身，而是这一点：

> 一个可启停的能力，不一定只包含一个 prompt 文件；它可以是多种组件的组合包。

## 1. 什么是 Capability Pack

在方法仓库里，更适合用中性的 `capability pack` 概念，而不是直接假设你已经有完整插件运行时。

`capability pack` 的最小定义应该是：

- 围绕一个明确目标组织
- 能作为一个整体被启用 / 停用
- 可以组合多种资产
- 有清晰的默认状态、作用域、所有权和边界

它不是“又一个更大的 skill”，也不是“所有东西都往里塞的文件夹”。

## 2. Plugin 和 Capability Pack 的关系

### Plugin

- 更偏运行时概念
- 通常意味着可安装、可加载、可启停
- 可能有 manifest、版本、市场、校验与加载逻辑

### Capability Pack

- 更偏方法与仓库组织概念
- 即使你还没有插件加载器，也可以先把能力边界设计清楚
- 它可以以后落成 plugin，但不要求当前阶段立即实现 runtime

一句话：

> `plugin` 更像实现形态，`capability pack` 更像方法边界。

## 3. Skill、Hook、MCP、Template、Rule、Pack 的边界

### Rule / `CLAUDE.md`

- 放长期稳定、默认始终生效的约束
- 重点是“必须遵守什么”

### Skill

- 放按需调用的完整流程或参考知识
- 重点是“如何把一件事做完”

### Hook

- 放固定生命周期上的确定性门禁
- 重点是“在什么时候自动执行”

### MCP

- 放外部系统能力接入
- 重点是“连接了什么外部能力”

### Template

- 放给新仓库复制和改造的骨架
- 重点是“第一次怎么起步”

### Capability Pack

- 放“哪些资产应该作为一个整体启停”
- 重点是“这是一组共同服务某个目标的能力”

所以 pack 不替代这些组件，而是给它们一个组合边界。

## 4. 什么时候应该做成 Capability Pack

更适合做 pack 的场景：

- 同一个目标需要多个 `skill + hook + template + MCP` 一起工作
- 仓库需要表达“这是一组一起启用的能力”，而不是松散清单
- 你希望按项目、按环境、按阶段启停整组能力
- 单个组件单独看价值有限，但组合起来才形成稳定能力

不适合做 pack 的场景：

- 只有一个独立 skill
- 只是一个长期默认规则，本来就该写进 `CLAUDE.md`
- 只是某个 MCP 连接本身，没有额外编组需求
- 只是“这些东西都和平台组有关”，但目标彼此无关

## 5. 能力包的最小设计问题

设计 pack 时，先回答 5 个问题：

1. 这组能力服务的唯一目标是什么？
2. 哪些东西必须始终生效，哪些应该可启停？
3. 这组能力包含哪些组件类型？
4. 谁拥有它，默认是否启用，作用域是什么？
5. 如果未来不实现插件运行时，这个 pack 仍然能否被人理解和复用？

如果这 5 个问题答不清，通常说明边界还没收敛好。

## 6. 最小 Manifest 建议

方法仓库不需要先实现加载器，但应该先把声明格式定出来。

一个够用的最小 manifest 至少应包含：

- `id`
- `purpose`
- `scope`
- `default_enabled`
- `owners`
- `activation`
- `components`
- `notes`

示例：

```yaml
id: delivery-governance
purpose: Safe autonomous issue delivery for code repositories.
scope: project
default_enabled: false
owners:
  - platform
activation:
  enable_when:
    - The repository uses autonomous agents for issue delivery.
    - Multiple guardrails must turn on together.
  disable_when:
    - The repo only needs ad hoc one-off skills.
components:
  skills:
    - issue-closed-loop
    - regression-guard
    - repo-closeout
  docs:
    - docs/plan-worktree-mode.md
    - docs/hook-gate.md
    - docs/permission-policy.md
  templates:
    - templates/CLAUDE.md
    - templates/project/permission-policy.example.md
    - templates/project/.claude/hooks.example.jsonc
  hooks: []
  mcp_servers: []
notes:
  - The pack defines grouping and activation only; each component remains independently usable.
```

这个 manifest 的目标不是“可执行”，而是先把编组边界写清楚。

## 7. 最小目录结构建议

如果当前仓库还没有插件运行时，推荐先用中性目录：

```text
capability-packs/
  <pack-id>/
    capability-pack.yaml
    README.md
```

其中：

- `capability-pack.yaml` 写清 pack 的目标、启停、组件与所有权
- `README.md` 解释这个 pack 解决什么问题、何时启用、何时不要启用

如果后续真的落成运行时 plugin，再把这个目录映射到具体实现即可。

## 8. 一个适合本仓库的示例：Delivery Governance Pack

对 `agent-methods` 来说，最自然的第一个示例不是市场型插件，而是“交付治理能力包”。

它适合把这些资产看成一个整体：

- `issue-closed-loop`
- `regression-guard`
- `repo-closeout`
- `hook-gate`
- `permission-policy`
- `plan-worktree-mode`
- `templates/CLAUDE.md`
- 项目级 hook / permission 示例模板

为什么这组东西适合放进一个 pack：

- 它们共同服务“安全、清晰、可验证地推进 issue”
- 单看每个 skill 都成立，但组合后才形成真正的交付治理能力
- 很多仓库会希望按项目阶段决定是否整体启用这组机制

## 9. 设计规则

- 按目标分组，不按文件类型分组
- 默认常驻的规则不要塞进 pack，应该写进仓库规则层
- 只有一个组件时，优先保留为单独资产，不要硬造 pack
- pack 是启停边界，不是运行时实现本身
- pack 必须有明确 owner；否则后续很快沦为无人维护的组合清单
- pack 里的组件应保持可独立理解，不要把关键说明只写在 pack 里

## 10. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/capability-pack.md`
- `skills/capability-pack-design/`
- `templates/project/capability-packs/`

三者一起，才算把“plugin 层值得迁移的组织方式”从概念提及变成可复用方法。
