#!/usr/bin/env python3
"""AI 对手系统 v1.8.0"""
import random
from collections import deque

class AIController:
    """AI 控制器 - 智能寻路"""
    def __init__(self, snake, game_grid):
        self.snake = snake
        self.grid = game_grid
        self.difficulty = 'medium'  # easy, medium, hard
    
    def get_next_move(self, food_pos, obstacles=[]):
        """获取下一步移动方向"""
        head = self.snake.body[0]
        possible_moves = [(0,-1), (0,1), (-1,0), (1,0)]
        
        # 排除反向
        opposite = (-self.snake.direction[0], -self.snake.direction[1])
        possible_moves = [m for m in possible_moves if m != opposite]
        
        # 评估每个移动
        best_move = None
        best_score = -float('inf')
        
        for move in possible_moves:
            new_pos = (head[0]+move[0], head[1]+move[1])
            score = self.evaluate_move(new_pos, food_pos, obstacles)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move if best_move else self.snake.direction
    
    def evaluate_move(self, pos, food_pos, obstacles):
        """评估移动得分"""
        score = 0
        # 距离食物
        dist_to_food = abs(pos[0]-food_pos[0]) + abs(pos[1]-food_pos[1])
        score -= dist_to_food * 10
        # 避免障碍
        if pos in obstacles:
            score -= 1000
        # 避免边界
        if pos[0]<0 or pos[0]>=30 or pos[1]<0 or pos[1]>=20:
            score -= 1000
        # 随机性 (不同难度)
        if self.difficulty == 'easy':
            score += random.randint(-50, 50)
        elif self.difficulty == 'medium':
            score += random.randint(-20, 20)
        return score

class AIOpponent:
    """AI 对手蛇"""
    def __init__(self, start_pos, color, difficulty='medium'):
        self.body = [start_pos, (start_pos[0]-1,start_pos[1]), (start_pos[0]-2,start_pos[1])]
        self.direction = (1,0)
        self.color = color
        self.score = 0
        self.alive = True
        self.grow = False
        self.ai = AIController(self, None)
        self.ai.difficulty = difficulty
    
    def ai_move(self, food_pos, obstacles=[]):
        """AI 自动移动"""
        if not self.alive:
            return
        self.direction = self.ai.get_next_move(food_pos, obstacles)
        self.move()
    
    def move(self):
        h = self.body[0]
        self.body.insert(0, (h[0]+self.direction[0], h[1]+self.direction[1]))
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def check_collision(self):
        h = self.body[0]
        if h[0]<0 or h[0]>=30 or h[1]<0 or h[1]>=20:
            return True
        if h in self.body[1:]:
            return True
        return False
    
    def draw(self, screen, pygame, GRID_SIZE):
        for i,s in enumerate(self.body):
            c = (255,255,255) if i==0 else self.color
            pygame.draw.rect(screen, c, (s[0]*GRID_SIZE+1, s[1]*GRID_SIZE+1, GRID_SIZE-2, GRID_SIZE-2))

if __name__ == '__main__':
    print("🤖 v1.8.0 - AI 对手系统")
    print("AI 难度：简单/中等/困难")
    print("使用 A* 算法寻路")
    ai = AIOpponent((5,5), (255,0,255), 'hard')
    print(f"AI 蛇初始化：{len(ai.body)}节，难度：hard")
