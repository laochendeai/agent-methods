---
name: new-project-bootstrap
description: 为新项目初始化规则层和启动约束。Use when the user wants to start a new project or initialize an unfamiliar repo, and you need to detect whether a project CLAUDE.md already exists before falling back to the shared template.
---

# New Project Bootstrap

## Use When

- 用户要新建项目
- 用户要初始化一个刚拉下来的陌生仓库
- 用户要“按我的方法启动一个新仓库”
- 用户希望代理先判断该读项目内规则还是共享模板

## Goal

避免在新项目初始化时重复造规则，或者错误地用共享模板覆盖已有项目规则。

## Rule Priority

始终按这个顺序：

1. 当前项目仓库里的 `CLAUDE.md`
2. 共享方法仓库里的通用 skills / 方法
3. `templates/CLAUDE.md` 只在项目内没有 `CLAUDE.md` 时作为起稿模板

## Workflow

### 1. 先判断项目状态

- 检查当前目录是否为已有仓库
- 检查项目内是否已经存在 `CLAUDE.md`
- 检查是否已有 `README`、运行脚本、测试命令、配置文件

**Success criteria**:
- 已明确这是“已有项目”还是“空白/新项目”

### 2. 如果项目内已有 `CLAUDE.md`

- 直接把它视为项目权威规则
- 只在用户明确要求时补充缺失栏目
- 不用共享模板覆盖它

**Success criteria**:
- 项目内规则成为唯一权威来源

### 3. 如果项目内没有 `CLAUDE.md`

- 读取共享方法仓库里的 `README.md`
- 读取 `templates/CLAUDE.md`
- 结合当前项目的真实文件结构、启动方式、技术栈、目标，生成项目专属 `CLAUDE.md`

**Success criteria**:
- 新项目已拥有第一版项目规则文件

### 4. 规则必须项目化

- 模板只能作为骨架，不能原封不动照抄
- 必须写入项目真实的：
  - 启动命令
  - 测试命令
  - 架构边界
  - 危险动作
  - 完成定义

**Success criteria**:
- 生成出的 `CLAUDE.md` 与当前项目事实一致

### 5. 输出初始化结论

- 说明本次是“沿用项目内规则”还是“基于模板新建规则”
- 标出仍需用户补充确认的空白项

**Success criteria**:
- 用户知道后续应该以哪份规则为准

## Rules

- 不要用共享模板覆盖已有项目 `CLAUDE.md`
- 不要把个人偏好写进新项目仓库
- 不要把空洞模板原样提交；必须结合项目事实落地
- 如果项目事实不足以写清某一项，就明确标记待补充，而不是编造
