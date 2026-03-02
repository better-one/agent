#!/usr/bin/env python3
"""统计追踪系统 v1.14.0"""
import json
from datetime import datetime

class StatsTracker:
    def __init__(self):
        self.stats = {
            "total_games": 0,
            "total_score": 0,
            "best_score": 0,
            "total_time": 0,
            "items_eaten": 0,
            "golden_foods": 0,
            "walls_passed": 0,
            "levels_completed": 0,
            "dual_wins": 0,
            "achievements_unlocked": 0,
        }
        self.session_stats = {}
    
    def record_game(self, score, time_played, items=0, golden=0):
        self.stats["total_games"] += 1
        self.stats["total_score"] += score
        if score > self.stats["best_score"]:
            self.stats["best_score"] = score
        self.stats["total_time"] += time_played
        self.stats["items_eaten"] += items
        self.stats["golden_foods"] += golden
    
    def get_summary(self):
        avg_score = self.stats["total_score"] / max(self.stats["total_games"], 1)
        return {
            "总游戏次数": self.stats["total_games"],
            "总分数": self.stats["total_score"],
            "最高分": self.stats["best_score"],
            "平均分数": f"{avg_score:.1f}",
            "总时长 (秒)": self.stats["total_time"],
            "道具吃掉": self.stats["items_eaten"],
            "金色食物": self.stats["golden_foods"],
        }
    
    def display(self):
        print("\n📊 统计信息:")
        for k, v in self.get_summary().items():
            print(f"  {k}: {v}")

print("📈 v1.14.0 - 统计系统")
st = StatsTracker()
st.record_game(350, 300, 5, 2)
st.record_game(420, 400, 8, 3)
st.display()
