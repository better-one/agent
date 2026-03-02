#!/usr/bin/env python3
"""云存档系统 v1.17.0"""
import json
from datetime import datetime
from pathlib import Path

class CloudSave:
    def __init__(self, save_file="cloud_save.json"):
        self.save_file = Path(save_file)
        self.cloud_data = self.load()
    
    def load(self):
        if self.save_file.exists():
            with open(self.save_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"saves": [], "last_sync": None}
    
    def save(self):
        self.save_file.parent.mkdir(exist_ok=True)
        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump(self.cloud_data, f, indent=2, ensure_ascii=False)
    
    def create_save(self, player_name, score, level, stats):
        save_data = {
            "id": len(self.cloud_data["saves"]) + 1,
            "player": player_name,
            "score": score,
            "level": level,
            "stats": stats,
            "date": datetime.now().isoformat(),
            "version": "1.17.0"
        }
        self.cloud_data["saves"].append(save_data)
        self.cloud_data["last_sync"] = datetime.now().isoformat()
        self.save()
        return save_data["id"]
    
    def list_saves(self):
        print("\n☁️ 云存档列表:")
        for save in self.cloud_data["saves"]:
            print(f"  #{save['id']} - {save['player']} | Lv.{save['level']} | {save['score']}分 | {save['date'][:16]}")
        if self.cloud_data["last_sync"]:
            print(f"\n最后同步：{self.cloud_data['last_sync'][:19]}")
    
    def load_save(self, save_id):
        for save in self.cloud_data["saves"]:
            if save["id"] == save_id:
                print(f"\n📥 读取存档 #{save_id}")
                print(f"   玩家：{save['player']}")
                print(f"   分数：{save['score']}")
                print(f"   关卡：{save['level']}")
                return save
        return None

print("☁️ v1.17.0 - 云存档系统")
cs = CloudSave()
cs.create_save("Player1", 450, 5, {"games": 10, "best": 450})
cs.create_save("Player2", 520, 6, {"games": 15, "best": 520})
cs.list_saves()
