# Context Budget Checklist

这不是运行时实现文件，而是给项目设计长上下文治理时的最小清单。

## Budget Ladder

先写清预算梯子顺序，例如：

1. tool result budget
2. snip
3. microcompact
4. collapse
5. autocompact
6. blocking / manual fallback

## Invariants

至少列出这些边界是否必须保留：

- tool_use / tool_result pairs
- plan boundary
- skill boundary
- memory boundary
- compact boundary

## Summary Sources

分别写清：

- 什么时候可以用 session memory summary
- 什么时候必须回退到传统 compact

## Overflow Recovery

逐项确认：

1. 最先尝试哪条恢复路径
2. 第二步走什么
3. 什么时候真正阻断

## Circuit Breaker

至少定义：

- consecutive compact failure limit
- trip 后如何处理

## Post-Compact Cleanup

分别列出：

- compact 后必须清理的缓存 / tracking
- compact 后必须保留的边界 / 状态

## Repository Rule Snippet

可直接改造成项目 `CLAUDE.md` 里的最小规则：

- Context handling must use an explicit budget ladder, not a single compact fallback.
- Critical execution invariants must be declared before any history pruning logic.
- Session memory is a distinct compaction layer, not a comment attached to compact.
- Overflow recovery must follow a fixed escalation order.
- Repeated compact failure must trip a circuit breaker.
- Post-compact cleanup must reset invalid state without deleting required continuity markers.
