# Delivery Governance Capability Pack

这是一个示例 capability pack，用来演示如何把“安全 issue 交付”相关资产编组成一组可整体启停的能力。

## Purpose

让仓库在进入高自主开发阶段时，可以成组开启以下治理能力：

- issue 闭环
- 回归排查
- 仓库收尾
- hook 门禁
- 权限策略骨架

## When To Enable

- 仓库已经开始依赖代理持续推进 issue
- 需要把闭环、回归、权限、hook 一起纳入标准工作流
- 团队不想继续靠口头提醒维持交付纪律

## When Not To Enable

- 目前只需要临时试验单个 skill
- 仓库还没有稳定 runbook、验证命令、协作流程
- 你只是需要一个 MCP 连接或一个独立模板

## Components In This Example

- `issue-closed-loop`
- `regression-guard`
- `repo-closeout`
- `docs/plan-worktree-mode.md`
- `docs/hook-gate.md`
- `docs/permission-policy.md`
- `templates/CLAUDE.md`
- 项目级 hook / permission 示例模板

配套 manifest 见同目录下的 `capability-pack.example.yaml`。
