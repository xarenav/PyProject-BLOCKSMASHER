"""
BLOCK SMASHER - Python/Pygame Enhanced Edition
Faithful recreation of the React/TypeScript version with neon-glass aesthetic
Features: Rajdhani-style font, glass morphism, glowing effects, smooth animations
"""

import pygame
import random
import math
import sys
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

# Initialize Pygame
pygame.init()

# Screen Configuration
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FPS = 60

# Exact Color Palette from React Version (OKLCH converted to RGB)
BG_DARK = (10, 14, 26)  # oklch(0.15 0.02 240)
BG_CARD = (18, 23, 40)  # oklch(0.18 0.02 240)
COLOR_CYAN = (64, 224, 208)  # Turquoise cyan
COLOR_PURPLE = (147, 112, 219)  # Medium purple
COLOR_ORANGE = (255, 140, 0)  # Dark orange
COLOR_PINK = (236, 72, 153)  # Hot pink
COLOR_YELLOW = (234, 179, 8)  # Yellow
COLOR_FOREGROUND = (230, 237, 243)  # Light text
COLOR_BORDER = (45, 50, 65)  # Border color

# Glass morphism RGBA
GLASS_BG = (20, 25, 40, 100)  # Semi-transparent dark
GLASS_BORDER = (64, 224, 208, 40)  # Cyan with alpha

# Game States
class GameState(Enum):
    MAIN_MENU = 1
    MAPS_SCREEN = 2
    GAME_SCREEN = 3
    SETTINGS_SCREEN = 4
    LEADERBOARD_SCREEN = 5

class MapsTab(Enum):
    CURATED = 1
    PROCEDURAL = 2

@dataclass
class Block:
    x: float
    y: float
    width: float
    height: float
    alive: bool
    color: Tuple[int, int, int]

@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float
    size: float
    color: Tuple[int, int, int]

@dataclass
class Settings:
    master_volume: float = 75
    music_volume: float = 65
    sfx_volume: float = 80
    difficulty: str = 'medium'
    quality: str = 'high'
    particle_effects: bool = True
    screen_shake: bool = True
    show_fps: bool = False

class BlockSmasher:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("BLOCK SMASHER - Futuristic Neon Edition")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load Fonts (Rajdhani-inspired - using bold sans-serif)
        self.font_title = pygame.font.SysFont('Arial', 90, bold=True)  # For "BLOCK SMASHER"
        self.font_large = pygame.font.SysFont('Arial', 56, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 38, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 28, bold=False)
        self.font_tiny = pygame.font.SysFont('Arial', 20, bold=False)
        
        # Game State
        self.state = GameState.MAIN_MENU
        self.maps_tab = MapsTab.CURATED
        self.settings = Settings()
        
        # Game Variables
        self.current_level = 1
        self.score = 0
        self.lives = 3
        self.paddle_x = CANVAS_WIDTH // 2 - 60
        self.paddle_width = 120
        self.paddle_height = 15
        self.ball_x = CANVAS_WIDTH // 2
        self.ball_y = CANVAS_HEIGHT - 100
        self.ball_vx = 0
        self.ball_vy = 0
        self.ball_radius = 8
        self.ball_launched = False
        self.blocks: List[Block] = []
        self.particles: List[Particle] = []
        self.unlocked_levels = [1]
        
        # Animation Variables
        self.time = 0
        self.menu_blocks = self.create_floating_blocks()
        self.game_over_type = None  # 'victory' or 'defeat'
        self.fps_counter = 0
        
        # Mouse State
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.mouse_clicked = False
        
    def create_floating_blocks(self):
        """Create floating decorative blocks for menu"""
        return [
            {'x': SCREEN_WIDTH * 0.75, 'y': SCREEN_HEIGHT * 0.15, 'size': 80, 'offset': 0},
            {'x': SCREEN_WIDTH * 0.82, 'y': SCREEN_HEIGHT * 0.45, 'size': 60, 'offset': 1},
            {'x': SCREEN_WIDTH * 0.70, 'y': SCREEN_HEIGHT * 0.70, 'size': 100, 'offset': 2},
            {'x': SCREEN_WIDTH * 0.62, 'y': SCREEN_HEIGHT * 0.25, 'size': 70, 'offset': 1.5},
        ]
    
    def seeded_random(self, seed: int):
        """Seeded RNG for procedural levels"""
        state = seed
        def rand():
            nonlocal state
            state = (state * 1664525 + 1013904223) % 4294967296
            return state / 4294967296
        return rand
    
    def generate_blocks_for_level(self, level: int) -> List[Block]:
        """Generate blocks based on level (same as React version)"""
        blocks = []
        
        if level == 1:
            # Level 1: Classic grid (4x6)
            rows, cols = 4, 6
            block_width, block_height = 60, 25
            gap_x, gap_y = 5, 5
            start_x, start_y = 50, 50
            colors = [COLOR_CYAN, COLOR_PURPLE, COLOR_ORANGE, COLOR_PINK]
            
            for row in range(rows):
                for col in range(cols):
                    x = start_x + col * (block_width + gap_x)
                    y = start_y + row * (block_height + gap_y)
                    blocks.append(Block(x, y, block_width, block_height, True, colors[row % len(colors)]))
        
        elif level == 2:
            # Level 2: Circular formation
            center_x, center_y = CANVAS_WIDTH // 2, 200
            radius = 100
            num_blocks = 8
            block_width, block_height = 60, 25
            colors = [COLOR_CYAN, COLOR_PURPLE, COLOR_ORANGE]
            
            for i in range(num_blocks):
                angle = (i / num_blocks) * 2 * math.pi
                x = center_x + math.cos(angle) * radius - block_width // 2
                y = center_y + math.sin(angle) * radius - block_height // 2
                blocks.append(Block(x, y, block_width, block_height, True, colors[i % 3]))
        
        elif level == 3:
            # Level 3: Inverted pyramid
            block_width, block_height = 55, 22
            colors = [COLOR_ORANGE, COLOR_CYAN, COLOR_PURPLE, COLOR_PINK]
            start_y = 60
            rows = 6
            
            for row in range(rows):
                blocks_in_row = 6 - row
                start_x = (CANVAS_WIDTH - (blocks_in_row * (block_width + 8))) // 2
                for col in range(blocks_in_row):
                    x = start_x + col * (block_width + 8)
                    y = start_y + row * (block_height + 8)
                    blocks.append(Block(x, y, block_width, block_height, True, colors[row % len(colors)]))
        
        elif level == 4:
            # Level 4: Checkerboard
            block_width, block_height = 60, 20
            rows, cols = 4, 8
            start_x = (CANVAS_WIDTH - (cols * (block_width + 6))) // 2
            start_y = 80
            
            for row in range(rows):
                for col in range(cols):
                    if (row + col) % 2 == 0:
                        x = start_x + col * (block_width + 6)
                        y = start_y + row * (block_height + 6)
                        color = COLOR_PURPLE if row % 2 == 0 else COLOR_CYAN
                        blocks.append(Block(x, y, block_width, block_height, True, color))
        
        elif level == 5:
            # Level 5: The Fortress
            block_width, block_height = 50, 18
            colors = [COLOR_ORANGE, COLOR_CYAN, COLOR_PURPLE, COLOR_PINK]
            
            # Multi-layered fortress
            for i in range(12):
                blocks.append(Block(100 + i * 50, 80, block_width, block_height, True, colors[0]))
            for i in range(10):
                blocks.append(Block(150 + i * 50, 110, block_width, block_height, True, colors[1]))
            for i in range(8):
                blocks.append(Block(200 + i * 50, 140, block_width, block_height, True, colors[2]))
            for i in range(6):
                blocks.append(Block(250 + i * 50, 170, block_width, block_height, True, colors[3]))
        
        elif level == 6:
            # Level 6: Explosive Chaos (procedural)
            random_gen = self.seeded_random(12345)
            colors = [COLOR_ORANGE, COLOR_CYAN, COLOR_PURPLE, COLOR_PINK, COLOR_YELLOW]
            margin = 50
            max_y = 420
            num_clusters = 10
            patterns = ['tight', 'scattered', 'line', 'arc']
            
            for c in range(num_clusters):
                cluster_x = margin + random_gen() * (CANVAS_WIDTH - margin * 2 - 150)
                cluster_y = margin + random_gen() * (max_y - margin - 100)
                pattern = patterns[int(random_gen() * len(patterns))]
                block_count = 5 + int(random_gen() * 4)
                color = colors[int(random_gen() * len(colors))]
                block_width = 40 + random_gen() * 15
                block_height = 18 + random_gen() * 8
                
                self._generate_cluster(blocks, pattern, cluster_x, cluster_y, block_count, 
                                     block_width, block_height, color, random_gen, margin, max_y)
        
        elif level >= 100:
            # Procedural levels (100+) - infinite random levels
            random_gen = self.seeded_random(level)
            colors = [COLOR_ORANGE, COLOR_CYAN, COLOR_PURPLE, COLOR_PINK, COLOR_YELLOW]
            margin = 50
            max_y = 420
            
            level_difficulty = (level - 100) % 12
            num_clusters = 6 + level_difficulty // 2
            patterns = ['tight', 'scattered', 'line', 'arc', 'spiral']
            
            for c in range(num_clusters):
                cluster_x = margin + random_gen() * (CANVAS_WIDTH - margin * 2 - 150)
                cluster_y = margin + random_gen() * (max_y - margin - 100)
                pattern = patterns[int(random_gen() * len(patterns))]
                block_count = 4 + int(random_gen() * 6)
                color = colors[int(random_gen() * len(colors))]
                block_width = 35 + random_gen() * 20
                block_height = 18 + random_gen() * 10
                
                self._generate_cluster(blocks, pattern, cluster_x, cluster_y, block_count,
                                     block_width, block_height, color, random_gen, margin, max_y)
        
        return blocks
    
    def _generate_cluster(self, blocks, pattern, cx, cy, count, bw, bh, color, rand_fn, margin, max_y):
        """Helper to generate block clusters"""
        if pattern == 'tight':
            rows, cols = 2, (count + 1) // 2
            gap = 3 + rand_fn() * 4
            for i in range(count):
                row, col = i // cols, i % cols
                x, y = cx + col * (bw + gap), cy + row * (bh + gap)
                if margin <= x <= CANVAS_WIDTH - margin - bw and margin <= y <= max_y - bh:
                    blocks.append(Block(x, y, bw, bh, True, color))
        
        elif pattern == 'scattered':
            radius = 25 + rand_fn() * 35
            for i in range(count):
                angle = (i / count) * 2 * math.pi + rand_fn() * 0.6
                r = radius * (0.6 + rand_fn() * 0.7)
                x, y = cx + math.cos(angle) * r, cy + math.sin(angle) * r
                if margin <= x <= CANVAS_WIDTH - margin - bw and margin <= y <= max_y - bh:
                    blocks.append(Block(x, y, bw, bh, True, color))
        
        elif pattern == 'line':
            angle = rand_fn() * math.pi / 3 - math.pi / 6
            spacing = bw + 2 + rand_fn() * 6
            for i in range(count):
                x = cx + i * spacing * math.cos(angle)
                y = cy + i * spacing * math.sin(angle) + math.sin(i * 0.9) * 12
                if margin <= x <= CANVAS_WIDTH - margin - bw and margin <= y <= max_y - bh:
                    blocks.append(Block(x, y, bw, bh, True, color))
        
        elif pattern == 'arc':
            arc_radius = 35 + rand_fn() * 50
            start_angle = rand_fn() * math.pi
            arc_length = math.pi * 0.5 + rand_fn() * math.pi * 0.6
            for i in range(count):
                t = i / (count - 1) if count > 1 else 0
                angle = start_angle + t * arc_length
                x, y = cx + math.cos(angle) * arc_radius, cy + math.sin(angle) * arc_radius
                if margin <= x <= CANVAS_WIDTH - margin - bw and margin <= y <= max_y - bh:
                    blocks.append(Block(x, y, bw, bh, True, color))
        
        elif pattern == 'spiral':
            spiral_tightness = 3 + rand_fn() * 4
            for i in range(count):
                angle = (i / count) * math.pi * 2 * 1.5
                radius = 10 + (i / count) * spiral_tightness * 15
                x, y = cx + math.cos(angle) * radius, cy + math.sin(angle) * radius
                if margin <= x <= CANVAS_WIDTH - margin - bw and margin <= y <= max_y - bh:
                    blocks.append(Block(x, y, bw, bh, True, color))
    
    def start_level(self, level: int):
        """Initialize level"""
        self.current_level = level
        self.lives = 3
        self.score = 0
        self.ball_launched = False
        self.paddle_x = CANVAS_WIDTH // 2 - 60
        self.ball_x = CANVAS_WIDTH // 2
        self.ball_y = CANVAS_HEIGHT - 100
        self.ball_vx = 0
        self.ball_vy = 0
        self.blocks = self.generate_blocks_for_level(level)
        self.particles = []
        self.game_over_type = None
        self.state = GameState.GAME_SCREEN
    
    def create_particles(self, x: float, y: float, count: int, color: Tuple[int, int, int]):
        """Create particle explosion"""
        if not self.settings.particle_effects:
            return
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            self.particles.append(Particle(
                x, y,
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                1.0, 1.0, random.uniform(2, 4),
                color
            ))
    
    def update_game(self):
        """Update game physics"""
        if self.game_over_type:
            return
        
        # Move paddle
        if 0 <= self.mouse_x <= CANVAS_WIDTH:
            self.paddle_x = self.mouse_x - self.paddle_width // 2
            self.paddle_x = max(0, min(self.paddle_x, CANVAS_WIDTH - self.paddle_width))
        
        # Ball follows paddle if not launched
        if not self.ball_launched:
            self.ball_x = self.paddle_x + self.paddle_width // 2
            self.ball_y = CANVAS_HEIGHT - 100
        else:
            # Update ball
            self.ball_x += self.ball_vx
            self.ball_y += self.ball_vy
            
            # Wall collision
            if self.ball_x - self.ball_radius <= 0 or self.ball_x + self.ball_radius >= CANVAS_WIDTH:
                self.ball_vx = -self.ball_vx
                self.create_particles(self.ball_x, self.ball_y, 8, COLOR_CYAN)
            
            if self.ball_y - self.ball_radius <= 0:
                self.ball_vy = -self.ball_vy
                self.create_particles(self.ball_x, self.ball_y, 8, COLOR_CYAN)
            
            # Paddle collision
            paddle_y = CANVAS_HEIGHT - 40
            if (self.paddle_x <= self.ball_x <= self.paddle_x + self.paddle_width and
                paddle_y - self.ball_radius <= self.ball_y <= paddle_y + self.paddle_height):
                hit_pos = (self.ball_x - (self.paddle_x + self.paddle_width / 2)) / (self.paddle_width / 2)
                self.ball_vx = hit_pos * 5
                self.ball_vy = -abs(self.ball_vy)
                self.create_particles(self.ball_x, self.ball_y, 12, COLOR_PURPLE)
            
            # Block collision
            for block in self.blocks:
                if not block.alive:
                    continue
                if (block.x <= self.ball_x <= block.x + block.width and
                    block.y <= self.ball_y <= block.y + block.height):
                    block.alive = False
                    self.ball_vy = -self.ball_vy
                    self.score += 100
                    self.create_particles(block.x + block.width / 2, block.y + block.height / 2, 20, block.color)
                    break
            
            # Ball fell
            if self.ball_y > CANVAS_HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over_type = 'defeat'
                else:
                    self.ball_launched = False
                    self.ball_vx = 0
                    self.ball_vy = 0
        
        # Update particles
        for particle in self.particles[:]:
            particle.x += particle.vx
            particle.y += particle.vy
            particle.vy += 0.3
            particle.life -= 0.015
            if particle.life <= 0:
                self.particles.remove(particle)
        
        # Victory check
        if all(not block.alive for block in self.blocks) and not self.game_over_type:
            self.game_over_type = 'victory'
            if self.current_level + 1 not in self.unlocked_levels and self.current_level < 100:
                self.unlocked_levels.append(self.current_level + 1)
    
    def draw_glow_text(self, text: str, font, color: Tuple[int, int, int], x: int, y: int, center=False):
        """Draw text with glow effect"""
        # Glow layers
        glow_color = (*color, 80)
        for offset in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
            glow_surf = font.render(text, True, glow_color)
            rect = glow_surf.get_rect(center=(x + offset[0], y + offset[1])) if center else glow_surf.get_rect(topleft=(x + offset[0], y + offset[1]))
            self.screen.blit(glow_surf, rect)
        
        # Main text
        text_surf = font.render(text, True, color)
        rect = text_surf.get_rect(center=(x, y)) if center else text_surf.get_rect(topleft=(x, y))
        self.screen.blit(text_surf, rect)
        return rect
    
    def draw_glass_rect(self, x: int, y: int, width: int, height: int, 
                       border_color: Tuple[int, int, int], glow: bool = False, radius: int = 12):
        """Draw glass morphism rectangle"""
        # Background
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill(GLASS_BG)
        self.screen.blit(s, (x, y))
        
        # Glow
        if glow:
            for i in range(3):
                glow_rect = pygame.Rect(x - i*3, y - i*3, width + i*6, height + i*6)
                glow_color = (*border_color, 30 - i*10)
                s_glow = pygame.Surface((width + i*6, height + i*6), pygame.SRCALPHA)
                pygame.draw.rect(s_glow, glow_color, (0, 0, width + i*6, height + i*6), border_radius=radius+i*2)
                self.screen.blit(s_glow, (x - i*3, y - i*3))
        
        # Border
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 2, border_radius=radius)
    
    def draw_button(self, text: str, x: int, y: int, width: int, height: int,
                   color: Tuple[int, int, int], icon: str = None) -> bool:
        """Draw glass button and return if hovered"""
        rect = pygame.Rect(x, y, width, height)
        is_hover = rect.collidepoint(self.mouse_x, self.mouse_y)
        
        self.draw_glass_rect(x, y, width, height, color, is_hover)
        
        # Icon
        icon_x = x + 20
        if icon:
            icon_surf = self.font_small.render(icon, True, color)
            self.screen.blit(icon_surf, (icon_x, y + height // 2 - 12))
            icon_x += 40
        
        # Text
        text_surf = self.font_medium.render(text, True, color)
        text_rect = text_surf.get_rect(midleft=(icon_x, y + height // 2))
        self.screen.blit(text_surf, text_rect)
        
        return is_hover
    
    def draw_main_menu(self):
        """Draw main menu (matching React design)"""
        # Radial gradient background
        for y in range(SCREEN_HEIGHT):
            for x in range(0, SCREEN_WIDTH, 4):
                dist_tl = math.sqrt((x - SCREEN_WIDTH*0.2)**2 + (y - SCREEN_HEIGHT*0.2)**2)
                dist_br = math.sqrt((x - SCREEN_WIDTH*0.8)**2 + (y - SCREEN_HEIGHT*0.8)**2)
                
                glow_tl = max(0, 40 - dist_tl / 15)
                glow_br = max(0, 40 - dist_br / 15)
                
                r = BG_DARK[0] + int(glow_tl * 0.3 + glow_br * 0.15)
                g = BG_DARK[1] + int(glow_tl * 0.8 + glow_br * 0.4)
                b = BG_DARK[2] + int(glow_tl * 0.8 + glow_br * 0.1)
                
                pygame.draw.line(self.screen, (r, g, b), (x, y), (x+4, y))
        
        # Floating blocks
        for block in self.menu_blocks:
            float_y = math.sin(self.time * 0.5 + block['offset']) * 15
            size = block['size']
            x, y = int(block['x']), int(block['y'] + float_y)
            
            # Draw block with glow
            s = pygame.Surface((size, size), pygame.SRCALPHA)
            s.fill((*COLOR_PURPLE, 60))
            self.screen.blit(s, (x, y))
            pygame.draw.rect(self.screen, COLOR_PURPLE, (x, y, size, size), 2, border_radius=8)
            
            # Glow effect
            for i in range(2):
                glow_size = size + i*6
                glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*COLOR_PURPLE, 20-i*10), (0, 0, glow_size, glow_size), border_radius=10)
                self.screen.blit(glow_surf, (x-i*3, y-i*3))
        
        # Title
        title_x, title_y = 120, 200
        self.draw_glow_text("BLOCK", self.font_title, COLOR_CYAN, title_x, title_y)
        self.draw_glow_text("SMASHER", self.font_title, COLOR_ORANGE, title_x, title_y + 100)
        
        # Gradient line
        line_y = title_y + 220
        for i in range(250):
            t = i / 250
            if t < 0.33:
                color = COLOR_CYAN
            elif t < 0.66:
                color = COLOR_PURPLE
            else:
                color = COLOR_ORANGE
            pygame.draw.line(self.screen, color, (title_x + i, line_y), (title_x + i, line_y + 3))
        
        # Menu buttons
        button_x, button_y = 120, 450
        button_spacing = 70
        
        buttons = [
            ("▶", "PLAY", GameState.MAPS_SCREEN),
            ("◆", "MAPS", GameState.MAPS_SCREEN),
            ("★", "LEADERBOARD", GameState.LEADERBOARD_SCREEN),
        ]
        
        for i, (icon, text, next_state) in enumerate(buttons):
            y = button_y + i * button_spacing
            hover = self.draw_button(text, button_x, y, 350, 55, COLOR_CYAN, icon)
            
            if hover and self.mouse_clicked:
                self.state = next_state
        
        # Info card
        info_y = button_y + len(buttons) * button_spacing + 40
        self.draw_glass_rect(button_x, info_y, 350, 80, COLOR_CYAN)
        premium_text = self.font_small.render("PREMIUM EDITION", True, (*COLOR_FOREGROUND, 150))
        version_text = self.font_tiny.render("Version 1.0.0", True, (*COLOR_FOREGROUND, 100))
        self.screen.blit(premium_text, (button_x + 20, info_y + 15))
        self.screen.blit(version_text, (button_x + 20, info_y + 48))
        
        # Top-right icon (Settings)
        settings_x, settings_y = SCREEN_WIDTH - 80, 40
        settings_rect = pygame.Rect(settings_x, settings_y, 50, 50)
        is_hover = settings_rect.collidepoint(self.mouse_x, self.mouse_y)
        self.draw_glass_rect(settings_x, settings_y, 50, 50, COLOR_CYAN, is_hover, 25)
        gear_icon = self.font_medium.render("⚙", True, COLOR_CYAN)
        self.screen.blit(gear_icon, (settings_x + 12, settings_y + 10))
        
        if is_hover and self.mouse_clicked:
            self.state = GameState.SETTINGS_SCREEN
    
    def draw_maps_screen(self):
        """Draw maps selection screen"""
        self.screen.fill(BG_DARK)
        
        # Title
        self.draw_glow_text("SELECT MAP", self.font_large, COLOR_CYAN, 60, 40)
        
        # Back button
        back_rect = pygame.Rect(60, 120, 150, 50)
        back_hover = back_rect.collidepoint(self.mouse_x, self.mouse_y)
        self.draw_glass_rect(60, 120, 150, 50, COLOR_CYAN, back_hover)
        back_text = self.font_small.render("← BACK", True, COLOR_CYAN)
        self.screen.blit(back_text, (85, 133))
        
        if back_hover and self.mouse_clicked:
            self.state = GameState.MAIN_MENU
        
        # Tab buttons
        curated_rect = pygame.Rect(280, 120, 220, 50)
        procedural_rect = pygame.Rect(520, 120, 220, 50)
        
        curated_hover = curated_rect.collidepoint(self.mouse_x, self.mouse_y)
        procedural_hover = procedural_rect.collidepoint(self.mouse_x, self.mouse_y)
        
        self.draw_glass_rect(280, 120, 220, 50, COLOR_CYAN, 
                           curated_hover or self.maps_tab == MapsTab.CURATED)
        self.draw_glass_rect(520, 120, 220, 50, COLOR_PURPLE, 
                           procedural_hover or self.maps_tab == MapsTab.PROCEDURAL)
        
        curated_text = self.font_small.render("CURATED", True, COLOR_CYAN)
        procedural_text = self.font_small.render("PROCEDURAL", True, COLOR_PURPLE)
        self.screen.blit(curated_text, (320, 133))
        self.screen.blit(procedural_text, (540, 133))
        
        if curated_hover and self.mouse_clicked:
            self.maps_tab = MapsTab.CURATED
        if procedural_hover and self.mouse_clicked:
            self.maps_tab = MapsTab.PROCEDURAL
        
        # Draw maps
        if self.maps_tab == MapsTab.CURATED:
            self.draw_curated_maps()
        else:
            self.draw_procedural_maps()
    
    def draw_curated_maps(self):
        """Draw curated map cards"""
        maps = [
            (1, "First Steps", "Easy", 24),
            (2, "Circular Formation", "Medium", 8),
            (3, "Pyramid Power", "Medium", 36),
            (4, "Checkerboard", "Hard", 32),
            (5, "The Fortress", "Hard", 64),
            (6, "Explosive Chaos", "Extreme", 80),
        ]
        
        start_x, start_y = 60, 220
        card_width, card_height = 420, 150
        spacing = 30
        
        for i, (level_id, name, difficulty, blocks) in enumerate(maps):
            row, col = i // 3, i % 3
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            
            locked = level_id not in self.unlocked_levels
            color = (100, 100, 100) if locked else COLOR_CYAN
            
            card_rect = pygame.Rect(x, y, card_width, card_height)
            is_hover = card_rect.collidepoint(self.mouse_x, self.mouse_y) and not locked
            
            self.draw_glass_rect(x, y, card_width, card_height, color, is_hover)
            
            # Level number
            level_text = self.font_large.render(str(level_id), True, color)
            self.screen.blit(level_text, (x + 25, y + 20))
            
            # Name
            name_text = self.font_medium.render(name, True, COLOR_FOREGROUND if not locked else (150, 150, 150))
            self.screen.blit(name_text, (x + 100, y + 25))
            
            # Details
            details_text = self.font_small.render(f"{difficulty} | {blocks} blocks", True, COLOR_PURPLE if not locked else (120, 120, 120))
            self.screen.blit(details_text, (x + 100, y + 75))
            
            # Lock icon
            if locked:
                lock_text = self.font_large.render("🔒", True, (150, 150, 150))
                lock_rect = lock_text.get_rect(center=(x + card_width // 2, y + card_height // 2))
                self.screen.blit(lock_text, lock_rect)
            
            # Click handler
            if is_hover and self.mouse_clicked:
                self.start_level(level_id)
    
    def draw_procedural_maps(self):
        """Draw procedural map cards"""
        start_x, start_y = 60, 220
        card_width, card_height = 310, 130
        spacing = 25
        
        for i in range(12):
            level_id = 101 + i
            row, col = i // 4, i % 4
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            
            card_rect = pygame.Rect(x, y, card_width, card_height)
            is_hover = card_rect.collidepoint(self.mouse_x, self.mouse_y)
            
            self.draw_glass_rect(x, y, card_width, card_height, COLOR_PURPLE, is_hover)
            
            # Icon and number
            shuffle_text = self.font_large.render("🔀", True, COLOR_CYAN)
            self.screen.blit(shuffle_text, (x + 20, y + 15))
            
            num_text = self.font_large.render(str(i + 1), True, COLOR_PURPLE)
            self.screen.blit(num_text, (x + 90, y + 20))
            
            # Name
            name_text = self.font_small.render(f"Random Level #{i + 1}", True, COLOR_FOREGROUND)
            self.screen.blit(name_text, (x + 20, y + 70))
            
            # Difficulty
            difficulties = ['Easy', 'Medium', 'Hard', 'Expert']
            difficulty = difficulties[(i // 3) % 4]
            diff_text = self.font_tiny.render(difficulty, True, COLOR_PURPLE)
            self.screen.blit(diff_text, (x + 20, y + 100))
            
            # Click
            if is_hover and self.mouse_clicked:
                self.start_level(level_id)
    
    def draw_game_screen(self):
        """Draw gameplay screen"""
        self.screen.fill(BG_DARK)
        
        # Canvas
        canvas_x = (SCREEN_WIDTH - CANVAS_WIDTH) // 2
        canvas_y = (SCREEN_HEIGHT - CANVAS_HEIGHT) // 2 + 30
        
        # Canvas border with glow
        for i in range(3):
            glow_rect = pygame.Rect(canvas_x - 3 - i*2, canvas_y - 3 - i*2, CANVAS_WIDTH + 6 + i*4, CANVAS_HEIGHT + 6 + i*4)
            pygame.draw.rect(self.screen, (*COLOR_CYAN, 60 - i*20), glow_rect, 2)
        
        # Canvas background
        canvas_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        canvas_surface.fill((15, 20, 35))
        self.screen.blit(canvas_surface, (canvas_x, canvas_y))
        
        # Draw blocks
        for block in self.blocks:
            if block.alive:
                bx, by = canvas_x + int(block.x), canvas_y + int(block.y)
                pygame.draw.rect(self.screen, block.color, (bx, by, block.width, block.height), border_radius=4)
                
                # Block glow
                glow_rect = pygame.Rect(bx - 2, by - 2, block.width + 4, block.height + 4)
                s = pygame.Surface((block.width + 4, block.height + 4), pygame.SRCALPHA)
                pygame.draw.rect(s, (*block.color, 80), (0, 0, block.width + 4, block.height + 4), 1, border_radius=5)
                self.screen.blit(s, (bx - 2, by - 2))
        
        # Draw paddle
        paddle_y = CANVAS_HEIGHT - 40
        px, py = canvas_x + int(self.paddle_x), canvas_y + paddle_y
        pygame.draw.rect(self.screen, COLOR_PURPLE, (px, py, self.paddle_width, self.paddle_height), border_radius=4)
        
        # Paddle glow
        for i in range(3):
            s = pygame.Surface((self.paddle_width + i*4, self.paddle_height + i*4), pygame.SRCALPHA)
            pygame.draw.rect(s, (*COLOR_PURPLE, 50 - i*15), (0, 0, self.paddle_width + i*4, self.paddle_height + i*4), 1, border_radius=6)
            self.screen.blit(s, (px - i*2, py - i*2))
        
        # Draw ball
        ball_pos = (canvas_x + int(self.ball_x), canvas_y + int(self.ball_y))
        pygame.draw.circle(self.screen, COLOR_CYAN, ball_pos, self.ball_radius)
        
        # Ball glow
        for i in range(3):
            s = pygame.Surface((self.ball_radius*2 + i*4, self.ball_radius*2 + i*4), pygame.SRCALPHA)
            pygame.draw.circle(s, (*COLOR_CYAN, 80 - i*25), (self.ball_radius + i*2, self.ball_radius + i*2), self.ball_radius + i*2, 1)
            self.screen.blit(s, (ball_pos[0] - self.ball_radius - i*2, ball_pos[1] - self.ball_radius - i*2))
        
        # Draw particles
        for particle in self.particles:
            if particle.life > 0:
                alpha = int((particle.life / particle.max_life) * 255)
                pos = (canvas_x + int(particle.x), canvas_y + int(particle.y))
                size = max(1, int(particle.size * (particle.life / particle.max_life)))
                s = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*particle.color, min(255, alpha)), (size, size), size)
                self.screen.blit(s, (pos[0] - size, pos[1] - size))
        
        # HUD
        level_text = f"Random Level #{self.current_level - 99}" if self.current_level >= 100 else f"Level {self.current_level}"
        hud = self.font_small.render(f"{level_text} | Score: {self.score} | Lives: {self.lives}", True, COLOR_FOREGROUND)
        self.screen.blit(hud, (60, 30))
        
        # FPS
        if self.settings.show_fps:
            fps_text = self.font_small.render(f"FPS: {self.fps_counter}", True, COLOR_ORANGE)
            self.screen.blit(fps_text, (SCREEN_WIDTH - 130, 30))
        
        # Launch hint
        if not self.ball_launched:
            hint = self.font_small.render("SPACE or CLICK to launch", True, COLOR_CYAN)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(hint, hint_rect)
        
        # Game over overlay
        if self.game_over_type:
            self.draw_game_over_overlay()
        
        # Back/Pause button
        pause_rect = pygame.Rect(60, 90, 70, 50)
        pause_hover = pause_rect.collidepoint(self.mouse_x, self.mouse_y)
        self.draw_glass_rect(60, 90, 70, 50, COLOR_ORANGE, pause_hover)
        pause_text = self.font_medium.render("⏸", True, COLOR_ORANGE)
        self.screen.blit(pause_text, (78, 98))
        
        if pause_hover and self.mouse_clicked:
            self.state = GameState.MAPS_SCREEN
    
    def draw_game_over_overlay(self):
        """Draw victory/defeat overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        if self.game_over_type == 'victory':
            self.draw_glow_text("VICTORY!", self.font_title, COLOR_CYAN, SCREEN_WIDTH // 2, 280, center=True)
            stars = self.font_large.render("★ ★ ★", True, COLOR_YELLOW)
            stars_rect = stars.get_rect(center=(SCREEN_WIDTH // 2, 380))
            self.screen.blit(stars, stars_rect)
        else:
            self.draw_glow_text("GAME OVER", self.font_title, COLOR_ORANGE, SCREEN_WIDTH // 2, 280, center=True)
        
        # Score
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, COLOR_FOREGROUND)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 460))
        self.screen.blit(score_text, score_rect)
        
        # Buttons
        retry_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, 550, 220, 70)
        menu_rect = pygame.Rect(SCREEN_WIDTH // 2 + 30, 550, 220, 70)
        
        retry_hover = retry_rect.collidepoint(self.mouse_x, self.mouse_y)
        menu_hover = menu_rect.collidepoint(self.mouse_x, self.mouse_y)
        
        self.draw_glass_rect(retry_rect.x, retry_rect.y, retry_rect.width, retry_rect.height, COLOR_PURPLE, retry_hover)
        self.draw_glass_rect(menu_rect.x, menu_rect.y, menu_rect.width, menu_rect.height, COLOR_CYAN, menu_hover)
        
        retry_text = self.font_medium.render("RETRY", True, COLOR_PURPLE)
        menu_text = self.font_medium.render("MENU", True, COLOR_CYAN)
        retry_text_rect = retry_text.get_rect(center=retry_rect.center)
        menu_text_rect = menu_text.get_rect(center=menu_rect.center)
        self.screen.blit(retry_text, retry_text_rect)
        self.screen.blit(menu_text, menu_text_rect)
        
        if retry_hover and self.mouse_clicked:
            self.start_level(self.current_level)
        if menu_hover and self.mouse_clicked:
            self.state = GameState.MAPS_SCREEN
    
    def draw_settings_screen(self):
        """Draw settings screen"""
        self.screen.fill(BG_DARK)
        
        self.draw_glow_text("SETTINGS", self.font_large, COLOR_CYAN, 60, 40)
        
        # Back button
        back_rect = pygame.Rect(60, 120, 150, 50)
        back_hover = back_rect.collidepoint(self.mouse_x, self.mouse_y)
        self.draw_glass_rect(60, 120, 150, 50, COLOR_CYAN, back_hover)
        back_text = self.font_small.render("← BACK", True, COLOR_CYAN)
        self.screen.blit(back_text, (85, 133))
        
        if back_hover and self.mouse_clicked:
            self.state = GameState.MAIN_MENU
        
        # Settings
        y = 240
        spacing = 90
        
        settings_items = [
            f"Particle Effects: {'ON' if self.settings.particle_effects else 'OFF'}",
            f"Screen Shake: {'ON' if self.settings.screen_shake else 'OFF'}",
            f"Show FPS: {'ON' if self.settings.show_fps else 'OFF'}",
            f"Quality: {self.settings.quality.upper()}",
            f"Difficulty: {self.settings.difficulty.upper()}",
        ]
        
        for i, item in enumerate(settings_items):
            item_y = y + i * spacing
            item_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, item_y, 600, 70)
            item_hover = item_rect.collidepoint(self.mouse_x, self.mouse_y)
            
            self.draw_glass_rect(item_rect.x, item_rect.y, item_rect.width, item_rect.height, COLOR_PURPLE, item_hover)
            
            item_text = self.font_medium.render(item, True, COLOR_FOREGROUND)
            item_text_rect = item_text.get_rect(center=item_rect.center)
            self.screen.blit(item_text, item_text_rect)
            
            # Toggle particle effects
            if i == 0 and item_hover and self.mouse_clicked:
                self.settings.particle_effects = not self.settings.particle_effects
            # Toggle show FPS
            elif i == 2 and item_hover and self.mouse_clicked:
                self.settings.show_fps = not self.settings.show_fps
    
    def draw_leaderboard_screen(self):
        """Draw leaderboard screen"""
        self.screen.fill(BG_DARK)
        
        self.draw_glow_text("LEADERBOARD", self.font_large, COLOR_CYAN, 60, 40)
        
        # Back button
        back_rect = pygame.Rect(60, 120, 150, 50)
        back_hover = back_rect.collidepoint(self.mouse_x, self.mouse_y)
        self.draw_glass_rect(60, 120, 150, 50, COLOR_CYAN, back_hover)
        back_text = self.font_small.render("← BACK", True, COLOR_CYAN)
        self.screen.blit(back_text, (85, 133))
        
        if back_hover and self.mouse_clicked:
            self.state = GameState.MAIN_MENU
        
        # Podium (1st place)
        podium_y = 250
        self.draw_glass_rect(SCREEN_WIDTH // 2 - 150, podium_y, 300, 180, COLOR_YELLOW, True)
        
        first_text = self.font_title.render("1", True, COLOR_YELLOW)
        first_rect = first_text.get_rect(center=(SCREEN_WIDTH // 2, podium_y + 50))
        self.screen.blit(first_text, first_rect)
        
        name_text = self.font_medium.render("Player One", True, COLOR_FOREGROUND)
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, podium_y + 110))
        self.screen.blit(name_text, name_rect)
        
        score_text = self.font_small.render("15,420 pts", True, COLOR_CYAN)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, podium_y + 145))
        self.screen.blit(score_text, score_rect)
        
        # Leaderboard list
        list_y = podium_y + 230
        entries = [
            ("Player Two", 12500),
            ("Player Three", 10800),
            ("Player Four", 9200),
            ("Player Five", 8100),
        ]
        
        for i, (name, score) in enumerate(entries):
            entry_y = list_y + i * 70
            self.draw_glass_rect(SCREEN_WIDTH // 2 - 350, entry_y, 700, 60, COLOR_PURPLE)
            
            rank_text = self.font_medium.render(f"#{i + 2}", True, COLOR_CYAN)
            self.screen.blit(rank_text, (SCREEN_WIDTH // 2 - 320, entry_y + 15))
            
            name_text = self.font_medium.render(name, True, COLOR_FOREGROUND)
            self.screen.blit(name_text, (SCREEN_WIDTH // 2 - 220, entry_y + 15))
            
            score_text = self.font_medium.render(f"{score:,} pts", True, COLOR_ORANGE)
            score_rect = score_text.get_rect(right=SCREEN_WIDTH // 2 + 330, centery=entry_y + 30)
            self.screen.blit(score_text, score_rect)
    
    def handle_events(self):
        """Handle pygame events"""
        self.mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos
                
                # Adjust for canvas in game screen
                if self.state == GameState.GAME_SCREEN:
                    canvas_x = (SCREEN_WIDTH - CANVAS_WIDTH) // 2
                    self.mouse_x = event.pos[0] - canvas_x
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_clicked = True
                
                if self.state == GameState.GAME_SCREEN and not self.game_over_type:
                    if not self.ball_launched:
                        self.ball_launched = True
                        self.ball_vx = random.uniform(-3, 3)
                        self.ball_vy = -6
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == GameState.GAME_SCREEN and not self.game_over_type:
                        if not self.ball_launched:
                            self.ball_launched = True
                            self.ball_vx = random.uniform(-3, 3)
                            self.ball_vy = -6
                
                elif event.key == pygame.K_ESCAPE:
                    if self.state == GameState.GAME_SCREEN:
                        self.state = GameState.MAPS_SCREEN
                    elif self.state != GameState.MAIN_MENU:
                        self.state = GameState.MAIN_MENU
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.time += 0.016
            self.handle_events()
            
            # Clear screen
            self.screen.fill(BG_DARK)
            
            # Draw current screen
            if self.state == GameState.MAIN_MENU:
                self.draw_main_menu()
            elif self.state == GameState.MAPS_SCREEN:
                self.draw_maps_screen()
            elif self.state == GameState.GAME_SCREEN:
                self.update_game()
                self.draw_game_screen()
            elif self.state == GameState.SETTINGS_SCREEN:
                self.draw_settings_screen()
            elif self.state == GameState.LEADERBOARD_SCREEN:
                self.draw_leaderboard_screen()
            
            # Update display
            pygame.display.flip()
            
            # Track FPS
            self.clock.tick(FPS)
            self.fps_counter = int(self.clock.get_fps())
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = BlockSmasher()
    game.run()
