# Permission Policy Example

这不是运行时配置文件，而是给项目写第一版权限策略时的可复用骨架。

## Default Allow

默认允许低风险、只读、可快速回收的动作，例如：

- 读取文件
- 搜索文本
- 查看目录结构
- 查看日志
- 运行只读诊断命令

## Default Ask

默认询问会产生副作用、但不一定应该永远禁止的动作，例如：

- 修改实现文件
- 修改配置文件
- 安装或删除依赖
- 重启本地服务
- 提交代码
- 推送分支

## Default Deny

默认拒绝高破坏性或高外溢性动作，例如：

- 强推
- 破坏性删除
- 修改生产凭据
- 破坏性数据库操作
- 无边界执行解释器或 eval

## Dangerous Allow Patterns To Avoid

这些写法看起来省事，实际上会绕过权限边界：

- `Bash(*)`
- `Bash(python:*)`
- `Bash(node:*)`
- `PowerShell(*)`
- `PowerShell(iex:*)`

## Conflict Checklist

如果权限行为和预期不一致，先查：

1. 具体命中了哪条规则
2. 是否被更宽的 `deny` 遮蔽
3. 是否被更宽的 `ask` 遮蔽
4. 规则来自 CLI、项目规则，还是个人规则

## Repository Rule Snippet

可直接改造成项目 `CLAUDE.md` 里的最小规则：

- Low-risk read-only actions default to allow.
- Side-effecting but recoverable actions default to ask.
- Destructive or high-blast-radius actions default to deny.
- Broad interpreter allow rules are prohibited.
- Permission conflicts must be diagnosable by source and shadowing relationship.
