---
name: project-bootstrap-plus
description: 初始化更完整的新项目骨架。Use when the user wants to bootstrap a new project or clean up an immature repo by adding a project-specific CLAUDE.md, README, .gitignore, issue templates, PR template, and a minimal repository structure without overwriting mature existing rules.
---

# Project Bootstrap Plus

## Use When

- 用户要从零启动一个新项目仓库
- 用户要把一个只有代码、没有规则和协作骨架的仓库补齐
- 用户要“按我的方法把新仓库初始化完整”
- 用户不仅要 `CLAUDE.md`，还要 `README`、`.gitignore`、issue/PR 模板和基础目录

## Goal

给新项目补齐一套最小可用的协作和代理运行骨架，同时避免用共享模板粗暴覆盖已有成熟内容。

## Rule Priority

始终按这个顺序：

1. 当前项目仓库里的 `CLAUDE.md` / `README` / `.gitignore` / `.github` 现状
2. `agent-methods` 里的通用 methods 和 skills
3. `agent-methods/templates/project/` 里的 starter kit 仅作为起稿和补缺依据

## Inputs

- 当前仓库真实文件结构
- 技术栈线索：`package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` / `Dockerfile` / `requirements.txt`
- 启动命令、测试命令、打包命令
- 用户能明确给出的产品目标和边界

## Workflow

### 1. 先盘点现状

- 检查仓库里是否已有：
  - `CLAUDE.md`
  - `README.md`
  - `.gitignore`
  - `.github/ISSUE_TEMPLATE/`
  - `.github/pull_request_template.md`
- 检查技术栈和现有目录结构
- 判断这是“空白仓库”“半成品仓库”还是“已有成熟规则的仓库”

**Success criteria**:
- 已明确哪些文件需要新建，哪些文件只需补强，哪些不能动

### 2. 生成或补强 `CLAUDE.md`

- 如果仓库已有成熟 `CLAUDE.md`，只补缺项，不覆盖原有项目事实
- 如果没有，基于 `templates/CLAUDE.md` 和仓库真实信息生成项目版

**Success criteria**:
- 项目规则层存在，并与当前项目事实一致

### 3. 生成或补强 `README.md`

- 如果已有 `README.md`，先保留其现有价值，只补全缺失的：
  - 项目概述
  - 启动方式
  - 测试方式
  - 打包/部署方式
  - 目录结构
  - 协作约定
- 如果没有，则参考 `templates/project/README.md` 生成第一版

**Success criteria**:
- `README.md` 能让新加入的人看懂项目怎么跑、怎么测、怎么协作

### 4. 生成或补强 `.gitignore`

- 根据技术栈定制，不要盲目套一个通用大文件
- 可以参考 `templates/project/.gitignore`
- 至少覆盖：
  - 本地环境文件
  - 编辑器垃圾
  - 构建产物
  - 测试缓存
  - 临时 brainstorm / checkpoints / logs

**Success criteria**:
- `.gitignore` 与技术栈匹配，且不会遗漏常见本地噪音

### 5. 补齐 GitHub 协作模板

- 如缺失，生成：
  - `.github/ISSUE_TEMPLATE/change-request.md`
  - `.github/ISSUE_TEMPLATE/bug-report.md`
  - `.github/pull_request_template.md`
- 如已存在，则保留项目现状，只在必要时补强

**Success criteria**:
- 仓库具备最小 issue / PR 协作面

### 6. 补基础目录结构

- 按项目真实需要补最小目录，不为“好看”制造空目录
- 常见候选：
  - `docs/`
  - `scripts/`
  - `tests/`
  - `.github/ISSUE_TEMPLATE/`

**Success criteria**:
- 仓库结构足以支撑后续协作，不引入空壳目录污染

### 7. 输出结果与待确认项

- 明确本次创建了什么、补强了什么
- 标出仍需用户确认的内容，例如：
  - 正式项目名
  - 对外产品定位
  - 真实部署命令
  - CI / release 方式

**Success criteria**:
- 用户知道哪些已经落地，哪些还需补充

## Rules

- 不要用共享模板覆盖已有成熟规则
- 不要生成大量空目录
- 不要把个人偏好写进项目协作文档
- 不要编造启动命令、测试命令、发布命令
- 模板只能做骨架，最终内容必须项目化

## References

按需读取这些模板：

- `templates/CLAUDE.md`
- `templates/project/README.md`
- `templates/project/.gitignore`
- `templates/project/.github/ISSUE_TEMPLATE/change-request.md`
- `templates/project/.github/ISSUE_TEMPLATE/bug-report.md`
- `templates/project/.github/pull_request_template.md`
