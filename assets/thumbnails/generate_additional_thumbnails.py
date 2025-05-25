"""
Generate additional thumbnail images for SoulCoreLegacy Arcade games.
This script creates visually distinct thumbnails for new games.
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

# Define colors for new games
COLORS = {
    'cyber_defense': {
        'bg': (0, 20, 30),  # Dark blue
        'primary': (0, 150, 200),  # Blue
        'secondary': (0, 255, 255),  # Cyan
        'accent': (255, 50, 50),  # Red
    },
    'quantum_puzzler': {
        'bg': (20, 0, 30),  # Dark purple
        'primary': (100, 0, 150),  # Purple
        'secondary': (200, 0, 255),  # Bright purple
        'accent': (0, 255, 200),  # Teal
    },
    'rhythm_master': {
        'bg': (30, 0, 20),  # Dark magenta
        'primary': (200, 0, 100),  # Magenta
        'secondary': (255, 100, 200),  # Pink
        'accent': (255, 255, 0),  # Yellow
    },
    'mech_commander': {
        'bg': (20, 20, 20),  # Dark gray
        'primary': (100, 100, 100),  # Gray
        'secondary': (150, 150, 150),  # Light gray
        'accent': (255, 100, 0),  # Orange
    },
    'crypto_tycoon': {
        'bg': (0, 20, 0),  # Dark green
        'primary': (0, 100, 0),  # Green
        'secondary': (0, 200, 0),  # Bright green
        'accent': (255, 215, 0),  # Gold
    },
    'vr_explorer': {
        'bg': (20, 0, 0),  # Dark red
        'primary': (150, 0, 0),  # Red
        'secondary': (255, 0, 0),  # Bright red
        'accent': (0, 200, 255),  # Blue
    }
}

def generate_cyber_defense_thumbnail():
    """Generate a thumbnail for Cyber Defense game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['cyber_defense']
    
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
    
    # Draw digital network lines
    for _ in range(20):
        start_x = random.randint(0, THUMBNAIL_WIDTH)
        start_y = random.randint(0, THUMBNAIL_HEIGHT)
        length = random.randint(30, 100)
        angle = random.uniform(0, math.pi * 2)
        end_x = start_x + int(math.cos(angle) * length)
        end_y = start_y + int(math.sin(angle) * length)
        
        pygame.draw.line(
            surface,
            colors['secondary'],
            (start_x, start_y),
            (end_x, end_y),
            1
        )
    
    # Draw shield icon
    shield_x = THUMBNAIL_WIDTH // 2
    shield_y = THUMBNAIL_HEIGHT // 2
    shield_width = 80
    shield_height = 100
    
    # Draw shield outline
    shield_points = [
        (shield_x, shield_y - shield_height // 2),
        (shield_x + shield_width // 2, shield_y - shield_height // 4),
        (shield_x + shield_width // 2, shield_y + shield_height // 4),
        (shield_x, shield_y + shield_height // 2),
        (shield_x - shield_width // 2, shield_y + shield_height // 4),
        (shield_x - shield_width // 2, shield_y - shield_height // 4)
    ]
    pygame.draw.polygon(surface, colors['primary'], shield_points)
    pygame.draw.polygon(surface, colors['secondary'], shield_points, 2)
    
    # Draw lock icon on shield
    lock_x = shield_x
    lock_y = shield_y
    lock_size = 30
    
    # Draw lock body
    pygame.draw.rect(
        surface,
        colors['accent'],
        pygame.Rect(lock_x - lock_size // 2, lock_y - lock_size // 4, lock_size, lock_size)
    )
    
    # Draw lock shackle
    pygame.draw.arc(
        surface,
        colors['accent'],
        pygame.Rect(lock_x - lock_size // 3, lock_y - lock_size // 2, lock_size * 2 // 3, lock_size // 2),
        math.pi,
        math.pi * 2,
        3
    )
    
    # Draw binary code in background
    font = pygame.font.SysFont("Arial", 10)
    for _ in range(50):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(0, THUMBNAIL_HEIGHT)
        binary = random.choice(["0", "1"])
        text = font.render(binary, True, (0, 200, 200, 100))
        surface.blit(text, (x, y))
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("CYBER DEFENSE", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 30))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_quantum_puzzler_thumbnail():
    """Generate a thumbnail for Quantum Puzzler game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['quantum_puzzler']
    
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
    
    # Draw quantum wave patterns
    for i in range(5):
        points = []
        amplitude = 20 + i * 5
        frequency = 0.02 + i * 0.005
        phase = i * math.pi / 5
        
        for x in range(0, THUMBNAIL_WIDTH, 2):
            y = THUMBNAIL_HEIGHT // 2 + int(amplitude * math.sin(x * frequency + phase))
            points.append((x, y))
        
        pygame.draw.lines(
            surface,
            (*colors['secondary'], 150),
            False,
            points,
            2
        )
    
    # Draw puzzle pieces
    for _ in range(6):
        x = random.randint(50, THUMBNAIL_WIDTH - 50)
        y = random.randint(50, THUMBNAIL_HEIGHT - 50)
        size = random.randint(30, 50)
        
        # Draw puzzle piece
        pygame.draw.rect(
            surface,
            colors['primary'],
            pygame.Rect(x - size // 2, y - size // 2, size, size),
            0,
            border_radius=5
        )
        
        # Draw puzzle connectors
        connector_size = size // 4
        
        # Top connector
        pygame.draw.circle(
            surface,
            colors['primary'],
            (x, y - size // 2),
            connector_size
        )
        
        # Right connector
        pygame.draw.circle(
            surface,
            colors['primary'],
            (x + size // 2, y),
            connector_size
        )
        
        # Draw quantum symbol on piece
        symbol_size = size // 3
        pygame.draw.circle(
            surface,
            colors['accent'],
            (x, y),
            symbol_size,
            2
        )
        
        # Draw electron orbit
        pygame.draw.ellipse(
            surface,
            colors['accent'],
            pygame.Rect(x - symbol_size, y - symbol_size // 2, symbol_size * 2, symbol_size),
            1
        )
    
    # Draw quantum particles
    for _ in range(20):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(0, THUMBNAIL_HEIGHT)
        size = random.randint(1, 3)
        
        # Draw particle with glow
        for i in range(3):
            pygame.draw.circle(
                surface,
                (*colors['accent'], 100 - i * 30),
                (x, y),
                size + i * 2
            )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("QUANTUM PUZZLER", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 30))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_rhythm_master_thumbnail():
    """Generate a thumbnail for Rhythm Master game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['rhythm_master']
    
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
    
    # Draw music staff lines
    staff_y = THUMBNAIL_HEIGHT // 2
    staff_spacing = 10
    
    for i in range(5):
        y = staff_y - staff_spacing * 2 + i * staff_spacing
        pygame.draw.line(
            surface,
            colors['secondary'],
            (50, y),
            (THUMBNAIL_WIDTH - 50, y),
            2
        )
    
    # Draw music notes
    note_positions = [
        (100, staff_y - staff_spacing),
        (150, staff_y - staff_spacing * 2),
        (200, staff_y),
        (250, staff_y - staff_spacing),
        (300, staff_y - staff_spacing * 2),
        (350, staff_y)
    ]
    
    for x, y in note_positions:
        # Draw note head
        pygame.draw.ellipse(
            surface,
            colors['accent'],
            pygame.Rect(x - 6, y - 5, 12, 10)
        )
        
        # Draw note stem
        pygame.draw.line(
            surface,
            colors['accent'],
            (x + 6, y),
            (x + 6, y - 30),
            2
        )
    
    # Draw equalizer bars
    bar_width = 15
    bar_spacing = 25
    bar_count = 8
    bar_start_x = (THUMBNAIL_WIDTH - (bar_count * bar_width + (bar_count - 1) * bar_spacing)) // 2
    bar_bottom_y = THUMBNAIL_HEIGHT - 50
    
    for i in range(bar_count):
        bar_height = random.randint(20, 80)
        bar_x = bar_start_x + i * (bar_width + bar_spacing)
        
        # Draw bar with gradient
        for y in range(bar_height):
            progress = y / bar_height
            color = (
                int(colors['primary'][0] * (1 - progress) + colors['accent'][0] * progress),
                int(colors['primary'][1] * (1 - progress) + colors['accent'][1] * progress),
                int(colors['primary'][2] * (1 - progress) + colors['accent'][2] * progress)
            )
            
            pygame.draw.line(
                surface,
                color,
                (bar_x, bar_bottom_y - y),
                (bar_x + bar_width, bar_bottom_y - y)
            )
    
    # Draw sound waves
    wave_y = THUMBNAIL_HEIGHT - 20
    wave_points = []
    
    for x in range(0, THUMBNAIL_WIDTH, 5):
        y = wave_y + int(10 * math.sin(x * 0.05))
        wave_points.append((x, y))
    
    pygame.draw.lines(
        surface,
        colors['secondary'],
        False,
        wave_points,
        2
    )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("RHYTHM MASTER", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 30))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_mech_commander_thumbnail():
    """Generate a thumbnail for Mech Commander game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['mech_commander']
    
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
    
    # Draw grid lines for battlefield
    grid_size = 30
    for x in range(0, THUMBNAIL_WIDTH, grid_size):
        pygame.draw.line(
            surface,
            (*colors['primary'], 50),
            (x, 0),
            (x, THUMBNAIL_HEIGHT)
        )
    
    for y in range(0, THUMBNAIL_HEIGHT, grid_size):
        pygame.draw.line(
            surface,
            (*colors['primary'], 50),
            (0, y),
            (THUMBNAIL_WIDTH, y)
        )
    
    # Draw mech robot
    mech_x = THUMBNAIL_WIDTH // 2
    mech_y = THUMBNAIL_HEIGHT // 2
    mech_width = 60
    mech_height = 100
    
    # Draw mech body
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(mech_x - mech_width // 3, mech_y - mech_height // 3, mech_width * 2 // 3, mech_height * 2 // 3)
    )
    
    # Draw mech head
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(mech_x - mech_width // 4, mech_y - mech_height // 2, mech_width // 2, mech_height // 6)
    )
    
    # Draw mech legs
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(mech_x - mech_width // 3, mech_y + mech_height // 6, mech_width // 4, mech_height // 3)
    )
    
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(mech_x + mech_width // 12, mech_y + mech_height // 6, mech_width // 4, mech_height // 3)
    )
    
    # Draw mech arms
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(mech_x - mech_width // 2, mech_y - mech_height // 6, mech_width // 6, mech_height // 3)
    )
    
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(mech_x + mech_width // 3, mech_y - mech_height // 6, mech_width // 6, mech_height // 3)
    )
    
    # Draw weapon
    pygame.draw.rect(
        surface,
        colors['accent'],
        pygame.Rect(mech_x + mech_width // 3, mech_y - mech_height // 6, mech_width // 4, mech_height // 12)
    )
    
    # Draw mech eye
    pygame.draw.rect(
        surface,
        colors['accent'],
        pygame.Rect(mech_x - mech_width // 6, mech_y - mech_height // 2 + mech_height // 24, mech_width // 3, mech_height // 24)
    )
    
    # Draw explosions
    for _ in range(3):
        explosion_x = random.randint(50, THUMBNAIL_WIDTH - 50)
        explosion_y = random.randint(50, THUMBNAIL_HEIGHT - 50)
        explosion_size = random.randint(10, 30)
        
        # Draw explosion rays
        for i in range(8):
            angle = math.radians(i * 45)
            end_x = explosion_x + math.cos(angle) * explosion_size
            end_y = explosion_y + math.sin(angle) * explosion_size
            
            pygame.draw.line(
                surface,
                colors['accent'],
                (explosion_x, explosion_y),
                (end_x, end_y),
                2
            )
        
        # Draw explosion center
        pygame.draw.circle(
            surface,
            (255, 200, 0),
            (explosion_x, explosion_y),
            explosion_size // 3
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("MECH COMMANDER", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 30))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_crypto_tycoon_thumbnail():
    """Generate a thumbnail for Crypto Tycoon game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['crypto_tycoon']
    
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
    
    # Draw stock chart
    chart_points = []
    chart_start_x = 50
    chart_end_x = THUMBNAIL_WIDTH - 50
    chart_start_y = THUMBNAIL_HEIGHT - 50
    chart_height = 100
    
    # Generate random chart data
    x_step = (chart_end_x - chart_start_x) / 20
    for i in range(21):
        x = chart_start_x + i * x_step
        
        if i == 0:
            y = chart_start_y - random.randint(20, chart_height - 20)
        else:
            prev_y = chart_points[-1][1]
            y = prev_y + random.randint(-20, 20)
            y = max(chart_start_y - chart_height, min(chart_start_y - 10, y))
        
        chart_points.append((x, y))
    
    # Draw chart line
    pygame.draw.lines(
        surface,
        colors['accent'],
        False,
        chart_points,
        3
    )
    
    # Draw chart grid
    for y in range(chart_start_y - chart_height, chart_start_y + 1, 20):
        pygame.draw.line(
            surface,
            (*colors['primary'], 50),
            (chart_start_x, y),
            (chart_end_x, y)
        )
    
    for x in range(chart_start_x, chart_end_x + 1, int(x_step * 4)):
        pygame.draw.line(
            surface,
            (*colors['primary'], 50),
            (x, chart_start_y - chart_height),
            (x, chart_start_y)
        )
    
    # Draw crypto coins
    coin_positions = [
        (100, 80),
        (200, 100),
        (300, 70)
    ]
    
    for x, y in coin_positions:
        # Draw coin
        pygame.draw.circle(
            surface,
            colors['accent'],
            (x, y),
            20
        )
        
        pygame.draw.circle(
            surface,
            colors['bg'],
            (x, y),
            15
        )
        
        # Draw currency symbol
        font = pygame.font.SysFont("Arial", 18, bold=True)
        symbols = ["$", "€", "¥"]
        symbol_text = font.render(random.choice(symbols), True, colors['accent'])
        symbol_rect = symbol_text.get_rect(center=(x, y))
        surface.blit(symbol_text, symbol_rect)
    
    # Draw dollar signs in background
    font = pygame.font.SysFont("Arial", 14)
    for _ in range(20):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(0, THUMBNAIL_HEIGHT)
        dollar_text = font.render("$", True, (*colors['secondary'], 100))
        surface.blit(dollar_text, (x, y))
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("CRYPTO TYCOON", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 30))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_vr_explorer_thumbnail():
    """Generate a thumbnail for VR Explorer game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['vr_explorer']
    
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
    
    # Draw VR headset
    headset_x = THUMBNAIL_WIDTH // 2
    headset_y = THUMBNAIL_HEIGHT // 2
    headset_width = 120
    headset_height = 60
    
    # Draw headset body
    pygame.draw.rect(
        surface,
        colors['primary'],
        pygame.Rect(headset_x - headset_width // 2, headset_y - headset_height // 2, headset_width, headset_height),
        0,
        border_radius=10
    )
    
    # Draw headset strap
    pygame.draw.arc(
        surface,
        colors['primary'],
        pygame.Rect(headset_x - headset_width // 2, headset_y - headset_height, headset_width, headset_height * 2),
        math.pi * 0.25,
        math.pi * 0.75,
        5
    )
    
    # Draw headset lenses
    lens_size = headset_height // 2
    lens_spacing = headset_width // 4
    
    pygame.draw.circle(
        surface,
        colors['accent'],
        (headset_x - lens_spacing, headset_y),
        lens_size // 2
    )
    
    pygame.draw.circle(
        surface,
        colors['accent'],
        (headset_x + lens_spacing, headset_y),
        lens_size // 2
    )
    
    # Draw virtual world elements
    # Mountains
    mountain_points = [
        (0, THUMBNAIL_HEIGHT),
        (50, THUMBNAIL_HEIGHT - 80),
        (100, THUMBNAIL_HEIGHT - 40),
        (150, THUMBNAIL_HEIGHT - 100),
        (200, THUMBNAIL_HEIGHT - 60),
        (250, THUMBNAIL_HEIGHT - 120),
        (300, THUMBNAIL_HEIGHT - 50),
        (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)
    ]
    
    pygame.draw.polygon(
        surface,
        (*colors['secondary'], 100),
        mountain_points
    )
    
    # Draw grid lines for virtual space
    for i in range(5):
        # Horizontal lines with perspective
        y_top = 50 + i * 20
        y_bottom = THUMBNAIL_HEIGHT - 50 + i * 10
        width_top = 100 + i * 50
        
        pygame.draw.line(
            surface,
            (*colors['secondary'], 100),
            (THUMBNAIL_WIDTH // 2 - width_top // 2, y_top),
            (THUMBNAIL_WIDTH // 2 + width_top // 2, y_top)
        )
        
        pygame.draw.line(
            surface,
            (*colors['secondary'], 100),
            (0, y_bottom),
            (THUMBNAIL_WIDTH, y_bottom)
        )
        
        # Vertical lines with perspective
        x_left = THUMBNAIL_WIDTH // 2 - width_top // 2
        x_right = THUMBNAIL_WIDTH // 2 + width_top // 2
        
        pygame.draw.line(
            surface,
            (*colors['secondary'], 100),
            (x_left, y_top),
            (0, y_bottom)
        )
        
        pygame.draw.line(
            surface,
            (*colors['secondary'], 100),
            (x_right, y_top),
            (THUMBNAIL_WIDTH, y_bottom)
        )
    
    # Draw floating objects in virtual space
    for _ in range(5):
        x = random.randint(THUMBNAIL_WIDTH // 4, THUMBNAIL_WIDTH * 3 // 4)
        y = random.randint(50, THUMBNAIL_HEIGHT // 2)
        size = random.randint(10, 30)
        shape = random.choice(["circle", "square", "triangle"])
        
        if shape == "circle":
            pygame.draw.circle(
                surface,
                colors['accent'],
                (x, y),
                size // 2
            )
        elif shape == "square":
            pygame.draw.rect(
                surface,
                colors['accent'],
                pygame.Rect(x - size // 2, y - size // 2, size, size)
            )
        else:  # triangle
            points = [
                (x, y - size // 2),
                (x - size // 2, y + size // 2),
                (x + size // 2, y + size // 2)
            ]
            pygame.draw.polygon(
                surface,
                colors['accent'],
                points
            )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("VR EXPLORER", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 30))
    surface.blit(title_text, title_rect)
    
    return surface

def main():
    """Generate all thumbnails."""
    # Create thumbnails
    thumbnails = {
        'cyber_defense': generate_cyber_defense_thumbnail(),
        'quantum_puzzler': generate_quantum_puzzler_thumbnail(),
        'rhythm_master': generate_rhythm_master_thumbnail(),
        'mech_commander': generate_mech_commander_thumbnail(),
        'crypto_tycoon': generate_crypto_tycoon_thumbnail(),
        'vr_explorer': generate_vr_explorer_thumbnail()
    }
    
    # Save thumbnails
    for game_id, surface in thumbnails.items():
        output_path = os.path.join(OUTPUT_DIR, f"{game_id}.png")
        pygame.image.save(surface, output_path)
        print(f"Generated thumbnail for {game_id}: {output_path}")

if __name__ == "__main__":
    main()
    pygame.quit()
