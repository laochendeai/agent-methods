---
name: memory-pipeline-governance
description: 把记忆从“是否保存”升级成分层记忆管线。Use when a repository needs to design memory extraction, session summaries, team-shared memory, MEMORY.md indexing, or secret-guarded sync boundaries.
---

# Memory Pipeline Governance

## Use When

- 仓库已经不满足于临时聊天记忆
- 你需要区分 session memory、personal memory、team memory
- 你要补 durable extraction、team sync 或 `MEMORY.md` 索引规则
- 共享记忆开始出现安全或作用域问题
- `memory-promote` 已经不够覆盖当前需求

## Goal

把记忆设计成分层、可索引、可同步、可控风险的 memory pipeline，而不是继续把所有内容堆进一个 memory 文件。

## Workflow

### 1. 先分层

- 至少分出：
  - session memory
  - personal durable memory
  - team shared memory

**Success criteria**:
- 每类记忆都有清楚作用域和职责

### 2. 定义 durable extraction

- 只从新增消息里抽取
- 先查重，再更新
- 避免和主代理本轮已写 memory 重复

**Success criteria**:
- durable memory 是增量提炼，不是全量重写

### 3. 把 `MEMORY.md` 降级为索引

- 正文写到 topic file
- `MEMORY.md` 只保留短入口

**Success criteria**:
- `MEMORY.md` 不会变成 prompt 污染源

### 4. 单独治理 session memory

- 给 session summary 单独预算
- 让它服务 resume / compact / away summary

**Success criteria**:
- session memory 不是 durable memory 的副本

### 5. 单独治理 team memory

- 团队记忆和个人记忆分目录
- 写入前过 secret guard
- 同步时使用 version / checksum / conflict 语义

**Success criteria**:
- team memory 是共享能力，不是泄漏面

## Rules

- 不要把 session / personal / team 三层混在一个目录
- 不要把 `MEMORY.md` 当正文总表
- 不要把敏感内容写进 team memory
- 不要对每轮会话做全量 durable rewrite
- 有共享同步语义时，必须显式设计冲突和校验边界
