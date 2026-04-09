---
name: worktree-isolation
description: 需要目录隔离时使用 worktree 而不是在脏工作区里硬做。Use when a task should run in an isolated checkout to avoid branch and workspace cross-contamination.
---

# Worktree Isolation

## Use When

- 当前工作区已有别的未完成任务
- 同仓库需要并行推进多个 issue
- 改动范围大，容易污染主工作区
- 需要为长生命周期任务保留独立目录
- 需要给并行代理或子任务独立工作目录

## Goal

在需要时把任务放进独立目录执行，减少上下文串扰、误改和收尾混乱。

## Workflow

### 1. 先判断是否真的需要 worktree

- 如果当前工作区干净、任务很小、不会并行，branch 通常就够了
- 如果需要目录隔离、并行或长期保留实验现场，再进入 worktree

**Success criteria**:
- 已明确 worktree 是必要隔离，而不是习惯性加复杂度

### 2. 做进入前检查

- 确认仓库是 Git 仓库
- 确认默认分支和 issue 编号
- 检查当前是否存在需要保护的本地未提交工作
- 确定本次任务的基线分支

**Success criteria**:
- 已确认 worktree 的创建前提和风险边界

### 3. 生成安全、稳定的名称

- 名称建议带 issue 编号和短 slug
- 只用字母、数字、点、下划线、短横线
- 不要使用含糊名称或路径逃逸式命名

**Success criteria**:
- worktree 可以被稳定识别、恢复、清理

### 4. 在隔离目录里执行 issue 闭环

- 在 worktree 中继续走 `issue-closed-loop`
- 必要时只复制最小本地配置
- 不要盲目复制 secrets、临时缓存或大目录

**Success criteria**:
- 实施阶段与主工作区隔离，且没有引入新的隐性风险

### 5. 任务结束后明确收尾

- PR 合并后默认清理临时 worktree 和分支
- 如需保留，明确记录保留原因
- 最后走 `repo-closeout`

**Success criteria**:
- worktree 不是“遗留目录”，而是被刻意创建和刻意回收的工作现场

## Rules

- 不要把所有任务都升级成 worktree
- 不要在不清楚风险时复制本地 secrets 或运行时状态
- 不要删除用途不明的 worktree
- worktree 的价值是隔离，不是制造更多长期噪音
