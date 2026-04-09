---
name: model-governance
description: 把 model identity、provider routing、allowlist、capability cache、deprecation 和 upgrade path 写成结构化治理规则。Use when a repository needs clearer model selection precedence, provider-aware policies, or a minimal checklist for model capability and deprecation governance.
---

# Model Governance

## Use When

- 仓库开始支持多个 provider 或多种 model selector
- 你需要区分 alias、family、version-prefix 和 exact model id
- 你要定义 allowlist、capability cache、deprecation 或 upgrade path
- 用户已经开始问“为什么这个 provider 下模型不一样”
- model selection 逻辑正在从简单字段演变成复杂条件链

## Goal

把模型选择从字符串配置升级成 provider-aware、capability-aware 的正式治理层。

## Workflow

### 1. 先定义 model identity

- 至少写清：
  - provider
  - selector kind
  - selector value
  - resolved id
  - capabilities

**Success criteria**:
- 当前系统已经能区分“写了什么”和“实际跑什么”

### 2. 固定 selection precedence

- 明确 session override、启动参数、环境变量、settings、built-in default 的顺序

**Success criteria**:
- 模型选择冲突时可以稳定解释来源

### 3. 把 provider routing 纳入 policy

- 不只决定请求去哪发
- 还要决定默认值、allowlist、deprecation 和 capability 解释

**Success criteria**:
- provider 差异不再散落在各处 if/else 里

### 4. 定义 allowlist 语义

- 区分 family alias、version prefix、exact id
- 明确 family wildcard 何时会被更具体规则收窄

**Success criteria**:
- allowlist 能表达粗粒度允许和细粒度限制两种意图

### 5. 设计 capability policy

- 明确 discovery、cache、refresh、override、fallback 规则
- 只在合适资格和成本条件下刷新

**Success criteria**:
- capability 不再只能靠硬编码维护

### 6. 单独治理 deprecation 和 upgrade

- deprecation 要带 provider 语义
- upgrade path 只在确实可达时提示

**Success criteria**:
- 模型生命周期变化可以被提前、明确地暴露

### 7. 补 explainability

- `status` / `doctor` 至少能解释：
  - 当前 provider
  - 当前 resolved model
  - allowlist 状态
  - capability 来源
  - deprecation / upgrade 信号

**Success criteria**:
- 维护者和用户都能知道当前 model policy 为什么成立

## Rules

- 不要把 model 当成一个单纯的字符串字段
- 不要让 provider routing 藏在实现细节里
- 不要让 allowlist 只支持 exact match
- 不要把 capability 永远写死在代码里
- 不要把 deprecation 和 upgrade 提示做成零散文案
