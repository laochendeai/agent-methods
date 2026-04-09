# Managed Settings Checklist

这不是运行时实现文件，而是给项目设计 settings source layering、managed settings 和 policy limits 时的最小清单。

## Source Inventory

先列出所有来源，并逐项标注：

- source name
- scope
- writable or read-only
- priority
- delivery mode
- trust level

## Source Order

明确普通 settings 的低到高顺序，例如：

- `user`
- `project`
- `local`
- `flag`
- `policy`

## Managed Authority Ladder

不要只写“policy 优先级最高”，还要回答：

1. managed family 里是否采用 `first source wins`
2. 如果是，authority ladder 是什么
3. 哪些来源属于管理员可控
4. 哪些来源只是低信任兜底

## File-Based Managed Settings

如果项目使用 base file + drop-ins，逐项确认：

1. base file 是否只提供默认托管值
2. drop-ins 是否按稳定顺序加载
3. 后面的 drop-in 是否允许覆盖前面文件
4. 每个 drop-in 是否只负责一类 policy area

## Remote Sync Model

至少定义：

- eligibility rules
- cache path or cache strategy
- polling interval
- checksum / etag strategy
- startup loading barrier
- fetch failure fallback

## Managed Settings vs Policy Limits

逐项确认：

1. 哪些字段属于 settings values
2. 哪些规则属于 feature restrictions
3. policy limits 是否独立于 settings merge chain
4. 用户是否能解释当前限制来自哪一层

## Dangerous Change Approval

只有当托管变化穿透信任边界时，才升级成审批事件。至少确认：

1. 哪些设置被视为 dangerous
2. 危险项新增时是否必须审批
3. 危险项变化时是否必须审批
4. 非交互环境下如何避免等待式死锁
5. 用户拒绝后系统如何停止或回退

## Source Explainability

至少保证系统能回答：

1. 当前 effective settings 来自哪一层
2. 为什么是这一层胜出
3. 当前托管内容来自远程、文件还是其它 authority
4. 当前限制是设置值还是 policy limit

## Repository Rule Snippet

可直接改造成项目 `CLAUDE.md` 里的最小规则：

- Settings must be documented as an ordered source chain, not a single file.
- Managed authority selection must be separated from ordinary settings merge.
- Managed settings and policy limits must remain distinct layers.
- Remote settings fetch failures should use an explicit fallback strategy.
- Dangerous managed changes must not silently cross trust boundaries.
- Effective settings must remain explainable by source and priority.
