---
name: multi-agent-orchestration
description: 把并行代理协作写成任务编排，而不是临时分工。Use when a repository needs explicit task decomposition, agent role boundaries, or safe rules for parallel execution.
---

# Multi-Agent Orchestration

## Use When

- 一个需求明显需要多代理并行
- 你要判断什么能并行，什么必须串行
- 已经有多个 agent 在干活，但 owner、状态和验收责任不清楚
- 你需要给仓库补 task / team / verifier 的最小协作骨架

## Goal

把多代理协作从“临时分工”升级成明确的任务编排：有状态模型、有 owner、有依赖、有最终兜底责任。

## Workflow

### 1. 先分清 issue、task、agent

- issue 是用户目标
- task 是内部可追踪工作项
- agent 是执行者

不要一上来就“开几个 agent”，先把要并行的 task 边界画清楚。

**Success criteria**:
- 已明确 issue 目标、task 切分和执行角色

### 2. 先建 task board，再并行

- 给每个 task 写：
  - subject
  - owner
  - status
  - blocked_by / blocks

**Success criteria**:
- 并行执行前已经有明确 owner 和依赖关系

### 3. 分离协作状态和运行状态

- task board 用：
  - `pending`
  - `in_progress`
  - `completed`
- runtime task 用：
  - `pending`
  - `running`
  - `completed`
  - `failed`
  - `killed`

**Success criteria**:
- 不会把“worker 进程结束”误判为“整个任务闭环完成”

### 4. 定义 leader / worker / verifier

- leader 负责拆解、分配、整合、最终验收
- worker 负责推进分段工作并更新状态
- verifier 负责独立检查，不负责扩 scope

**Success criteria**:
- 最终完成责任有明确 owner，不会漂移

### 5. 判断并行和串行边界

- 写入范围分离、工具集不同、验证可独立运行 -> 可并行
- 共享关键写入面、顺序决定正确性、最终整合 -> 必须串行

**Success criteria**:
- 并行不是为了“更多 agent”，而是为了真正缩短路径且不制造冲突

## Rules

- 不要跳过 task 拆解就直接多开 agent
- 不要让一个 worker 同时持有太多未完成任务
- 不要把最终验收责任外包给 worker
- idle 不是错误，状态脱节才是错误
- 并行前先确认写入面是否冲突
