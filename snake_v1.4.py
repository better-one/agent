#!/usr/bin/env python3
"""贪吃蛇 v1.4.0 - 关卡模式"""
import pygame, random, sys, json

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE = 600, 400, 20
GRID_W, GRID_H = WINDOW_WIDTH//GRID_SIZE, WINDOW_HEIGHT//GRID_SIZE

# 关卡布局
LEVELS = {
    1: {'name': '训练场', 'target': 100, 'obstacles': []},
    2: {'name': '迷宫', 'target': 200, 'obstacles': [(10,10), (10,11), (11,10), (11,11)]},
    3: {'name': '障碍赛', 'target': 300, 'obstacles': [(5,5), (15,5), (5,15), (15,15), (10,10)]},
    4: {'name': '传送门', 'target': 400, 'obstacles': [(8,8), (8,9), (9,8), (12,12), (12,13), (13,12)], 'portals': [((2,2), (18,18)), ((2,18), (18,2))]},
    5: {'name': '终极挑战', 'target': 500, 'obstacles': [(i,10) for i in range(5,15)] + [(10,i) for i in range(5,15)]}
}

class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.levels = LEVELS
    
    def get_level(self):
        return self.levels.get(self.current_level, LEVELS[1])
    
    def check_complete(self, score):
        if score >= self.get_level()['target']:
            self.current_level = min(self.current_level + 1, 5)
            return True
        return False
    
    def is_obstacle(self, pos):
        return pos in self.get_level().get('obstacles', [])
    
    def check_portal(self, pos):
        for p1, p2 in self.get_level().get('portals', []):
            if pos == p1: return p2
            if pos == p2: return p1
        return None

class Snake:
    def __init__(self): self.reset()
    def reset(self):
        self.body = [(5,5), (4,5), (3,5)]
        self.direction = (1,0)
        self.grow = False
    def move(self):
        h = self.body[0]
        self.body.insert(0, (h[0]+self.direction[0], h[1]+self.direction[1]))
        if not self.grow: self.body.pop()
        else: self.grow = False
    def change_dir(self, d):
        if (-self.direction[0], -self.direction[1]) != d: self.direction = d
    def check_collision(self, level_mgr):
        h = self.body[0]
        if h[0]<0 or h[0]>=GRID_W or h[1]<0 or h[1]>=GRID_H: return True
        if level_mgr.is_obstacle(h): return True
        return h in self.body[1:]
    def draw(self, screen):
        for i,s in enumerate(self.body):
            c = (0,200,0) if i==0 else (0,255,0)
            pygame.draw.rect(screen, c, (s[0]*GRID_SIZE+1, s[1]*GRID_SIZE+1, GRID_SIZE-2, GRID_SIZE-2))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('贪吃蛇 v1.4.0 - 关卡模式')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.level_mgr = LevelManager()
        self.reset()
    
    def reset(self):
        self.snake = Snake()
        self.food = self.spawn_food()
        self.score = 0
        self.level_complete = False
        self.game_over = False
    
    def spawn_food(self):
        while True:
            pos = (random.randint(0,GRID_W-1), random.randint(0,GRID_H-1))
            if pos not in self.snake.body and not self.level_mgr.is_obstacle(pos):
                return pos
    
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: return False
                if e.key == pygame.K_SPACE and self.game_over: self.reset()
                if e.key == pygame.K_UP: self.snake.change_dir((0,-1))
                if e.key == pygame.K_DOWN: self.snake.change_dir((0,1))
                if e.key == pygame.K_LEFT: self.snake.change_dir((-1,0))
                if e.key == pygame.K_RIGHT: self.snake.change_dir((1,0))
        return True
    
    def update(self):
        if self.game_over: return
        self.snake.move()
        
        # 传送门
        portal = self.level_mgr.check_portal(self.snake.body[0])
        if portal: self.snake.body[0] = portal
        
        if self.snake.body[0] == self.food:
            self.snake.grow = True
            self.score += 10
            self.food = self.spawn_food()
            if self.level_mgr.check_complete(self.score):
                self.level_complete = True
        
        if self.snake.check_collision(self.level_mgr):
            self.game_over = True
    
    def draw(self):
        self.screen.fill((0,0,0))
        # 绘制障碍
        for obs in self.level_mgr.get_level().get('obstacles', []):
            pygame.draw.rect(self.screen, (100,100,100), (obs[0]*GRID_SIZE, obs[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
        # 绘制传送门
        for p1,p2 in self.level_mgr.get_level().get('portals', []):
            pygame.draw.circle(self.screen, (255,0,255), (p1[0]*GRID_SIZE+10, p1[1]*GRID_SIZE+10), 8)
            pygame.draw.circle(self.screen, (255,0,255), (p2[0]*GRID_SIZE+10, p2[1]*GRID_SIZE+10), 8)
        # 绘制食物和蛇
        pygame.draw.circle(self.screen, (255,0,0), (self.food[0]*GRID_SIZE+10, self.food[1]*GRID_SIZE+10), 8)
        self.snake.draw(self.screen)
        # UI
        level = self.level_mgr.get_level()
        self.screen.blit(self.font.render(f"Level {self.level_mgr.current_level}: {level['name']}", True, (255,255,255)), (10,10))
        self.screen.blit(self.font.render(f"Score: {self.score}/{level['target']}", True, (255,255,255)), (10,40))
        if self.level_complete:
            self.screen.blit(self.font.render("Level Complete!", True, (0,255,0)), (WINDOW_WIDTH//2-100, WINDOW_HEIGHT//2))
        if self.game_over:
            self.screen.blit(self.font.render("GAME OVER - Space to restart", True, (255,0,0)), (WINDOW_WIDTH//2-150, WINDOW_HEIGHT//2))
        pygame.display.flip()
    
    def run(self):
        while self.handle_events():
            self.update()
            self.draw()
            self.clock.tick(10)
        pygame.quit(); sys.exit()

if __name__ == '__main__':
    print("🐍 v1.4.0 - 关卡模式")
    Game().run()
