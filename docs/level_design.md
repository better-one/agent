# 关卡模式设计文档 v1.4.0

## 概述
添加关卡系统，每关有不同的地图布局和目标。

## 关卡设计

### Level 1: 训练场
- 地图：空旷
- 目标：达到 100 分
- 障碍：无

### Level 2: 迷宫
- 地图：固定障碍物
- 目标：达到 200 分
- 障碍：4 个固定墙

### Level 3: 移动障碍
- 地图：移动的平台
- 目标：达到 300 分
- 障碍：2 个移动块

### Level 4: 传送门
- 地图：传送门对
- 目标：达到 400 分
- 特殊：进入一个传送门从另一个出来

### Level 5: 终极挑战
- 地图：组合所有元素
- 目标：达到 500 分
- 障碍：固定 + 移动 + 传送门

## 数据结构

```python
class Level:
    def __init__(self, level_num, layout, target_score, obstacles):
        self.level_num = level_num
        self.layout = layout  # 2D 数组表示地图
        self.target_score = target_score
        self.obstacles = obstacles  # 障碍列表
        self.completed = False

class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.levels = self.load_levels()
    
    def load_levels(self):
        # 从 JSON 文件加载关卡
        pass
    
    def check_level_complete(self, score):
        # 检查是否完成当前关卡
        pass
    
    def next_level(self):
        # 进入下一关
        pass
```

## UI 设计
- 关卡选择界面
- 关卡进度显示
- 完成度星级评价
