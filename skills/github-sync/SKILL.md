---
name: github-sync
description: 将当前OpenClaw workspace同步到GitHub仓库，自动执行git add、commit、push操作。确保简历文件夹不会被推送到GitHub。触发关键词：同步GitHub、上传到GitHub、git push、推送代码
metadata:
  {
    "openclaw": {
      "always": true
    }
  }
---

# GitHub Sync Skill

## 功能
将当前OpenClaw workspace同步到GitHub仓库，自动执行git add、commit、push操作。严格确保简历文件夹不会被推送到GitHub。

## 使用场景
- 当你想要保存当前的workspace修改到GitHub时
- 当你完成了一些配置修改或技能开发，想要备份到GitHub时
- 当你提到「同步GitHub」、「上传到GitHub」、「git push」、「推送代码」时

## 使用方法
### 1. 自动同步（推荐）
```
/skill github-sync sync
```
或直接调用脚本：
```bash
~/bin/openclaw-github-sync sync
```

### 2. 只查看状态（不同步）
```
/skill github-sync status
```
或直接调用脚本：
```bash
~/bin/openclaw-github-sync status
```

## 核心规则
⚠️ **强制遵守：**
1. **永远不要将简历文件夹推送到GitHub！**
2. 同步前会自动检查`.gitignore`文件，确保简历文件夹在忽略列表中
3. 如果简历文件夹不在`.gitignore`中，会自动添加并阻止推送
4. 只同步workspace目录，不会同步其他OpenClaw配置文件（如`~/.openclaw/openclaw.json`）

## 同步流程
1. 检查当前目录是否是git仓库
2. 检查`.gitignore`文件，确保简历文件夹被忽略
3. 执行`git status`查看修改
4. 自动添加所有修改（除了被忽略的文件）
5. 自动commit（commit message带时间戳）
6. 自动push到远程仓库

## 脚本位置
- 脚本路径：`/Users/zhouyidan/.openclaw/workspace/skills/github-sync/scripts/github-sync.sh`
- 已安装到：`~/bin/openclaw-github-sync`

## GitHub仓库信息
- 仓库地址：`https://github.com/yidanzhou79-eng/openclaw-workspace.git`
- 本地路径：`/Users/zhouyidan/.openclaw/workspace/`
