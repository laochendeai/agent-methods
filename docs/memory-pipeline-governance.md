# Memory Extraction / Session Memory / Team Memory Sync 方法

当前仓库已经有 `memory-promote`，但那解决的是“什么值得沉淀成长期规则”，不是完整的记忆系统设计。

成熟代理系统里的 memory 不是一个抽象名词，而是一条分层管线：

- turn 结束后抽 durable memory
- session 内维护当前状态摘要
- team 级记忆在仓库范围内同步
- `MEMORY.md` 只做索引，不直接堆正文

如果没有这层分工，系统很容易退化成：

- 什么都往一个 memory 文件里塞
- session summary 和 durable memory 混在一起
- 共享记忆里混入敏感信息
- 索引越写越长，最后反而污染 prompt

Claude code 里真正值得迁移的，是这组原则：

> 记忆必须分层、分作用域、分写法、分安全边界，不能只靠“会不会记住东西”。

## 1. 先分清 3 个 memory 层级

### 1.1 Session Memory

- 服务当前会话
- 重点是“现在进行到哪里”
- 典型用途：
  - resume
  - compaction
  - away summary
  - 当前状态和错误修正记录

这层不追求长期知识库，而追求：

> 让下一次继续工作时能快速恢复当前任务状态。

### 1.2 Personal Durable Memory

- 服务当前用户 / 当前项目的长期可复用事实
- 来源通常是 turn 结束后的 memory extraction
- 重点是：
  - 角色
  - 偏好
  - 项目约定
  - 反复出现的反馈

这层不应该被 session 噪音污染。

### 1.3 Team Shared Memory

- 服务整个仓库协作面
- 重点是团队共识、共享流程、长期约束
- 必须假设它会被同步给其他协作者

所以它和个人 durable memory 最大的区别不是“谁能看见”，而是：

> 共享记忆必须有更严格的安全与写入边界。

## 2. durable extraction 应该在 turn 结束后抽取

源码里值得迁移的关键点是：durable memory 不是用户每次手动整理，而是 turn 结束后由后台 extraction 代理从最近消息中提炼。

这带来两个好处：

- 记忆不会完全依赖人工
- 只处理本轮新信息，不必每次重扫全量历史

更稳妥的原则是：

- 只看最近新增消息
- 优先更新已有 memory，而不是重复创建
- 只允许受限的工具集合
- 主代理已经自己写了 memory 时，本轮提取应跳过，避免重复

一句话：

> durable extraction 是“增量提炼”，不是“全量复写”。

## 3. `MEMORY.md` 应该是索引，不是正文仓库

源码里有一个特别值得迁移的约束：

- memory 内容写到独立 topic file
- `MEMORY.md` 只保留指向这些文件的短指针

这样做的原因很直接：

- `MEMORY.md` 会进入 prompt
- 它必须足够短
- 它应该帮助定位，而不是自己变成庞大正文

所以更合理的原则是：

- 一条 memory 一个文件
- `MEMORY.md` 每行一条短入口
- 保持 concise，避免超过 prompt 可承受预算
- 发现重复时优先更新原文件，不要继续堆索引

一句话：

> `MEMORY.md` 负责导航，不负责承载全部内容。

## 4. session memory 不是 durable memory 的副本

很多系统会误把 session memory 当成“长期记忆的另一个文件”。这会导致两个坏结果：

- 当前状态和长期知识混在一起
- compact / resume 时拿不到真正适合当前会话的摘要

更合理的设计是：

- session memory 单独维护
- 它有自己的结构和 token 预算
- 重点保留当前状态、最近结论、错误修正
- 超预算时要主动压缩 section，而不是无限增长

这说明：

> session memory 是运行时摘要层，不是长期记忆层。

## 5. team memory sync 是另一条共享管线

team memory 不只是“多一个目录”，而是一条带同步语义的共享管线。

它至少意味着：

- repo 级作用域
- fetch / push / version / checksum
- 冲突与重试
- 共享写入的安全约束

这层和个人 durable memory 的区别在于：

- 个人 memory 可以偏个人工作记忆
- team memory 必须更接近团队共识和共享规范

更稳妥的原则是：

- 团队记忆和个人记忆分目录
- 团队记忆有自己的 `MEMORY.md`
- 同步必须有版本或 checksum 概念，不能只靠“最后覆盖”

## 6. 为什么 team memory 必须有 secret guard

这是这条方法里最不能省的一点。

一旦 team memory 会同步给仓库协作者，就必须默认它属于共享面。

所以团队记忆写入前必须检查：

- API key
- 凭证
- token
- 任何不该同步给协作者的敏感内容

一句话：

> 共享记忆没有 secret guard，就不是协作能力，而是泄漏通道。

## 7. 推荐的最小目录模型

一个够用的最小模型可以长这样：

```text
memory/
  session/
    summary.md
  personal/
    MEMORY.md
    user_role.md
    project_feedback.md
  team/
    MEMORY.md
    testing_policy.md
    release_habits.md
```

分层原则：

- `session/` 放当前会话摘要
- `personal/` 放个人 durable memory
- `team/` 放共享 durable memory

不要把三者混进一个文件夹里靠文件名猜语义。

## 8. 推荐的最小写入原则

### 对 session memory

- 允许频繁更新
- 但必须受 section budget 和 total budget 约束

### 对 personal durable memory

- 基于新增消息抽取
- 语义化分 topic file
- 更新旧文件优先于创建重复文件

### 对 team memory

- 只写团队级、项目级、共享级事实
- 写入前过 secret guard
- 同步时带版本 / checksum / conflict 处理

## 9. 不该保存什么

不应进入 durable memory 的典型内容：

- 一次性排障噪音
- 临时失败信息
- 仍未验证的猜测
- 明显敏感的凭证或个人秘密
- 只服务当前 turn 的短期上下文

这类信息更适合留在 session 层，或者干脆不持久化。

## 10. 推荐的最小检查清单

一个仓库准备补 memory pipeline 时，至少检查：

1. session / personal / team 三层是否分开？
2. durable extraction 是不是增量触发？
3. `MEMORY.md` 是索引还是正文堆积区？
4. session summary 是否有 token 预算？
5. team memory 是否有 secret guard？
6. team sync 是否有 version / checksum / conflict 处理？

本仓库提供可直接改造的索引模板：

- `templates/project/memory-index.example.md`

## 11. 设计规则

- 不要把 session memory 和 durable memory 混为一谈
- 不要把 `MEMORY.md` 写成正文全集
- durable extraction 只处理新增信息，不要每轮全量重写
- team memory 一定要有 secret guard
- 共享记忆和个人记忆必须分目录、分作用域
- 有同步语义的 memory 一定要有版本或 checksum，而不是简单覆盖

## 12. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/memory-pipeline-governance.md`
- `skills/memory-pipeline-governance/`
- `templates/project/memory-index.example.md`

这样以后再遇到“什么该进 session、什么该进长期记忆、什么能同步给团队、为什么 `MEMORY.md` 越来越臃肿”时，就可以按同一套管线方法处理。
