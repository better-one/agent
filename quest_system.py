#!/usr/bin/env python3
"""任务系统 v1.12.0"""
import json

class QuestSystem:
    def __init__(self):
        self.quests = {
            "daily": [
                {"id": "d1", "name": "新手任务", "desc": "玩一局游戏", "target": 1, "reward": 50},
                {"id": "d2", "name": "得分高手", "desc": "单局达到 200 分", "target": 200, "reward": 80},
                {"id": "d3", "name": "收藏家", "desc": "收集 10 个道具", "target": 10, "reward": 60},
            ],
            "weekly": [
                {"id": "w1", "name": "周常挑战", "desc": "累计 1000 分", "target": 1000, "reward": 300},
                {"id": "w2", "name": "胜利大师", "desc": "双人模式获胜 5 次", "target": 5, "reward": 400},
            ],
            "achievement": [
                {"id": "a1", "name": "传奇之路", "desc": "达到 500 分", "target": 500, "reward": 1000},
            ]
        }
        self.progress = {}
    
    def accept_quest(self, quest_id):
        self.progress[quest_id] = 0
        return f"接受任务：{quest_id}"
    
    def update_progress(self, quest_id, value):
        if quest_id in self.progress:
            self.progress[quest_id] = value
            return self.check_complete(quest_id)
        return None
    
    def check_complete(self, quest_id):
        for q_type, quests in self.quests.items():
            for quest in quests:
                if quest["id"] == quest_id:
                    if self.progress.get(quest_id, 0) >= quest["target"]:
                        return True, quest["reward"]
        return False, 0
    
    def list_quests(self):
        print("\n📜 任务列表:")
        for q_type, quests in self.quests.items():
            print(f"\n{q_type.upper()}:")
            for quest in quests:
                prog = self.progress.get(quest["id"], 0)
                print(f"  {quest['name']}: {prog}/{quest['target']} - 奖励：{quest['reward']}金币")

print("⚔️ v1.12.0 - 任务系统")
qs = QuestSystem()
qs.list_quests()
