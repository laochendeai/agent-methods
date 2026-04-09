---
name: capability-pack-design
description: 设计 capability pack 边界，而不是把相关能力散落成零碎开关。Use when a repository needs to group multiple skills, hooks, MCP servers, and templates into a single toggleable capability boundary.
---

# Capability Pack Design

## Use When

- 一个能力需要 `skill + hook + MCP + template` 共同成立
- 你在判断某个需求该保留为单个 skill，还是升级成 capability pack
- 仓库已经有很多独立资产，但缺少按目标组织的启停边界
- 你要给项目补最小 manifest 或目录结构建议

## Goal

把一组围绕同一目标的能力组织成可解释、可启停、可维护的 capability pack，而不是继续靠口头清单记忆。

## Workflow

### 1. 先按目标盘点资产

- 列出相关的 `rule / skill / hook / MCP / template`
- 只保留真正服务同一目标的资产

**Success criteria**:
- 已得到一组围绕单一目标的候选组件，而不是按文件类型堆料

### 2. 分离常驻规则与可启停能力

- 长期默认生效的约束留在 `CLAUDE.md` / rule 层
- 只有需要按项目、阶段、环境切换的部分才进入 pack

**Success criteria**:
- pack 边界里只保留需要成组启停的能力

### 3. 判断它是否真的值得做成 pack

- 是否至少涉及两类组件
- 是否存在成组启停价值
- 组件单独存在时是否会让人难以理解整体目标

如果都不满足，优先保留为单个 skill 或模板。

**Success criteria**:
- 已确认这是 pack 问题，而不是命名膨胀

### 4. 定义 pack 元信息

- 写清 `id`
- 写清 `purpose`
- 写清 `scope`
- 写清 `default_enabled`
- 写清 `owners`

**Success criteria**:
- pack 的启停边界、默认状态和责任人都明确了

### 5. 输出最小 manifest 和目录建议

- 写一份最小 manifest
- 写一个解释 pack 何时启用、何时不要启用的 README
- 如有需要，再给一个 starter 示例目录

**Success criteria**:
- 别人不看聊天记录，也能理解这个 capability pack

## Rules

- 不要为了“显得高级”把单个 skill 包装成 pack
- 不要把不相关能力因为同一 owner 就硬塞进同一个 pack
- pack 负责能力编组，不负责替代运行时插件加载器
- pack 里的组件必须仍可独立理解和维护
