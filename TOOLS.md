# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.
# TOOLS.md - 本地工具与技能说明

## 快速索引
- [Config-Backup（配置自动备份）](#config-backup配置自动备份)
- [Config-Validator（配置验证+安全重启）](#config-validator配置验证安全重启)

---
（下面是各个技能的详细说明）

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Config-Backup（配置自动备份）
### 用途
在修改OpenClaw配置文件`openclaw.json`之前，自动执行强制备份，保证每次修改都有完整可追溯的备份记录，防止配置丢失或错误。

### 什么时候用
- 任何时候要修改`openclaw.json`
- 任何时候要编辑OpenClaw配置
- 任何时候提到「备份配置」、「保存配置」

### 怎么用
- 直接调用脚本：`~/bin/openclaw-config-backup backup`
- 备份完成后会返回备份文件路径

### 注意事项
- ⚠️ **必须先备份，才允许修改配置！**
- 备份文件会自动存到：`/Users/zhouyidan/planb/`
- 备份文件名带时间戳，永不覆盖历史备份

## Config-Validator（配置验证+安全重启）
### 用途
在重启OpenClaw网关之前，自动检查`openclaw.json`配置文件的语法是否正确、是否符合OpenClaw的schema要求，验证通过才允许执行重启，验证失败则阻止重启并报告问题。

### 什么时候用
- 任何时候要重启OpenClaw网关
- 任何时候要重启gateway
- 任何时候提到「重启网关」、「验证配置」

### 怎么用
- 安全重启（推荐）：`~/bin/openclaw-config-validator safe-restart`
  - 先验证配置，验证通过才重启
  - 验证失败则阻止重启，报告问题
- 只验证不重启：`~/bin/openclaw-config-validator validate`

### 注意事项
- ⚠️ **禁止直接使用 `openclaw gateway restart`！**
- ⚠️ **必须用 `~/bin/openclaw-config-validator safe-restart` 来重启网关！**
- 验证失败时，必须先修复配置或回滚到上一个备份

## GitHub-Sync（GitHub同步）
### 用途
将当前OpenClaw workspace同步到GitHub仓库，自动执行git add、commit、push操作。严格确保简历文件夹不会被推送到GitHub。

### 什么时候用
- 任何时候提到「同步GitHub」、「上传到GitHub」、「git push」、「推送代码」

### 怎么用
- 自动同步（推荐）：`~/bin/openclaw-github-sync sync`
  - 自动检查.gitignore，确保简历文件夹被忽略
  - 自动add、commit、push
- 只查看状态（不同步）：`~/bin/openclaw-github-sync status`

### 注意事项
- ⚠️ **永远不要将简历文件夹推送到GitHub！**
- 脚本会自动检查并确保简历文件夹在.gitignore中
- 如果简历文件夹不在.gitignore中，会自动添加并阻止推送
- GitHub仓库：`https://github.com/yidanzhou79-eng/openclaw-workspace.git`
## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.