---
name: hook-gate
description: 设计 hook 门禁而不是临时提醒。Use when a repeated check has a stable lifecycle trigger and should be moved into hook configuration rather than staying as ad hoc chat guidance.
---

# Hook Gate

## Use When

- 你发现某个检查反复被人工提醒
- 某类工具调用前后总要补同样的门禁
- 你在判断一个检查该做成 hook、skill、rule 还是 CI
- 你需要给项目补一套最小 hook 策略

## Goal

把固定触发点上的重复检查升级成 hook 设计，而不是继续依赖聊天提醒或临时脚本。

## Workflow

### 1. 识别触发点

- 先明确这件事发生在：
  - 工具调用前
  - 工具调用后
  - 失败后
  - 会话开始/结束
  - 任务创建/子代理结束

**Success criteria**:
- 已明确 hook 应该挂在哪个生命周期点

### 2. 判断它是不是真的适合 hook

- 触发点稳定
- 输入边界清楚
- 结果能直接决定继续、阻止或告警
- 会重复出现

如果不满足这些条件，优先考虑 skill、rule 或 CI。

**Success criteria**:
- 已确认这是 hook 问题，而不是别的机制问题

### 3. 选择 hook 类型

- 便宜、确定的本地检查 -> `command`
- 轻量智能判断 -> `prompt`
- 外部审计/通知 -> `http`
- 独立 verifier -> `agent`

**Success criteria**:
- hook 类型和成本匹配，而不是默认上最重方案

### 4. 选择执行方式

- 必须拦住流程 -> 阻塞式
- 一次会话只需跑一次 -> `once`
- 不影响主流程 -> `async`
- 后台运行但失败要拉回前台 -> `asyncRewake`

**Success criteria**:
- 已明确 hook 的时机和阻塞语义

### 5. 输出最小配置骨架

- 写出 matcher
- 写出 hook 内容
- 写出失败时如何解释和修复

**Success criteria**:
- 项目里已经有可落地的 hook skeleton，而不是只有口头建议

## Rules

- 不要把大范围验证全塞进 hook
- 不要让 hook 长成第二套业务逻辑
- 不要为了“自动化”把所有提醒都改成 hook
- hook 失败必须可解释、可修复
