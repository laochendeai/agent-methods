# Release Checklist

## Release Identity

- Version:
- Branch:
- Tag:
- Release channel:
- Artifact types:

## Pre-Release

- [ ] 版本号已在代码与文档中同步
- [ ] 关键验证已完成
- [ ] `CHANGELOG` 已更新
- [ ] 安装/下载说明已更新

## Artifacts

- [ ] 产物命名包含版本、平台、架构
- [ ] 产物目录没有混淆的旧文件
- [ ] 如需要，校验和/签名/公证信息已补齐

## Release Notes

- [ ] 这次发布做了什么
- [ ] 用户如何获取和安装
- [ ] 已知限制和风险
- [ ] 升级/迁移说明

## Rollback

- [ ] 上一个稳定版本已记录
- [ ] 回滚入口已记录
- [ ] 关键 tag / commit 已记录

## Post-Release

- [ ] 发布后仓库已回到可继续协作的状态
- [ ] 主分支已同步
- [ ] 如有必要，已执行 `repo-closeout`
