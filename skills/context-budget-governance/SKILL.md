---
name: context-budget-governance
description: 把长上下文处理从“有个 /compact”升级成预算治理系统。Use when a repository needs compaction order, invariant protection, overflow recovery, or post-compact cleanup rules.
---

# Context Budget Governance

## Use When

- 仓库已经开始遇到长上下文问题
- 你需要定义 `snip` / `microcompact` / `compact` / `session memory` 的边界
- overflow 之后系统只会报错，不会恢复
- compact 后经常出现 plan、memory、tool pair 或缓存漂移
- 你想补一套预算梯子和 cleanup 规则

## Goal

把上下文压缩写成一套预算治理规则，而不是继续依赖零散的 compact 技巧。

## Workflow

### 1. 先定义预算梯子

- 列出从轻到重的预算处理顺序
- 先局部瘦身，再全局摘要

**Success criteria**:
- 已知道每个压缩层在什么时候接管

### 2. 先写不变量

- 标出绝不能被切断的边界：
  - tool pairs
  - plan
  - skills
  - memory
  - compact boundary

**Success criteria**:
- compact 不会在关键边界上靠猜测工作

### 3. 区分 summary 来源

- 判断什么时候可以用 `session memory compact`
- 判断什么时候必须回退到传统 compact

**Success criteria**:
- summary 来源有明确条件，不会空转或误用

### 4. 定义 overflow 恢复顺序

- 先走更便宜、保留更多细节的恢复手段
- 再走更重的 compact
- 最后才阻断或转人工

**Success criteria**:
- overflow 后不是单点报错，而是有编排好的恢复链

### 5. 加 circuit breaker

- 统计连续 compact 失败次数
- 达到上限后停止继续自动尝试

**Success criteria**:
- 系统不会在不可恢复状态下无限重试

### 6. 补 post-compact cleanup

- 清理失效缓存和 tracking
- 保留仍需跨 compact 延续的关键边界信息

**Success criteria**:
- compact 后状态收敛，而不是继续漂移

## Rules

- 不要一上来就 full compact
- 不要在不变量未定义前就实现预算裁剪
- 不要让 proactive compact 抢掉更合适的恢复路径
- 不要忽略连续失败的 circuit breaker
- 不要把 compact 结束当成 cleanup 的结束
