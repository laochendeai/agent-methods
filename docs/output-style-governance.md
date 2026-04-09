# Output Style / Response Contract 方法

`output style` 最容易被误解成“再写一段 prompt 语气说明”。

但从 Claude code 的实现看，它其实更像一层长期可治理的 response contract：

- 可加载
- 可命名
- 可分来源
- 可覆盖
- 可被 plugin 强制绑定

如果没有这层治理，系统很容易退化成：

- style 只是散落在聊天里的临时提示词
- 用户、项目、插件彼此覆盖关系说不清
- plugin 依赖某种输出约束时，只能靠口头约定
- 后面想分析“系统现在为什么这样说话”几乎无从下手

真正值得迁移的不是某一种文风，而是这组原则：

> 把输出约束做成结构化资产，而不是一次性 prompt 文本。

## 1. 先把 output style 当成 response contract

在方法层，output style 不只是“更详细”或“更简洁”，它定义的是：

- 输出长什么样
- 是否保留某些核心默认指令
- 哪些场景必须套用某种响应约束
- 当多个来源都想定义风格时，谁优先

所以更准确的说法是：

> output style 是 response contract 的一种可配置实现。

## 2. 推荐的最小数据模型

一个够用的最小 style 模型至少应该包含：

- `name`
- `description`
- `prompt`
- `source`

如果你的系统需要更细治理，还可以加：

- `keep_coding_instructions`
  表示 style 激活时，是否仍保留某些核心执行指令
- `force_for_plugin`
  表示某个 plugin 启用时，是否必须强制套用该 style

一句话：

> style 不是只有正文，它至少还需要元数据和来源。

## 3. 来源分层必须明确

源码里能看到 output style 至少可能来自：

- built-in
- plugin
- user
- project
- policy / managed

如果不分来源，就永远说不清：

- 是谁把当前风格改掉了
- 用户能不能覆盖 plugin 默认风格
- 项目规则和个人偏好冲突时谁生效

### 推荐的默认分层

一个合理的默认顺序通常是：

1. built-in baseline
2. plugin-provided style
3. user style
4. project style
5. policy / managed style

具体高低可以按产品需要调整，但必须事先写清楚。

## 4. 命名规则要能表达来源

普通项目 / 用户 style 可以直接用简单名称，例如：

- `Concise`
- `Reviewer`
- `Explainer`

但 plugin style 更适合带命名空间，例如：

- `myplugin:review`
- `myplugin:ops`

这样做的好处是：

- 避免名字冲突
- 一眼看出是谁提供的
- 后续做强制绑定或诊断时更容易解释

一句话：

> 名字不只是展示，它还承担来源可见性。

## 5. 覆盖关系必须清楚

当多个来源同时定义同名 style 或当前 style 时，系统必须给出明确覆盖规则。

至少要回答：

1. built-in 能不能被用户覆盖？
2. project style 能不能压过 user style？
3. plugin style 是默认项，还是可被用户完全替换？
4. policy / managed style 是否拥有最终覆盖权？

如果这些规则不清楚，style 就不再是资产，而是隐性副作用。

## 6. `force-for-plugin` 什么时候才合理

`force-for-plugin` 这类绑定很强，所以不应被滥用。

更适合使用的场景：

- plugin 真的依赖某种固定输出契约
- 如果不用这套 style，plugin 的说明或交互会明显失真
- 这是 product-level 绑定，而不是作者个人审美

不适合的场景：

- 只是“我觉得这个 plugin 配这个文风更好看”
- 只是想覆盖用户个人偏好
- 多个 plugin 都想争当前 session 的唯一风格

一句话：

> `force-for-plugin` 应该保护功能契约，而不是强推审美偏好。

## 7. style 和任务指令不要混层

style 的职责是约束输出形态，而不是替代核心任务指令。

更合理的分工是：

- 核心执行规则继续放在系统或仓库规则层
- output style 只补充“如何表达”
- 某些 style 可以选择是否保留默认 coding instructions

不要把“怎么说”和“应该做什么”混在一个文件里无边界扩张。

## 8. style 应该能进入诊断和分析

源码里还有一个值得迁移的点：style 不只是渲染层设定，它还会进入 prompt category / query source 这样的分类。

这说明 style 最好具备：

- 可追踪性
- 可诊断性
- 可被日志或分析系统识别

至少要能回答：

- 当前用了哪个 style
- 它来自哪里
- 是用户选的、项目默认的，还是 plugin 强制的

## 9. 推荐的最小目录模型

如果仓库要引入自定义 style，更适合先给它们一个显式目录：

```text
output-styles/
  concise-response.md
  reviewer-mode.md
  myplugin-review.md
```

每个文件都应包含：

- frontmatter
- 简短描述
- 实际 prompt 内容

## 10. 推荐的最小模板

本仓库提供可直接改造的最小示例：

- `templates/project/output-styles/response-contract.example.md`

它的重点不是某种具体文风，而是说明：

- 一个 style 文件最少该长什么样
- frontmatter 该放哪些信息
- response contract 应该写在哪一层

## 11. 设计规则

- 把 style 当成 response contract，不要当临时 prompt 碎片
- 输出约束和任务指令分层管理
- 明确 built-in / plugin / user / project / policy 的覆盖顺序
- plugin style 尽量命名空间化
- `force-for-plugin` 只在功能契约依赖时使用
- 当前 style 应可被诊断、追踪和解释

## 12. 本仓库对应资产

本仓库为这项方法补齐的资产是：

- `docs/output-style-governance.md`
- `skills/output-style-governance/`
- `templates/project/output-styles/response-contract.example.md`

这样以后再遇到“为什么这个插件非要这样输出、为什么项目和个人风格打架、为什么 style 改动后行为也变了”时，就可以按同一套 response contract 方法来处理。
