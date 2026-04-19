#!/usr/bin/env python3
"""
面试准备流程编排器 - 协调各个模块完成完整面试流程
"""

import os
import sys
from typing import Dict, Optional

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory_manager import MemoryManager
from question_generator import QuestionGenerator
from answer_evaluator import AnswerEvaluator


class InterviewOrchestrator:
    def __init__(self, workspace: str):
        self.workspace = workspace
        self.memory = MemoryManager(workspace)
        self.question_gen = QuestionGenerator()
        self.evaluator = AnswerEvaluator()
        
        print("=" * 60)
        print("🎯 面试准备系统启动")
        print("=" * 60)
    
    def handle_new_interview(self, company: str, role: str, intelligence: Dict = None) -> Dict:
        """
        处理新面试请求 - 面经搜索阶段
        
        Args:
            company: 公司名称
            role: 岗位名称
            intelligence: 面经情报（可选，如未提供会使用默认情报）
        
        Returns:
            结果字典
        """
        print(f"\n🚀 开始新面试准备：{company} {role}")
        print("-" * 60)
        
        if not intelligence:
            intelligence = self._get_default_intelligence(company, role)
        
        self.memory.init_user_profile(company, role, intelligence)
        
        result = {
            "status": "success",
            "intelligence": intelligence,
            "next_steps": ["模拟面试", "专项训练"]
        }
        
        self._display_intelligence(intelligence)
        
        return result
    
    def _get_default_intelligence(self, company: str, role: str) -> Dict:
        """获取默认面经情报（当没有搜索时使用）"""
        return {
            "common_questions": [
                "自我介绍",
                f"为什么想加入{company}？",
                f"你对{role}岗位有什么理解？",
                "谈谈你的项目经历",
                "你为什么适合这个岗位？"
            ],
            "difficult_topics": [
                "系统设计",
                "案例分析",
                "技术深度问题"
            ],
            "interview_process": [
                "简历筛选",
                "电话面试",
                "技术面试",
                "终面",
                "Offer"
            ],
            "success_tips": [
                "准备具体例子",
                "展示思考过程",
                "提问有深度的问题"
            ],
            "company_style": f"{company}注重技术能力和团队协作",
            "hot_topics": ["云计算", "人工智能", "用户体验"]
        }
    
    def _display_intelligence(self, intelligence: Dict):
        """显示面经情报"""
        print("\n📚 面经情报摘要")
        print("-" * 60)
        
        if intelligence.get("common_questions"):
            print(f"\n💬 常见问题 ({len(intelligence['common_questions'])}个):")
            for i, q in enumerate(intelligence["common_questions"][:5], 1):
                print(f"   {i}. {q}")
        
        if intelligence.get("interview_process"):
            print(f"\n📋 面试流程:")
            print(f"   {' → '.join(intelligence['interview_process'])}")
        
        if intelligence.get("success_tips"):
            print(f"\n💡 成功经验:")
            for tip in intelligence["success_tips"]:
                print(f"   - {tip}")
        
        print("\n✅ 情报加载完成！可以开始模拟面试了。")
    
    def start_simulation(self, difficulty: str = "auto") -> Optional[Dict]:
        """
        开始模拟面试 - 问题生成阶段
        
        Args:
            difficulty: 难度 (easy/medium/medium_hard/hard/auto)
        
        Returns:
            问题对象
        """
        print(f"\n🎮 开始模拟面试")
        print("-" * 60)
        
        target = self.memory.get_current_target()
        if not target:
            print("⚠️  请先使用 'new' 命令开始新面试准备")
            return None
        
        company = target.get("company", "")
        role = target.get("role", "")
        weak_points = self.memory.get_weak_points()
        asked_questions = self.memory.get_asked_questions()
        intelligence = self.memory.get_intelligence()
        
        print(f"🎯 目标: {company} {role}")
        if weak_points:
            print(f"📝 关注弱项: {len(weak_points)}个")
        
        question = self.question_gen.generate(
            company=company,
            role=role,
            difficulty=difficulty,
            avoid_questions=asked_questions,
            focus_weak_points=weak_points,
            intelligence=intelligence
        )
        
        self.memory.record_question_asked(question)
        
        self._display_question(question)
        
        return question
    
    def _display_question(self, question: Dict):
        """显示问题"""
        print(f"\n❓ 问题 #{question['id']}")
        print(f"🎯 类型: {question['type']} | 难度: {question['difficulty']}")
        print("-" * 60)
        print(f"\n{question['text']}\n")
        
        print("💡 提示:")
        for hint in question['hints']:
            print(f"   - {hint}")
        
        print("\n✅ 预期要点:")
        for point in question['expected_points']:
            print(f"   - {point}")
    
    def evaluate_answer(self, answer: str) -> Optional[Dict]:
        """
        评估用户回答 - 评估反馈阶段
        
        Args:
            answer: 用户回答
        
        Returns:
            评估结果
        """
        print(f"\n📊 评估回答")
        print("-" * 60)
        
        session = self.memory._load_json(f"users/{self.memory.current_user_id}/current_session.json")
        if not session or not session.get("current_question"):
            print("⚠️  没有当前问题，请先使用 'simulate' 开始模拟面试")
            return None
        
        question = session["current_question"]
        intelligence = self.memory.get_intelligence()
        
        evaluation = self.evaluator.evaluate(
            question=question,
            answer=answer,
            company_context=intelligence.get("company_style", ""),
            role_requirements=intelligence.get("role_requirements", {})
        )
        
        self.memory.update_performance(question, evaluation)
        
        self._display_evaluation(evaluation)
        
        return evaluation
    
    def _display_evaluation(self, evaluation: Dict):
        """显示评估结果"""
        overall = evaluation["overall_score"]
        
        print(f"\n{'🎉' if overall >= 8 else '👍' if overall >= 6 else '💪'} 总体评价")
        print("-" * 60)
        
        if overall >= 8:
            print(f"\n太棒了！你的回答非常出色 🌟")
        elif overall >= 6:
            print(f"\n不错！你的回答有很多亮点，还有一些提升空间")
        else:
            print(f"\n继续努力！这个问题有难度，我们来一起分析")
        
        print(f"\n📊 总分: {overall}/10")
        
        dimensions = evaluation["dimensions"]
        print(f"\n📈 各维度评分:")
        print(f"   技术准确性: {dimensions.get('technical_accuracy', 0)}/10")
        print(f"   回答深度: {dimensions.get('depth', 0)}/10")
        print(f"   逻辑结构: {dimensions.get('structure', 0)}/10")
        print(f"   批判性思维: {evaluation.get('critical_thinking_score', 0)}/10")
        
        strengths = evaluation["strengths"]
        if strengths:
            print(f"\n✅ 亮点:")
            for strength in strengths:
                print(f"   - {strength}")
        
        improvements = evaluation["improvements"]
        if improvements:
            print(f"\n📝 改进建议:")
            for improvement in improvements:
                print(f"   - {improvement}")
        
        errors = evaluation["errors"]
        if errors:
            print(f"\n⚠️  需要注意:")
            for error in errors:
                print(f"   - {error}")
        
        weak_points = self.memory.get_weak_points()
        if weak_points:
            print(f"\n🎯 当前弱项 ({len(weak_points)}个):")
            for i, wp in enumerate(weak_points[:3], 1):
                print(f"   {i}. {wp}")
        
        print("\n" + "-" * 60)
        print("💡 提示: 继续练习，重点关注上面提到的改进建议！")


def main():
    """主函数 - 简单的命令行界面"""
    workspace = "/Users/zhouyidan/.openclaw/workspace-interview-prep"
    orchestrator = InterviewOrchestrator(workspace)
    
    if len(sys.argv) < 2:
        print("\n使用方式:")
        print("  python orchestrator.py new [公司] [岗位]  - 开始新面试准备")
        print("  python orchestrator.py simulate [难度]        - 开始模拟面试")
        print("  python orchestrator.py evaluate \"回答内容\"    - 评估回答")
        print("\n难度选项: easy, medium, medium_hard, hard, auto")
        return
    
    command = sys.argv[1]
    
    if command == "new":
        company = sys.argv[2] if len(sys.argv) > 2 else "某公司"
        role = sys.argv[3] if len(sys.argv) > 3 else "某岗位"
        orchestrator.handle_new_interview(company, role)
    
    elif command == "simulate":
        difficulty = sys.argv[2] if len(sys.argv) > 2 else "auto"
        orchestrator.start_simulation(difficulty)
    
    elif command == "evaluate":
        answer = sys.argv[2] if len(sys.argv) > 2 else ""
        orchestrator.evaluate_answer(answer)
    
    else:
        print(f"⚠️  未知命令: {command}")


if __name__ == "__main__":
    main()
