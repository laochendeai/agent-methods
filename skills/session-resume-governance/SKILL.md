---
name: session-resume-governance
description: 把 session persistence 从“别乱存”变成可恢复设计。Use when a repository needs explicit decisions about what session state to persist, how resume should work, or why resume consistency is drifting.
---

# Session Resume Governance

## Use When

- 你要设计会话持久化 / resume / lineage
- 长任务、subagent、worktree 恢复经常出问题
- 仓库只强调“别把临时信息写进规则”，但没有正向恢复模型
- 你需要区分 transcript、metadata、sidecar 和 checkpoint

## Goal

把会话恢复需要的状态写成清晰分层，而不是把所有聊天相关信息混在一起存，导致 resume 漂移或失真。

## Workflow

### 1. 先分层，不要先建大表

- 分出：
  - transcript 正文
  - session 元数据
  - subagent / remote task sidecar
  - resume consistency checkpoint

**Success criteria**:
- 已明确哪些数据属于正文，哪些属于恢复辅助信息

### 2. 只保留恢复真正需要的状态

- 只持久化：
  - 恢复 conversation chain 必须的信息
  - 恢复角色 / 目录 / 任务必须的信息
  - resume 校验需要的信息

不要把 progress、loading、瞬时 UI 状态一起写进去。

**Success criteria**:
- 持久化边界已经收敛，不再是“先全存再说”

### 3. 定义最小 lineage 模型

- 写清：
  - `session_id`
  - `parent_session_id`
  - `forked_from_session_id`
  - `resume_source_session_id`

**Success criteria**:
- 会话来源和分叉关系可解释

### 4. 单独处理 subagent 和 worktree 恢复

- subagent 至少保留：
  - `agent_id`
  - `agent_type`
  - `description`
  - `worktree_path`
- worktree 至少保留：
  - 最后状态
  - 恢复路径
  - 路径失效后的降级策略

**Success criteria**:
- 子代理不会在恢复后 silently 退化，worktree 不会靠猜目录

### 5. 增加 resume 一致性诊断点

- 给 transcript 增加 checkpoint 或等价校验
- 能判断：
  - 恢复出来更多了
  - 恢复出来更少了
  - 链是否断了

**Success criteria**:
- resume 问题可以诊断，不再只是“感觉恢复不对”

## Rules

- 不要把 UI 瞬时状态写进恢复链
- 不要把所有恢复信息都硬塞进主 transcript
- lineage 必须显式，不要靠目录或文件名猜
- worktree 恢复必须处理“路径已不存在”的情况
- 没有 checkpoint 的 resume 很难长期稳定
