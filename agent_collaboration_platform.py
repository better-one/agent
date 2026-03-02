#!/usr/bin/env python3
"""
智能体协作平台 v1.0
支持多智能体之间的沟通、协作和版本管理
"""

import json
import uuid
from pathlib import Path
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional

class MessageType(Enum):
    REQUEST = "请求"
    RESPONSE = "响应"
    NOTIFICATION = "通知"
    TASK_ASSIGN = "任务分配"
    TASK_COMPLETE = "任务完成"
    DISCUSSION = "讨论"
    DECISION = "决策"

class AgentMessage:
    """智能体消息"""
    def __init__(self, from_agent: str, to_agent: str, msg_type: MessageType, content: str):
        self.id = str(uuid.uuid4())[:8]
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.type = msg_type
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.version = "1.0"
        self.replies = []
        self.status = "pending"
    
    def to_dict(self):
        return {
            'id': self.id,
            'from': self.from_agent,
            'to': self.to_agent,
            'type': self.type.value,
            'content': self.content,
            'timestamp': self.timestamp,
            'version': self.version,
            'replies': self.replies,
            'status': self.status
        }
    
    def __str__(self):
        return f"[{self.type.value}] {self.from_agent} → {self.to_agent}: {self.content[:50]}..."

class CollaborationRoom:
    """协作会议室"""
    def __init__(self, name: str, participants: List[str]):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.participants = participants
        self.messages = []
        self.created_at = datetime.now().isoformat()
        self.topic = ""
        self.status = "active"
    
    def add_message(self, message: AgentMessage):
        self.messages.append(message)
    
    def get_conversation_history(self):
        return [m.to_dict() for m in self.messages]
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'participants': self.participants,
            'message_count': len(self.messages),
            'topic': self.topic,
            'status': self.status,
            'created_at': self.created_at
        }

class AgentCollaborationPlatform:
    """智能体协作平台"""
    
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.rooms: Dict[str, CollaborationRoom] = {}
        self.messages: List[AgentMessage] = []
        self.agents_registry = []
        self.collaboration_history = []
        
        # 注册智能体
        self.register_agents()
    
    def register_agents(self):
        """注册所有智能体"""
        self.agents_registry = [
            "产品经理",
            "架构师",
            "测试工程师",
            "UI/UX设计师",
            "安全工程师",
            "运维工程师",
            "性能优化专家",
            "技术文档工程师",
            "代码审查员",
            "数据分析师",
            "发布经理"
        ]
        print(f"✅ 已注册 {len(self.agents_registry)} 个智能体")
    
    def create_room(self, name: str, participants: List[str], topic: str = "") -> str:
        """创建协作会议室"""
        room = CollaborationRoom(name, participants)
        room.topic = topic
        self.rooms[room.id] = room
        
        # 发送创建通知
        for agent in participants:
            self.send_message(
                from_agent="系统",
                to_agent=agent,
                msg_type=MessageType.NOTIFICATION,
                content=f"邀请你加入会议室「{name}」，主题：{topic}"
            )
        
        print(f"🏠 创建会议室：{name} (ID: {room.id})")
        print(f"   参与者：{', '.join(participants)}")
        print(f"   主题：{topic}")
        
        return room.id
    
    def send_message(self, from_agent: str, to_agent: str, msg_type: MessageType, content: str) -> str:
        """发送消息"""
        message = AgentMessage(from_agent, to_agent, msg_type, content)
        self.messages.append(message)
        
        # 如果在会议室中，添加到会议室消息
        for room in self.rooms.values():
            if from_agent in room.participants and to_agent in room.participants:
                room.add_message(message)
        
        print(f"💬 {message}")
        return message.id
    
    def create_task_force(self, task_name: str, lead_agent: str, members: List[str]) -> str:
        """创建任务小组"""
        participants = [lead_agent] + members
        room_id = self.create_room(
            name=f"任务组：{task_name}",
            participants=participants,
            topic=f"任务负责人：{lead_agent}"
        )
        
        # 分配任务
        self.send_message(
            from_agent="系统",
            to_agent=lead_agent,
            msg_type=MessageType.TASK_ASSIGN,
            content=f"你被任命为「{task_name}」任务负责人，团队成员：{', '.join(members)}"
        )
        
        for member in members:
            self.send_message(
                from_agent="系统",
                to_agent=member,
                msg_type=MessageType.TASK_ASSIGN,
                content=f"你被分配到「{task_name}」任务组，负责人：{lead_agent}"
            )
        
        return room_id
    
    def start_discussion(self, room_id: str, initiator: str, topic: str):
        """发起讨论"""
        room = self.rooms.get(room_id)
        if not room:
            print(f"❌ 会议室不存在：{room_id}")
            return
        
        print(f"\n💭 发起讨论：{topic}")
        print(f"   发起人：{initiator}")
        print(f"   会议室：{room.name}")
        
        self.send_message(
            from_agent=initiator,
            to_agent="all",
            msg_type=MessageType.DISCUSSION,
            content=f"【讨论】{topic}"
        )
    
    def make_decision(self, room_id: str, decision_maker: str, decision: str):
        """做出决策"""
        room = self.rooms.get(room_id)
        if not room:
            return
        
        print(f"\n✅ 决策：{decision}")
        print(f"   决策者：{decision_maker}")
        
        self.send_message(
            from_agent=decision_maker,
            to_agent="all",
            msg_type=MessageType.DECISION,
            content=f"【决策】{decision}"
        )
    
    def simulate_collaboration(self):
        """模拟智能体协作场景"""
        print("\n" + "="*60)
        print("🤖 智能体协作模拟")
        print("="*60)
        
        # 场景 1: 新功能开发协作
        print("\n📋 场景 1: v2.0 新功能开发")
        room1 = self.create_task_force(
            task_name="v2.0 新功能开发",
            lead_agent="产品经理",
            members=["架构师", "UI/UX设计师", "测试工程师"]
        )
        
        # 模拟讨论
        self.start_discussion(room1, "产品经理", "v2.0 需要哪些新功能？")
        
        # 智能体间沟通
        self.send_message("产品经理", "架构师", MessageType.REQUEST, "请评估在线多人功能的可行性")
        self.send_message("架构师", "产品经理", MessageType.RESPONSE, "技术可行，预计需要 3 天开发")
        self.send_message("产品经理", "UI/UX设计师", MessageType.REQUEST, "请设计多人模式的界面")
        self.send_message("UI/UX设计师", "产品经理", MessageType.RESPONSE, "原型图已完成，请查看")
        self.send_message("产品经理", "测试工程师", MessageType.REQUEST, "请制定测试计划")
        
        # 决策
        self.make_decision(room1, "产品经理", "v2.0 包含：在线多人、皮肤商城、排行榜 2.0")
        
        # 场景 2: Bug 修复协作
        print("\n\n🐛 场景 2: 紧急 Bug 修复")
        room2 = self.create_task_force(
            task_name="紧急 Bug 修复 #1234",
            lead_agent="测试工程师",
            members=["架构师", "安全工程师", "发布经理"]
        )
        
        self.start_discussion(room2, "测试工程师", "发现严重安全漏洞，需要紧急修复")
        self.send_message("测试工程师", "安全工程师", MessageType.REQUEST, "请分析漏洞影响范围")
        self.send_message("安全工程师", "架构师", MessageType.REQUEST, "请提供修复方案")
        self.send_message("架构师", "发布经理", MessageType.NOTIFICATION, "预计 2 小时后发布热修复")
        self.make_decision(room2, "发布经理", "启动紧急发布流程，30 分钟内上线")
        
        # 场景 3: 性能优化协作
        print("\n\n⚡ 场景 3: 性能优化专项")
        room3 = self.create_task_force(
            task_name="性能优化专项",
            lead_agent="性能优化专家",
            members=["架构师", "运维工程师", "数据分析师"]
        )
        
        self.start_discussion(room3, "性能优化专家", "目标：帧率从 60 提升到 90 FPS")
        self.send_message("性能优化专家", "数据分析师", MessageType.REQUEST, "请分析性能瓶颈数据")
        self.send_message("数据分析师", "性能优化专家", MessageType.RESPONSE, "主要瓶颈：渲染占用 45%，逻辑占用 30%")
        self.send_message("性能优化专家", "架构师", MessageType.REQUEST, "请优化渲染架构")
        self.send_message("架构师", "运维工程师", MessageType.NOTIFICATION, "部署性能监控")
        self.make_decision(room3, "性能优化专家", "采用批处理渲染，目标 90 FPS")
        
        # 生成协作报告
        self.generate_collaboration_report()
    
    def generate_collaboration_report(self):
        """生成协作报告"""
        print("\n" + "="*60)
        print("📊 协作报告")
        print("="*60)
        
        total_messages = len(self.messages)
        total_rooms = len(self.rooms)
        
        print(f"\n会议室数量：{total_rooms}")
        print(f"总消息数：{total_messages}")
        
        # 消息类型统计
        msg_types = {}
        for msg in self.messages:
            t = msg.type.value
            msg_types[t] = msg_types.get(t, 0) + 1
        
        print(f"\n消息类型分布:")
        for t, count in msg_types.items():
            bar = "█" * (count // 2)
            print(f"  {t:8} {count:3} {bar}")
        
        # 智能体活跃度
        agent_activity = {}
        for msg in self.messages:
            agent = msg.from_agent
            agent_activity[agent] = agent_activity.get(agent, 0) + 1
        
        print(f"\n智能体活跃度:")
        sorted_agents = sorted(agent_activity.items(), key=lambda x: x[1], reverse=True)
        for agent, count in sorted_agents:
            bar = "█" * (count // 2)
            print(f"  {agent:12} {count:3} {bar}")
        
        # 保存报告
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_rooms': total_rooms,
            'total_messages': total_messages,
            'rooms': [r.to_dict() for r in self.rooms.values()],
            'messages': [m.to_dict() for m in self.messages],
            'agent_activity': agent_activity
        }
        
        report_file = self.project_dir / "collaboration_reports" / f"collaboration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 协作报告已保存：{report_file}")

if __name__ == '__main__':
    platform = AgentCollaborationPlatform(Path('/home/firefly/snake_game'))
    platform.simulate_collaboration()
