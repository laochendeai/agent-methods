# Managed Settings / Settings Source / Policy Limits Governance 方法

很多 agent runtime 最后都会走到这一步：

- 用户自己能改配置
- 项目仓库也想带一层共享配置
- 本地还要有 gitignored 覆盖
- 命令行启动参数又想临时改行为
- 管理员 / 平台 / 企业侧还想再压一层托管策略

如果没有单独治理，系统很快就会进入下面这种状态：

- 当前生效设置到底来自哪里，说不清
- 用户和项目到底谁覆盖谁，说不清
- 托管策略失败时该继续跑还是该阻断，说不清
- 危险的远程配置变化来了，系统要不要先征得同意，说不清

Claude code 真正值得迁移的，不是某个企业 API，而是这组原则：

> 设置来源、托管策略、远程同步和功能限制必须是可解释的治理层，而不是隐性副作用。

## 1. 先把 settings 看成“来源分层系统”，不是一个文件

最容易犯的错误，是把配置理解成“读一个 settings.json，再 merge 一下”。

更稳妥的理解是：

> settings 是一条明确的 source chain。

源码里已经体现出至少这些来源：

- `user`
- `project`
- `local`
- `flag`
- `policy / managed`

而且这些来源不是平行关系，它们有固定优先级。

如果仓库以后还会接 `plugin`、`built-in defaults` 或其它 baseline，也应该先把它们当作更低优先级基座，而不是和用户配置混在同一层。

## 2. 推荐的最小来源模型

一个够用的 settings source 模型，至少要记录：

- `name`
- `scope`
- `writable`
- `priority`
- `delivery`
- `trust_level`

可以这样理解：

- `name`
  这是哪一层，例如 `user`、`project`、`policy`
- `scope`
  作用到谁，例如全局、项目、当前启动
- `writable`
  用户是否能直接编辑
- `priority`
  与其它来源冲突时谁覆盖谁
- `delivery`
  配置是来自本地文件、drop-in、远程同步还是命令行
- `trust_level`
  这层是否被视为托管 authority

一句话：

> 只知道“配置来自某个文件”远远不够，你还要知道它是否可写、是否托管、是否高优先级。

## 3. 推荐的默认 source order

Claude code 的源码里，文件型 source 的低到高顺序是：

1. `user`
2. `project`
3. `local`
4. `flag`
5. `policy / managed`

这背后隐含了几个重要判断：

- `project` 应能覆盖 `user`
  因为仓库共享规则通常比个人默认更贴近当前项目
- `local` 应能覆盖 `project`
  因为本地 gitignored 覆盖适合处理临时机器差异
- `flag` 应能覆盖常规持久设置
  因为它表达的是当前启动的临时明确意图
- `policy / managed` 应拥有更高约束力
  因为它代表管理员或平台托管底线

推荐你把这条链明确写进文档或模板里，而不是留给用户猜。

## 4. 不要把所有 managed source 都 deep merge 在一起

这里最值得迁移的点，不是“managed settings 存在哪里”，而是：

> 托管 authority 和普通用户配置不是同一种 merge 问题。

普通来源常适合按低到高优先级 deep merge。

但托管来源更适合先定义一条 authority ladder，再决定是否采用：

- `first source wins`
- 或 `controlled merge`

Claude code 在 `policySettings` 上采用的是一种很明确的规则：

- 远程托管最高
- 再到管理员级本地托管
- 再到 file-based managed settings
- 再到更低级、用户可写的兜底位置

也就是说：

> policy family 先决定“哪一个 authority 生效”，再把胜出的那一层 merge 进总设置链。

这样做的好处是：

- 不会把多个托管 authority 混成半真半假的结果
- 更容易解释“为什么这项限制是当前值”
- 更容易避免管理员意图被更低信任来源偷偷稀释

## 5. managed settings 不只是一个文件

源码里能看到，file-based managed settings 至少包含两层：

- base file
- drop-in directory

而 drop-ins 不是随便扫一遍就结束，它们通常需要：

- 独立文件存在
- 固定排序
- 后者覆盖前者

这背后的方法很清楚：

> 托管配置应允许按片段独立投放，而不是要求所有团队共同改一个总文件。

推荐默认规则：

- base file 提供默认托管值
- drop-ins 按稳定顺序叠加
- 每个 drop-in 应只负责一个相对清楚的 policy area

## 6. remote managed settings 和 policy limits 不是一回事

这是最容易混层的地方之一。

更合理的分工是：

### remote managed settings

负责：

- 下发正式 settings 值
- 进入总设置链
- 影响真实运行配置

### policy limits

负责：

- 表达组织级功能限制
- 禁用某类能力
- 决定哪些功能根本不应开放

一句话：

> managed settings 更像“配置值下发”，policy limits 更像“功能边界约束”。

不要把两者混成一个巨大的“企业配置对象”。

## 7. fail-open 和 blocking approval 要分两类问题

源码里最值得继承的，不是“远程失败了就都继续跑”，而是更细的判断：

### 传输 / 可用性问题

例如：

- 网络失败
- 重试耗尽
- 轮询暂时拿不到新内容
- 当前用户不具备远程托管资格

这类问题更适合：

- `fail-open`
- 使用缓存或旧值
- 不要因为远程托管系统暂时抖动就把主流程全部拖死

### 内容 / 风险升级问题

例如：

- 新的托管设置引入了危险能力
- 危险项与旧缓存相比发生了变化
- 这种变化会显著改变执行边界

这类问题更适合：

- 显式审批
- 交互式环境下展示 blocking confirmation
- 用户拒绝时停止继续

一句话：

> 远程拉取失败是可用性问题；危险配置变化是信任边界问题。两者不要用同一套退化规则。

## 8. 危险托管变更何时必须显式审批

更合理的触发线通常是：

- 这次变更引入了危险设置
- 或者危险设置相对上一次已知状态发生了变化
- 且当前环境可以进行交互确认

如果只是普通托管值变化，不要对所有更新都弹确认。

如果是非交互环境，也不要设计成“永远等用户点确认”，否则系统只会卡死。此时应事先定义：

- 继续沿用缓存
- 跳过危险变更
- 或直接按更高层平台策略拒绝启动

重点不是某一种具体 UI，而是这条原则：

> 只有当托管变更穿透了执行信任边界时，才把它升级成审批事件。

## 9. remote sync 要有 eligibility、cache、polling 和 checksum

如果系统要接远程托管设置，最小治理面通常应包含：

- `eligibility`
  哪些用户、provider、部署模式应该参与远程托管
- `cache`
  上一次成功结果如何保存与回退
- `polling`
  后台多久刷新一次
- `checksum / etag`
  如何判断内容是否真的变化
- `loading barrier`
  其它系统是否需要等待远程托管先完成首次加载

一句话：

> 远程托管不是“请求一下 API”，而是带资格判断、缓存、变化探测和等待语义的正式子系统。

## 10. 来源可解释性必须是一等能力

settings 治理做得再复杂，如果用户最后还是回答不了下面这些问题，这套系统就不算真正可治理：

1. 当前生效设置来自哪一层？
2. 这一层为什么比另一层优先？
3. 这是用户自己改的、项目默认的，还是托管策略压下来的？
4. 当前托管设置来自远程、管理员本地还是 drop-in？

所以建议至少保留：

- source display name
- source order
- 每层是否有内容
- 当前 effective settings 的 per-source 展开能力

不要把 provenance 只留在 debug 日志里。

## 11. 推荐的最小 checklist 资产

本仓库提供的最小模板是：

- `templates/project/managed-settings-checklist.md`

它的重点不是列举所有具体字段，而是逼项目先回答：

- source order 是什么
- 哪些层可写，哪些层只读
- managed family 是 merge 还是 single authority
- remote failure 如何退化
- 危险变更何时需要审批
- 用户怎样看见当前设置的来源

## 12. 设计规则

- 把 settings 当来源分层系统，不要当单文件
- 普通 source merge 和托管 authority 选择要分开设计
- managed settings 与 policy limits 分层治理，不要混层
- 远程托管的传输失败和危险内容变化要分开处理
- 只有穿透信任边界的托管变化才升级成审批事件
- effective settings 必须可追踪到来源

## 13. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/managed-settings-governance.md`
- `skills/managed-settings-governance/`
- `templates/project/managed-settings-checklist.md`

这样以后遇到“为什么同一个设置在不同机器不一样、为什么命令行参数没压过托管策略、为什么远程托管挂了但系统还在继续、为什么某次策略更新必须先确认”这类问题时，就可以按同一套 settings governance 方法来解释和收敛。
