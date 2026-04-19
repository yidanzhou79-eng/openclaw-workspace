---
name: config-validator
description: 在重启OpenClaw网关之前自动检查openclaw.json配置文件的语法是否正确、是否符合OpenClaw的schema要求，验证通过才允许执行重启，验证失败则阻止重启并报告问题。支持手动验证和安全重启。触发关键词：验证配置、检查配置、安全重启、重启网关前验证
---

# Config Validator Skill

## 功能
在重启OpenClaw网关之前，自动检查`openclaw.json`配置文件的语法是否正确、是否符合OpenClaw的schema要求，验证通过才允许执行重启，验证失败则阻止重启并报告问题。

## 使用方法
### 1. 手动验证配置
```
/skill config-validator validate
```
或直接调用脚本：
```bash
~/bin/openclaw-config-validator validate
```

### 2. 安全重启（推荐使用）
```
/skill config-validator safe-restart
```
或直接调用脚本：
```bash
~/bin/openclaw-config-validator safe-restart
```

## 核心规则
1. **必须检查前置**：任何重启网关的操作必须先执行配置验证
2. **验证通过才能重启**：只有JSON语法正确、符合schema要求才允许重启网关
3. **失败阻止重启**：验证失败则阻止重启操作，报告具体问题
4. **自动检查范围**：
   - JSON语法正确性
   - OpenClaw配置schema符合性
   - 必要字段完整性

## 脚本位置
- 脚本路径：`/Users/zhouyidan/.openclaw/workspace/skills/config-validator/scripts/config-validator.sh`
- 已安装到：`~/bin/openclaw-config-validator`
