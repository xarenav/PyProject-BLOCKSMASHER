"""
Block Smash - Futuristic Neon Block Breaker Game
Python/Pygame Implementation
"""

import pygame
import random
import math
import json
import os
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FPS = 60

# Colors (Cyan/Purple/Orange neon theme)
BG_DARK = (10, 14, 26)
COLOR_CYAN = (64, 224, 208)
COLOR_PURPLE = (147, 112, 219)
COLOR_ORANGE = (255, 140, 0)
COLOR_PINK = (236, 72, 153)
COLOR_YELLOW = (234, 179, 8)
COLOR_WHITE = (230, 237, 243)
COLOR_GLASS = (255, 255, 255, 30)

# Game States
class GameState(Enum):
    MAIN_MENU = 1
    MAPS_SCREEN = 2
    GAME_SCREEN = 3
    SETTINGS_SCREEN = 4
    LEADERBOARD_SCREEN = 5
    PAUSE_SCREEN = 6

# Tab States for Maps
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
    color: Tuple[int, int, int]

@dataclass
class Settings:
    sound_enabled: bool = True
    music_volume: float = 0.7
    sfx_volume: float = 0.8
    particle_effects: bool = True
    screen_shake: bool = True
    show_fps: bool = False

class BlockSmashGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Block Smash - Futuristic Neon Edition")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        try:
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 48)
            self.font_small = pygame.font.Font(None, 32)
            self.font_tiny = pygame.font.Font(None, 24)
        except:
            self.font_large = pygame.font.SysFont('Arial', 72)
            self.font_medium = pygame.font.SysFont('Arial', 48)
            self.font_small = pygame.font.SysFont('Arial', 32)
            self.font_tiny = pygame.font.SysFont('Arial', 24)
        
        # Game state
        self.state = GameState.MAIN_MENU
        self.maps_tab = MapsTab.CURATED
        self.settings = Settings()
        
        # Game variables
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
        
        # Animation variables
        self.menu_float_offset = 0
        self.menu_particles = []
        self.game_over_type = None  # 'victory' or 'defeat'
        
        # FPS tracking
        self.fps = 0
        
        # Mouse state
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        
    def seeded_random(self, seed: int):
        """Seeded random number generator for procedural levels"""
        state = seed
        def rand():
            nonlocal state
            state = (state * 1664525 + 1013904223) % 4294967296
            return state / 4294967296
        return rand
    
    def generate_blocks_for_level(self, level: int) -> List[Block]:
        """Generate blocks based on level number"""
        blocks = []
        
        if level == 1:
            # Level 1: Classic grid
            rows, cols = 4, 6
            block_width = 70
            block_height = 25
            start_x = (CANVAS_WIDTH - (cols * (block_width + 10))) // 2
            start_y = 80
            colors = [COLOR_CYAN, COLOR_PURPLE, COLOR_ORANGE, COLOR_PINK]
            
            for row in range(rows):
                for col in range(cols):
                    x = start_x + col * (block_width + 10)
                    y = start_y + row * (block_height + 10)
                    color = colors[row % len(colors)]
                    blocks.append(Block(x, y, block_width, block_height, True, color))
        
        elif level == 2:
            # Level 2: Circle formation
            center_x, center_y = CANVAS_WIDTH // 2, 200
            radius = 100
            num_blocks = 8
            block_width, block_height = 60, 25
            
            for i in range(num_blocks):
                angle = (i / num_blocks) * 2 * math.pi
                x = center_x + math.cos(angle) * radius - block_width // 2
                y = center_y + math.sin(angle) * radius - block_height // 2
                color = [COLOR_CYAN, COLOR_PURPLE, COLOR_ORANGE][i % 3]
                blocks.append(Block(x, y, block_width, block_height, True, color))
        
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
            # Level 5: The Fortress (multi-layered)
            block_width, block_height = 50, 18
            colors = [COLOR_ORANGE, COLOR_CYAN, COLOR_PURPLE, COLOR_PINK]
            
            # Outer wall
            for i in range(12):
                blocks.append(Block(100 + i * 50, 80, block_width, block_height, True, colors[0]))
            # Second layer
            for i in range(10):
                blocks.append(Block(150 + i * 50, 110, block_width, block_height, True, colors[1]))
            # Third layer
            for i in range(8):
                blocks.append(Block(200 + i * 50, 140, block_width, block_height, True, colors[2]))
            # Core
            for i in range(6):
                blocks.append(Block(250 + i * 50, 170, block_width, block_height, True, colors[3]))
        
        elif level == 6:
            # Level 6: Explosive Chaos (original procedural)
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
                
                if pattern == 'tight':
                    rows = 2
                    cols = (block_count + 1) // 2
                    gap = 4 + random_gen() * 3
                    for i in range(block_count):
                        row = i // cols
                        col = i % cols
                        x = cluster_x + col * (block_width + gap)
                        y = cluster_y + row * (block_height + gap)
                        if margin <= x <= CANVAS_WIDTH - margin - block_width and margin <= y <= max_y - block_height:
                            blocks.append(Block(x, y, block_width, block_height, True, color))
                
                elif pattern == 'scattered':
                    radius = 25 + random_gen() * 30
                    for i in range(block_count):
                        angle = (i / block_count) * 2 * math.pi + random_gen() * 0.5
                        r = radius * (0.7 + random_gen() * 0.6)
                        x = cluster_x + math.cos(angle) * r
                        y = cluster_y + math.sin(angle) * r
                        if margin <= x <= CANVAS_WIDTH - margin - block_width and margin <= y <= max_y - block_height:
                            blocks.append(Block(x, y, block_width, block_height, True, color))
                
                elif pattern == 'line':
                    angle = random_gen() * math.pi / 4 - math.pi / 8
                    spacing = block_width + 3 + random_gen() * 5
                    for i in range(block_count):
                        x = cluster_x + i * spacing * math.cos(angle)
                        y = cluster_y + i * spacing * math.sin(angle) + math.sin(i * 0.8) * 10
                        if margin <= x <= CANVAS_WIDTH - margin - block_width and margin <= y <= max_y - block_height:
                            blocks.append(Block(x, y, block_width, block_height, True, color))
                
                elif pattern == 'arc':
                    arc_radius = 40 + random_gen() * 40
                    start_angle = random_gen() * math.pi
                    arc_length = math.pi * 0.6 + random_gen() * math.pi * 0.4
                    for i in range(block_count):
                        t = i / (block_count - 1) if block_count > 1 else 0
                        angle = start_angle + t * arc_length
                        x = cluster_x + math.cos(angle) * arc_radius
                        y = cluster_y + math.sin(angle) * arc_radius
                        if margin <= x <= CANVAS_WIDTH - margin - block_width and margin <= y <= max_y - block_height:
                            blocks.append(Block(x, y, block_width, block_height, True, color))
        
        elif level >= 100:
            # Procedural levels (100+)
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
                
                if pattern == 'tight':
                    rows = 2
                    cols = (block_count + 1) // 2
                    gap = 3 + random_gen() * 4
                    for i in range(block_count):
                        row = i // cols
                        col = i % cols
                        x = cluster_x + col * (block_width + gap)
                        y = cluster_y + row * (block_height + gap)
                        if margin <= x <= CANVAS_WIDTH - margin - block_width and margin <= y <= max_y - block_height:
                            blocks.append(Block(x, y, block_width, block_height, True, color))
                
                elif pattern == 'scattered':
                    radius = 25 + random_gen() * 35
                    for i in range(block_count):
                        angle = (i / block_count) * 2 * math.pi + random_gen() * 0.6
                        r = radius * (0.6 + random_gen() * 0.7)
                        x = cluster_x + math.cos(angle) * r
                        y = cluster_y + math.sin(angle) * r
                        if margin <= x <= CANVAS_WIDTH - margin - block_width and margin <= y <= max_y - block_height:
                            blocks.append(Block(x, y, block_width, block_height, True, color))
                
                elif pattern == 'line':
                    angle = random_gen() * math.pi / 3 - math.pi / 6
                    spacing = block_width + 2 + random_gen() * 6
                    for i in range(block_count):
                        x = cluster_x + i * spacing * math.cos(angle)
                        y = cluster_y + i * spacing * math.sin(angle) + math.sin(i * 0.9) * 12
                        if margin <= x <= CANVAS_WIDTH - margin - block_width and margin <= y <= max_y - block_height:
                            blocks.append(Block(x, y, block_width, block_height, True, color))
                
                elif pattern == 'arc':
                    arc_radius = 35 + random_gen() * 50
                    start_angle = random_gen() * math.pi
                    arc_length = math.pi * 0.5 + random_gen() * math.pi * 0.6
                    for i in range(block_count):
                        t = i / (block_count - 1) if block_count > 1 else 0
                        angle = start_angle + t * arc_length
                        x = cluster_x + math.cos(angle) * arc_radius
                        y = cluster_y + math.sin(angle) * arc_radius
                        if margin <= x <= CANVAS_WIDTH - margin - block_width and margin <= y <= max_y - block_height:
                            blocks.append(Block(x, y, block_width, block_height, True, color))
                
                elif pattern == 'spiral':
                    spiral_tightness = 3 + random_gen() * 4
                    for i in range(block_count):
                        angle = (i / block_count) * math.pi * 2 * 1.5
                        radius = 10 + (i / block_count) * spiral_tightness * 15
                        x = cluster_x + math.cos(angle) * radius
                        y = cluster_y + math.sin(angle) * radius
                        if margin <= x <= CANVAS_WIDTH - margin - block_width and margin <= y <= max_y - block_height:
                            blocks.append(Block(x, y, block_width, block_height, True, color))
        
        return blocks
    
    def start_level(self, level: int):
        """Initialize a new level"""
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
            speed = random.uniform(1, 4)
            self.particles.append(Particle(
                x, y,
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                1.0,
                color
            ))
    
    def update_game(self):
        """Update game physics"""
        if self.game_over_type:
            return
        
        # Move paddle with mouse
        if 0 <= self.mouse_x <= CANVAS_WIDTH:
            self.paddle_x = self.mouse_x - self.paddle_width // 2
            self.paddle_x = max(0, min(self.paddle_x, CANVAS_WIDTH - self.paddle_width))
        
        # Move ball with paddle if not launched
        if not self.ball_launched:
            self.ball_x = self.paddle_x + self.paddle_width // 2
            self.ball_y = CANVAS_HEIGHT - 100
        else:
            # Update ball position
            self.ball_x += self.ball_vx
            self.ball_y += self.ball_vy
            
            # Ball collision with walls
            if self.ball_x - self.ball_radius <= 0 or self.ball_x + self.ball_radius >= CANVAS_WIDTH:
                self.ball_vx = -self.ball_vx
                self.create_particles(self.ball_x, self.ball_y, 8, COLOR_CYAN)
            
            if self.ball_y - self.ball_radius <= 0:
                self.ball_vy = -self.ball_vy
                self.create_particles(self.ball_x, self.ball_y, 8, COLOR_CYAN)
            
            # Ball collision with paddle
            if (self.paddle_x <= self.ball_x <= self.paddle_x + self.paddle_width and
                self.paddle_y - self.ball_radius <= self.ball_y <= self.paddle_y + self.paddle_height):
                # Calculate hit position (-1 to 1)
                hit_pos = (self.ball_x - (self.paddle_x + self.paddle_width / 2)) / (self.paddle_width / 2)
                self.ball_vx = hit_pos * 5
                self.ball_vy = -abs(self.ball_vy)
                self.create_particles(self.ball_x, self.ball_y, 10, COLOR_PURPLE)
            
            # Ball collision with blocks
            for block in self.blocks:
                if not block.alive:
                    continue
                
                if (block.x <= self.ball_x <= block.x + block.width and
                    block.y <= self.ball_y <= block.y + block.height):
                    block.alive = False
                    self.ball_vy = -self.ball_vy
                    self.score += 100
                    self.create_particles(
                        block.x + block.width / 2,
                        block.y + block.height / 2,
                        15,
                        block.color
                    )
                    break
            
            # Ball fell off screen
            if self.ball_y > CANVAS_HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over_type = 'defeat'
                else:
                    self.ball_launched = False
                    self.ball_x = CANVAS_WIDTH // 2
                    self.ball_y = CANVAS_HEIGHT - 100
                    self.ball_vx = 0
                    self.ball_vy = 0
        
        # Update particles
        for particle in self.particles[:]:
            particle.x += particle.vx
            particle.y += particle.vy
            particle.vy += 0.2  # Gravity
            particle.life -= 0.02
            if particle.life <= 0:
                self.particles.remove(particle)
        
        # Check for victory
        if all(not block.alive for block in self.blocks) and not self.game_over_type:
            self.game_over_type = 'victory'
            if self.current_level + 1 not in self.unlocked_levels and self.current_level < 100:
                self.unlocked_levels.append(self.current_level + 1)
    
    @property
    def paddle_y(self):
        return CANVAS_HEIGHT - 40
    
    def draw_glass_rect(self, x: int, y: int, width: int, height: int, 
                       border_color: Tuple[int, int, int], glow: bool = False):
        """Draw a glass morphism rectangle"""
        # Glass background
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill(COLOR_GLASS)
        self.screen.blit(s, (x, y))
        
        # Border
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 2, border_radius=10)
        
        # Glow effect
        if glow:
            glow_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*border_color, 50), 
                           (0, 0, width + 20, height + 20), border_radius=15)
            self.screen.blit(glow_surface, (x - 10, y - 10))
    
    def draw_button(self, text: str, x: int, y: int, width: int, height: int,
                   color: Tuple[int, int, int], hover: bool = False) -> bool:
        """Draw a button and return if clicked"""
        rect = pygame.Rect(x, y, width, height)
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)
        
        # Draw glass button
        self.draw_glass_rect(x, y, width, height, color, is_hover or hover)
        
        # Draw text
        text_surf = self.font_small.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surf, text_rect)
        
        return is_hover
    
    def draw_main_menu(self):
        """Draw main menu screen"""
        # Background gradient simulation
        for i in range(SCREEN_HEIGHT):
            alpha = int(30 * (1 - i / SCREEN_HEIGHT))
            color = (64 + alpha, 224 + alpha, 208 + alpha)
            pygame.draw.line(self.screen, color, (0, i), (SCREEN_WIDTH, i))
        
        # Title
        title = self.font_large.render("BLOCK SMASH", True, COLOR_CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        # Glowing title effect
        glow = self.font_large.render("BLOCK SMASH", True, (*COLOR_CYAN, 100))
        glow_rect = glow.get_rect(center=(SCREEN_WIDTH // 2 + 2, 152))
        self.screen.blit(glow, glow_rect)
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_tiny.render("Futuristic Neon Edition", True, COLOR_PURPLE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Buttons
        button_y = 320
        button_spacing = 80
        
        buttons = [
            ("PLAY", GameState.MAPS_SCREEN),
            ("LEADERBOARD", GameState.LEADERBOARD_SCREEN),
            ("SETTINGS", GameState.SETTINGS_SCREEN),
            ("QUIT", None)
        ]
        
        for i, (text, next_state) in enumerate(buttons):
            y = button_y + i * button_spacing
            hover = self.draw_button(text, SCREEN_WIDTH // 2 - 150, y, 300, 60, COLOR_CYAN)
            
            if hover and pygame.mouse.get_pressed()[0]:
                if next_state is None:
                    self.running = False
                else:
                    self.state = next_state
                pygame.time.wait(200)
    
    def draw_maps_screen(self):
        """Draw maps selection screen"""
        # Background
        self.screen.fill(BG_DARK)
        
        # Title
        title = self.font_medium.render("SELECT MAP", True, COLOR_CYAN)
        self.screen.blit(title, (50, 30))
        
        # Back button
        if self.draw_button("← BACK", 50, 100, 150, 50, COLOR_CYAN):
            if pygame.mouse.get_pressed()[0]:
                self.state = GameState.MAIN_MENU
                pygame.time.wait(200)
        
        # Tab buttons
        tab_y = 100
        curated_hover = self.draw_button("CURATED", 250, tab_y, 200, 50, COLOR_CYAN, 
                                        self.maps_tab == MapsTab.CURATED)
        procedural_hover = self.draw_button("PROCEDURAL", 470, tab_y, 200, 50, COLOR_PURPLE,
                                           self.maps_tab == MapsTab.PROCEDURAL)
        
        if curated_hover and pygame.mouse.get_pressed()[0]:
            self.maps_tab = MapsTab.CURATED
            pygame.time.wait(200)
        if procedural_hover and pygame.mouse.get_pressed()[0]:
            self.maps_tab = MapsTab.PROCEDURAL
            pygame.time.wait(200)
        
        # Draw maps grid
        if self.maps_tab == MapsTab.CURATED:
            self.draw_curated_maps()
        else:
            self.draw_procedural_maps()
    
    def draw_curated_maps(self):
        """Draw curated maps grid"""
        maps = [
            (1, "First Steps", "Easy", 24),
            (2, "Circular Formation", "Medium", 8),
            (3, "Pyramid Power", "Medium", 36),
            (4, "Checkerboard", "Hard", 32),
            (5, "The Fortress", "Hard", 64),
            (6, "Explosive Chaos", "Extreme", 80),
        ]
        
        start_x, start_y = 50, 200
        card_width, card_height = 350, 140
        spacing = 20
        
        for i, (level_id, name, difficulty, blocks) in enumerate(maps):
            row = i // 3
            col = i % 3
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            
            locked = level_id not in self.unlocked_levels
            
            # Card background
            self.draw_glass_rect(x, y, card_width, card_height, COLOR_CYAN if not locked else (100, 100, 100))
            
            # Level number
            level_text = self.font_medium.render(str(level_id), True, COLOR_CYAN if not locked else (100, 100, 100))
            self.screen.blit(level_text, (x + 20, y + 15))
            
            # Name
            name_text = self.font_small.render(name, True, COLOR_WHITE if not locked else (150, 150, 150))
            self.screen.blit(name_text, (x + 80, y + 20))
            
            # Difficulty and blocks
            diff_text = self.font_tiny.render(f"{difficulty} | {blocks} blocks", True, 
                                             COLOR_PURPLE if not locked else (120, 120, 120))
            self.screen.blit(diff_text, (x + 80, y + 60))
            
            # Click handler
            rect = pygame.Rect(x, y, card_width, card_height)
            if not locked and rect.collidepoint(pygame.mouse.get_pos()):
                # Hover effect
                pygame.draw.rect(self.screen, COLOR_CYAN, rect, 3, border_radius=10)
                
                if pygame.mouse.get_pressed()[0]:
                    self.start_level(level_id)
                    pygame.time.wait(200)
            
            # Lock overlay
            if locked:
                lock_text = self.font_medium.render("🔒", True, (150, 150, 150))
                lock_rect = lock_text.get_rect(center=(x + card_width // 2, y + card_height // 2))
                self.screen.blit(lock_text, lock_rect)
    
    def draw_procedural_maps(self):
        """Draw procedural maps grid"""
        start_x, start_y = 50, 200
        card_width, card_height = 270, 120
        spacing = 20
        
        for i in range(12):
            level_id = 101 + i
            row = i // 4
            col = i % 4
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            
            # Card background
            self.draw_glass_rect(x, y, card_width, card_height, COLOR_PURPLE)
            
            # Shuffle icon and number
            shuffle_text = self.font_medium.render("🔀", True, COLOR_CYAN)
            self.screen.blit(shuffle_text, (x + 20, y + 15))
            
            num_text = self.font_medium.render(str(i + 1), True, COLOR_PURPLE)
            self.screen.blit(num_text, (x + 80, y + 20))
            
            # Name
            name_text = self.font_small.render(f"Random Level #{i + 1}", True, COLOR_WHITE)
            self.screen.blit(name_text, (x + 20, y + 60))
            
            # Difficulty
            difficulties = ['Easy', 'Medium', 'Hard', 'Expert']
            difficulty = difficulties[(i // 3) % 4]
            diff_text = self.font_tiny.render(difficulty, True, COLOR_PURPLE)
            self.screen.blit(diff_text, (x + 20, y + 90))
            
            # Click handler
            rect = pygame.Rect(x, y, card_width, card_height)
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, COLOR_PURPLE, rect, 3, border_radius=10)
                
                if pygame.mouse.get_pressed()[0]:
                    self.start_level(level_id)
                    pygame.time.wait(200)
    
    def draw_game_screen(self):
        """Draw active gameplay screen"""
        # Dark background
        self.screen.fill(BG_DARK)
        
        # Game canvas area
        canvas_x = (SCREEN_WIDTH - CANVAS_WIDTH) // 2
        canvas_y = (SCREEN_HEIGHT - CANVAS_HEIGHT) // 2 + 30
        
        # Canvas border with glow
        pygame.draw.rect(self.screen, COLOR_CYAN, 
                        (canvas_x - 3, canvas_y - 3, CANVAS_WIDTH + 6, CANVAS_HEIGHT + 6), 3)
        
        # Canvas background
        canvas_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        canvas_surface.fill((15, 20, 35))
        self.screen.blit(canvas_surface, (canvas_x, canvas_y))
        
        # Draw blocks
        for block in self.blocks:
            if block.alive:
                block_rect = pygame.Rect(canvas_x + block.x, canvas_y + block.y, 
                                        block.width, block.height)
                pygame.draw.rect(self.screen, block.color, block_rect, border_radius=3)
                # Glow effect
                glow_rect = pygame.Rect(canvas_x + block.x - 2, canvas_y + block.y - 2,
                                       block.width + 4, block.height + 4)
                pygame.draw.rect(self.screen, (*block.color, 100), glow_rect, 2, border_radius=4)
        
        # Draw paddle
        paddle_rect = pygame.Rect(canvas_x + self.paddle_x, canvas_y + self.paddle_y,
                                 self.paddle_width, self.paddle_height)
        pygame.draw.rect(self.screen, COLOR_PURPLE, paddle_rect, border_radius=3)
        
        # Paddle glow
        for i in range(3):
            glow_rect = pygame.Rect(canvas_x + self.paddle_x - i*2, canvas_y + self.paddle_y - i*2,
                                   self.paddle_width + i*4, self.paddle_height + i*4)
            pygame.draw.rect(self.screen, (*COLOR_PURPLE, 50 - i*15), glow_rect, 1, border_radius=5)
        
        # Draw ball
        ball_pos = (int(canvas_x + self.ball_x), int(canvas_y + self.ball_y))
        pygame.draw.circle(self.screen, COLOR_CYAN, ball_pos, self.ball_radius)
        
        # Ball glow
        for i in range(3):
            pygame.draw.circle(self.screen, (*COLOR_CYAN, 80 - i*25), ball_pos, self.ball_radius + i*2, 1)
        
        # Draw particles
        for particle in self.particles:
            if particle.life > 0:
                alpha = int(particle.life * 255)
                color = (*particle.color, min(255, alpha))
                pos = (int(canvas_x + particle.x), int(canvas_y + particle.y))
                size = max(1, int(particle.life * 3))
                pygame.draw.circle(self.screen, color, pos, size)
        
        # HUD
        level_text = f"Random Level #{self.current_level - 99}" if self.current_level >= 100 else f"Level {self.current_level}"
        hud_text = self.font_tiny.render(f"{level_text} | Score: {self.score} | Lives: {self.lives}", 
                                        True, COLOR_WHITE)
        self.screen.blit(hud_text, (50, 20))
        
        # FPS
        if self.settings.show_fps:
            fps_text = self.font_tiny.render(f"FPS: {self.fps}", True, COLOR_ORANGE)
            self.screen.blit(fps_text, (SCREEN_WIDTH - 120, 20))
        
        # Controls hint
        if not self.ball_launched:
            hint = self.font_tiny.render("SPACE or CLICK to launch ball", True, COLOR_CYAN)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
            self.screen.blit(hint, hint_rect)
        
        # Game over overlay
        if self.game_over_type:
            self.draw_game_over_overlay()
        
        # Back button
        if self.draw_button("⏸", 50, 70, 60, 50, COLOR_ORANGE):
            if pygame.mouse.get_pressed()[0]:
                self.state = GameState.MAPS_SCREEN
                pygame.time.wait(200)
    
    def draw_game_over_overlay(self):
        """Draw victory or defeat overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        if self.game_over_type == 'victory':
            # Victory
            title = self.font_large.render("VICTORY!", True, COLOR_CYAN)
            stars = "★ ★ ★"
            star_text = self.font_medium.render(stars, True, COLOR_YELLOW)
        else:
            # Defeat
            title = self.font_large.render("GAME OVER", True, COLOR_ORANGE)
            star_text = None
        
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(title, title_rect)
        
        if star_text:
            star_rect = star_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
            self.screen.blit(star_text, star_rect)
        
        # Score
        score_text = self.font_small.render(f"Final Score: {self.score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(score_text, score_rect)
        
        # Buttons
        if self.draw_button("RETRY", SCREEN_WIDTH // 2 - 220, 500, 200, 60, COLOR_PURPLE):
            if pygame.mouse.get_pressed()[0]:
                self.start_level(self.current_level)
                pygame.time.wait(200)
        
        if self.draw_button("MENU", SCREEN_WIDTH // 2 + 20, 500, 200, 60, COLOR_CYAN):
            if pygame.mouse.get_pressed()[0]:
                self.state = GameState.MAPS_SCREEN
                pygame.time.wait(200)
    
    def draw_settings_screen(self):
        """Draw settings screen"""
        self.screen.fill(BG_DARK)
        
        # Title
        title = self.font_medium.render("SETTINGS", True, COLOR_CYAN)
        self.screen.blit(title, (50, 30))
        
        # Back button
        if self.draw_button("← BACK", 50, 100, 150, 50, COLOR_CYAN):
            if pygame.mouse.get_pressed()[0]:
                self.state = GameState.MAIN_MENU
                pygame.time.wait(200)
        
        # Settings options
        y = 200
        spacing = 80
        
        # Sound toggle
        sound_text = f"Sound Effects: {'ON' if self.settings.sound_enabled else 'OFF'}"
        self.draw_button(sound_text, SCREEN_WIDTH // 2 - 200, y, 400, 60, COLOR_PURPLE)
        
        # Music volume
        y += spacing
        music_text = f"Music Volume: {int(self.settings.music_volume * 100)}%"
        self.draw_button(music_text, SCREEN_WIDTH // 2 - 200, y, 400, 60, COLOR_PURPLE)
        
        # SFX volume
        y += spacing
        sfx_text = f"SFX Volume: {int(self.settings.sfx_volume * 100)}%"
        self.draw_button(sfx_text, SCREEN_WIDTH // 2 - 200, y, 400, 60, COLOR_PURPLE)
        
        # Particles
        y += spacing
        particles_text = f"Particle Effects: {'ON' if self.settings.particle_effects else 'OFF'}"
        if self.draw_button(particles_text, SCREEN_WIDTH // 2 - 200, y, 400, 60, COLOR_PURPLE):
            if pygame.mouse.get_pressed()[0]:
                self.settings.particle_effects = not self.settings.particle_effects
                pygame.time.wait(200)
        
        # Screen shake
        y += spacing
        shake_text = f"Screen Shake: {'ON' if self.settings.screen_shake else 'OFF'}"
        if self.draw_button(shake_text, SCREEN_WIDTH // 2 - 200, y, 400, 60, COLOR_PURPLE):
            if pygame.mouse.get_pressed()[0]:
                self.settings.screen_shake = not self.settings.screen_shake
                pygame.time.wait(200)
        
        # Show FPS
        y += spacing
        fps_text = f"Show FPS: {'ON' if self.settings.show_fps else 'OFF'}"
        if self.draw_button(fps_text, SCREEN_WIDTH // 2 - 200, y, 400, 60, COLOR_PURPLE):
            if pygame.mouse.get_pressed()[0]:
                self.settings.show_fps = not self.settings.show_fps
                pygame.time.wait(200)
    
    def draw_leaderboard_screen(self):
        """Draw leaderboard screen"""
        self.screen.fill(BG_DARK)
        
        # Title
        title = self.font_medium.render("LEADERBOARD", True, COLOR_CYAN)
        self.screen.blit(title, (50, 30))
        
        # Back button
        if self.draw_button("← BACK", 50, 100, 150, 50, COLOR_CYAN):
            if pygame.mouse.get_pressed()[0]:
                self.state = GameState.MAIN_MENU
                pygame.time.wait(200)
        
        # Podium (mock data)
        podium_y = 200
        
        # 1st place
        self.draw_glass_rect(SCREEN_WIDTH // 2 - 120, podium_y, 240, 150, COLOR_YELLOW, True)
        first_text = self.font_large.render("1", True, COLOR_YELLOW)
        first_rect = first_text.get_rect(center=(SCREEN_WIDTH // 2, podium_y + 40))
        self.screen.blit(first_text, first_rect)
        
        name_text = self.font_small.render("Player One", True, COLOR_WHITE)
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, podium_y + 90))
        self.screen.blit(name_text, name_rect)
        
        score_text = self.font_tiny.render("15,420 pts", True, COLOR_CYAN)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, podium_y + 120))
        self.screen.blit(score_text, score_rect)
        
        # Leaderboard list
        list_y = podium_y + 200
        entries = [
            ("Player Two", 12500),
            ("Player Three", 10800),
            ("Player Four", 9200),
            ("Player Five", 8100),
        ]
        
        for i, (name, score) in enumerate(entries):
            y = list_y + i * 60
            self.draw_glass_rect(SCREEN_WIDTH // 2 - 300, y, 600, 50, COLOR_PURPLE)
            
            rank = self.font_small.render(f"#{i + 2}", True, COLOR_CYAN)
            self.screen.blit(rank, (SCREEN_WIDTH // 2 - 280, y + 12))
            
            name_text = self.font_small.render(name, True, COLOR_WHITE)
            self.screen.blit(name_text, (SCREEN_WIDTH // 2 - 200, y + 12))
            
            score_text = self.font_small.render(f"{score:,} pts", True, COLOR_ORANGE)
            score_rect = score_text.get_rect(right=SCREEN_WIDTH // 2 + 280, centery=y + 25)
            self.screen.blit(score_text, score_rect)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos
                # Adjust for canvas offset
                if self.state == GameState.GAME_SCREEN:
                    canvas_x = (SCREEN_WIDTH - CANVAS_WIDTH) // 2
                    self.mouse_x = event.pos[0] - canvas_x
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
            self.handle_events()
            
            # Clear screen
            self.screen.fill(BG_DARK)
            
            # Update and draw based on state
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
            self.fps = int(self.clock.get_fps())
        
        pygame.quit()

if __name__ == "__main__":
    game = BlockSmashGame()
    game.run()
