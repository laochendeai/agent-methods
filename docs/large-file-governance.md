# Large File / God File Governance 方法

很多仓库对超长文件的处理只有两种极端：

- 看到行数大就要求马上拆
- 只要还能跑，就继续往一个文件里堆

这两种都不对。

真实项目里，长文件至少分三类：

- 只是比较长，但职责仍然单一的文件
- 合理的长文件例外
- 已经变成 god file 的混合职责文件

Claude code 样本里能同时看到这三类信号：

- `src/utils/bash/bashParser.ts` 这类文件虽然很长，但职责非常窄，像 grammar / parser / binding 这样的核心实现，可以作为长文件例外
- `src/screens/REPL.tsx`、`src/cli/print.ts`、`src/utils/sessionStorage.ts`、`src/utils/hooks.ts` 这类文件则表现出高导入、高耦合、高变更面的 orchestration 特征，更接近需要治理的 god file
- `src/utils/settings/settings.ts` 虽然仍然偏长，但周边已经拆出 `constants.ts`、`changeDetector.ts`、`validation.ts`、`mdm/settings.ts` 等叶子模块，说明真正有用的方法不是“一刀切”，而是持续把边界从主文件里抽出去

这说明值得沉淀的不是“禁止大文件”，而是：

> 把超长单文件的预警阈值、例外条件、拆分信号、重构路径和验证方式做成治理规则。

## 1. 先区分 long file、legitimate exception 和 god file

### long file

只是文件偏长，但通常仍满足：

- 领域边界单一
- API 面窄
- 改动主要集中在同一种职责
- 对外依赖关系相对稳定

### legitimate exception

这类文件可能很长，但并不一定应该优先拆分，例如：

- 生成文件
- parser / grammar / AST 实现
- 平台绑定或移植代码
- schema、fixture、大型映射表
- 大量文案或消息构造，但对外暴露面仍然集中

这类文件的问题不在“长”，而在是否：

- 高 churn
- 高耦合
- 混入多层职责

### god file

这类文件才是治理重点，常见信号包括：

- UI、状态、副作用、数据获取、权限判断、导出接口混在一起
- import 数非常高
- 多个团队或多类需求长期都往这里堆
- 很难给它写局部验证
- 每次改一点点都要读一大片上下文

一句话：

> 行数只是预警信号，god file 的本质是职责堆积和边界塌缩。

## 2. 不要只看行数，要看四类信号

一个够用的 large-file governance，至少看这四类信号：

### 1. size signal

- 总行数
- 新增行数是否持续堆进同一文件

### 2. coupling signal

- import 数
- 依赖面是否跨多个层级
- 是否同时读写很多不同模块

### 3. responsibility signal

- 是否同时承担 UI、状态、effect、I/O、adapter、validation
- 是否既定义协议又执行业务又渲染界面

### 4. churn signal

- 高频改动是否长期集中
- 是否反复出现 merge conflict
- 是否每次需求都默认落到这个文件

一句话：

> 大文件不可怕，可怕的是 size、coupling、responsibility、churn 同时抬高。

## 3. 推荐的默认阈值梯子

不要假设所有项目共用同一个魔法数字，但可以先有一套默认阈值梯子：

### 0-800 行

- 默认正常区间
- 不因为行数本身触发治理

### 800-1500 行

- 进入 warning 区间
- review 时开始检查是否已经有职责混合
- 新功能不要再无脑追加

### 1500-3000 行

- 进入治理区间
- 需要明确写出：
  - 为什么暂时不拆
  - 或这次准备沿哪个边界抽出叶子模块

### 3000+ 行

- 进入 freeze-new-accretion 区间
- 默认不再继续把新能力直接堆进这个文件
- 除非满足：
  - 已登记为例外文件
  - 或本次改动同时附带拆分计划 / 拆分提交

这些阈值不是法律，而是推荐起点。

对于不同技术栈可以调整：

- 代码生成型项目，行数阈值可以更宽
- 强交互 UI 项目，职责阈值应比行数阈值更敏感
- 基础 parser / compiler / schema 项目，例外文件会更多

### CI hard gate pattern

如果项目已经进入持续交付阶段，large-file governance 不应只停留在
review 建议。推荐把阈值落成 CI gate：

1. 在项目内放置 `scripts/check_large_files.py`。
2. 在项目内放置 `.governance/large_file_policy.json`。
3. 在本地总检查脚本中调用 `python scripts/check_large_files.py`。
4. 在 GitHub Actions 中添加 `large-file-governance` job。
5. 在 branch protection 中把该 job 设为 required check。

如果仓库是私有仓库且没有 GitHub Pro，GitHub 不允许 required
checks / rulesets。此时推荐启用本地 fallback：

1. 在项目内放置 `.githooks/pre-commit` 和 `.githooks/pre-push`。
2. 在项目内放置 `scripts/install_git_hooks.sh`。
3. 执行 `bash scripts/install_git_hooks.sh`，把 `core.hooksPath` 指向 `.githooks`。
4. `pre-commit` 阶段拦截 large-file violation。
5. `pre-push` 阶段运行项目总检查脚本；没有总检查脚本时至少运行 large-file gate。

本地 hooks 可以被 `--no-verify` 绕过，所以它不是 GitHub required check
的完全替代品；它是无付费计划时的最低成本强提醒和本地阻断层。

默认硬规则：

- 非例外源码文件超过 `max_lines` 直接 fail。
- 现有超长文件只能通过 `legacy_files` 登记为 frozen baseline。
- legacy 文件当前行数不得超过 baseline。
- 调高 baseline 是治理例外，必须在 PR 中解释原因。

模板入口：

- `templates/project/scripts/check_large_files.py`
- `templates/project/scripts/install_git_hooks.sh`
- `templates/project/.governance/large_file_policy.example.json`
- `templates/project/.githooks/pre-commit`
- `templates/project/.githooks/pre-push`
- `templates/project/.github/workflows/large-file-governance.example.yml`

## 4. 合理例外必须显式登记

最常见的坏习惯是：

- 口头说“这个文件比较特殊”
- 但从未写下为什么特殊

更好的方法是给例外文件单独登记理由：

1. 例外类型是什么
2. 为什么不适合按普通业务文件拆分
3. 哪些边界仍然必须保持稳定
4. 哪些新增改动依然要受限

一个长文件即使被认定为例外，也不意味着可以无限增长。

例如：

- generated file：可以长，但不应手工堆业务逻辑
- parser / grammar file：可以长，但应保持窄职责，不要把 unrelated helper 塞进去
- big mapping / schema file：可以长，但不要顺手加运行时副作用

一句话：

> 例外的意思是“按例外治理”，不是“以后没人再管”。

## 5. 判断一个文件是否已经该拆的最强信号

如果出现下面几类情况，就不该再只看行数了：

1. 一个文件同时横跨三层以上职责
2. 新需求总是默认改这个文件
3. review 时需要在同一文件里来回跳多个上下文
4. 同一文件反复出现冲突和回归
5. 抽一个小改动也需要加载大量无关上下文
6. 测试只能走巨大的端到端路径，缺少叶子验证点

这些信号比“是不是 1200 行还是 1800 行”更重要。

## 6. 推荐的拆分边界

真正有效的拆分不是“随便切文件”，而是先找正确边界。

优先级通常是：

### 1. orchestration 和 leaf logic 分离

把主文件保留为编排层，先抽出去：

- helper
- adapter
- validation
- serialization
- permission / policy check
- small workflow step

这是最稳妥的第一刀。

### 2. UI / state / side effect 分离

如果是前端大文件，优先分开：

- render 组件
- state hooks
- data loading
- event handling
- side effects / bridge

### 3. protocol / types / constants 分离

不要把：

- types
- message schema
- constants
- helper enums

继续混在主流程文件里。

### 4. read path / write path 分离

很多大文件同时承担：

- 读取
- 计算
- 写回
- 同步状态

这时可以按读写路径拆开，而不是只按函数名字拆。

### 5. domain slice 分离

如果一个文件开始同时服务多个子域，就该按子域切，而不是按代码形式切。

## 7. 推荐的最小治理动作

不是所有大文件都要立刻做大型重构。

一个更实际的最小动作梯子是：

### level 1: 标记

- 把文件列入 large-file inventory
- 标注当前行数、职责类型、是否高 churn

### level 2: 限制继续增长

- review 里明确“本次不要再把新职责堆进去”
- 必要时要求先抽一个 leaf module

### level 3: 建拆分 issue

- 把文件拆分计划写成 issue
- 锁定边界、顺序和验证矩阵

### level 4: 分阶段拆

- 每次只抽一类职责
- 每次抽完就验证
- 不要搞一次性大爆破

一句话：

> large-file governance 的重点是阻止继续恶化，并为渐进式拆分创造条件。

## 8. 推荐的验证方式

拆分大文件时，最容易犯的错是：

- 只看文件变短了没有
- 不看行为是否回归

更合理的验证矩阵至少包括：

1. 主路径 smoke
2. 新抽出的 leaf module 单测或最小脚本验证
3. 原有入口是否仍然能工作
4. 共享依赖和导出接口是否未破坏

如果一次改动同时涉及：

- 文件拆分
- 新功能
- 接口变化

最好拆成多步提交，避免 review 和回归判断失焦。

## 9. 可选的自动化门禁

large-file governance 不一定要上自动化，但可以逐步增加：

### review checklist

- 文件是否已进入 warning / governance 区间
- 本次是否又在继续堆职责

### CI 脚本

- 报告超阈值文件清单
- 报告本次 PR 是否继续给超长文件加行

### doctor / status

- 展示仓库当前 large-file inventory
- 展示哪些文件已登记为例外
- 展示哪些文件已经超过 freeze-new-accretion 阈值

重点不是“自动拒绝一切”，而是让超长文件问题可见。

## 10. 推荐的最小规则片段

可直接改造成项目 `CLAUDE.md` 的最小规则：

- Line count is only a signal; treat god files as a boundary-collapse problem, not a formatting problem.
- Files over the warning threshold must be reviewed for mixed responsibilities and continued accretion.
- Files over the governance threshold must carry either an exception rationale or a split plan.
- Files over the freeze threshold should not receive unrelated new capabilities without extraction work.
- Generated, parser, schema, fixture, and binding files may be exceptions, but they still need explicit ownership and growth boundaries.

## 11. 推荐的最小检查清单

一个仓库准备补 large-file governance 时，至少先回答：

1. 当前最大的 10 个文件分别是什么？
2. 哪些只是长文件，哪些是合理例外，哪些已经是 god file？
3. 仓库要采用什么阈值梯子？
4. 哪些文件进入 3000+ 后默认禁止继续堆新能力？
5. 例外文件如何登记理由和边界？
6. 拆分时优先按哪种 seam 切？
7. 拆分后的验证矩阵是什么？
8. 是否要通过 review、CI 或 doctor 让这类风险持续可见？

本仓库提供可直接改造的清单模板：

- `templates/project/large-file-governance-checklist.md`

## 12. 设计规则

- 不要把 large-file 问题简化成“超过多少行就失败”
- 不要把所有长文件都视为同一种治理对象
- 不要允许 3000+ 的 god file 继续无声堆积新职责
- 不要为了拆分而拆分，先找职责边界再切
- 不要把文件变短当成唯一成功标准，行为验证同样重要

## 13. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/large-file-governance.md`
- `skills/large-file-governance/`
- `templates/project/large-file-governance-checklist.md`

这样以后再遇到“一个文件 2000 多行但没人知道该不该拆、为什么 parser 文件可以保留但 REPL 文件不能继续堆、为什么每次需求都落到同一个超级文件里、为什么文件拆短了却回归更多”时，就可以按同一套 large-file governance 方法处理。
