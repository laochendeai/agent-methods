---
name: method-extract
description: 分析外部代码库并提炼成自己的方法、规则、技能与 issue。Use when the user wants to study another project and convert its reusable engineering patterns into their own assets.
---

# Method Extract

## Use When

- 用户给了一个外部仓库或本地源码目录
- 用户想“学习其思想和方法”，不是直接复制业务实现
- 用户想把外部项目的强项变成自己的 skill、规范、路线图、issue

## Goal

把一个外部项目拆成“可迁移方法”和“不可直接照搬部分”，然后沉淀成你自己的资产。

## Workflow

### 1. 建立结构地图

- 先看目录、入口、关键模块、配置与文档
- 找出：入口、上下文、工具、技能、权限、hooks、任务、工作流

**Success criteria**:
- 已能说清这个项目真正的骨架

### 2. 抽取机制，不抄表面

- 区分“产品功能”与“代理运行时机制”
- 优先抽取会长期复用的机制

**Success criteria**:
- 已得到一组可复用的工程方法，而不是零散功能点

### 3. 过滤不可照搬部分

- 去掉与原作者平台、产品、商业、内部系统强绑定的部分
- 保留方法，不保留噪音

**Success criteria**:
- 已明确哪些能迁移，哪些不能

### 4. 变成自己的资产

- 输出分析文档
- 生成适合自己的 skill
- 形成项目规则模板
- 如需要，继续拆成 issue 路线图

**Success criteria**:
- 结果已落到自己的仓库或规则层，而不是停留在口头理解

## Rules

- 不要把“搬代码”误当成“继承方法”
- 不要复制超出自己当前阶段维护能力的复杂度
- 优先沉淀少而硬的流程
- 一切结论都要能回到源代码证据
