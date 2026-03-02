#!/usr/bin/env python3
"""贪吃蛇 v1.5.0 - 双人模式"""
import pygame, random, sys

pygame.init()
W, H, GRID = 800, 600, 20
GW, GH = W//GRID, H//GRID

class Snake:
    def __init__(self, start, color, controls):
        self.body = [start, (start[0]-1,start[1]), (start[0]-2,start[1])]
        self.direction = (1,0)
        self.color = color
        self.controls = controls
        self.score = 0
        self.alive = True
        self.grow = False
    def move(self):
        h = self.body[0]
        self.body.insert(0, (h[0]+self.direction[0], h[1]+self.direction[1]))
        if not self.grow: self.body.pop()
        else: self.grow = False
    def control(self, key):
        if key == self.controls['up'] and self.direction != (0,1): self.direction = (0,-1)
        elif key == self.controls['down'] and self.direction != (0,-1): self.direction = (0,1)
        elif key == self.controls['left'] and self.direction != (1,0): self.direction = (-1,0)
        elif key == self.controls['right'] and self.direction != (-1,0): self.direction = (1,0)
    def check_collision(self, other_snake=None):
        h = self.body[0]
        if h[0]<0 or h[0]>=GW or h[1]<0 or h[1]>=GH: return True
        if h in self.body[1:]: return True
        if other_snake and h in other_snake.body: return True
        return False
    def draw(self, screen):
        for i,s in enumerate(self.body):
            c = (255,255,255) if i==0 else self.color
            pygame.draw.rect(screen, c, (s[0]*GRID+1, s[1]*GRID+1, GRID-2, GRID-2))

class Game:
    def __init__(self, mode='single'):
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption(f'贪吃蛇 v1.5.0 - {"双人模式" if mode=="dual" else "单人模式"}')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.mode = mode
        self.reset()
    
    def reset(self):
        self.snake1 = Snake((5,10), (0,255,0), {'up':pygame.K_w,'down':pygame.K_s,'left':pygame.K_a,'right':pygame.K_d})
        self.snake2 = Snake((35,10), (255,0,0), {'up':pygame.K_UP,'down':pygame.K_DOWN,'left':pygame.K_LEFT,'right':pygame.K_RIGHT}) if self.mode=='dual' else None
        self.food = self.spawn_food()
        self.game_over = False
    
    def spawn_food(self):
        while True:
            pos = (random.randint(0,GW-1), random.randint(0,GH-1))
            if pos not in self.snake1.body and (not self.snake2 or pos not in self.snake2.body):
                return pos
    
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: return False
                if e.key == pygame.K_SPACE and self.game_over: self.reset()
                if e.key == pygame.K_1: self.mode = 'single'; self.reset()
                if e.key == pygame.K_2: self.mode = 'dual'; self.reset()
                self.snake1.control(e.key)
                if self.snake2: self.snake2.control(e.key)
        return True
    
    def update(self):
        if self.game_over: return
        self.snake1.move()
        if self.snake1.body[0] == self.food:
            self.snake1.grow = True
            self.snake1.score += 10
            self.food = self.spawn_food()
        if self.snake1.check_collision(self.snake2):
            self.snake1.alive = False
            self.game_over = True
        
        if self.snake2:
            self.snake2.move()
            if self.snake2.body[0] == self.food:
                self.snake2.grow = True
                self.snake2.score += 10
                self.food = self.spawn_food()
            if self.snake2.check_collision(self.snake1):
                self.snake2.alive = False
                self.game_over = True
    
    def draw(self):
        self.screen.fill((0,0,0))
        # 中线
        if self.mode == 'dual':
            pygame.draw.line(self.screen, (50,50,50), (W//2,0), (W//2,H), 2)
        # 绘制
        self.snake1.draw(self.screen)
        if self.snake2: self.snake2.draw(self.screen)
        pygame.draw.circle(self.screen, (255,0,0), (self.food[0]*GRID+10, self.food[1]*GRID+10), 8)
        # UI
        self.screen.blit(self.font.render(f"P1: {self.snake1.score}", True, (0,255,0)), (10,10))
        if self.snake2:
            self.screen.blit(self.font.render(f"P2: {self.snake2.score}", True, (255,0,0)), (W-120,10))
            self.screen.blit(self.font.render("P1: WASD | P2: Arrows | 1:Single 2:Dual", True, (150,150,150)), (W//2-200, H-30))
        if self.game_over:
            winner = "P1" if (not self.snake2 or self.snake1.score > self.snake2.score) else "P2"
            self.screen.blit(self.font.render(f"{winner} Wins! Space to restart", True, (255,255,0)), (W//2-150, H//2))
        pygame.display.flip()
    
    def run(self):
        while self.handle_events():
            self.update()
            self.draw()
            self.clock.tick(10)
        pygame.quit(); sys.exit()

if __name__ == '__main__':
    print("🐍 v1.5.0 - 双人模式")
    print("P1: WASD | P2: 方向键 | 1:单人 2:双人")
    Game('dual').run()
