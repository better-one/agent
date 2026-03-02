#!/usr/bin/env python3
"""商店系统 v1.13.0"""
import json

class ShopSystem:
    def __init__(self):
        self.items = {
            "skins": [
                {"id": "fire", "name": "火焰皮肤", "price": 500},
                {"id": "ice", "name": "冰雪皮肤", "price": 500},
                {"id": "gold", "name": "黄金皮肤", "price": 1000},
            ],
            "effects": [
                {"id": "double_1h", "name": "双倍分数 1 小时", "price": 100},
                {"id": "exp_boost", "name": "经验加成", "price": 200},
            ],
            "powerups": [
                {"id": "extra_life", "name": "额外生命", "price": 300},
                {"id": "shield", "name": "护盾", "price": 150},
            ]
        }
        self.player_coins = 1000
        self.inventory = []
    
    def buy(self, item_id):
        for category, items in self.items.items():
            for item in items:
                if item["id"] == item_id:
                    if self.player_coins >= item["price"]:
                        self.player_coins -= item["price"]
                        self.inventory.append(item_id)
                        return True, f"购买成功！剩余金币：{self.player_coins}"
                    else:
                        return False, "金币不足"
        return False, "商品不存在"
    
    def display_shop(self):
        print(f"\n🛒 商店 (金币：{self.player_coins})")
        for category, items in self.items.items():
            print(f"\n{category.upper()}:")
            for item in items:
                in_inv = "✓" if item["id"] in self.inventory else " "
                print(f"  [{in_inv}] {item['name']} - {item['price']}金币")

print("🛍️ v1.13.0 - 商店系统")
shop = ShopSystem()
shop.display_shop()
