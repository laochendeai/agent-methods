---
name: plugin-lifecycle-governance
description: 把 plugin 的安装、启用、依赖、marketplace 信任、降级、自动更新和下架清理写成结构化生命周期治理。Use when a repository needs a plugin system, marketplace trust rules, dependency closure logic, or clearer plugin update/remove behavior.
---

# Plugin Lifecycle Governance

## Use When

- 仓库准备引入 plugin / extension / marketplace 体系
- 你需要区分 installed 和 enabled
- 你要设计 plugin dependency 和 cross-marketplace trust
- 你要定义 load-time demotion、policy block、autoupdate 或 delist cleanup
- 仓库里的 plugin 行为已经开始难以解释

## Goal

把 plugin 从“能装就行”的附件，升级成有清晰状态和边界的生命周期系统。

## Workflow

### 1. 先拆开安装状态和启用状态

- 明确：
  - installed
  - enabled
  - loaded
  - disabled / demoted / removed

**Success criteria**:
- 项目已经不再把“在磁盘上”和“当前正在生效”混为一谈

### 2. 固定 manifest 分层

- plugin manifest 只负责 plugin 自身元数据和组件入口
- marketplace manifest 负责分发、来源和市场级治理信息

**Success criteria**:
- manifest 职责边界清楚，不再互相抄字段

### 3. 定义 dependency 规则

- 先把 dependency 当 capability presence guarantee
- 定义 cycle、not-found、closure 和 reverse dependent 行为
- 默认阻断 cross-marketplace auto-install

**Success criteria**:
- 依赖展开和 trust boundary 都有明确规则

### 4. 设计 startup reconciliation 和 demotion

- 启动期检查 enabled / installed / loadable 是否一致
- 依赖不满足时进入 demotion，而不是静默失败

**Success criteria**:
- 用户可以知道 plugin 为什么没真正加载

### 5. 分开 user disable 和 policy block

- 用户禁用属于普通生命周期状态
- policy block 属于更高 trust layer 的硬边界

**Success criteria**:
- install / enable / UI filter 对 policy block 有统一解释

### 6. 定义 update 和 delist cleanup

- autoupdate 是否后台执行
- 更新后是否需要 restart
- 市场下架后是否自动清理
- 哪些 scope 可以自动卸载，哪些必须留给管理员

**Success criteria**:
- plugin 的退出和更新路径同样可解释

## Rules

- 不要把 installed 和 enabled 混成一个状态
- 不要把 plugin manifest 和 marketplace manifest 混层
- 不要默认允许跨 marketplace 自动拉依赖
- 不要因为 load 失败就静默忽略 demotion 原因
- 不要把 user disable 和 policy block 当同一种 toggle
- 不要只设计安装和更新，不设计下架与清理
