---
name: runtime-restart-verify
description: 安全重启本地程序并做运行时验证。Use when the user asks to restart an app, check ports, preserve the required env, and confirm the key endpoints are alive.
---

# Runtime Restart Verify

## Use When

- 用户说“重启程序”
- 用户说“帮我启动一下，我要检查”
- 用户说“谁占用了端口”
- 用户需要确认某个本地服务是否按最新代码跑起来

## Goal

在不误伤其他进程的前提下，重启目标程序，并给出可验证的运行结果。

## Workflow

### 1. 确认当前进程和端口

- 先看目标端口是否已有监听
- 识别是不是当前项目进程，而不是盲目 kill
- 尽量读取已有进程的关键环境变量

**Success criteria**:
- 已确认要停掉的就是目标程序

### 2. 停掉旧进程

- 只停止明确属于该项目的进程
- 不顺手处理无关服务

**Success criteria**:
- 旧实例已停止，端口释放或即将被新实例接管

### 3. 用最新代码启动

- 使用仓库推荐入口
- 保留必要环境变量
- 如需数据库或配置前提，启动前先确认

**Success criteria**:
- 新实例成功启动，没有明显启动错误

### 4. 验证关键路径

- 检查监听端口
- 检查主页或核心接口
- 检查一个最关键的运行时状态接口

**Success criteria**:
- 有可重复的“服务已活着”的证据

### 5. 回报结果

- 告知地址、PID、端口、关键状态
- 如有残余问题，直接说明

**Success criteria**:
- 用户能立刻打开并继续检查

## Rules

- 不要杀未知来源进程
- 不要假设环境变量存在，尽量核实
- 如果后台启动不稳定，先前台观察失败点再切后台
- 报告时给出 URL、PID、端口、状态，而不是只说“好了”
