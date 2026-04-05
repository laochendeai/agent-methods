---
name: regression-guard
description: 在改动后优先排查回归和连带故障。Use when code changes may have broken adjacent paths, and the user wants a targeted regression sweep instead of a shallow summary.
---

# Regression Guard

## Use When

- 用户说“这里改了那里又坏了”
- 用户要求 review、回归排查、改完后再确认有没有连带故障
- 变更涉及运行时、页面、配置、入口、共享模块

## Goal

优先发现真实风险和行为回归，而不是先写总结。

## Workflow

### 1. 读取 diff 和影响面

- 看当前 diff、最近提交、受影响模块
- 列出直接影响和相邻影响

**Success criteria**:
- 已有一份简短但明确的影响面清单

### 2. 建验证矩阵

- 按“直接路径 / 相邻路径 / 共享依赖 / 启动路径”分组
- 为每组指定最小有效验证动作

**Success criteria**:
- 每个高风险点都有对应验证动作

### 3. 跑针对性验证

- 优先跑与变更最相关的测试、脚本、接口检查、页面 smoke
- 如果没有现成测试，就用最短路径做真实运行验证

**Success criteria**:
- 关键风险路径都有实际验证结果

### 4. 先报发现，再报总结

- 如果发现问题，按严重级别列出
- 如果没发现问题，也要说明残余风险和未覆盖部分

**Success criteria**:
- 输出以 finding 为核心，而不是以自我总结为核心

## Rules

- 不要只验证改动点本身
- 共享模块、入口路径、配置读写、页面事件绑定要额外警惕
- 发现问题时优先给复现路径和文件位置
- 如果用户明确要求 review，结果必须以问题清单优先
