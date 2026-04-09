---
name: plan-mode-gate
description: 非 trivial 任务先规划再实施。Use when a task is complex enough that the agent should lock scope, approach, and verification before editing implementation files.
---

# Plan Mode Gate

## Use When

- 用户要你“先想清楚再做”
- 任务边界不清楚，容易一边读一边乱改
- 预计会跨多个文件或多个模块
- 需要先比较方案、锁定验证矩阵
- 你已经判断直接实现会明显增加返工风险

## Goal

在真正开始改实现文件前，先把范围、方案、验证方式和排除项锁定下来。

## Workflow

### 1. 判断是否真的需要 plan mode

- 区分 trivial 小改动和非 trivial 任务
- 如果只是机械小修，不要滥用 plan mode
- 如果任务复杂、模糊、跨模块，就进入 plan mode

**Success criteria**:
- 已明确本次任务是否需要先规划

### 2. 进入只读探索阶段

- 读取 issue、仓库规则、相关实现和相邻模块
- 搜索已有模式、相似实现、历史约束
- 只记录信息，不修改实现文件

**Success criteria**:
- 已理解当前实现方式和约束，而不是靠猜开始改

### 3. 锁定方案与验证矩阵

- 写清实现路径
- 写清本次不做的内容
- 写清需要跑的验证和 smoke
- 如存在明显分叉，明确为什么选这一条

**Success criteria**:
- 已形成可执行计划，不再处于“边改边想”的状态

### 4. 判断是否进入实施

- 如果范围清楚、方案清楚、验证清楚，就退出 plan mode
- 如果仍然混乱，继续收敛或拆 issue

**Success criteria**:
- 只有在方案锁定后才进入实现阶段

## Rules

- 在 plan mode 里不要顺手改实现文件
- 允许编辑计划文件或设计草稿，但不要把探索和实现混在一起
- 如果任务其实很小，不要强行套 plan mode
- 如果计划阶段发现需求本身有歧义，优先收敛边界，不要靠代码试错
