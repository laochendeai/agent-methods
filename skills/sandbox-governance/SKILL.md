---
name: sandbox-governance
description: 把 sandbox 从单一开关提升成文件、网络、依赖、override 和 violation handling 的结构化限制系统。 Use when a repository needs sandbox restriction profiles, permission-to-sandbox conversion rules, or clearer managed-only and doctor boundaries.
---

# Sandbox Governance

## Use When

- 仓库准备引入或重构 sandbox / isolation 机制
- 你需要解释 permission rule 为什么没有按预期落成 sandbox 限制
- 你发现 path 语义在不同配置层不一致
- 你要定义 managed-only domain/path 限制
- 你要补 sandbox doctor、override 或 fallback 边界

## Goal

把 sandbox 写成可解释、可调试、可托管的 restriction profile，而不是继续停留在“开或关”的状态。

## Workflow

### 1. 先拆出限制维度

- 至少分清：
  - filesystem
  - network
  - dependency checks
  - override mode
  - violation handling

**Success criteria**:
- sandbox 的不同限制面已经能单独解释

### 2. 分离 rule 层和 runtime config 层

- permission rule 负责表达意图
- sandbox config 负责执行落地

**Success criteria**:
- 用户可理解策略和 runtime 真正执行配置之间的转换关系已被写清

### 3. 写清 path semantics

- 区分 permission-rule 风格路径
- 区分 sandbox.filesystem.* 风格路径

**Success criteria**:
- 不会再把同一个 `/path` 在不同层里解释成不同东西而无人知晓

### 4. 收紧 managed-only 边界

- 只把高信任放行项交给 managed policy
- 不要把所有细小设置都升级成 only-managed

**Success criteria**:
- 高风险放行项和普通项目配置差异已经分开治理

### 5. 定义 strict / fallback / lock

- strict sandbox mode
- unsandboxed fallback
- policy lock

**Success criteria**:
- 当前限制模式和是否允许降级都可被明确解释

### 6. 把 doctor 和 override 变成正式能力

- 依赖检查
- 平台支持性检查
- 安装提示
- override 入口
- debug / status 解释

**Success criteria**:
- sandbox 运行失败时不会只剩模糊报错

### 7. 输出最小模板和诊断问题

- 记录 restriction profile
- 记录 managed-only 项
- 记录 violation handling

**Success criteria**:
- 仓库已经有最小 sandbox policy，而不是散乱配置

## Rules

- 不要把 sandbox 退化成单一开关
- 不要把 permission rule 和 runtime config 混成一层
- 不要忽略 path semantics 差异
- 不要滥用 managed-only 限制
- 不要缺少 doctor、override 和 violation explainability
