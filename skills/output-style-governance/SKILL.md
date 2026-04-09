---
name: output-style-governance
description: 把输出风格从临时 prompt 提升成结构化 response contract。Use when a repository needs custom output styles, source precedence rules, plugin-bound styles, or a minimal output-style file template.
---

# Output Style Governance

## Use When

- 仓库准备引入自定义 output style
- 用户、项目、plugin 都开始定义输出约束
- 你需要明确 style 的来源、命名和覆盖关系
- 某个 plugin 依赖固定 response contract
- 你想把风格提示从聊天里搬成长期资产

## Goal

把 output style 写成可管理、可覆盖、可诊断的 response contract，而不是零散 prompt 文本。

## Workflow

### 1. 先定义最小数据模型

- 至少写清：
  - name
  - description
  - prompt
  - source

**Success criteria**:
- style 已经是结构化资产，而不是匿名文本

### 2. 明确来源分层

- 列出 built-in / plugin / user / project / policy
- 明确谁覆盖谁

**Success criteria**:
- 当前 style 的来源和优先级可以被解释

### 3. 设计命名规则

- 普通 style 用清晰短名
- plugin style 用命名空间

**Success criteria**:
- style 名称不会在多来源环境里迅速冲突

### 4. 收敛 plugin 强制绑定

- 只在 plugin 真依赖固定输出契约时使用强制 style
- 避免多个 plugin 争夺唯一风格

**Success criteria**:
- `force-for-plugin` 只服务功能契约，不服务个人审美

### 5. 输出最小模板

- 给仓库一个可直接改造的 style 文件示例

**Success criteria**:
- 新项目不看聊天记录也能写出第一版 output style

## Rules

- 不要把 style 当临时 prompt 片段保存
- 不要把任务指令和表达风格混成一个层
- 不要让 plugin style 和普通 style 共享含糊命名
- 不要滥用强制绑定覆盖用户偏好
- style 的来源和覆盖关系必须可诊断
