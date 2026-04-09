---
name: permission-policy
description: 把权限从模糊提醒变成结构化规则。Use when a repository needs a clearer allow/ask/deny policy, explicit dangerous-pattern guidance, or diagnosis of permission rule conflicts.
---

# Permission Policy

## Use When

- 用户要补权限规则
- 你发现“谨慎执行”已经不够，必须写清 allow / ask / deny
- 某些高风险动作总在反复争议
- 你需要诊断权限规则冲突或遮蔽

## Goal

把权限策略写成清楚的规则层，让允许、询问、拒绝都有边界，并能解释为什么这样配置。

## Workflow

### 1. 先列动作，不要先写规则

- 把仓库常见动作按风险分成：
  - 只读低风险
  - 可恢复副作用
  - 高破坏性 / 高外溢性

**Success criteria**:
- 已有一份按风险分类的动作清单

### 2. 给每类动作分配行为

- 低风险 -> `allow`
- 中风险 -> `ask`
- 高风险 -> `deny`

如果某类动作难以统一，优先落到 `ask`，不要图省事直接全放开。

**Success criteria**:
- 规则行为和风险等级已经对齐

### 3. 排查危险宽规则

- 查找过宽的解释器、shell、eval、通配放行
- 优先移除或缩小它们

**Success criteria**:
- 不存在明显能绕过权限体系的大前缀 allow

### 4. 排查规则冲突

- 看具体 allow 是否被 ask/deny 覆盖
- 看规则来自哪一层
- 看哪些规则实际上永远不会生效

**Success criteria**:
- 权限问题不再只是“感觉不对”，而是能定位到具体遮蔽关系

### 5. 输出最小可复用策略

- 给出规则片段
- 给出危险反例
- 给出诊断思路

**Success criteria**:
- 项目已经有一份可以执行和维护的权限策略骨架

## Rules

- 不要把所有不确定动作都一股脑 deny
- 不要图方便写宽泛解释器 allow
- 权限策略必须能解释，而不只是“反正别乱动”
- 冲突规则要修，不要长期共存
