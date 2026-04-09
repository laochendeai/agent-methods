---
name: managed-settings-governance
description: 把 settings source layering、managed settings、policy limits 和危险变更审批写成结构化治理规则。Use when a repository needs clearer config source precedence, managed policy boundaries, remote settings sync rules, or a checklist for dangerous managed changes.
---

# Managed Settings Governance

## Use When

- 仓库开始同时出现 user / project / local / flag / policy 多层配置
- 你需要解释“当前设置到底从哪里来”
- 你准备接入 managed settings、drop-ins 或远程托管配置
- 你需要区分 managed settings 和 policy limits
- 你要定义哪些托管变更必须先审批

## Goal

把 settings、托管策略、远程同步和危险变更审批写成明确的方法层，而不是继续依赖隐性覆盖关系。

## Workflow

### 1. 先列出所有 settings source

- 至少写清：
  - name
  - scope
  - writable
  - priority
  - delivery
  - trust level

**Success criteria**:
- 当前仓库已经能说清有哪些来源、哪些可写、哪些托管

### 2. 固定 source order

- 明确普通 settings 的低到高优先级
- 不要把覆盖顺序留给实现细节或用户猜测

**Success criteria**:
- 同一项设置冲突时，谁覆盖谁可以被稳定解释

### 3. 分离 managed authority 和普通 merge

- 普通 source 可按低到高 merge
- 托管 source 先决定 authority ladder，再判断是 single winner 还是 controlled merge

**Success criteria**:
- 托管来源不会被混成不可解释的半合并状态

### 4. 分开 managed settings 和 policy limits

- managed settings 负责下发配置值
- policy limits 负责禁用或限制能力

**Success criteria**:
- 项目不会把“设置值”和“功能边界”混在一个大对象里

### 5. 定义 remote sync 退化策略

- 写清 eligibility
- 写清 cache / polling / checksum
- 写清拉取失败时是否 fail-open

**Success criteria**:
- 远程托管抖动时，系统仍有可预测行为

### 6. 收敛危险变更审批边界

- 只在危险能力新增或变化时升级成审批事件
- 非交互环境不要设计成交互死锁

**Success criteria**:
- 危险托管变化会被显式处理，但普通更新不会制造噪音

### 7. 保证来源可解释

- 至少能回答：
  - effective settings 来自哪一层
  - 为什么当前层胜出
  - 托管设置来自远程、文件还是其它 authority

**Success criteria**:
- 用户和维护者能追溯当前配置的来源

## Rules

- 不要把 settings 当成单文件问题
- 不要把普通 merge 和托管 authority 选择混在一起
- 不要把 managed settings 和 policy limits 混层
- 不要把远程拉取失败和危险内容变化用同一种退化策略处理
- 不要让高风险托管变更在无声状态下直接生效
