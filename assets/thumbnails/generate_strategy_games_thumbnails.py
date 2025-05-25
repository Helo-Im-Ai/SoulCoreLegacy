"""
Generate Strategy-themed thumbnail images for SoulCoreLegacy Arcade.
This script creates visually distinct thumbnails for Strategy games.
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

# Define colors for Strategy games
COLORS = {
    'space_commander': {  # Space strategy
        'bg': (0, 0, 30),  # Dark blue
        'primary': (0, 50, 100),  # Blue
        'secondary': (50, 100, 200),  # Light blue
        'accent': (255, 200, 0),  # Gold
    },
    'quantum_tactics': {  # Tactical strategy
        'bg': (0, 30, 30),  # Dark teal
        'primary': (0, 100, 100),  # Teal
        'secondary': (0, 150, 150),  # Light teal
        'accent': (255, 100, 0),  # Orange
    },
    'civilization_nexus': {  # 4X strategy
        'bg': (30, 0, 30),  # Dark purple
        'primary': (80, 0, 80),  # Purple
        'secondary': (120, 0, 120),  # Light purple
        'accent': (0, 255, 255),  # Cyan
    }
}

def generate_space_commander_thumbnail():
    """Generate a thumbnail for Space Commander (Space strategy) game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['space_commander']
    
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
    
    # Draw planets
    planet_positions = [
        (50, 50),
        (200, 70),
        (100, 150)
    ]
    
    planet_colors = [
        (200, 100, 0),  # Orange
        (0, 150, 200),  # Blue
        (150, 200, 0)   # Green
    ]
    
    planet_sizes = [20, 15, 25]
    
    for (x, y), color, size in zip(planet_positions, planet_colors, planet_sizes):
        # Draw planet
        pygame.draw.circle(
            surface,
            color,
            (x, y),
            size
        )
        
        # Draw planet details
        for i in range(3):
            pygame.draw.circle(
                surface,
                (color[0] + 20, color[1] + 20, color[2] + 20),
                (x, y),
                size - 5 - i * 3,
                1
            )
    
    # Draw spaceships
    ship_positions = [
        (THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT // 2),
        (THUMBNAIL_WIDTH // 2 - 50, THUMBNAIL_HEIGHT // 2 + 30),
        (THUMBNAIL_WIDTH // 2 + 40, THUMBNAIL_HEIGHT // 2 - 20),
        (THUMBNAIL_WIDTH // 2 - 30, THUMBNAIL_HEIGHT // 2 - 40),
        (THUMBNAIL_WIDTH // 2 + 60, THUMBNAIL_HEIGHT // 2 + 10)
    ]
    
    ship_colors = [
        (200, 200, 200),  # White (flagship)
        (150, 150, 150),  # Light gray
        (150, 150, 150),  # Light gray
        (150, 150, 150),  # Light gray
        (150, 150, 150)   # Light gray
    ]
    
    ship_sizes = [15, 10, 10, 10, 10]
    
    for (x, y), color, size in zip(ship_positions, ship_colors, ship_sizes):
        # Draw ship body
        pygame.draw.polygon(
            surface,
            color,
            [
                (x, y - size),
                (x - size // 2, y + size // 2),
                (x, y),
                (x + size // 2, y + size // 2)
            ]
        )
        
        # Draw ship engines
        pygame.draw.rect(
            surface,
            (255, 100, 0),  # Orange
            pygame.Rect(x - size // 4, y + size // 2, size // 2, size // 4)
        )
    
    # Draw movement paths
    for i in range(1, len(ship_positions)):
        start_x, start_y = ship_positions[0]
        end_x, end_y = ship_positions[i]
        
        # Draw dotted line
        for j in range(0, 10, 2):
            progress = j / 10
            path_x = start_x + (end_x - start_x) * progress
            path_y = start_y + (end_y - start_y) * progress
            
            pygame.draw.circle(
                surface,
                colors['accent'],
                (int(path_x), int(path_y)),
                2
            )
    
    # Draw strategic grid
    for x in range(0, THUMBNAIL_WIDTH, 30):
        pygame.draw.line(
            surface,
            (*colors['secondary'], 50),
            (x, 0),
            (x, THUMBNAIL_HEIGHT),
            1
        )
    
    for y in range(0, THUMBNAIL_HEIGHT, 30):
        pygame.draw.line(
            surface,
            (*colors['secondary'], 50),
            (0, y),
            (THUMBNAIL_WIDTH, y),
            1
        )
    
    # Draw HUD elements
    # Top bar
    pygame.draw.rect(
        surface,
        (*colors['primary'], 200),
        pygame.Rect(0, 0, THUMBNAIL_WIDTH, 30)
    )
    
    # Resources
    resource_icons = [
        {"icon": "⚡", "value": "1250", "x": 30},
        {"icon": "⛏️", "value": "750", "x": 100},
        {"icon": "🔬", "value": "500", "x": 170},
        {"icon": "👥", "value": "8/10", "x": 240}
    ]
    
    for resource in resource_icons:
        # Draw icon
        font = pygame.font.SysFont("Arial", 14)
        icon_text = font.render(resource["icon"], True, colors['accent'])
        icon_rect = icon_text.get_rect(center=(resource["x"], 15))
        surface.blit(icon_text, icon_rect)
        
        # Draw value
        value_text = font.render(resource["value"], True, (255, 255, 255))
        value_rect = value_text.get_rect(midleft=(resource["x"] + 15, 15))
        surface.blit(value_text, value_rect)
    
    # Draw mini-map
    map_rect = pygame.Rect(THUMBNAIL_WIDTH - 70, THUMBNAIL_HEIGHT - 70, 60, 60)
    pygame.draw.rect(
        surface,
        (*colors['primary'], 200),
        map_rect
    )
    pygame.draw.rect(
        surface,
        colors['accent'],
        map_rect,
        1
    )
    
    # Draw dots on mini-map
    for (x, y), color, _ in zip(planet_positions, planet_colors, planet_sizes):
        # Scale coordinates to mini-map
        map_x = map_rect.left + int((x / THUMBNAIL_WIDTH) * map_rect.width)
        map_y = map_rect.top + int((y / THUMBNAIL_HEIGHT) * map_rect.height)
        
        pygame.draw.circle(
            surface,
            color,
            (map_x, map_y),
            3
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("SPACE COMMANDER", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT - 15))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_quantum_tactics_thumbnail():
    """Generate a thumbnail for Quantum Tactics (Tactical strategy) game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['quantum_tactics']
    
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
    
    # Draw tactical grid
    cell_size = 30
    for x in range(0, THUMBNAIL_WIDTH, cell_size):
        pygame.draw.line(
            surface,
            (*colors['secondary'], 100),
            (x, 0),
            (x, THUMBNAIL_HEIGHT),
            1
        )
    
    for y in range(0, THUMBNAIL_HEIGHT, cell_size):
        pygame.draw.line(
            surface,
            (*colors['secondary'], 100),
            (0, y),
            (THUMBNAIL_WIDTH, y),
            1
        )
    
    # Draw terrain features
    # Mountains
    mountain_positions = [
        (60, 60),
        (180, 90),
        (90, 150)
    ]
    
    for x, y in mountain_positions:
        pygame.draw.polygon(
            surface,
            (100, 100, 100),  # Gray
            [
                (x, y - 15),
                (x - 15, y + 15),
                (x + 15, y + 15)
            ]
        )
    
    # Forests
    forest_positions = [
        (150, 60),
        (210, 150),
        (30, 120)
    ]
    
    for x, y in forest_positions:
        for i in range(3):
            offset_x = (i - 1) * 8
            pygame.draw.polygon(
                surface,
                (0, 100, 0),  # Green
                [
                    (x + offset_x, y - 15),
                    (x - 10 + offset_x, y + 5),
                    (x + 10 + offset_x, y + 5)
                ]
            )
    
    # Water
    water_positions = [
        (120, 120),
        (240, 60)
    ]
    
    for x, y in water_positions:
        pygame.draw.rect(
            surface,
            (0, 100, 200),  # Blue
            pygame.Rect(x - 15, y - 15, 30, 30)
        )
        
        # Water ripples
        for i in range(2):
            pygame.draw.arc(
                surface,
                (0, 150, 255),
                pygame.Rect(x - 10 + i * 10, y - 5 + i * 5, 10, 5),
                0, math.pi,
                1
            )
    
    # Draw units
    # Player units (blue)
    player_positions = [
        (90, 90),
        (60, 120),
        (120, 60)
    ]
    
    for x, y in player_positions:
        # Unit circle
        pygame.draw.circle(
            surface,
            (0, 0, 200),  # Blue
            (x, y),
            10
        )
        
        # Unit border
        pygame.draw.circle(
            surface,
            (0, 100, 255),  # Light blue
            (x, y),
            10,
            2
        )
        
        # Unit direction indicator
        pygame.draw.line(
            surface,
            (0, 200, 255),  # Cyan
            (x, y),
            (x + 8, y - 8),
            2
        )
    
    # Enemy units (red)
    enemy_positions = [
        (210, 90),
        (180, 120),
        (240, 120)
    ]
    
    for x, y in enemy_positions:
        # Unit circle
        pygame.draw.circle(
            surface,
            (200, 0, 0),  # Red
            (x, y),
            10
        )
        
        # Unit border
        pygame.draw.circle(
            surface,
            (255, 100, 100),  # Light red
            (x, y),
            10,
            2
        )
        
        # Unit direction indicator
        pygame.draw.line(
            surface,
            (255, 200, 200),  # Light pink
            (x, y),
            (x - 8, y - 8),
            2
        )
    
    # Draw movement path
    path_points = [
        (90, 90),
        (120, 90),
        (150, 90),
        (180, 90)
    ]
    
    # Draw path line
    for i in range(len(path_points) - 1):
        pygame.draw.line(
            surface,
            colors['accent'],
            path_points[i],
            path_points[i + 1],
            2
        )
    
    # Draw path points
    for x, y in path_points:
        pygame.draw.circle(
            surface,
            colors['accent'],
            (x, y),
            3
        )
    
    # Draw attack indicator
    pygame.draw.line(
        surface,
        (255, 0, 0),  # Red
        path_points[-1],
        enemy_positions[0],
        2
    )
    
    # Draw explosion at target
    explosion_x, explosion_y = enemy_positions[0]
    for i in range(8):
        angle = i * math.pi / 4
        length = random.randint(5, 10)
        end_x = explosion_x + math.cos(angle) * length
        end_y = explosion_y + math.sin(angle) * length
        
        pygame.draw.line(
            surface,
            (255, 200, 0),  # Yellow
            (explosion_x, explosion_y),
            (end_x, end_y),
            2
        )
    
    # Draw HUD elements
    # Unit info panel
    panel_rect = pygame.Rect(20, 20, 120, 80)
    pygame.draw.rect(
        surface,
        (*colors['primary'], 200),
        panel_rect,
        0,
        border_radius=5
    )
    pygame.draw.rect(
        surface,
        colors['secondary'],
        panel_rect,
        1,
        border_radius=5
    )
    
    # Unit name
    font = pygame.font.SysFont("Arial", 12, bold=True)
    name_text = font.render("ASSAULT MECH", True, (255, 255, 255))
    name_rect = name_text.get_rect(topleft=(panel_rect.left + 10, panel_rect.top + 10))
    surface.blit(name_text, name_rect)
    
    # Unit stats
    stats = [
        {"label": "HP", "value": "75/100"},
        {"label": "ATK", "value": "45"},
        {"label": "DEF", "value": "30"}
    ]
    
    for i, stat in enumerate(stats):
        # Label
        label_text = font.render(stat["label"], True, colors['accent'])
        label_rect = label_text.get_rect(topleft=(panel_rect.left + 10, panel_rect.top + 30 + i * 15))
        surface.blit(label_text, label_rect)
        
        # Value
        value_text = font.render(stat["value"], True, (255, 255, 255))
        value_rect = value_text.get_rect(topleft=(panel_rect.left + 50, panel_rect.top + 30 + i * 15))
        surface.blit(value_text, value_rect)
    
    # Action buttons
    button_labels = ["MOVE", "ATTACK", "DEFEND"]
    button_width = 60
    button_height = 20
    
    for i, label in enumerate(button_labels):
        button_rect = pygame.Rect(
            THUMBNAIL_WIDTH - 20 - button_width,
            20 + i * (button_height + 10),
            button_width,
            button_height
        )
        
        pygame.draw.rect(
            surface,
            colors['primary'],
            button_rect,
            0,
            border_radius=5
        )
        pygame.draw.rect(
            surface,
            colors['accent'],
            button_rect,
            1,
            border_radius=5
        )
        
        button_text = font.render(label, True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        surface.blit(button_text, button_text_rect)
    
    # Draw quantum effects
    for _ in range(10):
        effect_x = random.randint(0, THUMBNAIL_WIDTH)
        effect_y = random.randint(0, THUMBNAIL_HEIGHT)
        effect_size = random.randint(5, 15)
        
        # Draw quantum circle
        for i in range(3):
            pygame.draw.circle(
                surface,
                (*colors['accent'], 100 - i * 30),
                (effect_x, effect_y),
                effect_size + i * 3,
                1
            )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("QUANTUM TACTICS", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT - 15))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_civilization_nexus_thumbnail():
    """Generate a thumbnail for Civilization Nexus (4X strategy) game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['civilization_nexus']
    
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
    
    # Draw hex grid
    hex_size = 20
    hex_width = hex_size * 2
    hex_height = int(hex_size * math.sqrt(3))
    
    for row in range(-1, THUMBNAIL_HEIGHT // hex_height + 1):
        for col in range(-1, int(THUMBNAIL_WIDTH // (hex_width * 3/4)) + 1):
            # Calculate hex center
            x = col * hex_width * 3/4
            y = row * hex_height
            
            if col % 2 == 1:
                y += hex_height / 2
            
            # Draw hex
            hex_points = []
            for i in range(6):
                angle = i * math.pi / 3
                hex_x = x + hex_size * math.cos(angle)
                hex_y = y + hex_size * math.sin(angle)
                hex_points.append((hex_x, hex_y))
            
            pygame.draw.polygon(
                surface,
                (*colors['primary'], 50),
                hex_points,
                1
            )
    
    # Draw terrain types
    terrain_types = [
        {"color": (0, 150, 0), "count": 5},    # Forest
        {"color": (200, 200, 100), "count": 5},  # Desert
        {"color": (100, 100, 200), "count": 3},  # Water
        {"color": (150, 150, 150), "count": 3}   # Mountains
    ]
    
    for terrain in terrain_types:
        for _ in range(terrain["count"]):
            # Random position
            col = random.randint(0, int(THUMBNAIL_WIDTH // (hex_width * 3/4)))
            row = random.randint(0, int(THUMBNAIL_HEIGHT // hex_height))
            
            # Calculate hex center
            x = col * hex_width * 3/4
            y = row * hex_height
            
            if col % 2 == 1:
                y += hex_height / 2
            
            # Draw hex
            hex_points = []
            for i in range(6):
                angle = i * math.pi / 3
                hex_x = x + hex_size * math.cos(angle)
                hex_y = y + hex_size * math.sin(angle)
                hex_points.append((hex_x, hex_y))
            
            pygame.draw.polygon(
                surface,
                terrain["color"],
                hex_points
            )
    
    # Draw cities
    city_positions = [
        (THUMBNAIL_WIDTH // 4, THUMBNAIL_HEIGHT // 3),
        (THUMBNAIL_WIDTH * 3 // 4, THUMBNAIL_HEIGHT // 2),
        (THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT * 2 // 3)
    ]
    
    city_colors = [
        (200, 0, 0),    # Red
        (0, 0, 200),    # Blue
        (200, 200, 0)   # Yellow
    ]
    
    for (x, y), color in zip(city_positions, city_colors):
        # City circle
        pygame.draw.circle(
            surface,
            color,
            (x, y),
            10
        )
        
        # City border
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (x, y),
            10,
            2
        )
        
        # City buildings
        for i in range(-1, 2):
            building_height = random.randint(3, 7)
            pygame.draw.rect(
                surface,
                (255, 255, 255),
                pygame.Rect(x + i * 5 - 1, y - building_height, 3, building_height)
            )
    
    # Draw borders between territories
    border_points = [
        [(50, 50), (100, 70), (150, 50), (170, 100), (150, 150), (100, 170), (50, 150), (30, 100)],
        [(170, 100), (200, 50), (250, 70), (270, 120), (250, 170), (200, 150)],
        [(150, 150), (170, 100), (200, 150), (250, 170), (200, 200), (150, 180)]
    ]
    
    border_colors = [
        (255, 0, 0, 100),    # Red
        (0, 0, 255, 100),    # Blue
        (255, 255, 0, 100)   # Yellow
    ]
    
    for points, color in zip(border_points, border_colors):
        # Draw territory fill
        pygame.draw.polygon(
            surface,
            color,
            points
        )
        
        # Draw territory border
        pygame.draw.polygon(
            surface,
            (*color[:3], 200),
            points,
            2
        )
    
    # Draw units
    unit_positions = [
        (80, 100),
        (220, 120),
        (150, 170)
    ]
    
    unit_colors = [
        (255, 0, 0),    # Red
        (0, 0, 255),    # Blue
        (255, 255, 0)   # Yellow
    ]
    
    unit_types = ["⚔️", "🏹", "🐎"]
    
    for (x, y), color, unit_type in zip(unit_positions, unit_colors, unit_types):
        # Unit circle
        pygame.draw.circle(
            surface,
            color,
            (x, y),
            8
        )
        
        # Unit border
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (x, y),
            8,
            1
        )
        
        # Unit type
        font = pygame.font.SysFont("Arial", 10)
        type_text = font.render(unit_type, True, (255, 255, 255))
        type_rect = type_text.get_rect(center=(x, y))
        surface.blit(type_text, type_rect)
    
    # Draw HUD elements
    # Top bar
    pygame.draw.rect(
        surface,
        (*colors['primary'], 200),
        pygame.Rect(0, 0, THUMBNAIL_WIDTH, 30)
    )
    
    # Resources
    resource_icons = [
        {"icon": "🏛️", "value": "3", "x": 30},
        {"icon": "🌾", "value": "24", "x": 80},
        {"icon": "⚒️", "value": "18", "x": 130},
        {"icon": "📚", "value": "12", "x": 180},
        {"icon": "😊", "value": "85%", "x": 230}
    ]
    
    for resource in resource_icons:
        # Draw icon
        font = pygame.font.SysFont("Arial", 12)
        icon_text = font.render(resource["icon"], True, colors['accent'])
        icon_rect = icon_text.get_rect(center=(resource["x"], 15))
        surface.blit(icon_text, icon_rect)
        
        # Draw value
        value_text = font.render(resource["value"], True, (255, 255, 255))
        value_rect = value_text.get_rect(midleft=(resource["x"] + 10, 15))
        surface.blit(value_text, value_rect)
    
    # Mini-map
    map_rect = pygame.Rect(THUMBNAIL_WIDTH - 70, THUMBNAIL_HEIGHT - 70, 60, 60)
    pygame.draw.rect(
        surface,
        (*colors['primary'], 200),
        map_rect
    )
    pygame.draw.rect(
        surface,
        colors['accent'],
        map_rect,
        1
    )
    
    # Draw territories on mini-map
    for points, color in zip(border_points, border_colors):
        # Scale points to mini-map
        scaled_points = []
        for x, y in points:
            map_x = map_rect.left + int((x / THUMBNAIL_WIDTH) * map_rect.width)
            map_y = map_rect.top + int((y / THUMBNAIL_HEIGHT) * map_rect.height)
            scaled_points.append((map_x, map_y))
        
        pygame.draw.polygon(
            surface,
            color,
            scaled_points
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("CIVILIZATION NEXUS", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT - 15))
    surface.blit(title_text, title_rect)
    
    return surface

def main():
    """Generate all thumbnails."""
    # Create thumbnails
    thumbnails = {
        'space_commander': generate_space_commander_thumbnail(),
        'quantum_tactics': generate_quantum_tactics_thumbnail(),
        'civilization_nexus': generate_civilization_nexus_thumbnail()
    }
    
    # Save thumbnails
    for game_id, surface in thumbnails.items():
        output_path = os.path.join(OUTPUT_DIR, f"{game_id}.png")
        pygame.image.save(surface, output_path)
        print(f"Generated thumbnail for {game_id}: {output_path}")

if __name__ == "__main__":
    main()
    pygame.quit()
