---
name: large-file-governance
description: 把超长单文件、god file、例外文件和渐进式拆分路径做成正式治理规则。 Use when a repository keeps accumulating multi-thousand-line files, mixed-responsibility modules, or repeated PRs that keep adding logic to the same oversized file.
---

# Large File Governance

## Use When

- 仓库开始出现几百到几千行的超长文件
- 团队反复把新需求堆进同一个文件
- 你需要判断一个长文件是合理例外还是 god file
- 你准备拆分大文件，但不想做失控的大重构
- 你想为 review、CI 或 doctor 补一套 large-file 风险治理规则

## Goal

把“超长单文件何时需要治理、何时可以例外、如何渐进拆分”写成固定方法，而不是靠临场感觉。

## Workflow

### 1. 先做文件分型

- 区分 long file、legitimate exception、god file
- 不要只看行数

**Success criteria**:
- 仓库已经知道哪些文件是真问题，哪些只是长但合理

### 2. 盘点四类风险信号

- size
- coupling
- responsibility
- churn

**Success criteria**:
- 每个目标文件都能解释为什么进入治理区间

### 3. 定义阈值梯子

- warning threshold
- governance threshold
- freeze-new-accretion threshold

**Success criteria**:
- review 和后续自动化不再缺少统一判断线

### 4. 为例外文件登记理由

- generated
- parser / grammar
- schema / fixture
- binding / port

并写清：

- 为什么例外
- 允许增长到什么边界
- 哪些职责仍然不该混进去

**Success criteria**:
- 例外文件不是口头例外，而是有记录的例外

### 5. 选择拆分 seam

- orchestration vs leaf logic
- UI vs state vs side effect
- protocol / types / constants
- read path vs write path
- domain slice

**Success criteria**:
- 拆分不是机械切文件，而是沿真实边界切

### 6. 用渐进式动作收敛

- 先标记
- 再限制继续增长
- 再建拆分 issue
- 最后分阶段提取

**Success criteria**:
- 仓库先停止恶化，再渐进变好

### 7. 用验证兜底

- 主路径 smoke
- 叶子模块验证
- 导出接口检查
- 相邻回归检查

**Success criteria**:
- 文件变短的同时，行为也保持稳定

## Rules

- 不要把 line count 当成唯一标准
- 不要把所有长文件都强行拆掉
- 不要允许 3000+ 的 god file 继续无声堆新职责
- 不要一次性大爆破重构，优先做渐进式抽离
- 不要只看结构变短，不看行为回归
