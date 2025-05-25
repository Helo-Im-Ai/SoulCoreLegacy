"""
Generate RPG-themed thumbnail images for SoulCoreLegacy Arcade.
This script creates visually distinct thumbnails for RPG games.
"""

import pygame
import os
import math
import random
import sys

# Initialize pygame
pygame.init()

# Define constants
THUMBNAIL_WIDTH = 300
THUMBNAIL_HEIGHT = 200
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define colors for RPG games
COLORS = {
    'pixel_quest': {  # Retro RPG
        'bg': (20, 0, 40),  # Dark purple
        'primary': (100, 0, 150),  # Purple
        'secondary': (150, 100, 255),  # Light purple
        'accent': (255, 200, 0),  # Gold
    },
    'cyber_knights': {  # Cyberpunk RPG
        'bg': (0, 20, 30),  # Dark teal
        'primary': (0, 100, 150),  # Teal
        'secondary': (0, 200, 255),  # Cyan
        'accent': (255, 50, 100),  # Pink
    },
    'dragon_realm': {  # Fantasy RPG
        'bg': (30, 0, 0),  # Dark red
        'primary': (150, 0, 0),  # Red
        'secondary': (200, 100, 0),  # Orange
        'accent': (255, 255, 0),  # Yellow
    }
}

def generate_pixel_quest_thumbnail():
    """Generate a thumbnail for Pixel Quest (Retro RPG) game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['pixel_quest']
    
    # Fill background with gradient
    for y in range(THUMBNAIL_HEIGHT):
        # Calculate color for this line
        progress = y / THUMBNAIL_HEIGHT
        color_top = colors['bg']
        color_bottom = tuple(max(0, c - 10) for c in colors['bg'])
        
        color = tuple(
            int(color_top[i] * (1 - progress) + color_bottom[i] * progress)
            for i in range(3)
        )
        
        # Draw horizontal line with this color
        pygame.draw.line(
            surface,
            color,
            (0, y),
            (THUMBNAIL_WIDTH - 1, y)
        )
    
    # Draw pixel art landscape
    # Ground
    ground_height = 50
    pygame.draw.rect(
        surface,
        (0, 100, 0),  # Green
        pygame.Rect(0, THUMBNAIL_HEIGHT - ground_height, THUMBNAIL_WIDTH, ground_height)
    )
    
    # Pixel grid on ground
    for x in range(0, THUMBNAIL_WIDTH, 10):
        pygame.draw.line(
            surface,
            (0, 120, 0),
            (x, THUMBNAIL_HEIGHT - ground_height),
            (x, THUMBNAIL_HEIGHT),
            1
        )
    
    for y in range(THUMBNAIL_HEIGHT - ground_height, THUMBNAIL_HEIGHT, 10):
        pygame.draw.line(
            surface,
            (0, 120, 0),
            (0, y),
            (THUMBNAIL_WIDTH, y),
            1
        )
    
    # Draw mountains
    mountain_points = [
        (0, THUMBNAIL_HEIGHT - ground_height),
        (50, THUMBNAIL_HEIGHT - ground_height - 80),
        (100, THUMBNAIL_HEIGHT - ground_height - 40),
        (150, THUMBNAIL_HEIGHT - ground_height - 100),
        (200, THUMBNAIL_HEIGHT - ground_height - 60),
        (250, THUMBNAIL_HEIGHT - ground_height - 120),
        (300, THUMBNAIL_HEIGHT - ground_height - 50),
        (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT - ground_height)
    ]
    
    pygame.draw.polygon(
        surface,
        (100, 50, 150),  # Purple mountains
        mountain_points
    )
    
    # Draw pixel grid on mountains
    for x in range(0, THUMBNAIL_WIDTH, 10):
        for y in range(THUMBNAIL_HEIGHT - ground_height - 120, THUMBNAIL_HEIGHT - ground_height, 10):
            pygame.draw.rect(
                surface,
                (110, 60, 160),
                pygame.Rect(x, y, 10, 10),
                1
            )
    
    # Draw pixel art trees
    tree_positions = [50, 150, 250]
    for x in tree_positions:
        # Tree trunk
        pygame.draw.rect(
            surface,
            (100, 50, 0),  # Brown
            pygame.Rect(x - 5, THUMBNAIL_HEIGHT - ground_height - 30, 10, 30)
        )
        
        # Tree leaves (triangular)
        pygame.draw.polygon(
            surface,
            (0, 150, 0),  # Green
            [
                (x, THUMBNAIL_HEIGHT - ground_height - 60),
                (x - 20, THUMBNAIL_HEIGHT - ground_height - 30),
                (x + 20, THUMBNAIL_HEIGHT - ground_height - 30)
            ]
        )
        
        # Pixel grid on leaves
        for i in range(-2, 3):
            for j in range(-3, 0):
                pygame.draw.rect(
                    surface,
                    (0, 170, 0),
                    pygame.Rect(x + i * 10, THUMBNAIL_HEIGHT - ground_height - 30 + j * 10, 10, 10),
                    1
                )
    
    # Draw pixel art hero character
    hero_x = THUMBNAIL_WIDTH // 2 - 30
    hero_y = THUMBNAIL_HEIGHT - ground_height - 20
    
    # Hero body
    pygame.draw.rect(
        surface,
        (0, 0, 200),  # Blue
        pygame.Rect(hero_x - 5, hero_y - 10, 10, 20)
    )
    
    # Hero head
    pygame.draw.rect(
        surface,
        (255, 200, 150),  # Skin tone
        pygame.Rect(hero_x - 5, hero_y - 20, 10, 10)
    )
    
    # Hero sword
    pygame.draw.rect(
        surface,
        (200, 200, 200),  # Silver
        pygame.Rect(hero_x + 5, hero_y - 15, 15, 5)
    )
    
    # Draw pixel art enemy
    enemy_x = THUMBNAIL_WIDTH // 2 + 30
    enemy_y = THUMBNAIL_HEIGHT - ground_height - 15
    
    # Enemy body
    pygame.draw.rect(
        surface,
        (200, 0, 0),  # Red
        pygame.Rect(enemy_x - 7, enemy_y - 15, 14, 15)
    )
    
    # Enemy head
    pygame.draw.rect(
        surface,
        (0, 200, 0),  # Green
        pygame.Rect(enemy_x - 5, enemy_y - 25, 10, 10)
    )
    
    # Enemy eyes
    pygame.draw.rect(
        surface,
        (255, 255, 0),  # Yellow
        pygame.Rect(enemy_x - 3, enemy_y - 23, 2, 2)
    )
    pygame.draw.rect(
        surface,
        (255, 255, 0),  # Yellow
        pygame.Rect(enemy_x + 1, enemy_y - 23, 2, 2)
    )
    
    # Draw battle menu
    menu_rect = pygame.Rect(20, 20, THUMBNAIL_WIDTH - 40, 40)
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        menu_rect,
        0,
        border_radius=5
    )
    pygame.draw.rect(
        surface,
        colors['accent'],
        menu_rect,
        2,
        border_radius=5
    )
    
    # Menu options
    options = ["ATTACK", "MAGIC", "ITEM", "RUN"]
    option_width = (menu_rect.width - 20) // len(options)
    
    for i, option in enumerate(options):
        font = pygame.font.SysFont("Arial", 12, bold=True)
        option_text = font.render(option, True, colors['accent'])
        option_rect = option_text.get_rect(center=(menu_rect.left + 10 + i * option_width + option_width // 2, menu_rect.centery))
        surface.blit(option_text, option_rect)
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("PIXEL QUEST", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT - 15))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_cyber_knights_thumbnail():
    """Generate a thumbnail for Cyber Knights (Cyberpunk RPG) game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['cyber_knights']
    
    # Fill background with gradient
    for y in range(THUMBNAIL_HEIGHT):
        # Calculate color for this line
        progress = y / THUMBNAIL_HEIGHT
        color_top = colors['bg']
        color_bottom = tuple(max(0, c - 10) for c in colors['bg'])
        
        color = tuple(
            int(color_top[i] * (1 - progress) + color_bottom[i] * progress)
            for i in range(3)
        )
        
        # Draw horizontal line with this color
        pygame.draw.line(
            surface,
            color,
            (0, y),
            (THUMBNAIL_WIDTH - 1, y)
        )
    
    # Draw cyberpunk city skyline
    building_colors = [
        (0, 50, 80),
        (0, 60, 90),
        (0, 40, 70),
        (0, 70, 100)
    ]
    
    # Draw buildings
    for x in range(0, THUMBNAIL_WIDTH, 30):
        height = random.randint(80, 150)
        width = random.randint(20, 30)
        
        pygame.draw.rect(
            surface,
            random.choice(building_colors),
            pygame.Rect(x, THUMBNAIL_HEIGHT - height, width, height)
        )
        
        # Draw windows
        for i in range(3, height - 10, 10):
            for j in range(3, width - 5, 10):
                if random.random() < 0.7:  # 70% chance to draw a window
                    window_color = (0, 200, 255) if random.random() < 0.5 else (255, 50, 100)
                    pygame.draw.rect(
                        surface,
                        window_color,
                        pygame.Rect(x + j, THUMBNAIL_HEIGHT - height + i, 4, 4)
                    )
    
    # Draw neon signs
    neon_positions = [
        (50, 70),
        (150, 50),
        (250, 60)
    ]
    
    neon_colors = [
        (255, 0, 100),  # Pink
        (0, 255, 255),  # Cyan
        (255, 255, 0)   # Yellow
    ]
    
    for (x, y), color in zip(neon_positions, neon_colors):
        # Draw neon sign background
        pygame.draw.rect(
            surface,
            (30, 30, 30),
            pygame.Rect(x - 20, y - 10, 40, 20),
            0,
            border_radius=3
        )
        
        # Draw neon text
        font = pygame.font.SysFont("Arial", 12, bold=True)
        texts = ["BAR", "TECH", "GUNS"]
        text = random.choice(texts)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, text_rect)
        
        # Draw neon glow
        for i in range(3):
            pygame.draw.rect(
                surface,
                (*color, 100 - i * 30),
                pygame.Rect(x - 20 - i, y - 10 - i, 40 + i * 2, 20 + i * 2),
                1,
                border_radius=3 + i
            )
    
    # Draw cyber knight character
    knight_x = THUMBNAIL_WIDTH // 2 - 40
    knight_y = THUMBNAIL_HEIGHT - 60
    
    # Knight body
    pygame.draw.rect(
        surface,
        (50, 50, 50),  # Dark gray
        pygame.Rect(knight_x - 10, knight_y - 20, 20, 40),
        0,
        border_radius=5
    )
    
    # Knight head
    pygame.draw.rect(
        surface,
        (70, 70, 70),  # Gray
        pygame.Rect(knight_x - 7, knight_y - 35, 14, 15),
        0,
        border_radius=3
    )
    
    # Knight visor
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(knight_x - 5, knight_y - 30, 10, 3)
    )
    
    # Knight sword
    pygame.draw.rect(
        surface,
        (200, 200, 200),  # Silver
        pygame.Rect(knight_x + 10, knight_y - 30, 5, 40)
    )
    pygame.draw.rect(
        surface,
        colors['accent'],
        pygame.Rect(knight_x + 10, knight_y - 30, 5, 40),
        1
    )
    
    # Draw cyber enemy
    enemy_x = THUMBNAIL_WIDTH // 2 + 40
    enemy_y = THUMBNAIL_HEIGHT - 60
    
    # Enemy body
    pygame.draw.rect(
        surface,
        (100, 0, 0),  # Dark red
        pygame.Rect(enemy_x - 15, enemy_y - 25, 30, 45),
        0,
        border_radius=5
    )
    
    # Enemy head
    pygame.draw.circle(
        surface,
        (150, 0, 0),  # Red
        (enemy_x, enemy_y - 35),
        10
    )
    
    # Enemy eyes
    pygame.draw.circle(
        surface,
        colors['secondary'],
        (enemy_x - 4, enemy_y - 37),
        3
    )
    pygame.draw.circle(
        surface,
        colors['secondary'],
        (enemy_x + 4, enemy_y - 37),
        3
    )
    
    # Draw battle effects
    for _ in range(5):
        effect_x = random.randint(knight_x + 10, enemy_x - 10)
        effect_y = random.randint(knight_y - 30, knight_y)
        effect_size = random.randint(3, 8)
        
        pygame.draw.circle(
            surface,
            colors['accent'],
            (effect_x, effect_y),
            effect_size
        )
        
        # Draw effect rays
        for i in range(4):
            angle = i * math.pi / 2
            end_x = effect_x + int(math.cos(angle) * effect_size * 2)
            end_y = effect_y + int(math.sin(angle) * effect_size * 2)
            
            pygame.draw.line(
                surface,
                colors['accent'],
                (effect_x, effect_y),
                (end_x, end_y),
                1
            )
    
    # Draw HUD
    hud_rect = pygame.Rect(20, 20, THUMBNAIL_WIDTH - 40, 30)
    pygame.draw.rect(
        surface,
        (0, 0, 0, 150),
        hud_rect,
        0,
        border_radius=5
    )
    pygame.draw.rect(
        surface,
        colors['secondary'],
        hud_rect,
        1,
        border_radius=5
    )
    
    # Health bar
    health_rect = pygame.Rect(30, 30, 100, 10)
    pygame.draw.rect(
        surface,
        (50, 50, 50),
        health_rect
    )
    pygame.draw.rect(
        surface,
        (0, 255, 0),  # Green
        pygame.Rect(health_rect.left, health_rect.top, health_rect.width * 0.7, health_rect.height)
    )
    
    # Energy bar
    energy_rect = pygame.Rect(THUMBNAIL_WIDTH - 130, 30, 100, 10)
    pygame.draw.rect(
        surface,
        (50, 50, 50),
        energy_rect
    )
    pygame.draw.rect(
        surface,
        (0, 100, 255),  # Blue
        pygame.Rect(energy_rect.left, energy_rect.top, energy_rect.width * 0.5, energy_rect.height)
    )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("CYBER KNIGHTS", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT - 15))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_dragon_realm_thumbnail():
    """Generate a thumbnail for Dragon Realm (Fantasy RPG) game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['dragon_realm']
    
    # Fill background with gradient
    for y in range(THUMBNAIL_HEIGHT):
        # Calculate color for this line
        progress = y / THUMBNAIL_HEIGHT
        color_top = colors['bg']
        color_bottom = tuple(max(0, c - 10) for c in colors['bg'])
        
        color = tuple(
            int(color_top[i] * (1 - progress) + color_bottom[i] * progress)
            for i in range(3)
        )
        
        # Draw horizontal line with this color
        pygame.draw.line(
            surface,
            color,
            (0, y),
            (THUMBNAIL_WIDTH - 1, y)
        )
    
    # Draw fantasy landscape
    # Mountains
    mountain_points = [
        (0, THUMBNAIL_HEIGHT - 80),
        (50, THUMBNAIL_HEIGHT - 120),
        (100, THUMBNAIL_HEIGHT - 90),
        (150, THUMBNAIL_HEIGHT - 150),
        (200, THUMBNAIL_HEIGHT - 100),
        (250, THUMBNAIL_HEIGHT - 130),
        (300, THUMBNAIL_HEIGHT - 110),
        (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT - 80)
    ]
    
    pygame.draw.polygon(
        surface,
        (80, 40, 0),  # Brown
        mountain_points + [(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), (0, THUMBNAIL_HEIGHT)]
    )
    
    # Draw castle
    castle_x = THUMBNAIL_WIDTH // 2
    castle_y = THUMBNAIL_HEIGHT - 120
    castle_width = 100
    castle_height = 70
    
    # Main castle body
    pygame.draw.rect(
        surface,
        (100, 100, 100),  # Gray
        pygame.Rect(castle_x - castle_width // 2, castle_y - castle_height, castle_width, castle_height)
    )
    
    # Castle towers
    tower_width = 20
    tower_height = 30
    
    # Left tower
    pygame.draw.rect(
        surface,
        (80, 80, 80),  # Darker gray
        pygame.Rect(castle_x - castle_width // 2 - tower_width // 2, castle_y - castle_height - tower_height, tower_width, tower_height)
    )
    
    # Right tower
    pygame.draw.rect(
        surface,
        (80, 80, 80),  # Darker gray
        pygame.Rect(castle_x + castle_width // 2 - tower_width // 2, castle_y - castle_height - tower_height, tower_width, tower_height)
    )
    
    # Tower tops
    pygame.draw.polygon(
        surface,
        (120, 0, 0),  # Red
        [
            (castle_x - castle_width // 2 - tower_width // 2, castle_y - castle_height - tower_height),
            (castle_x - castle_width // 2 + tower_width // 2, castle_y - castle_height - tower_height),
            (castle_x - castle_width // 2, castle_y - castle_height - tower_height - 10)
        ]
    )
    
    pygame.draw.polygon(
        surface,
        (120, 0, 0),  # Red
        [
            (castle_x + castle_width // 2 - tower_width // 2, castle_y - castle_height - tower_height),
            (castle_x + castle_width // 2 + tower_width // 2, castle_y - castle_height - tower_height),
            (castle_x + castle_width // 2, castle_y - castle_height - tower_height - 10)
        ]
    )
    
    # Castle door
    pygame.draw.rect(
        surface,
        (80, 40, 0),  # Brown
        pygame.Rect(castle_x - 10, castle_y - 30, 20, 30),
        0,
        border_radius=10
    )
    
    # Castle windows
    for i in range(3):
        for j in range(2):
            window_x = castle_x - castle_width // 2 + 20 + i * 30
            window_y = castle_y - castle_height + 15 + j * 25
            
            pygame.draw.rect(
                surface,
                (200, 200, 100),  # Light yellow
                pygame.Rect(window_x, window_y, 10, 15),
                0,
                border_radius=5
            )
    
    # Draw dragon
    dragon_x = THUMBNAIL_WIDTH // 4
    dragon_y = THUMBNAIL_HEIGHT // 3
    
    # Dragon body
    pygame.draw.ellipse(
        surface,
        (150, 0, 0),  # Red
        pygame.Rect(dragon_x - 40, dragon_y - 20, 80, 40)
    )
    
    # Dragon neck and head
    pygame.draw.ellipse(
        surface,
        (150, 0, 0),  # Red
        pygame.Rect(dragon_x - 50, dragon_y - 40, 30, 30)
    )
    
    # Dragon wings
    pygame.draw.polygon(
        surface,
        (150, 0, 0),  # Red
        [
            (dragon_x, dragon_y),
            (dragon_x - 30, dragon_y - 40),
            (dragon_x - 40, dragon_y - 20)
        ]
    )
    
    pygame.draw.polygon(
        surface,
        (150, 0, 0),  # Red
        [
            (dragon_x, dragon_y),
            (dragon_x + 30, dragon_y - 40),
            (dragon_x + 40, dragon_y - 20)
        ]
    )
    
    # Dragon eyes
    pygame.draw.circle(
        surface,
        (255, 255, 0),  # Yellow
        (dragon_x - 45, dragon_y - 30),
        3
    )
    
    # Dragon fire breath
    fire_points = []
    for i in range(10):
        angle = random.uniform(-0.3, 0.3)
        length = random.randint(20, 50)
        x = dragon_x - 50 - length * math.cos(angle)
        y = dragon_y - 30 - length * math.sin(angle)
        fire_points.append((x, y))
    
    for point in fire_points:
        pygame.draw.line(
            surface,
            (255, 100, 0),  # Orange
            (dragon_x - 50, dragon_y - 30),
            point,
            random.randint(1, 3)
        )
    
    # Draw hero character
    hero_x = THUMBNAIL_WIDTH * 3 // 4
    hero_y = THUMBNAIL_HEIGHT - 50
    
    # Hero body
    pygame.draw.rect(
        surface,
        (0, 0, 150),  # Blue
        pygame.Rect(hero_x - 10, hero_y - 30, 20, 30)
    )
    
    # Hero head
    pygame.draw.circle(
        surface,
        (255, 200, 150),  # Skin tone
        (hero_x, hero_y - 40),
        10
    )
    
    # Hero sword
    pygame.draw.rect(
        surface,
        (200, 200, 200),  # Silver
        pygame.Rect(hero_x + 10, hero_y - 50, 5, 40)
    )
    
    # Hero shield
    pygame.draw.rect(
        surface,
        (150, 0, 0),  # Red
        pygame.Rect(hero_x - 20, hero_y - 30, 10, 20),
        0,
        border_radius=5
    )
    
    # Draw battle HUD
    hud_rect = pygame.Rect(20, THUMBNAIL_HEIGHT - 30, THUMBNAIL_WIDTH - 40, 20)
    pygame.draw.rect(
        surface,
        (0, 0, 0, 150),
        hud_rect,
        0,
        border_radius=5
    )
    pygame.draw.rect(
        surface,
        colors['accent'],
        hud_rect,
        1,
        border_radius=5
    )
    
    # Health and mana bars
    health_rect = pygame.Rect(30, THUMBNAIL_HEIGHT - 25, 100, 10)
    pygame.draw.rect(
        surface,
        (50, 50, 50),
        health_rect
    )
    pygame.draw.rect(
        surface,
        (255, 0, 0),  # Red
        pygame.Rect(health_rect.left, health_rect.top, health_rect.width * 0.6, health_rect.height)
    )
    
    mana_rect = pygame.Rect(THUMBNAIL_WIDTH - 130, THUMBNAIL_HEIGHT - 25, 100, 10)
    pygame.draw.rect(
        surface,
        (50, 50, 50),
        mana_rect
    )
    pygame.draw.rect(
        surface,
        (0, 0, 255),  # Blue
        pygame.Rect(mana_rect.left, mana_rect.top, mana_rect.width * 0.8, mana_rect.height)
    )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("DRAGON REALM", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface

def main():
    """Generate all thumbnails."""
    # Create thumbnails
    thumbnails = {
        'pixel_quest': generate_pixel_quest_thumbnail(),
        'cyber_knights': generate_cyber_knights_thumbnail(),
        'dragon_realm': generate_dragon_realm_thumbnail()
    }
    
    # Save thumbnails
    for game_id, surface in thumbnails.items():
        output_path = os.path.join(OUTPUT_DIR, f"{game_id}.png")
        pygame.image.save(surface, output_path)
        print(f"Generated thumbnail for {game_id}: {output_path}")

if __name__ == "__main__":
    main()
    pygame.quit()
