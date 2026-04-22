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

## Hard Gate Bootstrap

如果项目要把规则变成 GitHub 强门禁，至少落地：

1. 复制 `templates/project/scripts/check_large_files.py` 到项目 `scripts/check_large_files.py`。
2. 复制 `templates/project/.governance/large_file_policy.example.json` 到项目 `.governance/large_file_policy.json`。
3. 删除示例 legacy 项，登记项目真实的超长 legacy 文件 baseline。
4. 将 `python scripts/check_large_files.py` 接入本地总检查脚本。
5. 复制或改造 `templates/project/.github/workflows/large-file-governance.example.yml`。
6. 在 GitHub branch protection 中把 `large-file-governance` 设为 required check。

如果私有仓库没有 GitHub Pro，不能配置 required check，则启用本地 fallback：

1. 复制 `templates/project/.githooks/pre-commit` 到项目 `.githooks/pre-commit`。
2. 复制 `templates/project/.githooks/pre-push` 到项目 `.githooks/pre-push`。
3. 复制 `templates/project/scripts/install_git_hooks.sh` 到项目 `scripts/install_git_hooks.sh`。
4. 执行 `bash scripts/install_git_hooks.sh`。
5. 确认 `git config --get core.hooksPath` 输出 `.githooks`。

限制：本地 hooks 可以被 `--no-verify` 绕过；如果仓库以后变为 public
或启用 GitHub Pro，仍应把 `large-file-governance` 配成 required check。

推荐硬规则：

- 新文件超过 `max_lines` 直接失败。
- legacy 文件只能保持在登记 baseline 以下或等于 baseline。
- 调高 baseline 必须在 PR 中说明为什么不能本次拆分。

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
- If CI enforcement is enabled, `scripts/check_large_files.py` and `.governance/large_file_policy.json` are the source of truth for line-count thresholds and frozen legacy baselines.
- If GitHub required checks are unavailable, install `.githooks` through `scripts/install_git_hooks.sh` as the no-cost local fallback.
