#!/usr/bin/env python3
"""
测试改进后的问题生成器 - 使用面经情报
"""

import sys
sys.path.insert(0, '/Users/zhouyidan/.openclaw/workspace/skills/interview-prep/scripts')

from question_generator import QuestionGenerator

print("=" * 60)
print("🧪 测试改进后的问题生成器 - 面经情报功能")
print("=" * 60)

qg = QuestionGenerator()

# 模拟从搜索获取的面经情报
test_intelligence = {
    "common_questions": [
        "自我介绍一下",
        "为什么想加入Google？",
        "你对Solution Engineer岗位有什么理解？",
        "谈谈你最有成就感的项目经历",
        "描述一次你解决复杂技术问题的经历",
        "你如何与客户沟通技术问题？",
        "谈谈你对云计算的理解"
    ],
    "difficult_topics": [
        "系统设计",
        "技术深度",
        "客户沟通"
    ],
    "hot_topics": [
        "AI应用",
        "微服务架构",
        "Kubernetes"
    ],
    "company_style": "Google注重技术能力和创新思维"
}

test_weak_points = ["系统设计时容易忽略可扩展性考虑"]

print(f"\n🎯 目标公司: Google")
print(f"🎯 目标岗位: Solution Engineer")
print(f"📝 用户弱项: {test_weak_points}")
print(f"📚 面经问题数: {len(test_intelligence['common_questions'])}")
print()

print("-" * 60)
print("测试1: 优先使用面经中的问题")
print("-" * 60)

question = qg.generate(
    company="Google",
    role="Solution Engineer",
    difficulty="auto",
    avoid_questions=[],
    focus_weak_points=test_weak_points,
    intelligence=test_intelligence
)

print(f"🆔 问题ID: {question['id']}")
print(f"📝 问题内容: {question['text']}")
print(f"🎯 问题类型: {question['type']}")
print(f"📊 难度: {question['difficulty']}")

print()
print("-" * 60)
print("测试2: 避开已问过的问题")
print("-" * 60)

question2 = qg.generate(
    company="Google",
    role="Solution Engineer",
    difficulty="auto",
    avoid_questions=[question['text']],  # 避开刚才问的问题
    focus_weak_points=test_weak_points,
    intelligence=test_intelligence
)

print(f"🆔 问题ID: {question2['id']}")
print(f"📝 问题内容: {question2['text']}")
print(f"🎯 问题类型: {question2['type']}")

print()
print("=" * 60)
print("✅ 改进功能说明")
print("=" * 60)
print()
print("1. 📚 优先使用面经问题：")
print("   - 先从 common_questions 中选择问题")
print("   - 避开已经问过的问题")
print()
print("2. 💡 基于难点主题生成：")
print("   - 如果面经问题用完了，从 difficult_topics 生成问题")
print()
print("3. 🔥 基于热点主题生成：")
print("   - 从 hot_topics 生成问题，保持时效性")
print()
print("4. 🎨 兜底使用预设模板：")
print("   - 如果面经里没有合适的，使用原有模板")
print()
print("这样就保证了提问是基于搜索到的面试经验帖来思考的！")
