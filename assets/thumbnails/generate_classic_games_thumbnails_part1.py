"""
Generate classic games thumbnail images for SoulCoreLegacy Arcade (Part 1).
This script creates visually distinct thumbnails for Quantum Leap, Neon Blocks, and Cyber Spades.
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

# Define colors for classic games
COLORS = {
    'quantum_leap': {  # Frogger-type game
        'bg': (0, 30, 0),  # Dark green
        'primary': (0, 100, 0),  # Green
        'secondary': (0, 200, 0),  # Bright green
        'accent': (255, 255, 0),  # Yellow
    },
    'neon_blocks': {  # Tetris-type game
        'bg': (0, 0, 30),  # Dark blue
        'primary': (0, 0, 150),  # Blue
        'secondary': (0, 150, 255),  # Light blue
        'accent': (255, 0, 255),  # Magenta
    },
    'cyber_spades': {  # Spades card game
        'bg': (20, 20, 30),  # Dark slate
        'primary': (50, 50, 80),  # Slate
        'secondary': (100, 100, 150),  # Light slate
        'accent': (200, 200, 255),  # Light blue
    }
}

def generate_quantum_leap_thumbnail():
    """Generate a thumbnail for Quantum Leap (Frogger-type) game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['quantum_leap']
    
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
    
    # Draw lanes
    lane_height = 30
    num_lanes = THUMBNAIL_HEIGHT // lane_height
    
    for i in range(num_lanes):
        lane_y = i * lane_height
        
        # Alternate between road and water
        if i % 2 == 0:
            # Road
            pygame.draw.rect(
                surface,
                (50, 50, 50),  # Dark gray
                pygame.Rect(0, lane_y, THUMBNAIL_WIDTH, lane_height)
            )
            
            # Road markings
            for x in range(0, THUMBNAIL_WIDTH, 40):
                pygame.draw.rect(
                    surface,
                    (255, 255, 255),  # White
                    pygame.Rect(x, lane_y + lane_height // 2 - 2, 20, 4)
                )
        else:
            # Water
            pygame.draw.rect(
                surface,
                (0, 100, 200),  # Blue
                pygame.Rect(0, lane_y, THUMBNAIL_WIDTH, lane_height)
            )
            
            # Water ripples
            for x in range(0, THUMBNAIL_WIDTH, 20):
                pygame.draw.arc(
                    surface,
                    (0, 150, 255),
                    pygame.Rect(x, lane_y + 5, 20, 10),
                    0, math.pi,
                    1
                )
                pygame.draw.arc(
                    surface,
                    (0, 150, 255),
                    pygame.Rect(x + 10, lane_y + 15, 20, 10),
                    0, math.pi,
                    1
                )
    
    # Draw obstacles (cars on roads, logs on water)
    for i in range(num_lanes):
        lane_y = i * lane_height + lane_height // 2
        
        if i % 2 == 0:  # Road
            # Draw cars
            for _ in range(2):
                car_x = random.randint(0, THUMBNAIL_WIDTH - 40)
                car_color = random.choice([(255, 0, 0), (0, 0, 255), (255, 255, 0)])
                
                pygame.draw.rect(
                    surface,
                    car_color,
                    pygame.Rect(car_x, lane_y - 10, 40, 20),
                    0,
                    border_radius=5
                )
                
                # Car windows
                pygame.draw.rect(
                    surface,
                    (200, 200, 255),
                    pygame.Rect(car_x + 5, lane_y - 8, 10, 16),
                    0,
                    border_radius=2
                )
                pygame.draw.rect(
                    surface,
                    (200, 200, 255),
                    pygame.Rect(car_x + 25, lane_y - 8, 10, 16),
                    0,
                    border_radius=2
                )
        else:  # Water
            # Draw logs
            for _ in range(2):
                log_x = random.randint(0, THUMBNAIL_WIDTH - 60)
                
                pygame.draw.rect(
                    surface,
                    (100, 50, 0),  # Brown
                    pygame.Rect(log_x, lane_y - 8, 60, 16),
                    0,
                    border_radius=8
                )
                
                # Log details
                for j in range(3):
                    pygame.draw.line(
                        surface,
                        (80, 40, 0),  # Darker brown
                        (log_x + 10 + j * 15, lane_y - 8),
                        (log_x + 10 + j * 15, lane_y + 8),
                        1
                    )
    
    # Draw frog character
    frog_x = THUMBNAIL_WIDTH // 2
    frog_y = THUMBNAIL_HEIGHT - 20
    frog_size = 20
    
    # Frog body
    pygame.draw.circle(
        surface,
        colors['accent'],
        (frog_x, frog_y),
        frog_size // 2
    )
    
    # Frog eyes
    eye_offset = 4
    pygame.draw.circle(
        surface,
        (0, 0, 0),
        (frog_x - eye_offset, frog_y - eye_offset),
        3
    )
    pygame.draw.circle(
        surface,
        (0, 0, 0),
        (frog_x + eye_offset, frog_y - eye_offset),
        3
    )
    
    # Frog legs
    leg_length = 8
    pygame.draw.line(
        surface,
        colors['accent'],
        (frog_x - frog_size // 2, frog_y),
        (frog_x - frog_size // 2 - leg_length, frog_y + leg_length),
        3
    )
    pygame.draw.line(
        surface,
        colors['accent'],
        (frog_x + frog_size // 2, frog_y),
        (frog_x + frog_size // 2 + leg_length, frog_y + leg_length),
        3
    )
    
    # Draw quantum effects
    for _ in range(10):
        effect_x = random.randint(0, THUMBNAIL_WIDTH)
        effect_y = random.randint(0, THUMBNAIL_HEIGHT)
        effect_size = random.randint(5, 15)
        
        # Draw quantum circle
        for i in range(3):
            pygame.draw.circle(
                surface,
                (*colors['secondary'], 100 - i * 30),
                (effect_x, effect_y),
                effect_size + i * 3,
                1
            )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("QUANTUM LEAP", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_neon_blocks_thumbnail():
    """Generate a thumbnail for Neon Blocks (Tetris-type) game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['neon_blocks']
    
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
    
    # Draw tetris grid
    grid_left = THUMBNAIL_WIDTH // 2 - 60
    grid_top = 40
    grid_width = 120
    grid_height = 150
    cell_size = 15
    
    # Draw grid background
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        pygame.Rect(grid_left, grid_top, grid_width, grid_height)
    )
    
    # Draw grid lines
    for x in range(grid_left, grid_left + grid_width + 1, cell_size):
        pygame.draw.line(
            surface,
            (50, 50, 80),
            (x, grid_top),
            (x, grid_top + grid_height),
            1
        )
    
    for y in range(grid_top, grid_top + grid_height + 1, cell_size):
        pygame.draw.line(
            surface,
            (50, 50, 80),
            (grid_left, y),
            (grid_left + grid_width, y),
            1
        )
    
    # Draw tetris blocks
    tetris_shapes = [
        # I-block
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        # O-block
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        # T-block
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        # L-block
        [(0, 0), (0, 1), (0, 2), (1, 2)],
        # J-block
        [(1, 0), (1, 1), (1, 2), (0, 2)],
        # S-block
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        # Z-block
        [(0, 0), (1, 0), (1, 1), (2, 1)]
    ]
    
    tetris_colors = [
        (0, 255, 255),  # Cyan
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (255, 165, 0),  # Orange
        (0, 0, 255),    # Blue
        (0, 255, 0),    # Green
        (255, 0, 0)     # Red
    ]
    
    # Place blocks on the grid
    for i, (shape, color) in enumerate(zip(tetris_shapes, tetris_colors)):
        # Randomize position
        offset_x = random.randint(0, 8 - max(x for x, y in shape) - 1)
        offset_y = random.randint(0, 10 - max(y for x, y in shape) - 1)
        
        # Only place some blocks
        if random.random() < 0.7:
            for x, y in shape:
                cell_x = grid_left + (offset_x + x) * cell_size
                cell_y = grid_top + (offset_y + y) * cell_size
                
                pygame.draw.rect(
                    surface,
                    color,
                    pygame.Rect(cell_x + 1, cell_y + 1, cell_size - 2, cell_size - 2)
                )
                
                # Add highlight
                pygame.draw.line(
                    surface,
                    (255, 255, 255, 150),
                    (cell_x + 1, cell_y + 1),
                    (cell_x + cell_size - 2, cell_y + 1),
                    1
                )
                pygame.draw.line(
                    surface,
                    (255, 255, 255, 150),
                    (cell_x + 1, cell_y + 1),
                    (cell_x + 1, cell_y + cell_size - 2),
                    1
                )
    
    # Draw falling block
    falling_shape = random.choice(tetris_shapes)
    falling_color = random.choice(tetris_colors)
    falling_x = grid_left + 5 * cell_size
    falling_y = grid_top - 2 * cell_size
    
    for x, y in falling_shape:
        cell_x = falling_x + x * cell_size
        cell_y = falling_y + y * cell_size
        
        pygame.draw.rect(
            surface,
            falling_color,
            pygame.Rect(cell_x + 1, cell_y + 1, cell_size - 2, cell_size - 2)
        )
        
        # Add highlight
        pygame.draw.line(
            surface,
            (255, 255, 255, 150),
            (cell_x + 1, cell_y + 1),
            (cell_x + cell_size - 2, cell_y + 1),
            1
        )
        pygame.draw.line(
            surface,
            (255, 255, 255, 150),
            (cell_x + 1, cell_y + 1),
            (cell_x + 1, cell_y + cell_size - 2),
            1
        )
    
    # Draw next block preview
    preview_left = grid_left + grid_width + 20
    preview_top = grid_top + 20
    preview_width = 60
    preview_height = 60
    
    # Preview box
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        pygame.Rect(preview_left, preview_top, preview_width, preview_height)
    )
    pygame.draw.rect(
        surface,
        (50, 50, 80),
        pygame.Rect(preview_left, preview_top, preview_width, preview_height),
        1
    )
    
    # Preview label
    font = pygame.font.SysFont("Arial", 12)
    label_text = font.render("NEXT", True, (200, 200, 255))
    label_rect = label_text.get_rect(center=(preview_left + preview_width // 2, preview_top - 10))
    surface.blit(label_text, label_rect)
    
    # Preview block
    preview_shape = random.choice(tetris_shapes)
    preview_color = random.choice(tetris_colors)
    
    for x, y in preview_shape:
        cell_x = preview_left + 15 + x * cell_size
        cell_y = preview_top + 15 + y * cell_size
        
        pygame.draw.rect(
            surface,
            preview_color,
            pygame.Rect(cell_x + 1, cell_y + 1, cell_size - 2, cell_size - 2)
        )
    
    # Draw score
    score_left = grid_left - 80
    score_top = grid_top + 20
    
    # Score box
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        pygame.Rect(score_left, score_top, 60, 30)
    )
    pygame.draw.rect(
        surface,
        (50, 50, 80),
        pygame.Rect(score_left, score_top, 60, 30),
        1
    )
    
    # Score label
    font = pygame.font.SysFont("Arial", 12)
    label_text = font.render("SCORE", True, (200, 200, 255))
    label_rect = label_text.get_rect(center=(score_left + 30, score_top - 10))
    surface.blit(label_text, label_rect)
    
    # Score value
    font = pygame.font.SysFont("Arial", 14, bold=True)
    score_text = font.render("12,580", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(score_left + 30, score_top + 15))
    surface.blit(score_text, score_rect)
    
    # Draw neon effects
    for _ in range(10):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(0, THUMBNAIL_HEIGHT)
        size = random.randint(1, 3)
        color = random.choice(tetris_colors)
        
        pygame.draw.circle(
            surface,
            color,
            (x, y),
            size
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("NEON BLOCKS", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_cyber_spades_thumbnail():
    """Generate a thumbnail for Cyber Spades card game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['cyber_spades']
    
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
    
    # Draw digital table
    table_rect = pygame.Rect(20, 40, THUMBNAIL_WIDTH - 40, THUMBNAIL_HEIGHT - 80)
    pygame.draw.rect(
        surface,
        colors['primary'],
        table_rect,
        0,
        border_radius=20
    )
    
    # Draw table border
    pygame.draw.rect(
        surface,
        colors['secondary'],
        table_rect,
        2,
        border_radius=20
    )
    
    # Draw digital grid on table
    for x in range(table_rect.left, table_rect.right, 20):
        pygame.draw.line(
            surface,
            (*colors['secondary'], 30),
            (x, table_rect.top),
            (x, table_rect.bottom),
            1
        )
    
    for y in range(table_rect.top, table_rect.bottom, 20):
        pygame.draw.line(
            surface,
            (*colors['secondary'], 30),
            (table_rect.left, y),
            (table_rect.right, y),
            1
        )
    
    # Draw cards
    card_width = 40
    card_height = 60
    
    # Player's hand (bottom)
    player_cards = [
        (THUMBNAIL_WIDTH // 2 - 60, THUMBNAIL_HEIGHT - 70),
        (THUMBNAIL_WIDTH // 2 - 20, THUMBNAIL_HEIGHT - 70),
        (THUMBNAIL_WIDTH // 2 + 20, THUMBNAIL_HEIGHT - 70),
        (THUMBNAIL_WIDTH // 2 + 60, THUMBNAIL_HEIGHT - 70)
    ]
    
    for x, y in player_cards:
        # Card background
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            pygame.Rect(x - card_width // 2, y - card_height // 2, card_width, card_height),
            0,
            border_radius=3
        )
        
        # Card border
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            pygame.Rect(x - card_width // 2, y - card_height // 2, card_width, card_height),
            1,
            border_radius=3
        )
    
    # Draw spade symbol on one card
    spade_x = THUMBNAIL_WIDTH // 2 - 20
    spade_y = THUMBNAIL_HEIGHT - 70
    
    # Spade symbol
    pygame.draw.polygon(
        surface,
        (0, 0, 0),
        [
            (spade_x, spade_y - 15),
            (spade_x - 10, spade_y),
            (spade_x, spade_y + 10),
            (spade_x + 10, spade_y)
        ]
    )
    
    # Spade stem
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        pygame.Rect(spade_x - 2, spade_y + 10, 4, 10)
    )
    
    # Card value
    font = pygame.font.SysFont("Arial", 14, bold=True)
    value_text = font.render("A", True, (0, 0, 0))
    value_rect = value_text.get_rect(center=(spade_x - 12, spade_y - 20))
    surface.blit(value_text, value_rect)
    
    # Draw heart symbol on another card
    heart_x = THUMBNAIL_WIDTH // 2 + 20
    heart_y = THUMBNAIL_HEIGHT - 70
    
    # Heart symbol
    pygame.draw.polygon(
        surface,
        (255, 0, 0),
        [
            (heart_x, heart_y + 10),
            (heart_x - 10, heart_y - 5),
            (heart_x, heart_y - 15),
            (heart_x + 10, heart_y - 5)
        ]
    )
    
    # Card value
    font = pygame.font.SysFont("Arial", 14, bold=True)
    value_text = font.render("K", True, (255, 0, 0))
    value_rect = value_text.get_rect(center=(heart_x - 12, heart_y - 20))
    surface.blit(value_text, value_rect)
    
    # Draw cards in play (center)
    center_cards = [
        (THUMBNAIL_WIDTH // 2 - 30, THUMBNAIL_HEIGHT // 2 - 10),
        (THUMBNAIL_WIDTH // 2 + 30, THUMBNAIL_HEIGHT // 2 + 10),
        (THUMBNAIL_WIDTH // 2 - 10, THUMBNAIL_HEIGHT // 2 - 30),
        (THUMBNAIL_WIDTH // 2 + 50, THUMBNAIL_HEIGHT // 2 - 10)
    ]
    
    for x, y in center_cards:
        # Card background
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            pygame.Rect(x - card_width // 2, y - card_height // 2, card_width, card_height),
            0,
            border_radius=3
        )
        
        # Card border
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            pygame.Rect(x - card_width // 2, y - card_height // 2, card_width, card_height),
            1,
            border_radius=3
        )
    
    # Draw spade symbol on center card
    center_spade_x = THUMBNAIL_WIDTH // 2 - 30
    center_spade_y = THUMBNAIL_HEIGHT // 2 - 10
    
    # Spade symbol
    pygame.draw.polygon(
        surface,
        (0, 0, 0),
        [
            (center_spade_x, center_spade_y - 10),
            (center_spade_x - 8, center_spade_y),
            (center_spade_x, center_spade_y + 8),
            (center_spade_x + 8, center_spade_y)
        ]
    )
    
    # Spade stem
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        pygame.Rect(center_spade_x - 2, center_spade_y + 8, 4, 8)
    )
    
    # Card value
    font = pygame.font.SysFont("Arial", 14, bold=True)
    value_text = font.render("Q", True, (0, 0, 0))
    value_rect = value_text.get_rect(center=(center_spade_x - 12, center_spade_y - 20))
    surface.blit(value_text, value_rect)
    
    # Draw digital effects
    for _ in range(15):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(0, THUMBNAIL_HEIGHT)
        size = random.randint(1, 3)
        
        pygame.draw.circle(
            surface,
            colors['accent'],
            (x, y),
            size
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("CYBER SPADES", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface

def main():
    """Generate all thumbnails."""
    # Create thumbnails
    thumbnails = {
        'quantum_leap': generate_quantum_leap_thumbnail(),
        'neon_blocks': generate_neon_blocks_thumbnail(),
        'cyber_spades': generate_cyber_spades_thumbnail()
    }
    
    # Save thumbnails
    for game_id, surface in thumbnails.items():
        output_path = os.path.join(OUTPUT_DIR, f"{game_id}.png")
        pygame.image.save(surface, output_path)
        print(f"Generated thumbnail for {game_id}: {output_path}")

if __name__ == "__main__":
    main()
    pygame.quit()
