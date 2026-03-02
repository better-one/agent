#!/usr/bin/env python3
"""皮肤编辑器 v1.10.0 - 自定义你的贪吃蛇"""
import json
from pathlib import Path
from datetime import datetime

class SkinEditor:
    """皮肤编辑器"""
    def __init__(self, skins_file='custom_skins.json'):
        self.skins_file = Path(skins_file)
        self.custom_skins = self.load()
    
    def load(self):
        if self.skins_file.exists():
            with open(self.skins_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save(self):
        self.skins_file.parent.mkdir(exist_ok=True)
        with open(self.skins_file, 'w', encoding='utf-8') as f:
            json.dump(self.custom_skins, f, indent=2, ensure_ascii=False)
    
    def create_skin(self, name, snake_head, snake_body, food_color, bg_color, grid_color=(40,40,40)):
        """创建自定义皮肤"""
        skin_id = f"custom_{name.lower().replace(' ', '_')}"
        self.custom_skins[skin_id] = {
            'name': name,
            'snake_head': snake_head,
            'snake_body': snake_body,
            'food': food_color,
            'bg': bg_color,
            'grid': grid_color,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'author': 'Player'
        }
        self.save()
        return skin_id
    
    def delete_skin(self, skin_id):
        """删除皮肤"""
        if skin_id in self.custom_skins:
            del self.custom_skins[skin_id]
            self.save()
            return True
        return False
    
    def list_skins(self):
        """列出所有皮肤"""
        print(f"\n{'='*60}")
        print(f"🎨 自定义皮肤 ({len(self.custom_skins)}个)")
        print(f"{'='*60}")
        for skin_id, skin in self.custom_skins.items():
            print(f"\n{skin_id}:")
            print(f"  名称：{skin['name']}")
            print(f"  蛇头：RGB{skin['snake_head']}")
            print(f"  蛇身：RGB{skin['snake_body']}")
            print(f"  食物：RGB{skin['food']}")
            print(f"  背景：RGB{skin['bg']}")
            print(f"  创建：{skin['created']}")
        print(f"{'='*60}\n")
        return list(self.custom_skins.keys())
    
    def preview_colors(self, skin_id):
        """预览颜色"""
        if skin_id not in self.custom_skins:
            return None
        skin = self.custom_skins[skin_id]
        return {
            'snake_head': tuple(skin['snake_head']),
            'snake_body': tuple(skin['snake_body']),
            'food': tuple(skin['food']),
            'bg': tuple(skin['bg'])
        }

if __name__ == '__main__':
    print("🎨 v1.10.0 - 皮肤编辑器")
    editor = SkinEditor()
    
    # 创建几个示例皮肤
    print("\n创建示例皮肤...")
    
    editor.create_skin(
        name="火焰",
        snake_head=(255, 100, 0),
        snake_body=(255, 200, 50),
        food_color=(255, 50, 50),
        bg_color=(30, 10, 0)
    )
    print("✅ 创建：火焰")
    
    editor.create_skin(
        name="冰雪",
        snake_head=(100, 200, 255),
        snake_body=(200, 230, 255),
        food_color=(255, 100, 100),
        bg_color=(0, 20, 40)
    )
    print("✅ 创建：冰雪")
    
    editor.create_skin(
        name="霓虹",
        snake_head=(255, 0, 255),
        snake_body=(0, 255, 255),
        food_color=(255, 255, 0),
        bg_color=(20, 0, 30)
    )
    print("✅ 创建：霓虹")
    
    editor.create_skin(
        name="黄金",
        snake_head=(255, 215, 0),
        snake_body=(255, 200, 100),
        food_color=(255, 255, 255),
        bg_color=(30, 20, 0)
    )
    print("✅ 创建：黄金")
    
    editor.list_skins()
