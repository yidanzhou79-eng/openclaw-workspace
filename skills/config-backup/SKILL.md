---
name: config-backup
description: 在修改OpenClaw配置文件openclaw.json之前自动执行强制备份，保证每次修改都有完整可追溯的备份记录，防止配置丢失或错误。支持查看历史备份、一键回滚到任意备份版本、配置语法验证。触发关键词：备份配置、保存配置、备份openclaw、修改配置前备份
---

# Config Backup Skill

## 功能
在修改OpenClaw配置文件`openclaw.json`之前，自动执行强制备份，保证每次修改都有完整可追溯的备份记录，防止配置丢失或错误。

## 使用方法
### 1. 备份配置（修改配置前必须执行）
```
/skill config-backup backup
```
或直接调用脚本：
```bash
~/bin/openclaw-config-backup backup
```

### 2. 查看历史备份列表
```
/skill config-backup list
```

### 3. 回滚到指定备份
```
/skill config-backup rollback <备份时间戳/文件路径>
```

### 4. 验证当前配置语法
```
/skill config-backup validate
```

## 核心规则
1. **强制备份前置**：任何修改`openclaw.json`的操作必须先执行备份
2. **备份路径固定**：所有备份自动存放到 `/Users/zhouyidan/planb/` 目录
3. **备份文件名带时间戳**：格式为 `openclaw_config_backup_YYYY-MM-DD_HH:MM:SS.json`，永不覆盖历史备份
4. **备份校验**：备份完成后自动校验备份文件是否存在、大小是否正常
5. **配置语法校验**：修改完成后自动校验JSON语法是否正确
6. **回滚支持**：支持一键回滚到任意历史备份版本

## 脚本位置
- 脚本路径：`/Users/zhouyidan/.openclaw/workspace/skills/config-backup/scripts/config-backup.sh`
- 已安装到：`~/bin/openclaw-config-backup`
