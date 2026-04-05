---
name: release-closeout
description: 做一次通用的版本发布收尾。Use when a release build, tag, or distribution package is ready and the user wants a framework-style release closeout that checks version consistency, changelog/docs sync, artifact naming, release notes, rollback info, and post-release repository state without assuming a specific packaging stack.
---

# Release Closeout

## Use When

- 一个版本已经准备发布或刚完成发布
- 用户要“做发布收尾”
- 用户要检查 changelog、tag、release note、安装包命名是否一致
- 用户要确认发布后仓库和文档是否处于可继续协作状态

## Goal

用一套通用框架完成发布收尾，而不是假设所有项目都用同一种打包和发布方式。

## Scope

这个 skill 负责：

- 检查版本号、tag、release note、产物命名的一致性
- 检查 `CHANGELOG` / `README` / 下载说明 / 安装说明是否同步
- 检查发布产物是否有基本可识别性
- 汇总回滚信息、已知风险、发布后注意事项
- 检查发布后仓库是否需要回到干净主分支

这个 skill 不负责：

- 假设固定打包命令
- 假设固定发布平台
- 假设固定产物格式
- 编造未提供的发布信息

## Rule Priority

发布收尾时，优先读取项目自己的事实来源：

1. 当前项目仓库里的 `CLAUDE.md`
2. 当前项目仓库里的 `README.md` / `CHANGELOG.md` / 发布脚本 / installer 配置
3. 本 skill 的通用检查框架

## Workflow

### 1. 确认发布上下文

- 确认这次发布对应的版本号、分支、tag、目标渠道
- 明确产物格式，例如：
  - `zip`
  - `exe`
  - `msi`
  - Docker image
  - wheel
  - npm package
- 明确发布渠道，例如：
  - GitHub Release
  - 私有下载页
  - 商店
  - 对象存储

**Success criteria**:
- 已明确这次发布的版本身份和分发边界

### 2. 检查版本一致性

- 核对版本号是否在这些地方一致：
  - 代码版本文件
  - 安装包命名
  - tag
  - release title
  - `CHANGELOG`
- 若不一致，先列出差异再决定修正方式

**Success criteria**:
- 版本身份没有明显冲突

### 3. 检查发布说明与文档同步

- 看这些内容是否与本次发布一致：
  - `CHANGELOG`
  - `README`
  - 安装说明
  - 下载说明
  - 已知限制
- 如项目已有发布说明模板，可基于项目模板补全

**Success criteria**:
- 用户和下载者能看懂“这次发了什么、怎么用、有哪些限制”

### 4. 检查产物可识别性

- 核对产物名称、版本、平台、架构是否清晰
- 检查产物目录是否存在旧产物混淆
- 如果项目要求，还应确认：
  - 校验和
  - 签名/公证状态
  - 依赖打包是否齐全

**Success criteria**:
- 产物命名和分发信息足够明确，不会让用户拿错包

### 5. 汇总回滚与风险信息

- 记录这次发布至少应有的回滚线索：
  - 上一个稳定版本
  - 关键 tag / commit
  - 回滚方式入口
- 汇总已知风险、未解决问题、后续观察点

**Success criteria**:
- 发布后出了问题时，团队知道往哪里退

### 6. 检查发布后仓库状态

- 如果发布动作已完成，检查仓库是否需要：
  - 回到主分支
  - 推送 tag
  - 同步 release note
  - 清理一次性发布分支
- 如有需要，可建议再跑 `repo-closeout`

**Success criteria**:
- 发布后仓库不会停留在混乱状态

### 7. 输出发布收尾报告

- 明确：
  - 本次版本号
  - 发布渠道
  - 产物列表
  - 文档同步结果
  - 剩余风险
  - 回滚信息

**Success criteria**:
- 用户能一眼判断这次 release 是否真正收尾完成

## Rules

- 不要编造发布命令、tag、版本号、渠道
- 不要把项目特定流程写死成通用规则
- 如果项目没有 `CHANGELOG`，就明确指出，不要假装已同步
- 如果产物或发布说明不完整，优先报缺口，不要粉饰
- 收尾目标是“可发布、可分发、可回滚、可继续协作”

## Related Skills

- `repo-closeout`
- `issue-closed-loop`
- `runtime-restart-verify`
