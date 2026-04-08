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

- 用 `context + memory + skills + hooks + permissions + worktree` 组织能力
- 用“可执行流程”替代“每次都重新解释”
- 用闭环交付替代一次性回答
- 用权限、验证、隔离来降低代理误操作成本

## 这个仓库里的第一批产物

- `docs/claude-code-analysis.md`
  对样本源码的结构化拆解

- `docs/adoption-blueprint.md`
  如何把这些方法变成你自己的长期工程方式

- `skills/issue-closed-loop/`
  以 issue 为中心完成分支、实现、验证、PR、合并、回到干净主分支

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
- 每个技能都要有清晰的完成标准，而不是泛泛建议
- 优先做能直接减少返工和回归的技能

## 推荐使用方式

1. 业务仓库保留项目专属 `CLAUDE.md`
2. 本仓库保留跨项目方法和技能
3. 重复三次以上的流程，升级成一个 skill
4. 新需求优先走 `issue -> branch -> verify -> PR -> merge -> sync main`
5. 改动后默认跑 `regression-guard` 思路，而不是只看改动点
6. 新项目初始化时，先判断仓库里是否已有 `CLAUDE.md`；有就用项目内规则，没有才回退模板
7. 如果要一次补齐新仓库骨架，直接用 `project-bootstrap-plus`
8. 一轮工作完成后，用 `repo-closeout` 做统一收尾
9. 一次版本发布完成前后，用 `release-closeout` 做发布收尾

## 新项目启动

以后新建项目时，不要机械地总是读模板。正确流程是：

1. 先检查仓库里是否已有 `CLAUDE.md`
2. 如果已有，就以项目内规则为准
3. 如果没有，再读取本仓库的通用方法和 `templates/CLAUDE.md`
4. 基于项目事实生成项目专属 `CLAUDE.md`

对应 skill：

- `new-project-bootstrap`
- `project-bootstrap-plus`

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
