#!/usr/bin/env python3
"""每日挑战系统 v1.11.0"""
from datetime import datetime, timedelta
import random

class DailyChallenge:
    def __init__(self):
        self.challenges = [
            {"name": "速度挑战", "desc": "在 20 FPS 下达到 300 分", "reward": 100},
            {"name": "无道具挑战", "desc": "不吃道具达到 250 分", "reward": 80},
            {"name": "穿墙大师", "desc": "使用穿墙道具通过 20 次墙", "reward": 120},
            {"name": "美食家", "desc": "吃到 30 个金色食物", "reward": 150},
            {"name": "生存专家", "desc": "存活超过 8 分钟", "reward": 100},
        ]
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.daily_challenge = self.get_today_challenge()
    
    def get_today_challenge(self):
        seed = int(self.today.replace("-", ""))
        random.seed(seed)
        return random.choice(self.challenges)
    
    def check_complete(self, stats):
        challenge = self.daily_challenge
        completed = False
        if "速度" in challenge["name"] and stats.get("fps", 0) >= 20 and stats.get("score", 0) >= 300:
            completed = True
        elif "无道具" in challenge["name"] and stats.get("items_eaten", 0) == 0 and stats.get("score", 0) >= 250:
            completed = True
        return completed, challenge

print("📅 v1.11.0 - 每日挑战系统")
dc = DailyChallenge()
print(f"今日挑战：{dc.daily_challenge['name']} - {dc.daily_challenge['desc']}")
print(f"奖励：{dc.daily_challenge['reward']}金币")
