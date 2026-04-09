# Task / Multi-Agent Orchestration 方法

`issue-closed-loop` 解决的是“一个代理如何把一件事闭环做完”，但成熟的代理工程系统还需要第二层：

- 怎么把一件大事拆成 task
- 哪些 task 适合并行，哪些必须串行
- 多个 agent 怎么分工，谁对最终结果负责
- 并行时怎么避免所有人都“看起来在忙”，但没有人真正兜底

Claude code 这一层值得迁移的核心不是 swarm 本身，而是：

> 把任务板、运行态任务、队友身份、消息传递和最终验收责任分成了不同层，而不是混成“多开几个 agent 试试看”。

## 1. 先区分 3 个概念

### Issue

- 用户目标或需求闭环
- 对用户负责的交付单元

### Task

- 为推进 issue 而拆出的可跟踪工作项
- 应有 owner、状态、依赖关系

### Agent / Teammate

- 执行 task 的角色载体
- 可以是 leader、本地 worker、后台 worker、verifier

一句话：

> issue 是对外目标，task 是对内分工，agent 是执行者。

## 2. 任务编排里最重要的一个分层

源码里很值得迁移的一点是：**任务板状态** 和 **运行态状态** 不是一回事。

### 任务板状态

在 task list 层，状态是：

- `pending`
- `in_progress`
- `completed`

它回答的是：

- 这项工作有没有被认领
- 现在是否正在做
- 是否已经完成

### 运行态任务状态

在 runtime task 层，状态是：

- `pending`
- `running`
- `completed`
- `failed`
- `killed`

它回答的是：

- 这个后台执行单元当前有没有在跑
- 是正常结束、失败，还是被杀掉

这两个层级必须分开理解。

如果把它们混成一个状态机，会出现两个问题：

- 一个 task 明明仍属于 `in_progress`，但底层某个 worker 进程已经 `failed`
- 一个 worker 运行结束了，但 leader 还没做最终整合，任务却被误判为“完全完成”

## 3. 最小任务生命周期建议

对方法仓库来说，一个够用的最小模型应该包括两层：

### A. 协作层 Task

- `pending`
- `in_progress`
- `completed`

附带字段：

- `owner`
- `blocks`
- `blocked_by`
- `metadata`

### B. 执行层 Runtime Task

- `pending`
- `running`
- `completed`
- `failed`
- `killed`

附带字段：

- `task_id`
- `type`
- `description`
- `tool_use_id`
- `start_time`
- `end_time`
- `output_file`

建议把它理解成：

> task list 负责协调，runtime task 负责执行。

## 4. 前台任务和后台任务的边界

### 前台

- leader 当前正在推进的主线程工作
- 用户最终会直接看到的回答与整合
- 最终验收与收口

### 后台

- 本地 agent task
- remote agent task
- in-process teammate
- workflow / monitor 这类异步执行单元

后台任务的意义不是“替 leader 负责”，而是：

- 并行探索
- 并行实现
- 并行验证
- 异步观察或长时间运行

所以规则应该是：

> 可以后台执行，但不能后台决定最终完成。

## 5. Leader / Worker / Verifier 的职责边界

源码里明确有 leader、teammate、task ownership、message delivery 这些层。把它提炼成方法时，最重要的是职责分层。

### Leader

- 负责 issue 拆解
- 负责建 task list
- 负责分配 owner 与依赖
- 负责和用户交互
- 负责整合结果
- 负责最终验证与交付判断

Leader 可以自己做一部分实现，但不能把“最终完成责任”外包出去。

### Worker

- 负责认领 task
- 负责推进自己那一段具体工作
- 负责更新 task 状态
- 负责在阻塞时上报，而不是默默卡住

Worker 的目标是完成分段工作，不是直接向用户宣告整个 issue 已完成。

### Verifier

- 负责验证而不是扩 scope
- 负责检查实现是否真的满足完成条件
- 负责指出回归、依赖缺口、未覆盖路径

Verifier 可以是专门 agent，也可以由 leader 在最后一轮承担，但最终签字权仍应回到 leader。

一句话：

> worker 负责做，verifier 负责查，leader 负责兜底。

## 6. 依赖、认领、忙闲状态要显式

源码里 task 有：

- `owner`
- `blocks`
- `blockedBy`

team 里还有：

- idle / busy 状态
- 当前未完成任务列表

这背后的方法含义是：

- task 不只是待办标题，还要有依赖关系
- agent 是否空闲，不靠猜消息频率，而看它是否持有未完成任务
- 不能让一个 worker 同时持有一堆未完成任务再去并行扩散

推荐最小规则：

- 一个 worker 默认只持有一个主 task
- 有未解决 blocker 时不要强行 claim 下一个 task
- 依赖任务要用 `blocked_by` / `blocks` 显式表达

## 7. Idle 不是错误，静默才是错误

源码里很强调一件事：teammate 每轮结束后进入 idle 是正常现象。

正确理解是：

- idle 表示等待下一条输入
- 不表示 agent 崩了
- 不表示已经完成整个工作流

真正的问题不是 idle，而是：

- task 没有更新
- blocker 没有上报
- owner 和任务状态脱节

所以不要把“agent 暂时 idle”当作故障；应该把关注点放在 task ownership 和状态流转上。

## 8. 什么任务值得并行

更适合并行的任务：

- 写入范围明确分离
- 前后端、文档、验证、研究等天然分层
- 需要不同工具集或不同上下文窗口
- 可以先独立推进，再由 leader 汇总

典型例子：

- 一个 agent 查源码和方案，另一个 agent 改模板，leader 做整合
- 一个 worker 实现，另一个 verifier 跑回归
- 不同目录、不同模块、不同文件所有权的并行改动

## 9. 什么任务必须串行

应该保持串行的任务：

- 共享同一关键写入面
- 顺序本身就是正确性的前提
- 一步结果直接决定下一步边界
- 迁移、重构、发布这类强顺序过程

典型例子：

- 数据迁移脚本与回填逻辑
- 同一文件上的多处联动改动
- 需要先锁方案再实施的高耦合任务
- 最终整合、最终验证、最终对用户汇报

## 10. 单线程闭环和多代理闭环如何衔接

正确顺序不是“多代理替代 issue 闭环”，而是：

1. leader 先锁定 issue 范围
2. leader 把 issue 拆成 task
3. 能并行的部分交给 workers / verifier
4. 每个 task 回到明确 owner 和状态
5. leader 汇总结果
6. leader 做最终验证
7. 再按 issue-closed-loop 完成 commit / PR / merge / cleanup

也就是说：

> 多代理闭环是 issue 闭环的中间层，不是替代层。

## 11. 最小编排骨架建议

一个够用的最小骨架至少应包含：

- `issue_goal`
- `leader`
- `workers[]`
- `verifier`
- `task_board_statuses`
- `runtime_statuses`
- `claim_rules`
- `parallel_when`
- `serial_when`
- `done_gate`

示例：

```yaml
issue_goal: Add session persistence methods to the repo
leader:
  responsibilities:
    - define scope
    - assign tasks
    - integrate results
    - own final verification
workers:
  - name: doc-writer
    scope: docs and template changes
  - name: verifier
    scope: regression and acceptance checks
task_board_statuses:
  - pending
  - in_progress
  - completed
runtime_statuses:
  - pending
  - running
  - completed
  - failed
  - killed
claim_rules:
  - one active task per worker by default
  - blocked tasks cannot be claimed until blockers resolve
parallel_when:
  - write scopes are disjoint
  - one branch is implementation and another is verification
serial_when:
  - shared write surface
  - final integration
done_gate:
  - worker task completed
  - leader reviewed integration
  - final verification passed
```

## 12. 适合沉淀到项目规则里的最小约束

适合写进项目 `CLAUDE.md` 的最小规则：

- 并行前先拆 task，不要直接多人同时乱改
- task board 状态和 runtime 状态要分层
- leader 负责最终整合和验收
- worker 完成分段工作后必须更新状态或回报 blocker
- 验证可以委派，最终完成判断不能外包

## 13. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/task-orchestration.md`
- `skills/multi-agent-orchestration/`
- `templates/project/task-orchestration.example.yaml`

三者一起，才算把“多开几个 agent”升级成真正可维护的任务与多代理编排方法。
