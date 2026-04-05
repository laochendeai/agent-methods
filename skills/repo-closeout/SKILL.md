---
name: repo-closeout
description: 做一次仓库级安全收尾。Use when a task, PR, or work session is done and the user wants the repository left in a clean, collaboration-ready state by checking docs drift, syncing the main branch, reviewing stale branches/worktrees, and surfacing temporary noise without blindly deleting user data.
---

# Repo Closeout

## Use When

- 一个 issue / PR / 一轮开发已经完成
- 用户要“把仓库收尾干净”
- 用户要“切回干净的 master/main”
- 用户要清理本地分支、worktree、临时文件、文档漂移

## Goal

让仓库在一个阶段性工作完成后回到清晰、干净、可继续协作的状态，而不是留下脏分支、过期 worktree、文档漂移和临时噪音。

## Scope

这个 skill 负责：

- 检查当前 git 状态
- 确认主分支同步状态
- 识别已合并/陈旧的本地分支和 worktree
- 检查 `README` / `CLAUDE.md` / 模板是否需要同步
- 识别临时文件、日志、brainstorm、checkpoints 是否正在污染仓库
- 输出安全收尾建议，或在风险可控时执行收尾动作

这个 skill 不负责：

- 未经确认删除用户明显还在使用的数据
- 强制重写历史
- 粗暴清空所有未跟踪文件

## Workflow

### 1. 盘点当前仓库状态

- 查看当前分支、主分支、远端同步情况
- 检查工作区是否干净
- 检查是否存在未提交、未推送、未合并的改动

**Success criteria**:
- 已明确当前仓库是否适合进入收尾动作

### 2. 判断主分支闭环状态

- 如果刚完成 PR/merge，确认对应改动是否已进入主分支
- 确认本地 `master` / `main` 是否与远端同步
- 如需要，切回并同步主分支

**Success criteria**:
- 本地主分支是用户后续继续工作的可信起点

### 3. 审视分支与 worktree

- 列出本地分支和 worktree
- 识别已合并、明显陈旧、或仅用于一次性任务的对象
- 只在安全前提下清理；不确定时先报告再动手

**Success criteria**:
- 已识别可以清理和不能清理的对象

### 4. 检查文档和规则漂移

- 看本轮改动是否让这些文件变旧：
  - `README.md`
  - `CLAUDE.md`
  - 项目模板 / issue 模板 / PR 模板
- 若有明显漂移，补一轮最小同步

**Success criteria**:
- 代码状态和协作文档没有明显脱节

### 5. 检查临时噪音

- 识别本地临时文件：
  - brainstorm 文档
  - checkpoints
  - logs
  - 一次性导出物
  - 临时脚本和调试文件
- 区分：
  - 应加入 `.gitignore`
  - 应保留但不提交
  - 应在用户确认后清理

**Success criteria**:
- 仓库没有继续积累明显的临时污染

### 6. 输出收尾报告

- 说明已完成的收尾动作
- 说明未执行但建议处理的内容
- 说明剩余风险和人工确认项

**Success criteria**:
- 用户能一眼判断仓库是否已经回到“干净可继续”的状态

## Rules

- 不要自动删除未确认的重要数据
- 不要对未合并分支做破坏性操作
- 不要用 `git reset --hard`、`git clean -fdx` 这类粗暴手段
- 若当前工作区有用户未提交内容，优先保护现场
- 收尾目标是“可继续协作”，不是“表面看起来全空”
