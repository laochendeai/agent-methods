# Agent Methods

一个面向公开协作的工程方法治理仓库。

这里不放业务代码，专门沉淀代理工程里的可复用方法、skills、模板和闭环流程，把零散经验变成可执行、可验证、可传播的工程系统。

欢迎通过 Issue 和 PR 一起参与这个仓库：

- 补充新的 skill、template 和治理流程
- 提炼外部优秀项目中值得迁移的方法论
- 修正文档里不清晰、不严谨、不可执行的规则
- 分享真实项目中的落地案例、回归问题和治理经验

这个仓库不放业务代码，只放三类东西：

1. `docs/`
分析外部源码后提炼出的可迁移方法论。

2. `skills/`
可安装到 `Codex` / `Claude Code` / `OpenClaw` 的技能目录。

3. `templates/`
给新仓库使用的 `CLAUDE.md`、`README`、`.gitignore`、issue/PR 模板和规则骨架。

## 核心判断

那个项目真正先进的地方，不是“模型更强”，而是把代理能力做成了工程系统：

- 用 `context + memory + skills + hooks + plugins/capability-packs + permissions + worktree` 组织能力
- 用“可执行流程”替代“每次都重新解释”
- 用闭环交付替代一次性回答
- 用权限、验证、隔离来降低代理误操作成本

## 这个仓库里的第一批产物

- `docs/claude-code-analysis.md`
  对样本源码的结构化拆解

- `docs/adoption-blueprint.md`
  如何把这些方法变成你自己的长期工程方式

- `docs/hook-gate.md`
  解释什么检查应该前移到 hook，什么应该继续留在 skill、rule 或 CI

- `docs/capability-pack.md`
  解释如何把 `skill / hook / MCP / template` 组织成可启停能力包，而不是散落成零碎开关

- `docs/permission-policy.md`
  解释如何把权限写成 `allow / ask / deny` 策略，并诊断危险宽规则与遮蔽冲突

- `docs/mcp-governance.md`
  解释如何给 `MCP` 连接器做来源分层、签名去重、channel 风险隔离和 capability gating

- `docs/doctor-migration-governance.md`
  解释如何设计 doctor、自诊断、config repair、migration version 和半迁移修复边界

- `docs/context-budget-governance.md`
  解释如何设计预算梯子、不变量保护、overflow 恢复和 post-compact cleanup

- `docs/memory-pipeline-governance.md`
  解释如何设计 durable extraction、session summary、team sync、`MEMORY.md` 索引和 secret guard

- `docs/output-style-governance.md`
  解释如何把 output style 做成有来源分层、覆盖关系和 plugin 绑定边界的 response contract

- `docs/managed-settings-governance.md`
  解释如何给 settings source、managed settings、remote policy sync 和 policy limits 设计清晰分层、覆盖和审批边界

- `docs/plan-worktree-mode.md`
  解释什么时候先进入 `plan mode`，什么时候需要 `worktree` 隔离，以及两者如何和 issue 闭环配合

- `docs/session-persistence.md`
  解释哪些会话状态应该被持久化、如何设计 lineage / worktree / subagent 恢复，以及怎样诊断 resume 一致性漂移

- `docs/task-orchestration.md`
  解释 task board 与 runtime task 的状态分层、leader/worker/verifier 职责，以及并行/串行的判断线

- `skills/capability-pack-design/`
  为跨 `skill / hook / MCP / template` 的能力设计 pack 边界、manifest 和启停规则

- `skills/hook-gate/`
  为重复门禁设计 hook 策略，而不是继续依赖临时提醒

- `skills/multi-agent-orchestration/`
  为并行代理协作设计 task、owner、依赖和最终验收边界

- `skills/session-resume-governance/`
  为长任务和多会话仓库设计 session persistence、lineage、worktree 和 subagent 恢复边界

- `skills/permission-policy/`
  为仓库补清晰的权限分层、危险模式约束和冲突诊断思路

- `skills/mcp-governance/`
  为仓库补连接器来源分层、去重优先级、channel 风险边界和 capability 暴露规则

- `skills/doctor-repair-governance/`
  为仓库补 doctor 覆盖面、warning/error 分层、auto-fix 边界和 migration version 规则

- `skills/context-budget-governance/`
  为仓库补长上下文预算梯子、不变量保护、overflow 恢复和 compact cleanup 规则

- `skills/memory-pipeline-governance/`
  为仓库补 session memory、durable extraction、team memory sync 和 `MEMORY.md` 索引规则

- `skills/output-style-governance/`
  为仓库补 output style 的数据模型、覆盖顺序、plugin 绑定和模板边界

- `skills/managed-settings-governance/`
  为仓库补 settings source layering、managed settings、policy limits、remote sync 和危险变更审批规则

- `skills/issue-closed-loop/`
  以 issue 为中心完成分支、实现、验证、PR、合并、回到干净主分支

- `skills/plan-mode-gate/`
  在复杂任务中先锁定范围、方案和验证，再进入实施

- `skills/worktree-isolation/`
  在高串扰或并行任务中使用 `worktree` 做目录隔离，而不是在脏工作区里硬做

- `skills/regression-guard/`
  在改动后优先排查连带故障和回归

- `skills/runtime-restart-verify/`
  安全重启本地程序并做基本可用性验证

- `skills/method-extract/`
  分析外部代码库并沉淀为你自己的方法、规范、技能、issue

- `skills/memory-promote/`
  把稳定规则沉淀到仓库规则，把临时噪音挡在外面

- `skills/new-project-bootstrap/`
  新项目初始化时，先判断仓库里是否已有 `CLAUDE.md`；没有才用模板生成第一版项目规则

- `skills/project-bootstrap-plus/`
  为新项目补齐 `CLAUDE.md`、`README`、`.gitignore`、issue/PR 模板与最小目录结构

- `skills/repo-closeout/`
  在一个阶段性工作完成后，对仓库做安全收尾：同步主分支、审视分支/worktree、检查文档漂移、识别临时噪音

- `skills/release-closeout/`
  在版本发布前后做通用收尾：检查版本一致性、文档同步、产物命名、风险和回滚信息

- `templates/CLAUDE.md`
  新项目可直接复用的规则层模板

- `templates/project/`
  新项目 starter kit：`README`、`.gitignore`、issue 模板、PR 模板

- `templates/project/capability-packs/`
  capability pack 示例骨架，便于新仓库先声明能力编组边界

- `templates/project/mcp-governance-checklist.md`
  新项目梳理 connector policy、allowlist、capability gate 的最小检查清单

- `templates/project/doctor-governance-checklist.md`
  新项目设计 doctor、自诊断、修复分流和 migration retry 的最小检查清单

- `templates/project/context-budget-checklist.md`
  新项目设计 long-context 预算梯子、compact 边界和 overflow 恢复的最小检查清单

- `templates/project/memory-index.example.md`
  新项目设计 `MEMORY.md` 索引时可直接改造的最小示例

- `templates/project/output-styles/response-contract.example.md`
  新项目设计 output style / response contract 时可直接改造的最小示例

- `templates/project/managed-settings-checklist.md`
  新项目设计 settings source layering、managed settings 和 policy limits 时可直接复用的最小检查清单

- `templates/project/session-metadata.example.yaml`
  会话持久化与恢复的最小元数据示例骨架

- `templates/project/task-orchestration.example.yaml`
  多代理任务编排的最小状态与职责骨架

- `templates/project/release-checklist.md`
  通用版本发布核对单

## 安装

安装到 Codex：

```bash
bash scripts/install_codex_skills.sh
```

安装到 Claude Code：

```bash
bash scripts/install_claude_skills.sh
```

安装到 OpenClaw：

```bash
bash scripts/install_openclaw_skills.sh
```

同时安装到三边：

```bash
bash scripts/install_all.sh
```

安装方式默认使用符号链接，所以这个仓库更新后，技能会随之更新。
`OpenClaw` 这边同样使用 `~/.openclaw/skills/<skill-name>` 的软链接方式。

## 规则优先级

以后统一按这个优先级理解：

1. 当前项目仓库里的 `CLAUDE.md`
2. `agent-methods` 里的通用 skills 和方法
3. `agent-methods/templates/CLAUDE.md` 只给“新项目且仓库里还没有 `CLAUDE.md`”时使用

也就是说：

- 现有项目：优先读项目自己的 `CLAUDE.md`
- 新项目且没有规则：再用模板生成第一版
- 通用闭环、回归、防串扰方法：始终由这个仓库提供

## 设计原则

- 把长期稳定的方法沉淀成技能，不靠临时聊天记忆
- 把项目规则留在项目仓库，把跨仓库方法放在这个仓库
- 技能只写“模型不知道但你长期需要它遵守的流程”
- 当一个能力跨越 `skill / hook / MCP / template` 时，用 capability pack 组织，而不是把启停散落在多个地方
- `MCP` 连接器要单独做来源分层、去重和 capability 暴露治理，不要只把它当成“多了几个工具”
- 升级、自诊断、config repair、migration residue 要单独治理，不要只靠报错时人工排障
- 长上下文治理要先定义 budget ladder、invariants、recovery 和 cleanup，不要只加一个 `/compact`
- 记忆要分层成 session / personal / team 三条管线，不要把所有内容都塞进一个 memory 文件
- output style 要做成结构化 response contract，不要只靠一次性 prompt 语气说明
- settings source、managed settings 和 policy limits 要分层治理，不要把所有配置都混成“最后谁覆盖谁不清楚”的一团
- 对长任务 / resume 型系统，单独定义 session persistence 和 lineage 边界，不要把恢复状态和聊天噪音混存
- 并行执行前先定义 task、owner、依赖和最终验收责任，不要直接多开 agent 硬推
- 每个技能都要有清晰的完成标准，而不是泛泛建议
- 优先做能直接减少返工和回归的技能

## 推荐使用方式

1. 业务仓库保留项目专属 `CLAUDE.md`
2. 本仓库保留跨项目方法和技能
3. 重复三次以上的流程，升级成一个 skill
4. 新需求优先走 `issue -> branch -> verify -> PR -> merge -> sync main`
5. 改动后默认跑 `regression-guard` 思路，而不是只看改动点
6. 非 trivial 任务先用 `plan-mode-gate` 锁定方案，再开始改实现
7. 固定触发点上的重复门禁，优先用 `hook-gate` 设计成 hook，而不是继续靠聊天提醒
8. 当一个能力需要 `skill + hook + MCP + template` 一起工作时，先定义 capability pack 边界
9. 权限不要只写“谨慎”，优先用 `permission-policy` 明确 `allow / ask / deny`
10. 引入新的外部 connector 前，先用 `mcp-governance` 明确来源优先级、去重规则和高风险 channel 边界
11. 仓库开始积累 legacy config、升级迁移或自检需求时，先用 `doctor-repair-governance` 定义 severity、repair mode 和 migration version
12. 长任务开始触顶或已出现 compact 漂移时，先用 `context-budget-governance` 定义预算梯子和 cleanup，再补具体实现
13. 要补长期记忆能力时，先用 `memory-pipeline-governance` 分清 session、durable、team 和 `MEMORY.md` 索引边界
14. 要补长期输出约束时，先用 `output-style-governance` 明确来源分层、覆盖关系和 plugin 绑定边界
15. 要补配置来源分层、managed settings 或 policy limits 时，先用 `managed-settings-governance` 明确 source order、托管优先级、fail-open 和危险变更审批边界
16. 当前工作区脏、任务易串扰、或需要并行时，用 `worktree-isolation`
17. 新项目初始化时，先判断仓库里是否已有 `CLAUDE.md`；有就用项目内规则，没有才回退模板
18. 如果要一次补齐新仓库骨架，直接用 `project-bootstrap-plus`
19. 一轮工作完成后，用 `repo-closeout` 做统一收尾
20. 一次版本发布完成前后，用 `release-closeout` 做发布收尾

## 新项目启动

以后新建项目时，不要机械地总是读模板。正确流程是：

1. 先检查仓库里是否已有 `CLAUDE.md`
2. 如果已有，就以项目内规则为准
3. 如果没有，再读取本仓库的通用方法和 `templates/CLAUDE.md`
4. 基于项目事实生成项目专属 `CLAUDE.md`

对应 skill：

- `new-project-bootstrap`
- `project-bootstrap-plus`

## 复杂任务执行

复杂任务不要直接在当前目录里一边探索一边改。推荐顺序是：

1. 先判断这是不是 non-trivial 任务
2. 如果是，先进入 `plan-mode-gate`
3. 方案锁定后，再判断是否需要目录隔离
4. 如果当前工作区有串扰风险，就进入 `worktree-isolation`
5. 在隔离目录里继续走 `issue-closed-loop`
6. 完成后用 `repo-closeout` 收尾

对应资产：

- `docs/plan-worktree-mode.md`
- `skills/plan-mode-gate/`
- `skills/worktree-isolation/`
- `skills/issue-closed-loop/`
- `skills/repo-closeout/`

## 项目收尾

一轮开发完成后，推荐顺序是：

1. 确认 issue / PR / merge 已完成
2. 回到并同步主分支
3. 审视陈旧分支和 worktree
4. 检查 `README` / `CLAUDE.md` 是否需要补同步
5. 识别并隔离临时噪音文件

对应 skill：

- `repo-closeout`

## 发布收尾

版本发布前后，推荐顺序是：

1. 确认版本号、tag、产物、渠道
2. 检查 `CHANGELOG` / `README` / 下载说明是否同步
3. 检查产物命名、平台、架构、可分发性
4. 汇总已知风险和回滚信息
5. 发布后如有需要，再跑一轮 `repo-closeout`

对应 skill：

- `release-closeout`
