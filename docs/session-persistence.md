# Session Persistence / Resume / Lineage 方法

方法仓库如果只强调“临时信息不要乱记”，最后会走向另一个极端：

- 长任务一旦中断，恢复点丢失
- worktree、subagent、任务关系无法还原
- resume 看起来能用，但恢复出来的上下文和会话结束前并不一致

Claude code 这一层真正值得迁移的，不是某个具体 JSONL 格式，而是这组原则：

> 只持久化恢复真正需要的状态；把正文、元数据、sidecar、恢复校验分层；把 resume 一致性当成一等问题。

## 1. 先分清 4 类数据

### 1. 会话正文

- 用户消息
- assistant 消息
- attachment / system boundary
- 能参与会话链恢复的消息

这类数据的目标是：

- 重建 conversation chain
- 支撑 `resume`
- 支撑后续 summary / firstPrompt / messageCount 计算

### 2. 会话元数据

- title / tag
- agent setting
- mode
- PR link
- worktree state

这类数据的目标不是“聊天历史”，而是：

- 在 resume 列表里正确展示
- 在恢复后还原关键环境
- 在 compaction 后不丢失最小会话身份信息

### 3. sidecar 元数据

- subagent 的 `agentType`
- subagent 的 `worktreePath`
- 原始 task 描述
- remote task 的身份信息

这类数据适合单独写 sidecar，而不是硬塞进主 transcript。

### 4. 恢复一致性校验点

- messageCount checkpoint
- compact / snip 边界
- 内容替换记录
- worktree 最后一跳状态

这类数据的目标是：

- 检查“写进去的”和“恢复出来的”是不是同一条链
- 避免 resume  silently 变成另一段会话

## 2. 什么应该持久化

建议持久化的内容，必须至少满足下面之一：

- resume 需要它才能恢复正确上下文
- UI / 状态展示需要它才能正确识别会话
- 子代理或任务恢复需要它才能回到正确角色 / 目录 / 任务
- compaction / snip 后需要它来校验恢复一致性

典型应该持久化的内容：

- transcript chain 本身
- session id
- transcript path / project path
- custom title / tag / agent setting / mode
- parent session id
- worktree state
- subagent metadata
- remote task identity
- compact / snip 相关恢复边界
- 必要的 file history / attribution snapshot

## 3. 什么不应该持久化

不建议持久化的内容通常是：

- 只服务当前 UI 的瞬时 progress
- 高频噪音状态
- 可重新推导的临时显示信息
- 个人偏好或一次性 debug 碎片

典型不该持久化的内容：

- progress ticker
- 瞬时 loading 状态
- 某次临时排障笔记
- 只用于当前进程的短生命周期缓存
- 明显不属于恢复链路的聊天噪音

一句话：

> 持久化“恢复所需状态”，不要持久化“当时看起来有点有用的所有东西”。

## 4. 设计原则

### 4.1 正文和元数据分层

会话正文负责重建链路；title、tag、agent、worktree 这类恢复辅助信息应该按元数据处理，而不是和正文混成一个概念。

### 4.2 sidecar 用来装“恢复路由信息”

源码里一个很重要的做法是：subagent 的 `agentType`、`worktreePath`、描述等，放在 sidecar 文件里，而不是强行扩展主 transcript 的 schema。

这类信息的共同特征是：

- 对恢复很关键
- 不是会话正文的一部分
- 更接近“如何恢复到正确执行位点”

### 4.3 先写可恢复最小点，再等完整响应

源码里值得迁移的一个关键点是：用户消息在 query 真正返回前就先落盘。

这避免了一个常见故障：

- 用户消息已经被接受
- 但进程在 API 响应前被杀掉
- transcript 里没有真正会话消息
- `resume` 直接报 “No conversation found”

所以原则是：

> 一旦用户输入成为恢复起点，就应该先持久化这个起点，而不是等整轮交互结束。

### 4.4 恢复一致性必须可度量

成熟系统不会只说“resume 失败了”，而会检查：

- in-memory messageCount
- on-disk chain reconstruct 后的实际位置
- delta 是多了还是少了

这类 checkpoint 让你能定位是：

- pre-compact 历史没有被正确裁剪
- 链路被截断
- sidechain / tool result / snip 破坏了 parent chain

### 4.5 worktree 恢复必须是显式状态，不是猜

源码里把 worktree state 单独记下来，并在恢复时重新检查路径是否还存在。

这很重要，因为 resume 不是“猜当前目录应该去哪”，而是：

- 上次会话退出时到底在不在 worktree
- 那个 worktree 现在还存不存在
- 如果不存在，要把状态显式改成 exited，而不是继续保留脏路径

## 5. 最小会话元数据模型建议

一个够用的最小模型可以分成 5 块：

### 1. Session Identity

- `session_id`
- `project_path`
- `transcript_path`
- `created_at`
- `last_updated_at`

### 2. Resume Surface Metadata

- `custom_title`
- `tag`
- `agent_setting`
- `mode`
- `pr_link`

### 3. Lineage

- `parent_session_id`
- `forked_from_session_id`
- `resume_source_session_id`

### 4. Execution Context

- `cwd`
- `worktree_path`
- `worktree_branch`
- `original_project_root`

### 5. Child Recovery Metadata

- `subagents[]`
- `remote_tasks[]`
- `content_replacements[]`
- `checkpoints[]`

示例：

```yaml
session:
  session_id: sess_123
  project_path: /repo
  transcript_path: /repo/.sessions/sess_123.jsonl
  created_at: 2026-04-09T10:00:00Z
  last_updated_at: 2026-04-09T10:24:10Z
  custom_title: fix resume consistency
  tag: persistence
  agent_setting: codex-default
  mode: normal
lineage:
  parent_session_id: sess_100
  forked_from_session_id: null
  resume_source_session_id: sess_123
execution:
  cwd: /repo
  worktree_path: /repo/.worktrees/fix-resume
  worktree_branch: issue-5-session-persistence
  original_project_root: /repo
subagents:
  - agent_id: agent_a1
    agent_type: verifier
    description: verify resume path
    worktree_path: /repo/.worktrees/fix-resume
remote_tasks:
  - task_id: task_88
    task_type: background_review
    session_id: remote_sess_1
checkpoints:
  - type: turn_message_count
    value: 128
  - type: compact_boundary
    tail_uuid: msg_900
```

重点不是字段名照抄，而是这 5 块不要混掉。

## 6. Resume / Lineage / Subagent / Worktree 的基本关系

### Resume

- 恢复的是“同一条会话链”或它的可控分叉
- 重点是 transcript chain + metadata cache + checkpoint

### Lineage

- 描述这条会话从哪里来
- 重点是 parent / fork / resume source

### Subagent

- 描述子代理是谁、在哪儿、用什么角色启动
- 重点是 `agentType`、`description`、`worktreePath`

### Worktree

- 描述恢复时应不应该回到隔离目录
- 重点是“最后状态”与“路径是否还存在”

把它们串起来可以理解为：

> transcript 负责恢复主链，lineage 负责说明关系，subagent sidecar 负责恢复子链角色，worktree state 负责恢复执行位置。

## 7. 常见失败模式与诊断顺序

### 1. `resume` 找不到会话

先查：

- 用户消息是否在 API 响应前已写入
- transcript 里是不是只有 queue / progress 类噪音
- session file 指针是否正确指向当前 session

### 2. resume 后消息变多了

常见原因：

- compact / snip 之后没有正确裁剪旧历史
- preserved segment relink 失败
- content replacement / sidechain 让链重建回到了 pre-compact 历史

先查：

- messageCount checkpoint
- compact boundary
- snip removed UUID 过滤

### 3. resume 后消息变少了

常见原因：

- parentUuid 链断裂
- sidechain 消息没有落到正确文件
- 主链引用到了只存在于 sidechain 的 UUID

先查：

- dangling parentUuid
- main session / sidechain 的写入边界
- dedup 是否错误跨文件生效

### 4. 恢复到错误目录

先查：

- persisted worktree state 是否存在
- worktreePath 现在是否还存在
- 是 fresh worktree 优先，还是旧 transcript 状态优先

### 5. 子代理恢复成了错误角色

先查：

- `agentType` 是否有 sidecar
- `description` 是否被保留
- `worktreePath` 是否丢失

## 8. 推荐的诊断清单

排查恢复问题时，建议按这个顺序：

1. 当前恢复的是哪一个 `session_id`
2. transcript path 和 project path 是否匹配
3. conversation chain 的 leaf 是哪个 UUID
4. messageCount checkpoint 的 delta 是多少
5. worktree state 是 `undefined`、`null` 还是有效对象
6. 子代理 metadata 是主 transcript 内联，还是 sidecar 丢失
7. 最近一次 compaction / snip 是否留下了可恢复边界

## 9. 适合沉淀到项目规则里的最小约束

适合写进项目 `CLAUDE.md` 的最小规则：

- 只持久化恢复真正需要的会话状态
- 会话正文、恢复元数据、子代理 sidecar 要分层
- worktree 恢复状态必须显式记录，不靠猜测
- resume 一致性必须有 checkpoint 或等价校验
- progress / loading 之类瞬时状态不进入恢复链

## 10. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/session-persistence.md`
- `skills/session-resume-governance/`
- `templates/project/session-metadata.example.yaml`

三者一起，才算把“别乱记 session”补全成“该如何正确持久化并恢复会话”。
