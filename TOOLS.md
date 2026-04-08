# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

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

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Resume-JD Matching Agent 配置说明

### 模型选择：
- **火山引擎 Doubao-Seedream-4.5**（当前配置）
  - 优点：多模态，理解能力强，擅长中文解析
  - 缺点：需要单独配置图像生成（如果有需要）

### Agent 能力设计：
1. **输入处理**：
   - JD（岗位描述）文本解析
   - 简历文本解析
   - 可选的简历附件（PDF/DOC）

2. **匹配度分析**：
   - 技能点对比
   - 经验年限匹配
   - 学历要求匹配
   - 软技能匹配
   - 行业背景匹配

3. **改进建议**：
   - 简历修改建议
   - 技能补充方向
   - 经验突出点优化
   - 格式和结构建议

### 可能需要的外部工具：
- 文件解析（PDF解析）
- 数据可视化（匹配度图表）
- 简历模板库