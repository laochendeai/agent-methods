---
name: doctor-repair-governance
description: 把升级、自诊断、配置修复和迁移残留治理正式化。Use when a repository needs a doctor flow, config repair policy, migration versioning, or clearer auto-fix vs manual-fix boundaries.
---

# Doctor Repair Governance

## Use When

- 用户在升级后遇到配置或启动异常
- 仓库想补一套 `doctor` / self-check 流程
- 你需要定义哪些问题可以 auto-fix，哪些必须 manual-fix
- 你准备引入或重构配置迁移逻辑
- 系统已经开始出现 legacy key、半迁移残留、重复告警

## Goal

把诊断、修复、迁移写成明确的方法层，而不是继续让用户在报错堆里猜。

## Workflow

### 1. 先盘点诊断面

- 列出：
  - 安装 / 入口健康
  - 配置合法性
  - 权限 / plugin / connector 健康
  - 上下文压力
  - 迁移残留

**Success criteria**:
- 已知道 doctor 到底要覆盖哪些问题面

### 2. 分离严重性和修复方式

- 先判断 `warning` 还是 `error`
- 再判断 `auto-fix` 还是 `manual-fix`

不要把两者混成一句模糊提示。

**Success criteria**:
- 每类问题都知道有多严重、由谁修

### 3. 收敛 auto-fix 范围

- 只保留幂等、低歧义、低副作用修复
- 会覆盖用户意图或需要授权的项，转成 manual-fix

**Success criteria**:
- auto-fix 不会为了“方便”把系统推入更糟状态

### 4. 给迁移加版本和顺序

- 为同步迁移维护版本号
- 明确同步组和异步组
- 只有同步组完整成功后才 bump 版本

**Success criteria**:
- 迁移不是零散脚本，而是可追踪的版本化流程

### 5. 处理半迁移残留

- 先写新位置，再删旧位置
- 保留已有有效意图
- 失败时允许下一次重试
- doctor 持续暴露剩余残留

**Success criteria**:
- legacy key 和半迁移状态不会长期无声漂移

### 6. 输出用户可执行的诊断结果

- 每条结果至少说明：
  - issue
  - severity
  - repair mode
  - source
  - next step

**Success criteria**:
- 用户看到 doctor 输出后知道现在该做什么

## Rules

- 不要把 warning / error 和 auto-fix / manual-fix 混成一个维度
- 不要对高歧义配置做静默 auto-fix
- 不要在同步迁移完成前提前标记版本完成
- 不要因为有迁移逻辑就取消 doctor 对残留状态的可见性
- retry 逻辑必须明确，不要让失败迁移永远沉没
