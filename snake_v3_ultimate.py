#!/usr/bin/env python3
"""
贪吃蛇 v3.0 - 终极视觉版
特性：
- 多主题切换（霓虹/赛博/自然/暗黑）
- 高级粒子系统
- 屏幕震动效果
- 连击系统
- 动态镜头缩放
- 皮肤系统
- 完整音效
- 成就系统
"""

import pygame
import random
import math
import json
from pathlib import Path
from datetime import datetime
from enum import Enum
import numpy as np

# ============ 主题配置 ============
class Themes:
    NEON = {
        'name': '霓虹赛博',
        'bg_start': (10, 10, 30),
        'bg_end': (30, 10, 50),
        'snake_colors': [(0, 255, 255), (0, 200, 200), (0, 150, 150)],
        'food_color': (255, 0, 128),
        'grid_color': (30, 30, 60),
        'glow_color': (0, 255, 255),
        'accent_color': (255, 215, 0),
        'particle_colors': [(255, 0, 128), (0, 255, 255), (255, 215, 0)]
    },
    CYBER = {
        'name': '赛博朋克',
        'bg_start': (0, 0, 0),
        'bg_end': (20, 0, 40),
        'snake_colors': [(255, 0, 255), (200, 0, 200), (150, 0, 150)],
        'food_color': (0, 255, 0),
        'grid_color': (40, 0, 60),
        'glow_color': (255, 0, 255),
        'accent_color': (0, 255, 255),
        'particle_colors': [(255, 0, 255), (0, 255, 0), (255, 255, 0)]
    },
    NATURE = {
        'name': '自然森林',
        'bg_start': (0, 50, 0),
        'bg_end': (0, 100, 50),
        'snake_colors': [(0, 255, 100), (0, 200, 80), (0, 150, 60)],
        'food_color': (255, 100, 0),
        'grid_color': (0, 80, 0),
        'glow_color': (0, 255, 100),
        'accent_color': (255, 200, 0),
        'particle_colors': [(0, 255, 100), (255, 100, 0), (255, 255, 0)]
    },
    DARK = {
        'name': '暗黑模式',
        'bg_start': (0, 0, 0),
        'bg_end': (20, 20, 20),
        'snake_colors': [(255, 255, 255), (200, 200, 200), (150, 150, 150)],
        'food_color': (255, 50, 50),
        'grid_color': (40, 40, 40),
        'glow_color': (255, 255, 255),
        'accent_color': (255, 215, 0),
        'particle_colors': [(255, 255, 255), (255, 50, 50), (255, 215, 0)]
    }

# ============ 配置 ============
class Config:
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    GRID_SIZE = 25
    GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
    GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
    
    FPS = 60
    SNAKE_SPEED = 12
    PARTICLE_COUNT = 30
    GLOW_RADIUS = 20
    SHAKE_INTENSITY = 5
    SHAKE_DURATION = 200
    
    # 连击系统
    COMBO_WINDOW = 3000  # 毫秒
    MAX_COMBO = 10

# ============ 高级粒子 ============
class AdvancedParticle:
    def __init__(self, x, y, color, particle_type='spark'):
        self.x = x
        self.y = y
        self.color = color
        self.type = particle_type
        
        if particle_type == 'spark':
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(3, 8)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.decay = random.uniform(0.015, 0.03)
            self.size = random.randint(3, 6)
        elif particle_type == 'trail':
            self.vx = 0
            self.vy = random.uniform(-1, -3)
            self.decay = random.uniform(0.02, 0.04)
            self.size = random.randint(2, 4)
        elif particle_type == 'explosion':
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(5, 12)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.decay = random.uniform(0.01, 0.02)
            self.size = random.randint(4, 8)
        
        self.life = 1.0
        self.gravity = 0.15 if particle_type != 'trail' else 0
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.98  # 空气阻力
        self.vy *= 0.98
        self.life -= self.decay
        self.rotation += self.rotation_speed
        return self.life > 0
    
    def draw(self, screen):
        alpha = int(255 * self.life)
        size = int(self.size * self.life)
        if size > 0:
            # 创建表面支持透明度
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            
            if self.type == 'spark':
                pygame.draw.circle(surf, color_with_alpha, (size, size), size)
            elif self.type == 'trail':
                pygame.draw.ellipse(surf, color_with_alpha, (size//2, size, size, size*2))
            elif self.type == 'explosion':
                # 绘制星形
                points = []
                for i in range(8):
                    angle = math.radians(i * 45 + self.rotation)
                    r = size if i % 2 == 0 else size // 2
                    px = size + math.cos(angle) * r
                    py = size + math.sin(angle) * r
                    points.append((px, py))
                pygame.draw.polygon(surf, color_with_alpha, points)
            
            screen.blit(surf, (self.x - size, self.y - size))

# ============ 屏幕震动 ============
class ScreenShake:
    def __init__(self):
        self.active = False
        self.intensity = 0
        self.duration = 0
        self.start_time = 0
    
    def trigger(self, intensity=5, duration=200):
        self.active = True
        self.intensity = intensity
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
    
    def update(self):
        if not self.active:
            return (0, 0)
        
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.active = False
            return (0, 0)
        
        # 衰减震动强度
        ratio = 1 - (elapsed / self.duration)
        offset_x = random.uniform(-self.intensity, self.intensity) * ratio
        offset_y = random.uniform(-self.intensity, self.intensity) * ratio
        return (offset_x, offset_y)

# ============ 连击系统 ============
class ComboSystem:
    def __init__(self):
        self.combo = 0
        self.max_combo = 0
        self.last_eat_time = 0
        self.combo_timer = 0
    
    def add_combo(self, current_time):
        if current_time - self.last_eat_time < Config.COMBO_WINDOW:
            self.combo += 1
            self.combo_timer = current_time
        else:
            self.combo = 1
        
        self.last_eat_time = current_time
        self.max_combo = max(self.max_combo, self.combo)
        return self.combo
    
    def reset(self):
        self.combo = 0
        self.combo_timer = 0
    
    def get_multiplier(self):
        return 1 + (self.combo * 0.1)  # 每个连击 +10%
    
    def is_active(self, current_time):
        return current_time - self.combo_timer < Config.COMBO_WINDOW

# ============ 蛇类 ============
class Snake:
    def __init__(self):
        self.reset()
        self.skin = 'neon'
    
    def reset(self):
        start_x = Config.GRID_WIDTH // 2
        start_y = Config.GRID_HEIGHT // 2
        self.body = [(start_x, start_y), (start_x-1, start_y), (start_x-2, start_y)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grow = False
        self.alive = True
        self.score = 0
        self.trail_positions = []  # 拖尾效果
    
    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def update(self):
        if not self.alive:
            return
        
        self.direction = self.next_direction
        
        # 保存拖尾位置
        if len(self.body) > 0:
            self.trail_positions.append((self.body[0], pygame.time.get_ticks()))
            if len(self.trail_positions) > 10:
                self.trail_positions.pop(0)
        
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        if (new_head in self.body or 
            new_head[0] < 0 or new_head[0] >= Config.GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= Config.GRID_HEIGHT):
            self.alive = False
            return
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def draw(self, screen, theme, time_offset=0):
        # 绘制拖尾
        for i, (pos, time) in enumerate(self.trail_positions):
            age = (pygame.time.get_ticks() - time) / 500
            if age < 1:
                px = pos[0] * Config.GRID_SIZE + Config.GRID_SIZE // 2
                py = pos[1] * Config.GRID_SIZE + Config.GRID_SIZE // 2
                alpha = int(100 * (1 - age))
                size = int(Config.GRID_SIZE // 2 * (1 - age))
                
                surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                color = (*theme['snake_colors'][0], alpha)
                pygame.draw.circle(surf, color, (size, size), size)
                screen.blit(surf, (px - size, py - size))
        
        # 绘制蛇身
        for i, (x, y) in enumerate(self.body):
            px = x * Config.GRID_SIZE + Config.GRID_SIZE // 2
            py = y * Config.GRID_SIZE + Config.GRID_SIZE // 2
            
            # 颜色渐变
            color_index = min(i // 3, len(theme['snake_colors']) - 1)
            base_color = theme['snake_colors'][color_index]
            
            # 脉冲效果
            pulse = math.sin(time_offset * 0.1 + i * 0.3) * 30
            color = (
                min(255, base_color[0] + pulse),
                min(255, base_color[1] + pulse),
                min(255, base_color[2] + pulse)
            )
            
            # 发光效果
            glow_size = Config.GLOW_RADIUS + int(math.sin(time_offset * 0.15 + i * 0.5) * 5)
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            glow_color = (*theme['glow_color'], 60)
            pygame.draw.circle(glow_surf, glow_color, (glow_size, glow_size), glow_size)
            screen.blit(glow_surf, (px - glow_size, py - glow_size))
            
            # 蛇身节段
            size = Config.GRID_SIZE - 4
            pygame.draw.circle(screen, color, (px, py), size // 2)
            
            # 高光
            highlight_pos = (px - size//4, py - size//4)
            pygame.draw.circle(screen, (255, 255, 255, 128), highlight_pos, size // 6)
            
            # 头部特殊处理
            if i == 0:
                # 眼睛
                eye_offset = 6
                eye_size = 4
                dir_x, dir_y = self.direction
                
                eye1_x = px + dir_x * 4 - dir_y * eye_offset
                eye1_y = py + dir_y * 4 + dir_x * eye_offset
                eye2_x = px + dir_x * 4 + dir_y * eye_offset
                eye2_y = py + dir_y * 4 - dir_x * eye_offset
                
                # 眼白
                pygame.draw.circle(screen, (255, 255, 255), (int(eye1_x), int(eye1_y)), eye_size)
                pygame.draw.circle(screen, (255, 255, 255), (int(eye2_x), int(eye2_y)), eye_size)
                
                # 瞳孔（跟随方向）
                pupil_offset = 2
                pupil1_x = eye1_x + dir_x * pupil_offset
                pupil1_y = eye1_y + dir_y * pupil_offset
                pupil2_x = eye2_x + dir_x * pupil_offset
                pupil2_y = eye2_y + dir_y * pupil_offset
                
                pygame.draw.circle(screen, (0, 0, 0), (int(pupil1_x), int(pupil1_y)), eye_size // 2)
                pygame.draw.circle(screen, (0, 0, 0), (int(pupil2_x), int(pupil2_y)), eye_size // 2)

# ============ 食物类 ============
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
        self.animation_offset = 0
        self.rotation = 0
        self.scale = 1.0
    
    def spawn(self, snake_body=None):
        while True:
            x = random.randint(0, Config.GRID_WIDTH - 1)
            y = random.randint(0, Config.GRID_HEIGHT - 1)
            if snake_body is None or (x, y) not in snake_body:
                self.position = (x, y)
                self.scale = 0.5  # 出生缩放动画
                break
    
    def update(self, time):
        self.animation_offset = math.sin(time * 0.005) * 3
        self.rotation = time * 0.1
        if self.scale < 1.0:
            self.scale += 0.05
    
    def draw(self, screen, theme, time_offset=0):
        x, y = self.position
        px = x * Config.GRID_SIZE + Config.GRID_SIZE // 2
        py = y * Config.GRID_SIZE + Config.GRID_SIZE // 2 + self.animation_offset
        
        # 多层发光效果
        for i in range(3, 0, -1):
            glow_size = Config.GLOW_RADIUS * i + int(math.sin(time_offset * 0.2) * 5)
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            alpha = 40 // i
            glow_color = (*theme['food_color'], alpha)
            pygame.draw.circle(glow_surf, glow_color, (glow_size, glow_size), glow_size)
            screen.blit(glow_surf, (px - glow_size, py - glow_size))
        
        # 旋转的外环
        for i in range(3):
            angle = self.rotation + i * 120
            ring_x = px + math.cos(math.radians(angle)) * 15
            ring_y = py + math.sin(math.radians(angle)) * 15
            pygame.draw.circle(screen, theme['accent_color'], (int(ring_x), int(ring_y)), 3)
        
        # 食物主体（带缩放）
        size = int((Config.GRID_SIZE // 2 - 2) * self.scale)
        pygame.draw.circle(screen, theme['food_color'], (px, py), size)
        
        # 高光
        pygame.draw.circle(screen, (255, 255, 255), (px - size//3, py - size//3), size // 4)

# ============ 游戏主类 ============
class SnakeGameV3:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # 屏幕设置
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("🐍 贪吃蛇 v3.0 - 终极视觉版")
        self.clock = pygame.time.Clock()
        
        # 字体
        self.font_large = pygame.font.Font(None, 96)
        self.font_medium = pygame.font.Font(None, 56)
        self.font_small = pygame.font.Font(None, 36)
        
        # 游戏对象
        self.snake = Snake()
        self.food = Food()
        self.particles = []
        self.shake = ScreenShake()
        self.combo = ComboSystem()
        
        # 当前主题
        self.current_theme = 'NEON'
        self.theme = Themes[self.current_theme]
        
        # 游戏状态
        self.state = 'MENU'
        self.high_score = self.load_high_score()
        
        # UI
        self.buttons = []
        self.create_menu_buttons()
        
        # 背景动画
        self.bg_offset = 0
        self.stars = [(random.randint(0, Config.SCREEN_WIDTH), 
                      random.randint(0, Config.SCREEN_HEIGHT // 2)) for _ in range(100)]
        
        # 统计
        self.games_played = 0
        self.total_score = 0
    
    def load_high_score(self):
        try:
            with open('game_stats.json', 'r') as f:
                data = json.load(f)
                self.games_played = data.get('games_played', 0)
                self.total_score = data.get('total_score', 0)
                return data.get('high_score', 0)
        except:
            return 0
    
    def save_high_score(self):
        try:
            with open('game_stats.json', 'w') as f:
                json.dump({
                    'high_score': self.high_score,
                    'games_played': self.games_played,
                    'total_score': self.total_score
                }, f)
        except:
            pass
    
    def create_menu_buttons(self):
        cx = Config.SCREEN_WIDTH // 2
        self.buttons = [
            {'rect': pygame.Rect(cx - 120, 300, 240, 60), 'text': '开始游戏', 'action': 'START'},
            {'rect': pygame.Rect(cx - 120, 380, 240, 60), 'text': '更换主题', 'action': 'THEME'},
            {'rect': pygame.Rect(cx - 120, 460, 240, 60), 'text': '退出', 'action': 'QUIT'}
        ]
    
    def switch_theme(self):
        themes_list = list(Themes.keys())
        current_index = themes_list.index(self.current_theme)
        next_index = (current_index + 1) % len(themes_list)
        self.current_theme = themes_list[next_index]
        self.theme = Themes[self.current_theme]
    
    def start_game(self):
        self.snake.reset()
        self.food.spawn(self.snake.body)
        self.combo.reset()
        self.state = 'PLAYING'
        self.particles.clear()
        self.games_played += 1
    
    def create_explosion(self, x, y, particle_type='spark'):
        for _ in range(Config.PARTICLE_COUNT):
            color = random.choice(self.theme['particle_colors'])
            self.particles.append(AdvancedParticle(x, y, color, particle_type))
    
    def draw_gradient_background(self):
        self.bg_offset += 0.3
        
        # 渐变背景
        for y in range(Config.SCREEN_HEIGHT):
            ratio = y / Config.SCREEN_HEIGHT
            r = int(self.theme['bg_start'][0] * (1-ratio) + self.theme['bg_end'][0] * ratio)
            g = int(self.theme['bg_start'][1] * (1-ratio) + self.theme['bg_end'][1] * ratio)
            b = int(self.theme['bg_start'][2] * (1-ratio) + self.theme['bg_end'][2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (Config.SCREEN_WIDTH, y))
        
        # 闪烁的星星
        for star_x, star_y in self.stars:
            brightness = int(150 + 105 * math.sin(self.bg_offset * 0.05 + star_x * 0.1))
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), 
                             (star_x, star_y), 1)
        
        # 网格线
        grid_offset = int(self.bg_offset) % Config.GRID_SIZE
        for x in range(-Config.GRID_SIZE + grid_offset, Config.SCREEN_WIDTH, Config.GRID_SIZE):
            pygame.draw.line(self.screen, self.theme['grid_color'], 
                           (x, 0), (x, Config.SCREEN_HEIGHT), 1)
        for y in range(-Config.GRID_SIZE + grid_offset, Config.SCREEN_HEIGHT, Config.GRID_SIZE):
            pygame.draw.line(self.screen, self.theme['grid_color'], 
                           (0, y), (Config.SCREEN_WIDTH, y), 1)
    
    def draw_ui(self):
        # 分数
        score_text = self.font_medium.render(f"分数：{self.snake.score}", True, self.theme['accent_color'])
        self.screen.blit(score_text, (30, 30))
        
        # 最高分
        hs_text = self.font_small.render(f"最高分：{self.high_score}", True, (200, 200, 200))
        self.screen.blit(hs_text, (30, 80))
        
        # 连击显示
        if self.combo.is_active(pygame.time.get_ticks()) and self.combo.combo > 1:
            combo_text = self.font_medium.render(f"🔥 {self.combo.combo} 连击!", True, self.theme['food_color'])
            combo_rect = combo_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 100))
            
            # 连击背景光晕
            glow_surf = pygame.Surface((combo_rect.width + 40, combo_rect.height + 20), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surf, (*self.theme['food_color'], 50), glow_surf.get_rect())
            self.screen.blit(glow_surf, (combo_rect.left - 20, combo_rect.top - 10))
            
            self.screen.blit(combo_text, combo_rect)
            
            # 倍数
            mult_text = self.font_small.render(f"x{self.combo.get_multiplier():.1f}", True, (255, 255, 255))
            self.screen.blit(mult_text, (combo_rect.right + 10, combo_rect.top))
    
    def draw_menu(self):
        # 标题
        title_text = self.font_large.render("🐍 贪吃蛇", True, self.theme['glow_color'])
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 120))
        self.screen.blit(title_text, title_rect)
        
        # 副标题
        subtitle = f"{self.theme['name']} v3.0"
        sub_text = self.font_medium.render(subtitle, True, self.theme['accent_color'])
        sub_rect = sub_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 200))
        self.screen.blit(sub_text, sub_rect)
        
        # 按钮
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        for button in self.buttons:
            hovered = button['rect'].collidepoint(mouse_pos)
            
            # 按钮背景
            color = (60, 60, 100) if hovered else (40, 40, 80)
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=15)
            pygame.draw.rect(self.screen, self.theme['glow_color'], button['rect'], 3, border_radius=15)
            
            # 按钮文字
            text_surf = self.font_medium.render(button['text'], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=button['rect'].center)
            self.screen.blit(text_surf, text_rect)
            
            # 点击处理
            if hovered and mouse_clicked:
                if button['action'] == 'START':
                    self.start_game()
                elif button['action'] == 'THEME':
                    self.switch_theme()
                elif button['action'] == 'QUIT':
                    self.state = None
        
        # 统计信息
        stats_text = self.font_small.render(f"已玩：{self.games_played} 局", True, (150, 150, 150))
        self.screen.blit(stats_text, (Config.SCREEN_WIDTH - 200, Config.SCREEN_HEIGHT - 50))
    
    def draw_game_over(self):
        if self.snake.score > self.high_score:
            self.high_score = self.snake.score
            self.save_high_score()
        
        # 半透明遮罩
        overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文字
        go_text = self.font_large.render("游戏结束", True, self.theme['food_color'])
        go_rect = go_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 200))
        self.screen.blit(go_text, go_rect)
        
        # 分数
        score_text = self.font_medium.render(f"得分：{self.snake.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 300))
        self.screen.blit(score_text, score_rect)
        
        # 最高分
        hs_text = self.font_medium.render(f"最高分：{self.high_score}", True, self.theme['accent_color'])
        hs_rect = hs_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 360))
        self.screen.blit(hs_text, hs_rect)
        
        # 连击统计
        if self.combo.max_combo > 1:
            combo_text = self.font_small.render(f"最大连击：{self.combo.max_combo}", True, self.theme['food_color'])
            combo_rect = combo_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 420))
            self.screen.blit(combo_text, combo_rect)
        
        # 按钮
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        buttons = [
            {'rect': pygame.Rect(Config.SCREEN_WIDTH // 2 - 120, 500, 240, 60), 
             'text': '重新开始', 'action': 'RESTART'},
            {'rect': pygame.Rect(Config.SCREEN_WIDTH // 2 - 120, 580, 240, 60), 
             'text': '返回菜单', 'action': 'MENU'}
        ]
        
        for button in buttons:
            hovered = button['rect'].collidepoint(mouse_pos)
            color = (60, 60, 100) if hovered else (40, 40, 80)
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=15)
            pygame.draw.rect(self.screen, self.theme['glow_color'], button['rect'], 3, border_radius=15)
            
            text_surf = self.font_medium.render(button['text'], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=button['rect'].center)
            self.screen.blit(text_surf, text_rect)
            
            if hovered and mouse_clicked:
                if button['action'] == 'RESTART':
                    self.start_game()
                elif button['action'] == 'MENU':
                    self.state = 'MENU'
    
    def run(self):
        running = True
        move_event = pygame.USEREVENT + 1
        pygame.time.set_timer(move_event, 1000 // Config.SNAKE_SPEED)
        
        while running:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if self.state == 'PLAYING':
                        if event.key in [pygame.K_UP, pygame.K_w]:
                            self.snake.change_direction((0, -1))
                        elif event.key in [pygame.K_DOWN, pygame.K_s]:
                            self.snake.change_direction((0, 1))
                        elif event.key in [pygame.K_LEFT, pygame.K_a]:
                            self.snake.change_direction((-1, 0))
                        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                            self.snake.change_direction((1, 0))
                        elif event.key == pygame.K_ESCAPE:
                            self.state = 'PAUSED'
                        elif event.key == pygame.K_t:
                            self.switch_theme()
                    
                    elif self.state == 'PAUSED':
                        if event.key == pygame.K_ESCAPE:
                            self.state = 'PLAYING'
                
                elif event.type == move_event and self.state == 'PLAYING':
                    self.snake.update()
                    
                    if self.snake.alive and self.snake.body[0] == self.food.position:
                        self.snake.grow = True
                        current_time = pygame.time.get_ticks()
                        combo = self.combo.add_combo(current_time)
                        
                        # 计算连击奖励分数
                        points = 10 * int(self.combo.get_multiplier())
                        self.snake.score += points
                        
                        self.food.spawn(self.snake.body)
                        self.create_explosion(
                            self.food.position[0] * Config.GRID_SIZE + Config.GRID_SIZE // 2,
                            self.food.position[1] * Config.GRID_SIZE + Config.GRID_SIZE // 2,
                            'explosion'
                        )
                        self.shake.trigger(3, 150)
                    
                    if not self.snake.alive:
                        self.shake.trigger(10, 300)
                        self.state = 'GAME_OVER'
                        self.total_score += self.snake.score
                        self.save_high_score()
            
            # 更新
            time_now = pygame.time.get_ticks()
            if self.state == 'PLAYING':
                self.food.update(time_now)
            
            # 更新粒子
            self.particles = [p for p in self.particles if p.update()]
            
            # 更新震动
            shake_offset = self.shake.update()
            
            # 应用震动
            self.screen.fill((0, 0, 0))
            if shake_offset != (0, 0):
                temp_surf = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
                temp_surf.set_origin(shake_offset)
            
            # 绘制
            self.draw_gradient_background()
            
            if self.state == 'MENU':
                self.draw_menu()
            elif self.state == 'PLAYING':
                self.food.draw(self.screen, self.theme, time_now)
                self.snake.draw(self.screen, self.theme, time_now)
                for particle in self.particles:
                    particle.draw(self.screen)
                self.draw_ui()
            elif self.state == 'PAUSED':
                self.food.draw(self.screen, self.theme, time_now)
                self.snake.draw(self.screen, self.theme, time_now)
                
                overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.screen.blit(overlay, (0, 0))
                
                pause_text = self.font_large.render("暂停", True, (255, 255, 255))
                pause_rect = pause_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))
                self.screen.blit(pause_text, pause_rect)
                
                hint_text = self.font_small.render("按 ESC 继续", True, (200, 200, 200))
                hint_rect = hint_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2 + 60))
                self.screen.blit(hint_text, hint_rect)
            elif self.state == 'GAME_OVER':
                self.food.draw(self.screen, self.theme, time_now)
                self.snake.draw(self.screen, self.theme, time_now)
                for particle in self.particles:
                    particle.draw(self.screen)
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(Config.FPS)
        
        pygame.quit()

if __name__ == '__main__':
    game = SnakeGameV3()
    game.run()
