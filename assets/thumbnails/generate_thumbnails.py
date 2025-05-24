"""
Generate thumbnail images for SoulCoreLegacy Arcade games.
This script creates visually distinct thumbnails for each game.
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

# Define colors
COLORS = {
    'cosmic_racer': {
        'bg': (5, 0, 20),  # Deep space black
        'primary': (100, 0, 255),  # Deep purple
        'secondary': (0, 200, 255),  # Bright blue
        'accent': (255, 215, 0),  # Gold
    },
    'dungeon_delver': {
        'bg': (20, 10, 5),  # Dark brown
        'primary': (150, 75, 0),  # Brown
        'secondary': (255, 100, 0),  # Orange
        'accent': (255, 215, 0),  # Gold
    },
    'nft_artisan': {
        'bg': (5, 15, 20),  # Dark teal
        'primary': (0, 150, 150),  # Teal
        'secondary': (0, 255, 200),  # Bright teal
        'accent': (255, 50, 150),  # Pink
    },
    'snake': {
        'bg': (0, 15, 0),  # Dark green
        'primary': (0, 150, 0),  # Green
        'secondary': (0, 255, 0),  # Bright green
        'accent': (200, 255, 0),  # Yellow-green
    },
    'pong': {
        'bg': (0, 0, 15),  # Dark blue
        'primary': (0, 0, 150),  # Blue
        'secondary': (0, 100, 255),  # Bright blue
        'accent': (0, 255, 255),  # Cyan
    },
    'asteroids': {
        'bg': (15, 15, 15),  # Dark gray
        'primary': (100, 100, 100),  # Gray
        'secondary': (150, 150, 150),  # Light gray
        'accent': (255, 255, 255),  # White
    }
}

def generate_cosmic_racer_thumbnail():
    """Generate a thumbnail for Cosmic Racer game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['cosmic_racer']
    
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
    
    # Draw stars
    for _ in range(100):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(0, THUMBNAIL_HEIGHT)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        pygame.draw.circle(
            surface,
            (brightness, brightness, brightness),
            (x, y),
            size
        )
    
    # Draw a race track
    track_width = 80
    track_points = []
    for i in range(0, 360, 5):
        angle = math.radians(i)
        radius = 60 + math.sin(angle * 3) * 20
        x = THUMBNAIL_WIDTH // 2 + int(math.cos(angle) * radius)
        y = THUMBNAIL_HEIGHT // 2 + int(math.sin(angle) * radius)
        track_points.append((x, y))
    
    # Draw outer track
    pygame.draw.lines(surface, colors['secondary'], True, track_points, 5)
    
    # Draw inner track
    inner_track_points = []
    for i in range(0, 360, 5):
        angle = math.radians(i)
        radius = 30 + math.sin(angle * 3) * 10
        x = THUMBNAIL_WIDTH // 2 + int(math.cos(angle) * radius)
        y = THUMBNAIL_HEIGHT // 2 + int(math.sin(angle) * radius)
        inner_track_points.append((x, y))
    
    pygame.draw.lines(surface, colors['secondary'], True, inner_track_points, 3)
    
    # Draw a spaceship
    ship_x = THUMBNAIL_WIDTH // 2 + 40
    ship_y = THUMBNAIL_HEIGHT // 2 - 10
    ship_points = [
        (ship_x, ship_y),
        (ship_x - 15, ship_y + 10),
        (ship_x - 10, ship_y),
        (ship_x - 15, ship_y - 10)
    ]
    pygame.draw.polygon(surface, colors['accent'], ship_points)
    
    # Draw engine flame
    flame_points = [
        (ship_x - 15, ship_y),
        (ship_x - 25, ship_y + 5),
        (ship_x - 25, ship_y - 5)
    ]
    pygame.draw.polygon(surface, (255, 100, 0), flame_points)
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("COSMIC RACER", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 30))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_dungeon_delver_thumbnail():
    """Generate a thumbnail for Dungeon Delver game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['dungeon_delver']
    
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
    
    # Draw dungeon walls
    cell_size = 30
    for y in range(0, THUMBNAIL_HEIGHT, cell_size):
        for x in range(0, THUMBNAIL_WIDTH, cell_size):
            # Skip some cells to create a dungeon layout
            if random.random() < 0.7:
                continue
            
            # Draw a stone block
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(surface, colors['primary'], rect)
            pygame.draw.rect(surface, colors['secondary'], rect, 1)
            
            # Add some texture
            for _ in range(3):
                tx = x + random.randint(5, cell_size - 5)
                ty = y + random.randint(5, cell_size - 5)
                tsize = random.randint(1, 3)
                pygame.draw.circle(surface, (50, 25, 0), (tx, ty), tsize)
    
    # Draw a hero character
    hero_x = THUMBNAIL_WIDTH // 2
    hero_y = THUMBNAIL_HEIGHT // 2
    
    # Draw body
    pygame.draw.circle(surface, (200, 150, 100), (hero_x, hero_y - 10), 8)
    pygame.draw.rect(surface, (0, 0, 150), pygame.Rect(hero_x - 6, hero_y, 12, 15))
    
    # Draw sword
    pygame.draw.line(surface, (200, 200, 200), (hero_x + 6, hero_y), (hero_x + 20, hero_y - 10), 3)
    
    # Draw a treasure chest
    chest_x = THUMBNAIL_WIDTH // 4 * 3
    chest_y = THUMBNAIL_HEIGHT // 4 * 3
    pygame.draw.rect(surface, (150, 75, 0), pygame.Rect(chest_x - 15, chest_y - 10, 30, 20))
    pygame.draw.rect(surface, colors['accent'], pygame.Rect(chest_x - 15, chest_y - 10, 30, 20), 2)
    pygame.draw.rect(surface, colors['accent'], pygame.Rect(chest_x - 2, chest_y - 5, 4, 10))
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("DUNGEON DELVER", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 30))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_nft_artisan_thumbnail():
    """Generate a thumbnail for NFT Artisan game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['nft_artisan']
    
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
    
    # Draw a digital canvas
    canvas_rect = pygame.Rect(50, 50, THUMBNAIL_WIDTH - 100, THUMBNAIL_HEIGHT - 100)
    pygame.draw.rect(surface, (240, 240, 240), canvas_rect)
    pygame.draw.rect(surface, colors['primary'], canvas_rect, 3)
    
    # Draw some digital art on the canvas
    # Abstract shapes
    for _ in range(5):
        shape_type = random.choice(['circle', 'rect', 'polygon'])
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        
        x = random.randint(canvas_rect.left + 20, canvas_rect.right - 20)
        y = random.randint(canvas_rect.top + 20, canvas_rect.bottom - 20)
        
        if shape_type == 'circle':
            radius = random.randint(10, 30)
            pygame.draw.circle(surface, color, (x, y), radius)
        elif shape_type == 'rect':
            width = random.randint(20, 50)
            height = random.randint(20, 50)
            pygame.draw.rect(surface, color, pygame.Rect(x - width // 2, y - height // 2, width, height))
        else:  # polygon
            points = []
            for i in range(random.randint(3, 6)):
                angle = math.radians(i * (360 / random.randint(3, 6)))
                radius = random.randint(15, 30)
                px = x + int(math.cos(angle) * radius)
                py = y + int(math.sin(angle) * radius)
                points.append((px, py))
            pygame.draw.polygon(surface, color, points)
    
    # Draw NFT token symbol
    token_x = THUMBNAIL_WIDTH - 40
    token_y = 40
    pygame.draw.circle(surface, colors['accent'], (token_x, token_y), 20)
    font = pygame.font.SysFont("Arial", 18, bold=True)
    token_text = font.render("NFT", True, (0, 0, 0))
    token_rect = token_text.get_rect(center=(token_x, token_y))
    surface.blit(token_text, token_rect)
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("NFT ARTISAN", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 30))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_snake_thumbnail():
    """Generate a thumbnail for Quantum Snake game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['snake']
    
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
    
    # Draw grid
    cell_size = 20
    for x in range(0, THUMBNAIL_WIDTH, cell_size):
        pygame.draw.line(surface, (0, 50, 0), (x, 0), (x, THUMBNAIL_HEIGHT), 1)
    for y in range(0, THUMBNAIL_HEIGHT, cell_size):
        pygame.draw.line(surface, (0, 50, 0), (0, y), (THUMBNAIL_WIDTH, y), 1)
    
    # Draw quantum effects (wavy lines)
    for y in range(0, THUMBNAIL_HEIGHT, 40):
        points = []
        for x in range(0, THUMBNAIL_WIDTH, 5):
            points.append((x, y + math.sin(x * 0.05) * 10))
        pygame.draw.lines(surface, (0, 100, 0, 100), False, points, 2)
    
    # Draw snake
    snake_segments = [
        (THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT // 2),
        (THUMBNAIL_WIDTH // 2 - cell_size, THUMBNAIL_HEIGHT // 2),
        (THUMBNAIL_WIDTH // 2 - cell_size * 2, THUMBNAIL_HEIGHT // 2),
        (THUMBNAIL_WIDTH // 2 - cell_size * 3, THUMBNAIL_HEIGHT // 2),
        (THUMBNAIL_WIDTH // 2 - cell_size * 4, THUMBNAIL_HEIGHT // 2),
        (THUMBNAIL_WIDTH // 2 - cell_size * 4, THUMBNAIL_HEIGHT // 2 - cell_size),
        (THUMBNAIL_WIDTH // 2 - cell_size * 4, THUMBNAIL_HEIGHT // 2 - cell_size * 2)
    ]
    
    # Draw snake body
    for segment in snake_segments:
        pygame.draw.rect(
            surface,
            colors['secondary'],
            pygame.Rect(segment[0] - cell_size // 2, segment[1] - cell_size // 2, cell_size, cell_size)
        )
    
    # Draw snake head
    head = snake_segments[0]
    pygame.draw.rect(
        surface,
        colors['accent'],
        pygame.Rect(head[0] - cell_size // 2, head[1] - cell_size // 2, cell_size, cell_size)
    )
    
    # Draw food
    food_x = THUMBNAIL_WIDTH // 2 + cell_size * 3
    food_y = THUMBNAIL_HEIGHT // 2 - cell_size * 2
    pygame.draw.rect(
        surface,
        (255, 0, 0),
        pygame.Rect(food_x - cell_size // 2, food_y - cell_size // 2, cell_size, cell_size)
    )
    
    # Draw quantum portal
    portal1_x = THUMBNAIL_WIDTH // 4
    portal1_y = THUMBNAIL_HEIGHT // 4
    portal2_x = THUMBNAIL_WIDTH // 4 * 3
    portal2_y = THUMBNAIL_HEIGHT // 4 * 3
    
    for i in range(5):
        pygame.draw.circle(
            surface,
            (0, 150 + i * 20, 150 + i * 20),
            (portal1_x, portal1_y),
            15 - i * 2,
            2
        )
        pygame.draw.circle(
            surface,
            (0, 150 + i * 20, 150 + i * 20),
            (portal2_x, portal2_y),
            15 - i * 2,
            2
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("QUANTUM SNAKE", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 30))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_pong_thumbnail():
    """Generate a thumbnail for Neon Pong game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['pong']
    
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
    
    # Draw center line
    for y in range(0, THUMBNAIL_HEIGHT, 20):
        pygame.draw.rect(
            surface,
            colors['secondary'],
            pygame.Rect(THUMBNAIL_WIDTH // 2 - 2, y, 4, 10)
        )
    
    # Draw paddles
    paddle_width = 10
    paddle_height = 60
    
    # Left paddle
    pygame.draw.rect(
        surface,
        colors['accent'],
        pygame.Rect(30, THUMBNAIL_HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
    )
    
    # Right paddle
    pygame.draw.rect(
        surface,
        colors['accent'],
        pygame.Rect(THUMBNAIL_WIDTH - 30 - paddle_width, THUMBNAIL_HEIGHT // 2 - paddle_height // 2 + 20, paddle_width, paddle_height)
    )
    
    # Draw ball with glow effect
    ball_x = THUMBNAIL_WIDTH // 2 + 40
    ball_y = THUMBNAIL_HEIGHT // 2 - 20
    ball_radius = 8
    
    # Draw glow
    for i in range(5):
        pygame.draw.circle(
            surface,
            (*colors['accent'], 150 - i * 30),
            (ball_x, ball_y),
            ball_radius + i * 3
        )
    
    # Draw ball
    pygame.draw.circle(
        surface,
        colors['accent'],
        (ball_x, ball_y),
        ball_radius
    )
    
    # Draw neon effects
    for i in range(5):
        angle = math.radians(i * 72)
        length = 100
        end_x = ball_x + math.cos(angle) * length
        end_y = ball_y + math.sin(angle) * length
        
        # Draw line with glow effect
        for j in range(3):
            pygame.draw.line(
                surface,
                (*colors['accent'], 100 - j * 30),
                (ball_x, ball_y),
                (end_x, end_y),
                3 - j
            )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("NEON PONG", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 30))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_asteroids_thumbnail():
    """Generate a thumbnail for Asteroids Annihilation game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['asteroids']
    
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
    
    # Draw stars
    for _ in range(100):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(0, THUMBNAIL_HEIGHT)
        size = random.randint(1, 3)
        brightness = random.randint(100, 200)
        pygame.draw.circle(
            surface,
            (brightness, brightness, brightness),
            (x, y),
            size
        )
    
    # Draw asteroids
    for _ in range(8):
        x = random.randint(50, THUMBNAIL_WIDTH - 50)
        y = random.randint(50, THUMBNAIL_HEIGHT - 50)
        size = random.randint(15, 40)
        
        # Create irregular polygon for asteroid
        points = []
        for i in range(8):
            angle = math.radians(i * 45 + random.randint(-10, 10))
            radius = size + random.randint(-size // 3, size // 3)
            px = x + int(math.cos(angle) * radius)
            py = y + int(math.sin(angle) * radius)
            points.append((px, py))
        
        pygame.draw.polygon(surface, colors['primary'], points)
        pygame.draw.polygon(surface, colors['secondary'], points, 2)
        
        # Add some texture
        for _ in range(3):
            tx = x + random.randint(-size // 2, size // 2)
            ty = y + random.randint(-size // 2, size // 2)
            tsize = random.randint(2, 5)
            pygame.draw.circle(surface, colors['secondary'], (tx, ty), tsize, 1)
    
    # Draw player ship
    ship_x = THUMBNAIL_WIDTH // 2
    ship_y = THUMBNAIL_HEIGHT // 2
    ship_points = [
        (ship_x, ship_y - 15),
        (ship_x - 10, ship_y + 10),
        (ship_x, ship_y + 5),
        (ship_x + 10, ship_y + 10)
    ]
    pygame.draw.polygon(surface, colors['accent'], ship_points)
    
    # Draw laser shots
    laser_start = (ship_x, ship_y - 15)
    laser_end = (ship_x, ship_y - 100)
    
    # Draw laser with glow effect
    for i in range(3):
        pygame.draw.line(
            surface,
            (255, 0, 0, 200 - i * 50),
            laser_start,
            laser_end,
            3 - i
        )
    
    # Draw explosion
    explosion_x = THUMBNAIL_WIDTH // 4 * 3
    explosion_y = THUMBNAIL_HEIGHT // 4
    
    for i in range(8):
        angle = math.radians(i * 45)
        length = random.randint(10, 30)
        end_x = explosion_x + math.cos(angle) * length
        end_y = explosion_y + math.sin(angle) * length
        
        # Draw explosion ray
        pygame.draw.line(
            surface,
            (255, 200, 0),
            (explosion_x, explosion_y),
            (end_x, end_y),
            3
        )
    
    # Draw explosion center
    pygame.draw.circle(surface, (255, 255, 0), (explosion_x, explosion_y), 10)
    pygame.draw.circle(surface, (255, 100, 0), (explosion_x, explosion_y), 6)
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("ASTEROIDS", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 30))
    surface.blit(title_text, title_rect)
    
    return surface

def main():
    """Generate all thumbnails."""
    # Create thumbnails
    thumbnails = {
        'cosmic_racer': generate_cosmic_racer_thumbnail(),
        'dungeon_delver': generate_dungeon_delver_thumbnail(),
        'nft_artisan': generate_nft_artisan_thumbnail(),
        'snake': generate_snake_thumbnail(),
        'pong': generate_pong_thumbnail(),
        'asteroids': generate_asteroids_thumbnail()
    }
    
    # Save thumbnails
    for game_id, surface in thumbnails.items():
        output_path = os.path.join(OUTPUT_DIR, f"{game_id}.png")
        pygame.image.save(surface, output_path)
        print(f"Generated thumbnail for {game_id}: {output_path}")

if __name__ == "__main__":
    main()
    pygame.quit()
