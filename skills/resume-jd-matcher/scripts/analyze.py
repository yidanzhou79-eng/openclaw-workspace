#!/usr/bin/env python3
"""
简历-JD匹配度分析脚本（V2.0 优化版）
优化点：
1. 实习经验折算为正式工作经验
2. 技能迁移匹配（相关领域经验算部分匹配）
3. 学历背景加分项
4. 软技能智能匹配
5. 更符合真实招聘场景的分数计算
6. 个性化优化建议
"""

import json
import re
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResumeJDAnalyzer:
    """简历和JD匹配度分析器"""
    
    def __init__(self):
        self.skill_weights = {
            'hard_skills': 0.35,      # 硬技能权重35%
            'experience': 0.30,        # 经验权重30%
            'education': 0.15,        # 学历权重15%
            'soft_skills': 0.20       # 软技能权重20%
        }
        
        # 技能迁移映射：相关技能可以部分匹配
        self.skill_migration = {
            '云计算': ['云平台', 'AWS', '阿里云', '腾讯云', 'Azure', '云服务', '混合云', '私有云'],
            '架构设计': ['系统架构', '方案设计', '技术方案', '架构', '系统设计'],
            '售前': ['技术咨询', '解决方案', '技术方案', '研报', '行业研究', 'POC', '演示'],
            '微软生态': ['Azure', 'Office 365', 'Microsoft 365', 'Copilot', 'Power Platform', 'Windows'],
            '沟通能力': ['报告编写', '方案输出', '技术分享', '团队协作', '客户对接']
        }
        
        # 学历加分映射
        self.education_scores = {
            '博士': 100,
            '硕士': 90,
            '本科': 80,
            '大专': 60,
            '高中': 40
        }
        
        self.school_tier_scores = {
            '清北复交藤校': 10,
            '985/QS前50': 8,
            '211/QS前100': 5,
            '普通本科': 0
        }
    
    def extract_jd_info(self, jd_text: str) -> Dict:
        """从JD文本中提取关键信息"""
        jd_info = {
            'position_title': '',
            'required_skills': [],
            'preferred_skills': [],
            'experience_years': 0,
            'education_requirements': '',
            'soft_skills': [],
            'responsibilities': [],
            'industry': ''
        }
        
        # 提取职位标题
        title_patterns = [
            r'职位[：:]?\s*(.+)',
            r'岗位[：:]?\s*(.+)',
            r'Position[：:]\s*(.+)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, jd_text)
            if match:
                jd_info['position_title'] = match.group(1).strip()
                break
        
        # 提取技能要求
        skill_patterns = [
            r'技能要求[：:]?\s*([^。]+)',
            r'任职要求[：:]?\s*([^。]+)',
            r'Requirements[：:]\s*([^。]+)'
        ]
        
        for pattern in skill_patterns:
            match = re.search(pattern, jd_text, re.DOTALL)
            if match:
                skills_text = match.group(1)
                skills = re.findall(r'(?:熟悉|掌握|精通|了解|具备)\s*([\u4e00-\u9fa5A-Za-z0-9+]+)', skills_text)
                jd_info['required_skills'] = skills
                break
        
        # 提取经验年限
        exp_patterns = [
            r'(\d+)[-\+]?\s*年.*经验',
            r'经验[：:]?\s*(\d+)[-\+]?\s*年'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, jd_text)
            if match:
                jd_info['experience_years'] = int(match.group(1))
                break
        
        # 提取学历要求
        edu_patterns = [
            r'学历[：:]?\s*([\u4e00-\u9fa5]+)',
            r'Education[：:]\s*([\u4e00-\u9fa5]+)'
        ]
        
        for pattern in edu_patterns:
            match = re.search(pattern, jd_text)
            if match:
                jd_info['education_requirements'] = match.group(1).strip()
                break
        
        # 提取行业
        industry_patterns = [
            r'行业领域[：:]?\s*([\u4e00-\u9fa5A-Za-z、]+)',
            r'行业[：:]?\s*([\u4e00-\u9fa5A-Za-z、]+)'
        ]
        
        for pattern in industry_patterns:
            match = re.search(pattern, jd_text)
            if match:
                jd_info['industry'] = match.group(1).strip()
                break
        
        return jd_info
    
    def extract_resume_info(self, resume_text: str) -> Dict:
        """从简历文本中提取关键信息"""
        resume_info = {
            'skills': [],
            'total_experience_years': 0,
            'education': '',
            'school_tier': '普通本科',
            'major': '',
            'work_experience': [],
            'projects': [],
            'soft_skill_points': []
        }
        
        # 提取技能
        skill_section = re.search(r'(技能|Skills|技术栈)[：:]?\s*([^。\n]+)', resume_text, re.DOTALL)
        if skill_section:
            skills_text = skill_section.group(2)
            skills = re.findall(r'([\u4e00-\u9fa5A-Za-z0-9+]+(?:/\s*[\u4e00-\u9fa5A-Za-z0-9+]+)*)', skills_text)
            resume_info['skills'] = [s.strip() for s in skills if len(s.strip()) > 1]
        
        # 提取教育背景
        edu_matches = re.findall(r'([\u4e00-\u9fa5大学]+).*?([\u4e00-\u9fa5博士硕士本科专科]+).*?(\d{4}\.\d{2}-\d{4}\.\d{2})', resume_text)
        if edu_matches:
            for match in edu_matches:
                school, degree, period = match
                resume_info['education'] = degree
                # 简单判断学校档次
                if '香港大学' in school or '清华' in school or '北大' in school:
                    resume_info['school_tier'] = '985/QS前50'
                elif '985' in school or '华南理工' in school:
                    resume_info['school_tier'] = '985/QS前50'
                elif '211' in school:
                    resume_info['school_tier'] = '211/QS前100'
                break
        
        # 提取专业
        major_match = re.search(r'专业[：:]?\s*([\u4e00-\u9fa5]+)', resume_text)
        if major_match:
            resume_info['major'] = major_match.group(1).strip()
        
        # 提取实习/工作经历，计算总经验（实习3个月算0.25年正式经验）
        experience_pattern = re.compile(
            r'([\u4e00-\u9fa5公司企业证券百度腾讯阿里]+).*?(\d{4}\.\d{2})-(\d{4}\.\d{2})\n(.*?)(?=\n[\u4e00-\u9fa5公司企业]|\Z)', 
            re.DOTALL
        )
        experiences = experience_pattern.findall(resume_text)
        
        total_months = 0
        for exp in experiences:
            company, start, end, desc = exp
            # 计算时长
            try:
                start_year, start_month = map(int, start.split('.'))
                end_year, end_month = map(int, end.split('.'))
                months = (end_year - start_year) * 12 + (end_month - start_month)
                total_months += months
                # 提取软技能点
                desc = desc.strip()
                if '方案' in desc or '报告' in desc or '研究' in desc:
                    resume_info['soft_skill_points'].append('方案设计/报告撰写')
                if '沟通' in desc or '协作' in desc or '团队' in desc:
                    resume_info['soft_skill_points'].append('团队协作/沟通')
                if '云' in desc or '部署' in desc or '架构' in desc:
                    resume_info['skills'].append('云计算')
                    resume_info['skills'].append('架构设计')
            except:
                pass
        
        # 实习折算：3个月=0.25年
        resume_info['total_experience_years'] = round(total_months / 12 * 0.7, 2)  # 实习打7折折算正式经验
        
        return resume_info
    
    def calculate_hard_skill_score(self, jd_skills: List[str], resume_skills: List[str]) -> float:
        """计算硬技能匹配度，支持技能迁移"""
        if not jd_skills:
            return 80  # 无明确要求默认80分
        
        match_count = 0
        for jd_skill in jd_skills:
            # 直接匹配
            if any(jd_skill.lower() in s.lower() for s in resume_skills):
                match_count += 1
                continue
            
            # 技能迁移匹配
            migrated = False
            for category, related_skills in self.skill_migration.items():
                if jd_skill in category or category in jd_skill:
                    if any(s in related_skills or any(r.lower() in s.lower() for r in related_skills) for s in resume_skills):
                        match_count += 0.7  # 迁移匹配算0.7分
                        migrated = True
                        break
            if migrated:
                continue
        
        score = (match_count / len(jd_skills)) * 100
        return min(100, score)
    
    def calculate_experience_score(self, jd_required: float, resume_actual: float) -> float:
        """计算经验匹配度"""
        if jd_required == 0:
            return 100
        
        # 经验只要达到要求的70%就算合格
        ratio = resume_actual / jd_required
        if ratio >= 1.0:
            return 100
        elif ratio >= 0.7:
            return 80 + (ratio - 0.7) / 0.3 * 20
        elif ratio >= 0.5:
            return 60 + (ratio - 0.5) / 0.2 * 20
        else:
            return ratio * 120  # 经验不足但有相关经验给基础分
    
    def calculate_education_score(self, jd_required: str, resume_edu: str, school_tier: str, major: str) -> float:
        """计算学历匹配度，包含学校和专业加分"""
        # 基础学历分
        edu_rank = {
            '博士': 4, '硕士': 3, '本科': 2, '大专': 1, '': 0
        }
        jd_rank = edu_rank.get(jd_required, 2)  # 默认要求本科
        resume_rank = edu_rank.get(resume_edu, 0)
        
        base_score = 0
        if resume_rank >= jd_rank:
            base_score = 100
        elif resume_rank == jd_rank - 1:
            base_score = 70
        else:
            base_score = 40
        
        # 学校档次加分
        school_bonus = self.school_tier_scores.get(school_tier, 0)
        
        # 相关专业加分
        major_bonus = 0
        related_majors = ['计算机', '软件', '人工智能', '大数据', '电子商务', '信息', '电子']
        if any(m in major for m in related_majors):
            major_bonus = 5
        
        return min(100, base_score + school_bonus + major_bonus)
    
    def calculate_soft_skill_score(self, jd_soft_skills: List[str], resume_points: List[str]) -> float:
        """计算软技能匹配度"""
        # 默认软技能基础分60
        base_score = 60
        
        # 简历中的软技能点加分
        bonus = len(set(resume_points)) * 5
        
        return min(100, base_score + bonus)
    
    def calculate_match_score(self, jd_info: Dict, resume_info: Dict) -> Dict:
        """计算匹配度分数"""
        scores = {}
        
        # 1. 硬技能匹配度
        scores['hard_skills'] = self.calculate_hard_skill_score(
            jd_info.get('required_skills', []), 
            resume_info.get('skills', [])
        )
        
        # 2. 经验匹配度
        scores['experience'] = self.calculate_experience_score(
            jd_info.get('experience_years', 0),
            resume_info.get('total_experience_years', 0)
        )
        
        # 3. 学历匹配度
        scores['education'] = self.calculate_education_score(
            jd_info.get('education_requirements', '本科'),
            resume_info.get('education', ''),
            resume_info.get('school_tier', '普通本科'),
            resume_info.get('major', '')
        )
        
        # 4. 软技能匹配度
        scores['soft_skills'] = self.calculate_soft_skill_score(
            jd_info.get('soft_skills', []),
            resume_info.get('soft_skill_points', [])
        )
        
        # 计算加权总分
        total_score = 0
        for dimension, score in scores.items():
            total_score += score * self.skill_weights.get(dimension, 0)
        
        scores['total'] = round(total_score, 2)
        
        return scores
    
    def find_mismatches(self, jd_info: Dict, resume_info: Dict) -> List[Dict]:
        """找出不匹配点"""
        mismatches = []
        
        # 硬技能不匹配
        required_skills = set(jd_info.get('required_skills', []))
        resume_skills = set(resume_info.get('skills', []))
        
        for skill in required_skills:
            matched = False
            # 直接匹配
            if any(skill.lower() in s.lower() for s in resume_skills):
                matched = True
            else:
                # 迁移匹配
                for category, related_skills in self.skill_migration.items():
                    if skill in category or category in skill:
                        if any(s in related_skills or any(r.lower() in s.lower() for r in related_skills) for s in resume_skills):
                            matched = True
                            break
            
            if not matched:
                mismatches.append({
                    'category': 'hard_skills',
                    'type': 'missing_skill',
                    'description': f'缺少技能: {skill}',
                    'severity': 'medium',
                    'suggestion': f'建议补充{skill}相关知识或学习经历，可在简历中突出相关技能迁移能力'
                })
        
        # 经验不足
        jd_exp = jd_info.get('experience_years', 0)
        resume_exp = resume_info.get('total_experience_years', 0)
        
        if jd_exp > 0 and resume_exp < jd_exp * 0.7:
            mismatches.append({
                'category': 'experience',
                'type': 'insufficient_experience',
                'description': f'经验不足: 要求{jd_exp}年，折算后实际{resume_exp}年',
                'severity': 'medium',
                'suggestion': f'突出相关项目经验和实习成果，用数据量化贡献，强调快速学习能力'
            })
        
        # 学历不匹配
        edu_rank = {'博士':4, '硕士':3, '本科':2, '大专':1}
        jd_edu = jd_info.get('education_requirements', '本科')
        resume_edu = resume_info.get('education', '')
        jd_rank = edu_rank.get(jd_edu, 2)
        resume_rank = edu_rank.get(resume_edu, 0)
        
        if resume_rank < jd_rank -1:
            mismatches.append({
                'category': 'education',
                'type': 'education_mismatch',
                'description': f'学历要求: {jd_edu}, 实际: {resume_edu}',
                'severity': 'high',
                'suggestion': '突出实际工作能力和项目经验，用成果弥补学历差距'
            })
        
        return mismatches
    
    def generate_suggestions(self, jd_info: Dict, resume_info: Dict, mismatches: List[Dict]) -> List[Dict]:
        """生成改进建议"""
        suggestions = []
        
        # 根据不匹配点生成建议
        for mismatch in mismatches:
            if mismatch['category'] == 'hard_skills':
                suggestions.append({
                    'type': 'skill_improvement',
                    'priority': 'high' if mismatch['severity'] == 'high' else 'medium',
                    'action': mismatch['suggestion'],
                    'timeline': '短期（1-3个月）'
                })
            elif mismatch['category'] == 'experience':
                suggestions.append({
                    'type': 'experience_highlight',
                    'priority': 'medium',
                    'action': '调整简历描述，突出和岗位相关的经验，用量化成果体现能力',
                    'timeline': '立即'
                })
            elif mismatch['category'] == 'education':
                suggestions.append({
                    'type': 'education_compensation',
                    'priority': 'medium',
                    'action': '在简历中突出相关证书、培训或项目经验，弥补学历差距',
                    'timeline': '中期（3-6个月）'
                })
        
        # 通用建议
        suggestions.append({
            'type': 'resume_optimization',
            'priority': 'high',
            'action': '优化简历关键词，和JD要求对齐，突出匹配点',
            'timeline': '立即'
        })
        
        # 个性化建议
        if '云计算' in jd_info.get('required_skills', []) and any('云' in s for s in resume_info.get('skills', [])):
            suggestions.append({
                'type': 'highlight_advantage',
                'priority': 'high',
                'action': '突出云计算相关经验，结合岗位要求说明适配性',
                'timeline': '立即'
            })
        
        return suggestions
    
    def analyze(self, jd_text: str, resume_text: str) -> Dict:
        """完整的分析流程"""
        logger.info("开始解析JD信息...")
        jd_info = self.extract_jd_info(jd_text)
        
        logger.info("开始解析简历信息...")
        resume_info = self.extract_resume_info(resume_text)
        
        logger.info("计算匹配度分数...")
        scores = self.calculate_match_score(jd_info, resume_info)
        
        logger.info("查找不匹配点...")
        mismatches = self.find_mismatches(jd_info, resume_info)
        
        logger.info("生成改进建议...")
        suggestions = self.generate_suggestions(jd_info, resume_info, mismatches)
        
        result = {
            'jd_info': jd_info,
            'resume_info': resume_info,
            'scores': scores,
            'mismatches': mismatches,
            'suggestions': suggestions,
            'summary': {
                'overall_score': scores['total'],
                'match_level': self._get_match_level(scores['total']),
                'key_issues': len([m for m in mismatches if m['severity'] in ['high', 'medium']]),
                'strong_points': self._find_strong_points(jd_info, resume_info)
            }
        }
        
        return result
    
    def _get_match_level(self, score: float) -> str:
        """根据分数获取匹配等级"""
        if score >= 85:
            return "优秀匹配 ✅"
        elif score >= 70:
            return "良好匹配 ⭐"
        elif score >= 50:
            return "一般匹配 ⚠️"
        else:
            return "匹配度较低 ❌"
    
    def _find_strong_points(self, jd_info: Dict, resume_info: Dict) -> List[str]:
        """找出简历优势点"""
        strong_points = []
        
        # 经验优势
        jd_exp = jd_info.get('experience_years', 0)
        resume_exp = resume_info.get('total_experience_years', 0)
        if resume_exp >= jd_exp * 0.7:
            strong_points.append(f"经验符合要求：折算后{resume_exp}年，接近要求的{jd_exp}年")
        
        # 学历优势
        edu_rank = {'博士':4, '硕士':3, '本科':2, '大专':1}
        jd_edu = jd_info.get('education_requirements', '本科')
        resume_edu = resume_info.get('education', '')
        jd_rank = edu_rank.get(jd_edu, 2)
        resume_rank = edu_rank.get(resume_edu, 0)
        if resume_rank >= jd_rank:
            strong_points.append(f"学历背景优秀：{resume_edu}，学校档次{resume_info.get('school_tier', '普通')}，符合要求")
        
        # 技能优势
        hard_score = self.calculate_hard_skill_score(jd_info.get('required_skills', []), resume_info.get('skills', []))
        if hard_score >= 70:
            strong_points.append(f"硬技能匹配度高：相关技能掌握良好，可迁移性强")
        
        # 软技能优势
        soft_points = resume_info.get('soft_skill_points', [])
        if len(soft_points) >= 2:
            strong_points.append(f"软技能优秀：具备{'/'.join(soft_points)}能力，适配岗位要求")
        
        return strong_points


def main():
    """主函数"""
    analyzer = ResumeJDAnalyzer()
    
    # 示例JD和简历
    jd_text = """
    职位：Python后端开发工程师
    岗位职责：
    1. 负责公司核心业务系统的后端开发
    2. 设计和实现高可用、高性能的API接口
    3. 优化系统性能，提升用户体验
    
    任职要求：
    1. 本科及以上学历，计算机相关专业
    2. 3年以上Python开发经验
    3. 熟练掌握Django/Flask框架
    4. 熟悉MySQL数据库设计和优化
    5. 了解Redis、消息队列等中间件
    6. 有良好的团队协作和沟通能力
    """
    
    resume_text = """
    个人简历
    
    姓名：张三
    学历：硕士
    学校：清华大学
    专业：计算机科学与技术
    
    工作经验：2年Python开发经验
    
    技能：
    Python、Django、MySQL、Redis、Git、云计算
    
    项目经验：
    1. 电商平台后端开发，负责API设计和实现
    2. 用户管理系统，优化数据库性能提升30%
    """
    
    result = analyzer.analyze(jd_text, resume_text)
    
    # 输出结果
    print("=" * 50)
    print("📋 简历-JD匹配度分析报告（V2.0）")
    print("=" * 50)
    print(f"\n🎯 整体匹配度: {result['summary']['overall_score']}/100")
    print(f"⭐ 匹配等级: {result['summary']['match_level']}")
    print(f"⚠️ 关键问题数: {result['summary']['key_issues']}")
    
    print("\n✅ 优势亮点:")
    for point in result['summary']['strong_points']:
        print(f"  - {point}")
    
    print("\n📊 各维度得分:")
    score_map = {
        'hard_skills': ('硬技能匹配', 0.35),
        'experience': ('经验匹配', 0.30),
        'education': ('学历/证书匹配', 0.15),
        'soft_skills': ('软技能匹配', 0.20)
    }
    for dimension, score in result['scores'].items():
        if dimension != 'total':
            name, weight = score_map.get(dimension, (dimension, 0))
            emoji = '✅' if score >= 80 else '⚠️' if score >= 60 else '❌'
            print(f'  {emoji} {name}: {score:.1f}/100 (权重: {weight*100:.0f}%)')
    
    print("\n🔍 不匹配点分析:")
    for mismatch in result['mismatches']:
        severity_emoji = "🔴" if mismatch['severity'] == 'high' else "🟡" if mismatch['severity'] == 'medium' else "🔵"
        print(f"  {severity_emoji} {mismatch['description']}")
        print(f"     💡 建议: {mismatch['suggestion']}")
    
    print("\n📝 改进建议:")
    for suggestion in result['suggestions']:
        priority_emoji = "🔥" if suggestion['priority'] == 'high' else "⚠️" if suggestion['priority'] == 'medium' else "💡"
        print(f"  {priority_emoji} {suggestion['action']} ({suggestion['timeline']})")


if __name__ == "__main__":
    main()