# Plugin Lifecycle / Marketplace / Dependency Governance 方法

很多仓库在引入 plugin 体系时，前几步通常都很顺：

- 能下载
- 能放到某个目录
- 能加载几个命令

但真正的问题会在后面集中爆发：

- 安装了不等于启用了，到底哪个状态才算“生效”
- plugin 依赖别的 plugin 时，缺依赖要怎么处理
- marketplace 之间能不能相互拉依赖
- 托管策略能不能直接封掉某个 plugin
- 自动更新、下架清理、启动降级该由谁负责

如果这些边界不先治理，plugin 很快就会从“扩展系统”退化成“带缓存目录的混乱附件”。

Claude code 真正值得迁移的，不是插件市场界面，而是这组原则：

> plugin 不是一次性扩展包，而是有安装、启用、加载、更新、降级和移除边界的长期运行时资产。

## 1. 先把 plugin 分成“安装状态”和“启用状态”

源码里一个特别值得学的点是：

> 安装状态和启用状态是两套不同的状态面。

更合理的默认分工是：

- `installed`
  表示 plugin 的内容已经落到磁盘或缓存里
- `enabled`
  表示当前仓库 / 当前范围想让它参与运行

这两个状态不要混成一个布尔值。

因为：

- 安装通常更偏全局资产管理
- 启用通常更偏当前仓库、当前范围或当前会话的运行选择

一句话：

> “plugin 在磁盘上”不等于“plugin 正在这个项目里工作”。

## 2. 推荐的最小生命周期模型

一个够用的 plugin lifecycle，至少要能区分这些阶段：

1. `available`
2. `installed`
3. `enabled`
4. `loaded`
5. `demoted`
6. `disabled`
7. `updated_pending_restart`
8. `removed`
9. `delisted_flagged`

可以这样理解：

- `available`
  marketplace 或本地来源里能找到
- `installed`
  已经进入本地安装/缓存系统
- `enabled`
  当前设置层明确要求它参与运行
- `loaded`
  本次启动真正成功加载
- `demoted`
  原本启用，但因依赖或完整性问题在本次会话被降级
- `disabled`
  设置层明确不启用
- `updated_pending_restart`
  新版本已在磁盘就绪，但当前进程仍跑旧版本
- `removed`
  用户主动卸载或关闭后清理完成
- `delisted_flagged`
  市场已下架，系统已自动处理并留下标记

## 3. manifest 和 marketplace manifest 不要混层

源码里专门处理了一个高频错误：

- 作者把 marketplace entry 的字段直接抄进 plugin manifest

这其实说明两者本来就不是一个东西。

更合理的分工是：

### plugin manifest

负责：

- plugin 自身元数据
- 命令、agent、skill、hook 等组件入口
- 依赖声明
- 本地目录结构约束

### marketplace manifest / entry

负责：

- source
- id
- category
- tags
- strictness
- 市场级分发信息

一句话：

> plugin manifest 负责“这个 plugin 是什么”，marketplace manifest 负责“这个 plugin 从哪里来、如何被分发和治理”。

## 4. validation 必须在 load 之前完成

plugin validation 不应只是“给开发者看的辅助工具”，它其实是生命周期治理的第一道门。

至少应覆盖：

- manifest schema
- 常见误配
- path traversal
- 目录基准误解
- marketplace-only 字段误放

值得继承的原则有两个：

### 严格反馈开发错误

- 作者输错字段
- 把 marketplace 字段放进 plugin manifest
- 依赖路径写成越界路径

这些都应该被指出。

### 运行时不要无声吞掉高风险结构问题

就算加载器本身为了韧性会 strip 一些未知字段，也不代表验证层应该装作没看见。

一句话：

> validation 的职责不是挑剔，而是尽早阻止错误元数据进入生命周期后半段。

## 5. dependency 不是 package graph，而是 presence guarantee

这点非常关键。

源码里把 dependency 讲得很清楚：

> Plugin A 依赖 Plugin B，不是说 A 要 import B 的代码，而是说 B 提供的 namespaced components 在 A 运行时必须可用。

这意味着 dependency 治理更像运行时 capability 依赖，而不是构建期包管理。

推荐最小规则：

- 依赖要能展开 transitive closure
- 安装期要做 cycle / not-found 检查
- 已经启用的依赖不应被重复写回
- root plugin 自己不能因为“已安装”就跳过必要注册

## 6. cross-marketplace dependency 默认应阻断

这是 plugin 安全边界里最应该明确写出来的一条：

> 一个 marketplace 里的 plugin，不应默认自动拉另一个 marketplace 里的依赖。

原因很直接：

- 用户信任了 marketplace A
- 不代表系统可以静默替他信任 marketplace B

更合理的默认线是：

- 默认阻断跨 marketplace 自动安装
- 允许 root marketplace 显式声明 allowlist
- 用户手动预装的跨市场依赖可以被视为显式信任
- 不要让 transitive dependency 无限传播信任

一句话：

> 跨市场依赖是 trust boundary，不是便利性优化。

## 7. load-time demotion 要作为正式状态，不要只报错

plugin 系统最怕的一类问题是：

- 设置里说启用
- 运行时实际缺依赖或条件不满足
- 结果系统既不真正加载，也不明确告诉用户发生了什么

Claude code 值得迁移的点在于，它把这类问题做成了 `verifyAndDemote`：

- 启动时检查 enabled set 是否满足依赖
- 不满足时做 fixed-point demotion
- demotion 只影响当前加载结果，不静默回写用户设置

这背后的方法是：

> 有些问题不该直接把设置改掉，而应先在运行期降级并把原因显式暴露出来。

这样做的好处：

- 保留用户原始意图
- 让 doctor / status 仍能解释问题
- 避免系统为了“自作聪明修复”反而改坏长期状态

## 8. policy block 和 user control 要分开

另一个容易混乱的地方，是把“用户禁用”和“组织策略封禁”混成同一种 disabled。

更合理的做法是：

- `disabled by user`
  表示用户或项目自己不想启用
- `blocked by policy`
  表示更高层 authority 根本不允许安装或启用

这两者的后果不同：

- 用户禁用可以之后自己再开
- policy block 应成为 install / enable / UI filter 的统一真相来源

一句话：

> policy block 不是 another toggle，它是更高信任层对生命周期的硬边界。

## 9. autoupdate 要和 restart semantics 一起设计

源码里另一个很重要的点是：

- marketplace 可以后台刷新
- plugin 可以后台更新
- 但更新不是 inplace 热替换
- 新版本落盘后，当前会话通常需要 restart 才真正生效

这说明 autoupdate 不能只回答“要不要更新”，还要回答：

- 更新在前台还是后台
- 更新失败是否阻断当前会话
- 更新完成后如何通知
- 当前会话和磁盘状态不一致时如何解释

更稳妥的默认原则：

- autoupdate 默认为后台、非阻断
- 磁盘更新成功后保留 `pending restart` 可见状态
- 不要伪装成“已经热更新完成”

## 10. delisted plugin cleanup 要单独治理

很多 plugin 系统只考虑“新增和更新”，很少考虑“市场已经撤下这个 plugin 以后怎么办”。

更成熟的做法是把它当成独立状态迁移：

- 检测 marketplace 已不再列出该 plugin
- 判断 marketplace 是否要求强制移除
- 只对用户可控范围执行自动卸载
- 对 managed-only 安装留给管理员处理
- 记录 flagged 状态，避免反复处理

一句话：

> 下架不是普通错误，它是生命周期里的正式退出路径。

## 11. startup reconciliation 不能缺

plugin 体系一旦复杂，就一定会出现这些分裂：

- settings 说 enabled
- 安装元数据却没有
- 磁盘缓存被清了
- 市场已经换了新版本
- 当前项目只应该看相关 installation

所以启动期至少要有一层 reconciliation，回答：

1. 当前哪些 plugin 真正 enabled？
2. 这些 enabled plugin 是否真的 installed？
3. 缺失的是否可以自动补装？
4. 当前项目应该只看哪些相关 installation？
5. 本次会话最终哪些 loaded、哪些 demoted、哪些 blocked？

不要把这些问题都推迟到用户第一次调用插件命令时才暴露。

## 12. 推荐的最小 checklist 资产

本仓库提供的最小模板是：

- `templates/project/plugin-governance-checklist.md`

它的重点不是复刻 plugin 市场结构，而是逼项目先回答：

- install 和 enable 是否分开建模
- manifest 和 marketplace manifest 是否分层
- dependency 是不是 presence guarantee
- cross-marketplace trust 默认如何处理
- demotion、policy block、autoupdate、delist cleanup 各自负责什么

## 13. 设计规则

- 把 plugin 当生命周期资产，不要当一次性扩展包
- 安装状态和启用状态必须分开
- plugin manifest 和 marketplace manifest 不要混层
- dependency 默认按 capability presence 处理，不按包管理思维硬套
- 跨 marketplace 依赖默认阻断，显式信任再放开
- load-time demotion 应保留用户意图，不要静默回写
- policy block、autoupdate、delist cleanup 各自都要有单独边界

## 14. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/plugin-lifecycle-governance.md`
- `skills/plugin-lifecycle-governance/`
- `templates/project/plugin-governance-checklist.md`

这样以后遇到“插件明明装了为什么项目里没生效、为什么跨市场依赖不能自动拉、为什么更新完还要重启、为什么市场下架后系统替我删了但又不是所有 scope 都删了”这类问题时，就可以按同一套 plugin lifecycle governance 方法来解释和收敛。
