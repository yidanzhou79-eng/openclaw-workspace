# Interview-Prep 技能使用指南

专业的面试准备系统，提供完整的面试流程模拟和个性化辅导。

## 🚀 快速开始

### 1. 初始化面试准备

```bash
cd /Users/zhouyidan/.openclaw/workspace-interview-prep/skills/interview-prep/scripts
python orchestrator.py new "Google" "Solution Engineer"
```

### 2. 开始模拟面试

```bash
python orchestrator.py simulate
# 或指定难度
python orchestrator.py simulate hard
```

### 3. 评估你的回答

```bash
python orchestrator.py evaluate "你的回答内容..."
```

## 📋 工作流程

### 阶段一：面经搜索和情报收集
- 自动初始化用户档案
- 展示面试情报（常见问题、流程、技巧等）
- 准备开始模拟面试

### 阶段二：模拟面试
- 智能生成问题（基于公司风格和你的弱项）
- 避免重复问题
- 提供提示和预期要点

### 阶段三：回答评估
- 多维度评分（技术准确性、深度、结构、批判性思维）
- 识别亮点和改进空间
- 追踪你的弱项
- 记录进步历史

## 🎯 难度选项

- `easy` - 入门级，适合刚开始准备
- `medium` - 标准难度（默认）
- `medium_hard` - 中等偏难
- `hard` - 高级难度
- `auto` - 自动根据你的表现调整（推荐）

## 📊 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 技术准确性 | 40% | 回答的正确性和专业性 |
| 回答深度 | 30% | 细节、例子、展开程度 |
| 逻辑结构 | 20% | 条理性、组织性 |
| 批判性思维 | 10% | 多角度分析、权衡讨论 |

## 💾 数据存储

所有数据都保存在 `INTERVIEW_DATA/` 目录下：

```
INTERVIEW_DATA/
├── users/yuki/
│   ├── profile.json           # 用户基本信息
│   ├── current_session.json   # 当前会话状态
│   ├── performance_history.json # 表现历史记录
│   └── weak_points.json       # 弱项追踪
├── interview_sessions/        # 面试会话（可选）
└── knowledge_base/            # 知识库（可选）
```

## 🔧 模块说明

### 1. orchestrator.py（流程编排器）
主入口，协调各个模块完成完整面试流程。

### 2. memory_manager.py（记忆管理器）
- 用户档案管理
- 会话状态追踪
- 弱项检测和记录
- 表现历史存储

### 3. question_generator.py（问题生成器）
- 基于弱项智能选题
- 公司风格个性化
- 避免重复问题
- 难度自动调整

### 4. answer_evaluator.py（回答评估器）
- 多维度评分
- 亮点识别
- 改进建议
- 批判性思维评估

## 📝 使用示例

### 完整示例流程

```bash
# 1. 开始新的面试准备
python orchestrator.py new "字节跳动" "产品经理"

# 2. 开始模拟面试（自动难度）
python orchestrator.py simulate

# 3. 评估回答
python orchestrator.py evaluate "我的回答是这样的..."

# 4. 继续下一题
python orchestrator.py simulate

# 5. 再评估
python orchestrator.py evaluate "第二个回答..."
```

### 测试各个模块

```bash
# 测试记忆管理器
python memory_manager.py

# 测试问题生成器
python question_generator.py

# 测试回答评估器
python answer_evaluator.py
```

## 🎨 特色功能

### 1. 智能弱项追踪
- 自动检测你的薄弱环节
- 优先针对弱项出题
- 记录进步趋势

### 2. 个性化问题
- 结合公司风格
- 针对岗位要求
- 避免重复问题

### 3. 建设性反馈
- 强调你的亮点
- 提供具体改进建议
- 鼓励持续进步

### 4. 完整历史记录
- 每次练习都有记录
- 可视化进步趋势
- 弱项解决追踪

## 💡 使用建议

1. **定期练习**：每天1-2道题，保持状态
2. **重点突破**：优先练习弱项领域
3. **认真对待反馈**：每条建议都要思考
4. **记录想法**：可以在回答后补充笔记
5. **模拟真实环境**：尽量在限时条件下回答

## 🔮 未来扩展

计划中的功能：
- [ ] 真实面经搜索集成
- [ ] 简历分析和优化建议
- [ ] 行业知识库
- [ ] 面试日程提醒
- [ ] 多语言支持

---

祝你面试顺利！🎯

*版本 1.0.0 | 最后更新: 2026-04-11*
