# Large File Governance Checklist

这不是运行时实现文件，而是给项目设计超长单文件治理、例外登记和渐进式拆分策略时的最小清单。

## File Inventory

至少列出：

1. 当前最大的 10 个源码文件
2. 每个文件的行数
3. 每个文件的大致职责
4. 每个文件最近是否高频改动

## File Classification

逐项确认每个目标文件属于：

- long file
- legitimate exception
- god file

并写清为什么。

## Threshold Ladder

至少定义：

- warning threshold
- governance threshold
- freeze-new-accretion threshold

并写清这些阈值是否按语言、目录或文件类型不同而调整。

## Exception Registry

如果某些大文件属于例外，至少写清：

1. 例外类型
2. 例外原因
3. 允许保留的边界
4. 明确不允许再混入什么职责

## Risk Signals

逐项确认目标文件是否存在：

- 高 import / 高 coupling
- 多层职责混合
- 高频冲突或高 churn
- 缺少局部验证点
- 新需求持续堆进同一文件

## Split Seams

至少选定优先 seam：

- orchestration vs leaf logic
- UI vs state vs side effect
- protocol / types / constants
- read path vs write path
- domain slice

## Growth Rules

至少写清：

1. warning 区间文件是否允许继续追加新职责
2. governance 区间文件是否必须附带 split plan 或 exception rationale
3. freeze 区间文件是否默认禁止无关新功能继续堆入

## Verification

至少保证：

- 主路径 smoke 仍然存在
- 被抽出的 leaf module 有最小验证
- 导出接口或调用路径未破坏
- 相邻路径做过回归检查

## Visibility

至少选择一种可见性路径：

- review checklist
- CI 报告
- doctor / status
- repo 文档中的 large-file inventory

## Repository Rule Snippet

可直接改造成项目 `CLAUDE.md` 的最小规则：

- Line count is only a signal; classify oversized files before deciding action.
- Oversized files must be distinguished between legitimate exceptions and mixed-responsibility god files.
- Files above the governance threshold need either an exception rationale or a split plan.
- Files above the freeze threshold should not keep receiving unrelated new capabilities.
- Large-file refactors must verify behavior, not just reduce line count.
