#!/usr/bin/env python3
"""游戏回放系统 v1.15.0"""
import json
from datetime import datetime

class ReplaySystem:
    def __init__(self):
        self.replays = []
    
    def record_move(self, snake_pos, food_pos, direction, timestamp):
        return {
            "snake": snake_pos,
            "food": food_pos,
            "direction": direction,
            "time": timestamp
        }
    
    def save_replay(self, moves, score, level):
        replay = {
            "id": len(self.replays) + 1,
            "date": datetime.now().isoformat(),
            "score": score,
            "level": level,
            "moves": moves,
            "duration": len(moves)
        }
        self.replays.append(replay)
        return replay["id"]
    
    def list_replays(self):
        print("\n🎬 回放列表:")
        for replay in self.replays:
            print(f"  #{replay['id']} - {replay['date'][:16]} | 分数：{replay['score']} | 关卡：{replay['level']} | 步数：{replay['duration']}")
    
    def play_replay(self, replay_id):
        for replay in self.replays:
            if replay["id"] == replay_id:
                print(f"\n▶️ 回放 #{replay_id}")
                print(f"   日期：{replay['date']}")
                print(f"   分数：{replay['score']}")
                print(f"   总步数：{replay['duration']}")
                return replay["moves"]
        return None

print("🎥 v1.15.0 - 回放系统")
rs = ReplaySystem()
moves = [rs.record_move((i,5), (10,10), (1,0), i) for i in range(100)]
rs.save_replay(moves, 350, 3)
rs.save_replay(moves, 420, 4)
rs.list_replays()
