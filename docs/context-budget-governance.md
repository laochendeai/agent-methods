# Context Budget / Compaction / Collapse Governance 方法

很多系统提到“上下文太长就 compact 一下”，但真正难的不是有没有 `/compact`，而是如何把上下文预算治理成一套稳定机制。

如果没有这层，长任务通常会退化成几种坏状态：

- 该保留的不变量被错误裁断
- 自动 compact 和其他压缩机制互相抢活
- overflow 之后只会报错，不会恢复
- compact 之后缓存、plan、memory、skill 状态开始悄悄漂移

Claude code 里真正值得迁移的，不是某一个压缩函数，而是这组原则：

> 先治理预算，再治理摘要；先保护不变量，再压缩历史；先定义恢复顺序，再谈单点算法。

## 1. 先把问题定义成“预算治理”

这层方法处理的不是“消息太多”，而是：

- 哪些内容必须优先保留
- 哪些内容可以先瘦身
- 哪些内容必须改成 sidecar / attachment / summary
- 什么时候应该自动压缩
- 压缩失败后应该怎么恢复

所以不要把它叫成“compact 技巧”，更准确的说法是：

> 这是 context budget governance。

## 2. 预算梯子必须有顺序

成熟系统不会一上来就把整段历史总结成一条消息，而是按更细粒度的预算梯子逐层处理。

从源码里能看到的关键顺序是：

1. tool result budget
2. `snip`
3. `microcompact`
4. `context collapse`
5. `autocompact`
6. blocking / overflow recovery

这背后的方法是：

### 2.1 先限制“单条结果太大”

如果某个工具结果本身就过大，先做结果预算，不要让后面的 compact 替它收拾残局。

### 2.2 再做局部裁剪

`snip` 和 `microcompact` 的价值，不是“替代 compact”，而是：

- 尽量保留细粒度上下文
- 只先收缩最不值得保留的部分
- 延后整段历史摘要的时机

### 2.3 再做 collapse / autocompact

只有前面的细粒度手段不够时，才应该进入更重的上下文折叠或整段摘要。

一句话：

> 预算梯子应该从局部瘦身走向全局摘要，而不是反过来。

## 3. 不变量必须先定义，不能边压边猜

压缩上下文前，先明确哪些东西绝不能被错误切断。

至少包括：

- `tool_use / tool_result` 配对关系
- thinking / assistant trajectory 的完整边界
- plan 及其后续可恢复入口
- 已调用 skill 的关键信息
- memory / `CLAUDE.md` 注入边界
- compact boundary 本身

如果这些不变量没有先被定义，compact 就不再是“压缩”，而是在破坏执行链。

## 4. 为什么不能直接只靠一次 full compact

一次 full compact 最大的问题不是成本，而是信息损失和控制粗糙：

- 很容易把仍然高价值的近期上下文一起抹平
- 失去粒度后，恢复时只能依赖单条 summary
- 更难定位 compact 之后到底丢了什么

所以更稳妥的原则是：

- 先尽量保留近期原文
- 先用局部压缩减少浪费
- 只有必要时才做整段 compact

## 5. session memory compact 是单独层，不是 compact 的注释

源码里一个很重要的信号是：`session memory` 可以在符合条件时直接接管 compact。

这说明：

- `session memory` 不是附赠说明
- 它是一个正式的摘要来源
- 它可以替代传统 compact 的 summary 生成路径

更适合 `session memory compact` 的情况：

- 已有有效 session summary
- 已知哪些历史已经被概括
- 需要保留更少生成成本，同时维持更稳定的恢复点

不适合时，应回退到传统 compact，而不是硬用空 summary 顶上去。

## 6. overflow 恢复必须有固定顺序

当上下文真正撞到限制时，系统不应该只会抛 `prompt too long`。

更合理的恢复顺序应该先定义好，例如：

1. 先尝试最便宜、信息保留更多的恢复手段
2. 再尝试更重的 compact
3. 仍失败时再进入阻断或人工路径

源码里的关键思想是：

- 不要让 proactive compact 抢掉其他恢复路径
- 某些模式打开时，应让 collapse / reactive compact 先接管
- blocking preempt 不应过早把恢复通道堵死

一句话：

> overflow recovery 是一条编排链，不是单次 if/else。

## 7. circuit breaker 是预算治理的一部分

如果系统在明显不可恢复的上下文上，每轮都继续自动 compact，只会持续浪费 API 调用和时间。

所以预算治理还需要：

- 连续失败计数
- 失败上限
- 超过上限后停止重复尝试

这不是优化细节，而是治理底线。

## 8. compact 后必须做 cleanup

compact 结束不是终点，后面还要清理一批已经失效的缓存和 tracking state。

这层常被忽略，但实际很关键，因为 compact 后很多“压缩前状态”已经不再成立。

推荐至少清理：

- microcompact 相关状态
- 已失效的 memory / transcript cache
- classifier approvals / speculative checks
- 与 compact 前上下文强绑定的缓存

同时要明确哪些东西不该被清：

- 后续恢复仍需要的 skill 内容
- 仍需要跨 compact 延续的最小身份信息

一句话：

> compact 不只是生成 summary，还包含对旧状态的失效处理。

## 9. 推荐的最小预算治理模型

一个够用的最小模型可以写成这样：

```yaml
context_budget:
  ladder:
    - tool_result_budget
    - snip
    - microcompact
    - collapse
    - autocompact
  invariants:
    - tool_pairs
    - plan_boundary
    - skill_boundary
    - memory_boundary
    - compact_boundary
  recovery:
    first: cheapest_valid_recovery
    then: heavy_compact
    finally: block_and_prompt
  failures:
    consecutive_compact_failures_trip_breaker: 3
  cleanup:
    reset_invalid_caches: true
```

重点不是字段名，而是这几个概念必须存在：

- ladder
- invariants
- recovery order
- circuit breaker
- post-compact cleanup

## 10. 推荐的最小检查清单

一个仓库准备补长上下文治理时，至少检查：

1. 预算梯子顺序是否明确？
2. 哪些内容绝不能被切断？
3. `session memory compact` 何时可用，何时必须回退？
4. overflow 后先走哪条恢复路径？
5. 连续 compact 失败时何时停手？
6. compact 后哪些缓存要清，哪些状态必须保留？

本仓库提供可直接改造的清单模板：

- `templates/project/context-budget-checklist.md`

## 11. 设计规则

- 先定义预算梯子，再写单点 compact 算法
- 先保护不变量，再讨论压缩率
- overflow 恢复顺序必须固定，不要临时拼逻辑
- `session memory` 是正式 compaction layer，不是附属说明
- compact 失败要有 circuit breaker
- compact 后必须清掉失效状态，但不要误清仍需跨 turn 保留的边界信息

## 12. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/context-budget-governance.md`
- `skills/context-budget-governance/`
- `templates/project/context-budget-checklist.md`

这样以后再遇到“为什么历史越压越乱、为什么 overflow 后只会报错、为什么 compact 一次后状态开始漂”时，就可以按同一套治理框架处理。
