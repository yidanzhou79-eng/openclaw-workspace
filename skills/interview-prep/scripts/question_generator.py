#!/usr/bin/env python3
"""
问题生成器 - 基于公司风格、岗位要求和用户弱项智能生成面试问题
"""

import random
from typing import Dict, List, Optional
from datetime import datetime


class QuestionGenerator:
    def __init__(self):
        self.templates = self._load_default_templates()
    
    def _load_default_templates(self) -> Dict:
        """加载默认问题模板"""
        return {
            "behavioral": [
                "告诉我一个你解决过的复杂问题",
                "描述一次你在团队中遇到冲突的经历",
                "分享一个你在截止日期前完成项目的例子",
                "讲一个你从错误中学习的故事",
                "描述一次你需要快速学习新技能的经历"
            ],
            "technical": [
                "解释一下你最熟悉的技术栈",
                "谈谈你对系统设计的理解",
                "描述一个你解决过的技术难题",
                "你如何进行代码审查？",
                "谈谈你对测试的看法"
            ],
            "system_design": [
                "设计一个可扩展的社交媒体平台",
                "如何设计一个高并发的电商系统？",
                "设计一个实时数据处理系统",
                "如何构建一个分布式缓存系统？",
                "设计一个消息推送系统"
            ],
            "case_study": [
                "如果客户要求的功能不可行，你会如何处理？",
                "如何评估一个新产品的市场机会？",
                "描述你如何分析用户需求",
                "如何平衡技术可行性和业务需求？",
                "分享一个你说服利益相关者的案例"
            ],
            "product_sense": [
                "你最喜欢的产品是什么？为什么？",
                "如何改进我们的产品？",
                "谈谈你对用户体验的理解",
                "如何衡量产品成功？",
                "你怎么看待竞品分析？"
            ]
        }
    
    def generate(self, company: str, role: str, difficulty: str = "auto", 
                 avoid_questions: List[str] = None, 
                 focus_weak_points: List[str] = None,
                 intelligence: Dict = None) -> Dict:
        """
        生成面试问题
        
        Args:
            company: 目标公司
            role: 目标岗位
            difficulty: 难度 (easy/medium/hard/expert/auto)
            avoid_questions: 需要避免的问题ID列表
            focus_weak_points: 需要重点关注的弱项列表
            intelligence: 面经情报（包含搜索到的面经问题）
        
        Returns:
            问题对象
        """
        avoid_questions = avoid_questions or []
        focus_weak_points = focus_weak_points or []
        
        question_type = self._select_question_type(focus_weak_points)
        
        if difficulty == "auto":
            difficulty = self._calculate_appropriate_difficulty(focus_weak_points)
        
        # 优先使用搜索到的面经问题
        question_text = self._select_from_intelligence(intelligence, question_type, difficulty, avoid_questions)
        
        # 如果面经中没有合适的问题，使用预设模板
        if not question_text:
            template = self._select_template(question_type, difficulty)
            question_text = self._customize_template(template, company, role, difficulty)
        
        question_id = f"q{int(datetime.now().timestamp()) % 10000:04d}"
        
        return {
            "id": question_id,
            "text": question_text,
            "type": question_type,
            "difficulty": difficulty,
            "expected_points": self._get_expected_points(question_type, difficulty),
            "hints": self._get_hints(question_type)
        }
    
    def _select_question_type(self, weak_points: List[str]) -> str:
        """基于弱项选择问题类型"""
        question_types = ["behavioral", "technical", "system_design", "case_study", "product_sense"]
        
        weak_type_map = {
            "系统设计": "system_design",
            "案例分析": "case_study",
            "技术深度": "technical",
            "技术准确性": "technical",
            "critical_thinking": "case_study",
            "answer_depth": "system_design"
        }
        
        for weakness in weak_points:
            for key, q_type in weak_type_map.items():
                if key in weakness:
                    print(f"🎯 针对弱项选择问题类型: {q_type}")
                    return q_type
        
        selected = random.choice(question_types)
        print(f"🎲 随机选择问题类型: {selected}")
        return selected
    
    def _calculate_appropriate_difficulty(self, weak_points: List[str]) -> str:
        """计算合适的难度"""
        if len(weak_points) >= 2:
            return "medium"
        elif len(weak_points) == 1:
            return "medium_hard"
        else:
            return "medium"
    
    def _select_template(self, question_type: str, difficulty: str) -> str:
        """选择问题模板"""
        templates = self.templates.get(question_type, self.templates["behavioral"])
        
        difficulty_adjusted = []
        for template in templates:
            if difficulty == "easy":
                if "简单" in template or "基础" in template:
                    difficulty_adjusted.append(template)
            elif difficulty == "hard":
                if "复杂" in template or "困难" in template or "设计" in template:
                    difficulty_adjusted.append(template)
        
        if not difficulty_adjusted:
            difficulty_adjusted = templates
        
        return random.choice(difficulty_adjusted)
    
    def _customize_template(self, template: str, company: str, role: str, difficulty: str) -> str:
        """个性化改造模板"""
        question = template
        
        question = question.replace("{COMPANY}", company if company else "某公司")
        question = question.replace("{ROLE}", role if role else "该岗位")
        
        difficulty_words = {
            "easy": ["简单的", "基础的"],
            "medium": ["常见的", "标准的"],
            "medium_hard": ["有挑战性的", "中等难度的"],
            "hard": ["困难的", "高级的"],
            "expert": ["专家级的", "极难的"]
        }
        
        if "{DIFFICULTY}" in question:
            word = random.choice(difficulty_words.get(difficulty, ["标准的"]))
            question = question.replace("{DIFFICULTY}", word)
        
        return question
    
    def _get_expected_points(self, question_type: str, difficulty: str) -> List[str]:
        """获取预期要点"""
        points_map = {
            "behavioral": ["使用STAR结构", "具体例子", "结果和影响", "学到的经验"],
            "technical": ["技术准确性", "深度解释", "示例代码或架构", "权衡讨论"],
            "system_design": ["架构图", "扩展性考虑", "性能优化", "容错机制"],
            "case_study": ["问题分析", "多角度思考", "数据支持", "建议方案"],
            "product_sense": ["用户视角", "数据驱动", "竞品对比", "改进建议"]
        }
        
        base_points = points_map.get(question_type, ["清晰表达", "逻辑结构"])
        
        if difficulty in ["hard", "expert"]:
            base_points.append("深入分析")
            base_points.append("创新思维")
        
        return base_points
    
    def _select_from_intelligence(self, intelligence: Dict, question_type: str, 
                                     difficulty: str, avoid_questions: List[str]) -> Optional[str]:
        """从面经情报中选择问题"""
        if not intelligence:
            return None
        
        # 1. 优先从 common_questions 中选择
        common_questions = intelligence.get("common_questions", [])
        if common_questions:
            # 过滤掉已经问过的问题
            available_questions = [q for q in common_questions if q not in avoid_questions]
            if available_questions:
                print(f"📚 从面经中选择问题（从 {len(common_questions)} 个面经问题中）")
                selected = random.choice(available_questions)
                return selected
        
        # 2. 从 difficult_topics 中生成问题
        difficult_topics = intelligence.get("difficult_topics", [])
        if difficult_topics:
            topic = random.choice(difficult_topics)
            topic_based_questions = [
                f"谈谈你对{topic}的理解？",
                f"你在{topic}方面有什么经验？",
                f"{topic}对你来说有什么挑战？"
            ]
            print(f"💡 基于面经难点主题生成问题: {topic}")
            return random.choice(topic_based_questions)
        
        # 3. 从 hot_topics 中生成问题
        hot_topics = intelligence.get("hot_topics", [])
        if hot_topics:
            topic = random.choice(hot_topics)
            hot_based_questions = [
                f"你如何看待{topic}这个趋势？",
                f"{topic}对这个岗位有什么影响？",
                f"你在{topic}方面有什么实践经验？"
            ]
            print(f"🔥 基于面经热点主题生成问题: {topic}")
            return random.choice(hot_based_questions)
        
        return None
    
    def _get_hints(self, question_type: str) -> List[str]:
        """获取提示"""
        hints_map = {
            "behavioral": ["记得用STAR: Situation-Task-Action-Result", "具体比笼统好"],
            "technical": ["先讲整体思路，再讲细节", "诚实面对不懂的问题"],
            "system_design": ["先澄清需求，再设计架构", "考虑扩展性和性能"],
            "case_study": ["先问问题再回答", "展示你的分析过程"],
            "product_sense": ["从用户需求出发", "用数据支持观点"]
        }
        
        return hints_map.get(question_type, ["清晰表达你的想法"])


def main():
    """测试问题生成器"""
    print("=" * 50)
    print("问题生成器测试 - 带面经情报")
    print("=" * 50)
    
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
    print("✅ 预期要点:")
    for point in question['expected_points']:
        print(f"   - {point}")
    print()
    print("💡 提示:")
    for hint in question['hints']:
        print(f"   - {hint}")


if __name__ == "__main__":
    main()
