#!/usr/bin/env python3
"""
Interview-Prep 技能安装验证脚本
"""

import os
import sys

print("=" * 60)
print("🧪 Interview-Prep 技能安装验证")
print("=" * 60)

# 检查目录结构
workspace = "/Users/zhouyidan/.openclaw/workspace-interview-prep"
skill_dir = os.path.join(workspace, "skills", "interview-prep")
scripts_dir = os.path.join(skill_dir, "scripts")
data_dir = os.path.join(workspace, "INTERVIEW_DATA")

print("\n📁 检查目录结构...")
dirs_to_check = [skill_dir, scripts_dir, data_dir]
for d in dirs_to_check:
    if os.path.exists(d):
        print(f"   ✅ {d}")
    else:
        print(f"   ❌ {d} - 不存在")

# 检查核心文件
print("\n📄 检查核心文件...")
core_files = [
    os.path.join(skill_dir, "SKILL.md"),
    os.path.join(skill_dir, "README.md"),
    os.path.join(scripts_dir, "__init__.py"),
    os.path.join(scripts_dir, "memory_manager.py"),
    os.path.join(scripts_dir, "question_generator.py"),
    os.path.join(scripts_dir, "answer_evaluator.py"),
    os.path.join(scripts_dir, "orchestrator.py")
]

for f in core_files:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"   ✅ {os.path.basename(f)} ({size} bytes)")
    else:
        print(f"   ❌ {os.path.basename(f)} - 不存在")

# 尝试导入模块
print("\n🔧 测试模块导入...")
try:
    sys.path.insert(0, scripts_dir)
    
    from memory_manager import MemoryManager
    print("   ✅ MemoryManager 导入成功")
    
    from question_generator import QuestionGenerator
    print("   ✅ QuestionGenerator 导入成功")
    
    from answer_evaluator import AnswerEvaluator
    print("   ✅ AnswerEvaluator 导入成功")
    
except Exception as e:
    print(f"   ❌ 模块导入失败: {e}")
    import traceback
    traceback.print_exc()

# 简单功能测试
print("\n🧪 简单功能测试...")
try:
    # 测试记忆管理器初始化
    mm = MemoryManager(workspace)
    print("   ✅ MemoryManager 初始化成功")
    
    # 测试问题生成器
    qg = QuestionGenerator()
    test_question = qg.generate(
        company="TestCorp",
        role="Engineer",
        difficulty="medium",
        avoid_questions=[],
        focus_weak_points=[]
    )
    print(f"   ✅ 问题生成成功: {test_question['text'][:50]}...")
    
    # 测试回答评估器
    ae = AnswerEvaluator()
    test_eval = ae.evaluate(
        question=test_question,
        answer="这是一个测试回答，包含一些内容。首先，我会分析问题，然后提出解决方案。例如，这样做的好处是...",
        company_context={},
        role_requirements={}
    )
    print(f"   ✅ 回答评估成功: 总分 {test_eval['overall_score']}/10")
    
    print("\n" + "=" * 60)
    print("🎉 Interview-Prep 技能安装验证完成！")
    print("=" * 60)
    print("\n📖 使用方式:")
    print("   cd " + scripts_dir)
    print("   python orchestrator.py new \"公司名\" \"岗位名\"")
    print("   python orchestrator.py simulate")
    print("   python orchestrator.py evaluate \"你的回答\"")
    print("\n📚 详细文档请查看: " + os.path.join(skill_dir, "README.md"))
    
except Exception as e:
    print(f"   ❌ 功能测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
