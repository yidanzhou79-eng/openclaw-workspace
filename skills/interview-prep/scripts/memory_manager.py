#!/usr/bin/env python3
"""
记忆管理器 - 管理用户档案、会话状态、弱项追踪和表现历史
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


class MemoryManager:
    def __init__(self, workspace: str):
        self.workspace = workspace
        self.data_dir = os.path.join(workspace, "INTERVIEW_DATA")
        self.current_user_id = "yuki"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        dirs = [
            self.data_dir,
            os.path.join(self.data_dir, "users"),
            os.path.join(self.data_dir, "users", self.current_user_id),
            os.path.join(self.data_dir, "interview_sessions"),
            os.path.join(self.data_dir, "knowledge_base")
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
    
    def _save_json(self, filepath: str, data: Any):
        """保存JSON文件"""
        full_path = os.path.join(self.data_dir, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_json(self, filepath: str, default: Any = None) -> Any:
        """加载JSON文件"""
        full_path = os.path.join(self.data_dir, filepath)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    
    def init_user_profile(self, company: str, role: str, intelligence: Dict):
        """初始化用户档案"""
        profile = {
            "user_id": self.current_user_id,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "basic_info": {
                "target_company": company,
                "target_role": role
            },
            "current_target": {
                "company": company,
                "role": role
            },
            "statistics": {
                "total_interviews": 0,
                "total_questions": 0,
                "average_score": 0
            }
        }
        
        self._save_json(f"users/{self.current_user_id}/profile.json", profile)
        
        session = {
            "session_id": f"{company.lower()}_{role.lower()}_{datetime.now().strftime('%Y%m%d')}",
            "target": {"company": company, "role": role},
            "intelligence": intelligence,
            "asked_questions": [],
            "status": "ready",
            "current_question": None
        }
        
        self._save_json(f"users/{self.current_user_id}/current_session.json", session)
        
        weak_points = {
            "user_id": self.current_user_id,
            "last_updated": datetime.now().isoformat(),
            "weak_points": [],
            "high_priority_weak_points": [],
            "resolved_weak_points": []
        }
        
        self._save_json(f"users/{self.current_user_id}/weak_points.json", weak_points)
        
        history = {
            "user_id": self.current_user_id,
            "history": [],
            "trend_analysis": {
                "last_7_days": {
                    "average_score": 0,
                    "improvement": 0,
                    "best_category": None,
                    "worst_category": None
                },
                "overall": {
                    "start_score": 0,
                    "current_score": 0,
                    "total_practice_hours": 0
                }
            }
        }
        
        self._save_json(f"users/{self.current_user_id}/performance_history.json", history)
        
        print(f"✅ 用户档案初始化完成：{company} {role}")
    
    def record_question_asked(self, question: Dict):
        """记录已问问题"""
        session = self._load_json(f"users/{self.current_user_id}/current_session.json")
        if not session:
            print("⚠️  没有活跃的会话")
            return
        
        question_record = {
            "id": question.get("id", f"q{len(session['asked_questions']) + 1:03d}"),
            "text": question.get("text", ""),
            "type": question.get("type", "general"),
            "difficulty": question.get("difficulty", "medium"),
            "asked_at": datetime.now().isoformat()
        }
        
        session["asked_questions"].append(question_record)
        session["current_question"] = question
        session["last_updated"] = datetime.now().isoformat()
        
        self._save_json(f"users/{self.current_user_id}/current_session.json", session)
        print(f"✅ 问题已记录：{question_record['id']}")
    
    def update_performance(self, question: Dict, evaluation: Dict):
        """更新用户表现记录"""
        history = self._load_json(f"users/{self.current_user_id}/performance_history.json")
        if not history:
            print("⚠️  没有历史记录")
            return
        
        history_record = {
            "timestamp": datetime.now().isoformat(),
            "question_id": question.get("id", "unknown"),
            "question_type": question.get("type", "general"),
            "difficulty": question.get("difficulty", "medium"),
            "score": evaluation.get("dimensions", {}),
            "strengths": evaluation.get("strengths", []),
            "improvements": evaluation.get("improvements", [])
        }
        
        history["history"].append(history_record)
        
        profile = self._load_json(f"users/{self.current_user_id}/profile.json")
        if profile:
            profile["statistics"]["total_questions"] += 1
            if history["history"]:
                scores = [h.get("score", {}).get("overall", 0) for h in history["history"]]
                profile["statistics"]["average_score"] = sum(scores) / len(scores)
            profile["last_updated"] = datetime.now().isoformat()
            self._save_json(f"users/{self.current_user_id}/profile.json", profile)
        
        new_weak_points = self._detect_weak_points(evaluation, question.get("type", "general"))
        self._update_weak_points(new_weak_points)
        
        self._save_json(f"users/{self.current_user_id}/performance_history.json", history)
        print(f"✅ 表现记录已更新")
    
    def _detect_weak_points(self, evaluation: Dict, question_type: str) -> List[Dict]:
        """检测弱项"""
        weak_points = []
        dimensions = evaluation.get("dimensions", {})
        
        if dimensions.get("technical_accuracy", 10) < 6:
            weak_points.append({
                "category": "technical_accuracy",
                "description": f"{question_type}类型问题的技术准确性需要提高"
            })
        
        if evaluation.get("critical_thinking_score", 10) < 5:
            weak_points.append({
                "category": "critical_thinking",
                "description": "回答缺少多角度分析和权衡讨论"
            })
        
        if dimensions.get("depth", 10) < 6:
            weak_points.append({
                "category": "answer_depth",
                "description": "回答可以更深入，建议展开细节"
            })
        
        return weak_points
    
    def _update_weak_points(self, new_weak_points: List[Dict]):
        """更新弱项记录"""
        weak_points_data = self._load_json(f"users/{self.current_user_id}/weak_points.json")
        if not weak_points_data:
            return
        
        for new_wp in new_weak_points:
            existing = None
            for wp in weak_points_data["weak_points"]:
                if wp["category"] == new_wp["category"]:
                    existing = wp
                    break
            
            if existing:
                existing["last_observed"] = datetime.now().isoformat()
                existing["occurrence_count"] = existing.get("occurrence_count", 0) + 1
                if existing["occurrence_count"] > 3:
                    existing["improvement_trend"] = "needs_attention"
            else:
                weak_points_data["weak_points"].append({
                    "id": f"wp{len(weak_points_data['weak_points']) + 1:03d}",
                    "category": new_wp["category"],
                    "description": new_wp["description"],
                    "first_observed": datetime.now().isoformat(),
                    "last_observed": datetime.now().isoformat(),
                    "occurrence_count": 1,
                    "improvement_trend": "new",
                    "related_questions": [],
                    "practice_suggestions": self._get_practice_suggestions(new_wp["category"])
                })
        
        weak_points_data["high_priority_weak_points"] = [
            wp["id"] for wp in weak_points_data["weak_points"]
            if wp.get("occurrence_count", 0) >= 2 or wp.get("improvement_trend") == "needs_attention"
        ]
        
        weak_points_data["last_updated"] = datetime.now().isoformat()
        self._save_json(f"users/{self.current_user_id}/weak_points.json", weak_points_data)
    
    def _get_practice_suggestions(self, category: str) -> List[str]:
        """获取练习建议"""
        suggestions = {
            "technical_accuracy": ["复习相关技术概念", "做专项练习", "查找权威资料"],
            "critical_thinking": ["每次回答前列出3个角度", "强制讨论优缺点", "用具体例子说明权衡"],
            "answer_depth": ["追问自己'为什么'和'如何'", "加入具体场景", "详细说明实现细节"],
            "system_design": ["复习CAP理论", "练习微服务架构", "重点考虑扩展性"],
            "behavioral": ["使用STAR结构", "准备具体例子", "强调结果和影响"]
        }
        return suggestions.get(category, ["继续练习，保持耐心"])
    
    def get_weak_points(self) -> List[str]:
        """获取用户弱项列表"""
        weak_points_data = self._load_json(f"users/{self.current_user_id}/weak_points.json")
        if not weak_points_data:
            return []
        return [wp["description"] for wp in weak_points_data.get("weak_points", [])]
    
    def get_asked_questions(self) -> List[str]:
        """获取已问问题ID列表"""
        session = self._load_json(f"users/{self.current_user_id}/current_session.json")
        if not session:
            return []
        return [q["id"] for q in session.get("asked_questions", [])]
    
    def get_intelligence(self) -> Dict:
        """获取面经情报"""
        session = self._load_json(f"users/{self.current_user_id}/current_session.json")
        if not session:
            return {}
        return session.get("intelligence", {})
    
    def get_current_target(self) -> Dict:
        """获取当前目标公司和岗位"""
        profile = self._load_json(f"users/{self.current_user_id}/profile.json")
        if not profile:
            return {}
        return profile.get("current_target", {})


def main():
    """测试记忆管理器"""
    workspace = "/Users/zhouyidan/.openclaw/workspace-interview-prep"
    mm = MemoryManager(workspace)
    
    print("=" * 50)
    print("记忆管理器测试")
    print("=" * 50)
    
    test_intel = {
        "common_questions": ["自我介绍", "为什么想加入我们"],
        "interview_process": ["电话面", "技术面", "终面"],
        "company_style": "注重技术和团队协作"
    }
    
    mm.init_user_profile("TestCorp", "Engineer", test_intel)
    print("\n✅ 初始化完成")
    
    weak_points = mm.get_weak_points()
    print(f"\n当前弱项: {weak_points}")
    
    target = mm.get_current_target()
    print(f"\n当前目标: {target}")


if __name__ == "__main__":
    main()
