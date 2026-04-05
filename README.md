# Agent Methods

把 `/media/leo-cy/WORK/Claude code 源码` 里值得迁移的工程思想，沉淀成我自己的代理工程操作系统。

这个仓库不放业务代码，只放三类东西：

1. `docs/`
分析外部源码后提炼出的可迁移方法论。

2. `skills/`
可安装到 `Codex` / `Claude Code` 的技能目录。

3. `templates/`
给新仓库使用的 `CLAUDE.md` 模板和规则骨架。

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
  以 issue 为中心完成分支、实现、验证、PR、合并、回到干净 `master`

- `skills/regression-guard/`
  在改动后优先排查连带故障和回归

- `skills/runtime-restart-verify/`
  安全重启本地程序并做基本可用性验证

- `skills/method-extract/`
  分析外部代码库并沉淀为你自己的方法、规范、技能、issue

- `skills/memory-promote/`
  把稳定规则沉淀到仓库规则，把临时噪音挡在外面

- `templates/CLAUDE.md`
  新项目可直接复用的规则层模板

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

同时安装到两边：

```bash
bash scripts/install_all.sh
```

安装方式默认使用符号链接，所以这个仓库更新后，技能会随之更新。
`OpenClaw` 这边同样使用 `~/.openclaw/skills/<skill-name>` 的软链接方式。

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
4. 新需求优先走 `issue -> branch -> verify -> PR -> merge -> sync master`
5. 改动后默认跑 `regression-guard` 思路，而不是只看改动点
