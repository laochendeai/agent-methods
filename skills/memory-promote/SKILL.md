---
name: memory-promote
description: 只把稳定规则沉淀到正确层级。Use when new preferences, conventions, or workflows appear and you need to decide whether they belong in project rules, personal memory, or nowhere permanent.
---

# Memory Promote

## Use When

- 会话里出现了新的稳定偏好或流程
- 用户说“以后都这么做”
- 需要决定某条新规则应不应该写进仓库

## Goal

把稳定规则放进正确层级，同时阻止临时噪音污染仓库规则。

## Workflow

### 1. 分类

把新信息分成三类：

- 项目级稳定规则
- 个人级偏好
- 临时会话信息

**Success criteria**:
- 每条信息都已完成归类

### 2. 判断是否值得持久化

- 只有稳定、重复、长期有效的内容才进入项目规则
- 临时排障结论、一次性 workaround 不进入规则层

**Success criteria**:
- 已筛掉不该持久化的内容

### 3. 放到正确位置

- 项目规则 -> 仓库 `CLAUDE.md`
- 个人偏好 -> 个人层，不进仓库
- 临时信息 -> 不沉淀

**Success criteria**:
- 规则层保持干净且可信

## Rules

- 不要把短期情境误写成长期规则
- 不要把个人偏好写进团队仓库
- 如果一条规则还没有稳定重复出现，先观察，不急着写
