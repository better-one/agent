#!/usr/bin/env python3
"""
智能体版本控制系统
管理智能体的版本迭代和协作历史
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class AgentVersion:
    """智能体版本"""
    def __init__(self, agent_name: str, version: str, changes: List[str]):
        self.agent_name = agent_name
        self.version = version
        self.changes = changes
        self.timestamp = datetime.now().isoformat()
        self.checksum = hashlib.md5(f"{agent_name}{version}{self.timestamp}".encode()).hexdigest()[:8]
    
    def to_dict(self):
        return {
            'agent': self.agent_name,
            'version': self.version,
            'changes': self.changes,
            'timestamp': self.timestamp,
            'checksum': self.checksum
        }

class CollaborationSession:
    """协作会话"""
    def __init__(self, session_id: str, participants: List[str], topic: str):
        self.session_id = session_id
        self.participants = participants
        self.topic = topic
        self.start_time = datetime.now().isoformat()
        self.end_time = None
        self.messages = []
        self.decisions = []
        self.outputs = []
    
    def add_message(self, message: dict):
        self.messages.append(message)
    
    def add_decision(self, decision: str):
        self.decisions.append({
            'content': decision,
            'timestamp': datetime.now().isoformat()
        })
    
    def end_session(self):
        self.end_time = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'session_id': self.session_id,
            'topic': self.topic,
            'participants': self.participants,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'message_count': len(self.messages),
            'decision_count': len(self.decisions),
            'outputs': self.outputs
        }

class AgentVersionControl:
    """智能体版本控制"""
    
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.versions_dir = project_dir / "agent_versions"
        self.sessions_dir = project_dir / "collaboration_sessions"
        self.versions_dir.mkdir(exist_ok=True)
        self.sessions_dir.mkdir(exist_ok=True)
        
        self.agent_versions: Dict[str, List[AgentVersion]] = {}
        self.sessions: Dict[str, CollaborationSession] = {}
        
        # 初始化版本
        self.initialize_versions()
    
    def initialize_versions(self):
        """初始化所有智能体版本"""
        agents = [
            "产品经理", "架构师", "测试工程师", "UI/UX设计师",
            "安全工程师", "运维工程师", "性能优化专家",
            "技术文档工程师", "代码审查员", "数据分析师", "发布经理"
        ]
        
        for agent in agents:
            v1 = AgentVersion(agent, "v1.0.0", ["初始版本"])
            self.agent_versions[agent] = [v1]
        
        print(f"✅ 初始化 {len(agents)} 个智能体版本")
    
    def create_version(self, agent_name: str, new_version: str, changes: List[str]) -> AgentVersion:
        """创建新版本"""
        if agent_name not in self.agent_versions:
            print(f"❌ 智能体不存在：{agent_name}")
            return None
        
        version = AgentVersion(agent_name, new_version, changes)
        self.agent_versions[agent_name].append(version)
        
        print(f"📦 {agent_name} 发布新版本：{new_version}")
        for change in changes:
            print(f"   + {change}")
        
        # 保存版本信息
        self.save_agent_versions(agent_name)
        
        return version
    
    def start_collaboration_session(self, topic: str, participants: List[str]) -> str:
        """开始协作会话"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session = CollaborationSession(session_id, participants, topic)
        self.sessions[session_id] = session
        
        print(f"\n🤝 开始协作会话：{session_id}")
        print(f"   主题：{topic}")
        print(f"   参与者：{', '.join(participants)}")
        
        return session_id
    
    def record_collaboration_message(self, session_id: str, from_agent: str, to_agent: str, content: str, msg_type: str):
        """记录协作消息"""
        if session_id not in self.sessions:
            return
        
        message = {
            'from': from_agent,
            'to': to_agent,
            'content': content,
            'type': msg_type,
            'timestamp': datetime.now().isoformat()
        }
        
        self.sessions[session_id].add_message(message)
    
    def record_decision(self, session_id: str, decision: str):
        """记录决策"""
        if session_id in self.sessions:
            self.sessions[session_id].add_decision(decision)
            print(f"   ✅ 决策：{decision}")
    
    def end_collaboration_session(self, session_id: str, outputs: List[str]):
        """结束协作会话"""
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        session.outputs = outputs
        session.end_session()
        
        print(f"\n✅ 协作会话结束：{session_id}")
        print(f"   消息数：{len(session.messages)}")
        print(f"   决策数：{len(session.decisions)}")
        print(f"   产出：{len(outputs)} 项")
        
        # 保存会话记录
        self.save_session(session)
    
    def save_agent_versions(self, agent_name: str):
        """保存智能体版本历史"""
        versions = [v.to_dict() for v in self.agent_versions.get(agent_name, [])]
        version_file = self.versions_dir / f"{agent_name}_versions.json"
        
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump({
                'agent': agent_name,
                'current_version': versions[-1] if versions else None,
                'version_history': versions
            }, f, ensure_ascii=False, indent=2)
    
    def save_session(self, session: CollaborationSession):
        """保存协作会话"""
        session_file = self.sessions_dir / f"{session.session_id}.json"
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session.to_dict(), f, ensure_ascii=False, indent=2)
    
    def generate_version_report(self):
        """生成版本报告"""
        print("\n" + "="*60)
        print("📊 智能体版本报告")
        print("="*60)
        
        print(f"\n智能体数量：{len(self.agent_versions)}")
        print(f"协作会话数：{len(self.sessions)}")
        
        print(f"\n版本历史:")
        for agent, versions in self.agent_versions.items():
            latest = versions[-1]
            print(f"\n  {agent}:")
            print(f"    当前版本：{latest.version}")
            print(f"    版本数：{len(versions)}")
            if len(versions) > 1:
                print(f"    最近更新：{latest.timestamp[:16]}")
                print(f"    变更：{', '.join(latest.changes[:3])}")
        
        # 保存报告
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_agents': len(self.agent_versions),
            'total_sessions': len(self.sessions),
            'agents': {
                agent: [v.to_dict() for v in versions]
                for agent, versions in self.agent_versions.items()
            },
            'sessions': {
                sid: session.to_dict()
                for sid, session in self.sessions.items()
            }
        }
        
        report_file = self.project_dir / "version_reports" / f"version_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 版本报告已保存")

if __name__ == '__main__':
    vcs = AgentVersionControl(Path('/home/firefly/snake_game'))
    
    # 模拟版本迭代
    print("\n" + "="*60)
    print("📦 模拟版本迭代")
    print("="*60)
    
    vcs.create_version("产品经理", "v1.1.0", ["增加 RICE 评分模型", "添加市场分析模块"])
    vcs.create_version("架构师", "v1.1.0", ["集成自动化审查", "增加架构模式库"])
    vcs.create_version("测试工程师", "v1.1.0", ["引入模糊测试", "增加边界测试用例"])
    
    # 模拟协作会话
    print("\n" + "="*60)
    print("🤝 模拟协作会话")
    print("="*60)
    
    session_id = vcs.start_collaboration_session(
        topic="v2.0 在线多人功能设计",
        participants=["产品经理", "架构师", "UI/UX设计师"]
    )
    
    vcs.record_collaboration_message(session_id, "产品经理", "架构师", "请评估技术可行性", "请求")
    vcs.record_collaboration_message(session_id, "架构师", "产品经理", "可行，需 3 天", "响应")
    vcs.record_collaboration_message(session_id, "产品经理", "UI/UX设计师", "请设计界面", "请求")
    vcs.record_decision(session_id, "采用 WebSocket 实现实时通信")
    vcs.record_decision(session_id, "UI 采用分屏设计")
    
    vcs.end_collaboration_session(session_id, ["技术架构图", "UI 原型", "开发计划"])
    
    # 生成报告
    vcs.generate_version_report()
