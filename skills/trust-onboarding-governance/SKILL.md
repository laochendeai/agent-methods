---
name: trust-onboarding-governance
description: 把首次进入仓库时的 onboarding 与 trust gate 做成有状态、有风险披露、有记忆粒度且与后续 permission flow 分层的固定治理流程。 Use when a repository needs first-entry trust checks, project onboarding state, repo risk disclosure, or scoped trust memory.
---

# Trust Onboarding Governance

## Use When

- 仓库第一次进入时只有模糊提醒，没有正式 trust gate
- 你需要把 onboarding 和 trust 建成显式流程，而不是欢迎文案
- 你要盘点 hooks、MCP、bash、credential helper、危险 env 等首次披露项
- 你要定义 trust acceptance 的 session / project 记忆粒度
- 你要明确 trust gate 和后续 permission flow 的分层

## Goal

把“进入一个仓库之前如何建立基本信任关系”写成固定治理流程，而不是继续依赖一次性提醒。

## Workflow

### 1. 先拆清 onboarding 和 trust gate

- onboarding 关注项目是否准备好协作
- trust gate 关注这个目录是否值得信任并继续运行代理

**Success criteria**:
- 两层职责已经分开，不再混成一个欢迎弹窗

### 2. 把 onboarding 建成显式状态机

- 定义步骤
- 定义完成条件
- 定义启用条件
- 定义展示上限和完成标记

**Success criteria**:
- 系统能明确判断何时显示 onboarding、何时停止

### 3. 盘点首次进入仓库时的 capability surface

- hooks
- MCP servers
- bash permissions
- commands / skills / plugins 带来的 bash 执行
- credential helpers
- cloud auth helpers
- dangerous env vars

**Success criteria**:
- trust gate 的风险提示来自真实仓库能力，而不是泛化警告

### 4. 让风险提示带上来源

- 说明来自项目配置还是本地配置
- 说明哪些来源引入了高风险能力

**Success criteria**:
- 用户能回答“风险来自哪里”，而不只是“系统说有风险”

### 5. 设计 trust memory scope

- session scope
- project scope

并写清：

- 哪些目录只应 session 记忆
- 哪些项目应该持久化

**Success criteria**:
- trust 决策不会无边界扩散成全局永久信任

### 6. 定义 skip / reuse / retrigger

- 已接受时何时跳过
- 同一目录何时复用
- 进入新项目或风险面扩张时何时重新触发

**Success criteria**:
- trust gate 不会乱弹，也不会因为旧决策覆盖新风险

### 7. 保持与 permission flow 分层

- trust gate 只做仓库级初始信任
- permission flow 继续处理工具级授权、来源记录与持久化更新

**Success criteria**:
- 首次 trust 决策不会替代后续细粒度授权

## Rules

- 不要把 onboarding 和 trust gate 混成一个提示框
- 不要用抽象提醒替代 capability surface 披露
- 不要把 trust acceptance 做成全局永久信任
- 不要让 trust gate 替代具体 permission flow
- 不要丢失 approval source、持久化更新和审计信号
