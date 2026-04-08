---
name: issue-closed-loop
description: "以 issue 为中心完成仓库闭环交付。Use when the user wants end-to-end issue delivery: read issue, branch, implement, verify, PR, merge, and return to a clean default branch."
---

# Issue Closed Loop

## Use When

- 用户要求“按仓库流程完成闭环”
- 用户要求“围绕某个 issue 做完，不要停在半路”
- 用户要求“做完并推上去”

## Goal

把一个 issue 从需求状态推进到真正完成状态，而不是只停留在“本地改了代码”。

## Workflow

### 1. 锁定 issue 与仓库规则

- 读取 issue 内容、相关评论、仓库 `CLAUDE.md`、已有设计文档
- 明确范围、约束、完成标准、排除项

**Success criteria**:
- 已明确 issue 编号、目标、边界、完成条件

### 2. 建独立分支

- 从最新仓库主分支（通常是 `main`）切出专用分支
- 分支名带上 issue 编号和简短 slug

**Success criteria**:
- 变更在专用分支上进行，不污染主分支

### 3. 做最小闭环实现

- 只实现 issue 要求的范围
- 不顺手做无关重构
- 读清相关代码后再改，不盲改

**Success criteria**:
- 需求实现完成，且范围没有无声膨胀

### 4. 做针对性验证

- 先根据影响面列出验证矩阵
- 运行最相关的测试、检查、smoke
- 如果涉及启动、接口、页面，就验证实际运行路径

**Success criteria**:
- 改动点和相邻风险点都有验证证据

### 5. 提交并推送

- 提交信息说明 issue 意图
- 推送专用分支
- 保持 diff 可读，不混入无关文件

**Success criteria**:
- 远端分支可见，提交意图清楚

### 6. 建 PR 并完成合并

- PR 描述写清问题、方案、验证
- 如仓库流程允许，推进到合并
- 合并后同步本地主分支

**Success criteria**:
- issue 对应改动已进入主分支
- 本地回到干净的主分支

### 7. 输出闭环结果

- 报告变更结果、验证结果、PR/merge 状态、是否还有剩余风险

**Success criteria**:
- 用户能一眼判断这件事是否真正完成

## Rules

- 不要跳过验证
- 不要把 unrelated change 一起提交
- 如果被外部权限、账号、CI、人工审批卡住，要尽量推进到最远，并明确说明阻塞点
- 合并后默认回到干净主分支
- 如果中途发现 issue 本身歧义，先用仓库现有文档和代码证据收敛，再决定是否升级为新 issue
