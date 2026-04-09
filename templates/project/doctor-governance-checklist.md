# Doctor Governance Checklist

这不是运行时实现文件，而是给项目设计 `doctor` / config repair / migration 流程时的最小清单。

## Diagnostic Coverage

先列出 doctor 要覆盖的问题面：

- installation / invocation health
- config validation
- plugin / connector / permission health
- context pressure
- legacy config and migration residue

## Severity Model

对每类问题先标：

- `warning`
- `error`

## Repair Mode

再标修复方式：

- `auto-fix`
- `manual-fix`

## Auto-Fix Guard

只有同时满足这些条件才放入 auto-fix：

- 修改目标明确
- 幂等
- 不覆盖用户有效意图
- 失败不会制造更糟的半迁移状态

## Migration Model

至少定义：

- current migration version
- applied migration version
- sync migrations
- async migrations
- retry policy

## Half-Migration Checks

逐项确认：

1. 是否先写新位置，再删旧位置
2. 是否会保留更晚的显式配置
3. 是否只有整组同步迁移成功后才 bump 版本
4. 失败后是否允许下一次重试
5. doctor 是否仍会报告残留旧字段

## Diagnostic Output

每条输出至少回答：

1. 问题是什么
2. 严重性是什么
3. 能不能自动修
4. 来源在哪
5. 下一步该做什么

## Repository Rule Snippet

可直接改造成项目 `CLAUDE.md` 里的最小规则：

- Doctor flows must separate severity from repair mode.
- Only idempotent, low-ambiguity fixes may run automatically.
- Config migrations must be versioned and ordered.
- Sync migration completion is recorded only after the full sync set succeeds.
- Async migrations may retry on later starts if they are non-blocking.
- Doctor output must explain residue, blockers, and the next repair step in user-facing terms.
