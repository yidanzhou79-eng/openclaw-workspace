记录上一次 JSON 文件备份时间
记录每日 Git 推送状态

---

## 2026-04-08 新增安全规则（强制遵守）

### 1. 配置文件修改规则
⚠️ **任何时候修改 openclaw.json 前必须遵守：**
- 必须先调用 `~/bin/openclaw-config-backup backup` 自动备份配置
- 备份成功后才允许修改配置
- 修改完成后必须调用 `~/bin/openclaw-config-backup validate` 验证配置语法
- 验证通过后才可以重启网关

### 2. 网关重启规则
⚠️ **任何时候重启网关前必须遵守：**
- 必须先调用 `~/bin/openclaw-config-validator validate` 验证配置
- 验证通过后，必须使用 `~/bin/openclaw-config-validator safe-restart` 来安全重启
- **绝对禁止**直接使用 `openclaw gateway restart` 命令
- 验证失败时，必须阻止重启操作，报告具体问题并尝试修复或回滚

### 3. 新增技能
- config-backup：配置自动备份技能（修改配置前强制使用）
- config-validator：配置验证技能（重启网关前强制使用）
- 

### 4. 脚本使用说明
- 配置备份：`~/bin/openclaw-config-backup <backup|list|rollback|validate>`
- 配置验证+安全重启：`~/bin/openclaw-config-validator <validate|safe-restart>`
