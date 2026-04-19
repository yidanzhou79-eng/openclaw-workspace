#!/usr/bin/env python3
"""
回答评估器 - 多维度评估用户回答质量
"""

from typing import Dict, List, Tuple


class AnswerEvaluator:
    def __init__(self):
        self.rubrics = self._load_scoring_rubrics()
    
    def _load_scoring_rubrics(self) -> Dict:
        """加载评分标准"""
        return {
            "technical_accuracy": {
                "weight": 0.40,
                "description": "技术准确性"
            },
            "depth": {
                "weight": 0.30,
                "description": "回答深度"
            },
            "structure": {
                "weight": 0.20,
                "description": "逻辑结构"
            },
            "critical_thinking": {
                "weight": 0.10,
                "description": "批判性思维"
            }
        }
    
    def evaluate(self, question: Dict, answer: str, 
                 company_context: Dict = None, 
                 role_requirements: Dict = None) -> Dict:
        """
        多维度评估回答
        
        Args:
            question: 问题对象
            answer: 用户回答
            company_context: 公司风格上下文
            role_requirements: 岗位要求
        
        Returns:
            评估结果
        """
        evaluation = {
            "overall_score": 0,
            "dimensions": {},
            "errors": [],
            "strengths": [],
            "improvements": [],
            "critical_thinking_score": 0
        }
        
        tech_score, tech_errors = self._evaluate_technical_accuracy(question, answer)
        evaluation["dimensions"]["technical_accuracy"] = tech_score
        evaluation["errors"].extend(tech_errors)
        
        depth_score, depth_feedback = self._evaluate_depth(question, answer)
        evaluation["dimensions"]["depth"] = depth_score
        evaluation["improvements"].extend(depth_feedback)
        
        structure_score, structure_feedback = self._evaluate_structure(answer)
        evaluation["dimensions"]["structure"] = structure_score
        
        ct_score, ct_feedback = self._evaluate_critical_thinking(question, answer)
        evaluation["critical_thinking_score"] = ct_score
        evaluation["improvements"].extend(ct_feedback)
        
        weights = self.rubrics
        evaluation["overall_score"] = (
            evaluation["dimensions"]["technical_accuracy"] * weights["technical_accuracy"]["weight"] +
            evaluation["dimensions"]["depth"] * weights["depth"]["weight"] +
            evaluation["dimensions"]["structure"] * weights["structure"]["weight"] +
            evaluation["critical_thinking_score"] * weights["critical_thinking"]["weight"]
        )
        
        evaluation["overall_score"] = round(evaluation["overall_score"], 1)
        
        evaluation["strengths"] = self._identify_strengths(answer, question)
        
        return evaluation
    
    def _evaluate_technical_accuracy(self, question: Dict, answer: str) -> Tuple[float, List[str]]:
        """评估技术准确性"""
        score = 10
        errors = []
        
        answer_lower = answer.lower()
        
        if len(answer.strip()) < 20:
            score -= 3
            errors.append("回答过于简短，建议提供更多细节")
        
        question_type = question.get("type", "general")
        if question_type == "technical":
            if "代码" in answer or "架构" in answer or "技术" in answer:
                pass
            else:
                score -= 2
                errors.append("技术问题建议加入具体技术细节")
        
        return max(0, score), errors
    
    def _evaluate_depth(self, question: Dict, answer: str) -> Tuple[float, List[str]]:
        """评估回答深度"""
        score = 10
        feedback = []
        
        if len(answer.split("。")) < 3 and len(answer.split("\n")) < 3:
            score -= 3
            feedback.append("回答可以更深入一些，建议展开细节")
        
        if "例如" not in answer and "比如" not in answer and "具体" not in answer:
            score -= 2
            feedback.append("建议加入具体例子或实际场景，让回答更生动")
        
        if "为什么" not in answer and "因为" not in answer and "原因" not in answer:
            score -= 2
            feedback.append("建议解释原因和思考过程")
        
        return max(0, score), feedback
    
    def _evaluate_structure(self, answer: str) -> Tuple[float, List[str]]:
        """评估逻辑结构"""
        score = 10
        feedback = []
        
        structure_indicators = ["第一", "第二", "第三", "首先", "其次", "最后", 
                               "1.", "2.", "3.", "-", "•"]
        
        has_structure = any(indicator in answer for indicator in structure_indicators)
        
        if not has_structure and len(answer) > 100:
            score -= 2
            feedback.append("建议用序号或项目符号组织回答，让结构更清晰")
        
        paragraphs = answer.split("\n")
        if len(paragraphs) == 1 and len(answer) > 200:
            score -= 1
            feedback.append("建议适当分段，提高可读性")
        
        return max(0, score), feedback
    
    def _evaluate_critical_thinking(self, question: Dict, answer: str) -> Tuple[float, List[str]]:
        """评估批判性思维（独立重点）"""
        score = 0
        feedback = []
        
        perspectives = ["一方面", "另一方面", "但是", "然而", "不过", "虽然", "尽管"]
        if any(p in answer for p in perspectives):
            score += 3
        else:
            feedback.append("💡 建议从多个角度分析问题，展示全面思考")
        
        reasoning = ["因为", "所以", "因此", "由于", "导致", "结果"]
        if any(r in answer for r in reasoning):
            score += 3
        else:
            feedback.append("💡 建议展示你的思考过程，而不仅是结论")
        
        tradeoffs = ["优点", "缺点", "好处", "坏处", "优势", "劣势", "权衡"]
        if any(t in answer for t in tradeoffs):
            score += 2
        else:
            feedback.append("💡 建议讨论不同方案的优缺点和权衡")
        
        evidence = ["例如", "比如", "举例", "数据", "研究", "统计"]
        if any(e in answer for e in evidence):
            score += 2
        else:
            feedback.append("💡 建议用具体例子或数据支持你的观点")
        
        return score, feedback
    
    def _identify_strengths(self, answer: str, question: Dict) -> List[str]:
        """识别亮点"""
        strengths = []
        
        if len(answer) > 200:
            strengths.append("回答内容详实，信息量充足")
        
        if "例如" in answer or "比如" in answer:
            strengths.append("很好地使用了具体例子")
        
        structure_indicators = ["第一", "第二", "第三", "首先", "其次", "最后", "1.", "2.", "3."]
        if any(indicator in answer for indicator in structure_indicators):
            strengths.append("结构清晰，逻辑有条理")
        
        if "因为" in answer or "所以" in answer:
            strengths.append("展示了思考过程")
        
        if len(answer.split("。")) > 3:
            strengths.append("回答有层次感")
        
        if not strengths:
            strengths.append("勇于表达自己的想法")
        
        return strengths


def main():
    """测试回答评估器"""
    print("=" * 50)
    print("回答评估器测试")
    print("=" * 50)
    
    evaluator = AnswerEvaluator()
    
    test_question = {
        "id": "q001",
        "text": "告诉我一个你解决过的复杂问题",
        "type": "behavioral",
        "difficulty": "medium"
    }
    
    test_answer = """
在我的上一个项目中，我们遇到了一个复杂的问题。
第一，我先分析了问题的根本原因。
然后，我提出了两个解决方案：方案A和方案B。
例如，方案A的优点是快速实施，但缺点是扩展性不好。
所以我最终选择了方案B，因为它更符合长期需求。
最后，这个项目成功上线了。
"""
    
    print(f"\n📝 问题: {test_question['text']}")
    print(f"💬 回答:\n{test_answer}")
    print()
    
    evaluation = evaluator.evaluate(test_question, test_answer)
    
    print("📊 评估结果:")
    print(f"   总分: {evaluation['overall_score']}/10")
    print(f"   技术准确性: {evaluation['dimensions']['technical_accuracy']}/10")
    print(f"   回答深度: {evaluation['dimensions']['depth']}/10")
    print(f"   逻辑结构: {evaluation['dimensions']['structure']}/10")
    print(f"   批判性思维: {evaluation['critical_thinking_score']}/10")
    print()
    
    print("✅ 亮点:")
    for strength in evaluation['strengths']:
        print(f"   - {strength}")
    print()
    
    print("📝 改进建议:")
    for improvement in evaluation['improvements']:
        print(f"   - {improvement}")
    print()
    
    if evaluation['errors']:
        print("⚠️  需要注意:")
        for error in evaluation['errors']:
            print(f"   - {error}")


if __name__ == "__main__":
    main()
