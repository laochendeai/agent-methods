---
name: mcp-governance
description: 把 MCP 从“接了几个 server”提升成连接器治理规则。Use when a repository needs to add, review, deduplicate, or gate MCP connectors, especially when multiple config sources, high-risk channels, or capability-based exposure are involved.
---

# MCP Governance

## Use When

- 仓库准备接入新的 `MCP` server
- 你发现同一个外部能力从多个来源重复接入
- 你需要明确 connector 的优先级、allowlist 或 capability gate
- 某个 channel server 不应该和普通连接器走同一套启用逻辑
- 用户在问“为什么这个 server 没加载 / 没暴露 / 被抑制”

## Goal

把 `MCP` 写成清楚的连接器治理规则，而不是继续停留在“能连就算支持”的状态。

## Workflow

### 1. 先盘点来源

- 列出连接器来自哪里：
  - managed / policy
  - user / project manual config
  - plugin / capability pack
  - synced connector
  - runtime additive

**Success criteria**:
- 已知道每个 connector 的来源和意图强度

### 2. 做签名级去重

- 不按名字判断重复
- 对 `stdio` 连接看 `command + args`
- 对远程连接看归一化后的 `url`
- 明确谁压过谁，避免双重接入

**Success criteria**:
- 同一个底层连接不会从多个来源同时暴露

### 3. 拆分 gate

- 分开定义：
  - policy gate
  - source gate
  - risk / allowlist gate
  - capability gate
  - state gate

不要把这些都塞进一个 `enabled` 字段。

**Success criteria**:
- 每个 gate 都有单独职责，不会互相混淆

### 4. 单独识别高风险 channel server

- 判断它是否会参与对话注入、通知或审批 relay
- 如果是，不要套用普通 connector 默认逻辑
- 给它单独 allowlist、显式 capability 和审计要求

**Success criteria**:
- channel 类连接器不会被当成普通只读工具面

### 5. 按 capability 暴露 surface

- 只在 server 真支持时暴露对应 surface：
  - tools
  - resources
  - prompts
  - skills
  - notifications / permission relay

**Success criteria**:
- 模型和 UI 只看到真实可用且被允许的能力

### 6. 输出最小规则和检查清单

- 记录来源分层
- 记录优先级和去重原则
- 记录 channel 单独治理条件
- 记录 capability 暴露矩阵

**Success criteria**:
- 仓库已经有一套可执行的 MCP connector policy，而不是散乱配置

## Rules

- 不要只按 connector 名字做去重
- 不要让自动注入压过用户显式配置
- 不要把 channel server 和普通 server 走同一套风险规则
- 不要暴露 server 不支持的 surface
- 诊断必须能解释“为什么没有加载 / 为什么没有暴露”
