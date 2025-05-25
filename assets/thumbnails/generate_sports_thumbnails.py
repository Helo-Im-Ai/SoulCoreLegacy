"""
Generate sports-themed thumbnail images for SoulCoreLegacy Arcade games.
This script creates visually distinct thumbnails for new sports games.
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

# Define colors for sports games
COLORS = {
    'cyber_soccer': {
        'bg': (0, 50, 0),  # Dark green
        'primary': (0, 150, 0),  # Green
        'secondary': (200, 200, 200),  # Silver
        'accent': (255, 50, 50),  # Red
    },
    'extreme_racing': {
        'bg': (50, 0, 0),  # Dark red
        'primary': (200, 0, 0),  # Red
        'secondary': (255, 150, 0),  # Orange
        'accent': (255, 255, 0),  # Yellow
    },
    'space_basketball': {
        'bg': (0, 0, 50),  # Dark blue
        'primary': (0, 0, 200),  # Blue
        'secondary': (255, 100, 0),  # Orange
        'accent': (255, 255, 255),  # White
    },
    'virtual_tennis': {
        'bg': (0, 30, 0),  # Dark green
        'primary': (100, 200, 100),  # Light green
        'secondary': (255, 255, 0),  # Yellow
        'accent': (255, 255, 255),  # White
    },
    'mech_boxing': {
        'bg': (30, 0, 30),  # Dark purple
        'primary': (150, 0, 150),  # Purple
        'secondary': (200, 200, 0),  # Gold
        'accent': (255, 50, 50),  # Red
    },
    'cyber_surfing': {
        'bg': (0, 30, 50),  # Dark blue
        'primary': (0, 150, 200),  # Blue
        'secondary': (0, 255, 255),  # Cyan
        'accent': (255, 255, 255),  # White
    }
}

def generate_cyber_soccer_thumbnail():
    """Generate a thumbnail for Cyber Soccer game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['cyber_soccer']
    
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
    
    # Draw soccer field
    field_rect = pygame.Rect(20, 40, THUMBNAIL_WIDTH - 40, THUMBNAIL_HEIGHT - 80)
    pygame.draw.rect(surface, colors['primary'], field_rect)
    
    # Draw field lines
    # Center line
    pygame.draw.line(
        surface,
        colors['secondary'],
        (THUMBNAIL_WIDTH // 2, field_rect.top),
        (THUMBNAIL_WIDTH // 2, field_rect.bottom),
        2
    )
    
    # Center circle
    pygame.draw.circle(
        surface,
        colors['secondary'],
        (THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT // 2),
        30,
        2
    )
    
    # Goal areas
    goal_width = 40
    goal_height = 80
    
    # Left goal area
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(field_rect.left, THUMBNAIL_HEIGHT // 2 - goal_height // 2, goal_width, goal_height),
        2
    )
    
    # Right goal area
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(field_rect.right - goal_width, THUMBNAIL_HEIGHT // 2 - goal_height // 2, goal_width, goal_height),
        2
    )
    
    # Draw soccer ball
    ball_x = THUMBNAIL_WIDTH // 2 + 50
    ball_y = THUMBNAIL_HEIGHT // 2 - 10
    ball_radius = 10
    
    # Draw ball
    pygame.draw.circle(
        surface,
        colors['accent'],
        (ball_x, ball_y),
        ball_radius
    )
    
    # Draw ball pattern
    pygame.draw.circle(
        surface,
        (0, 0, 0),
        (ball_x, ball_y),
        ball_radius,
        1
    )
    
    # Draw players (simplified as circles with team colors)
    player_positions = [
        (THUMBNAIL_WIDTH // 4, THUMBNAIL_HEIGHT // 2 - 30),
        (THUMBNAIL_WIDTH // 4, THUMBNAIL_HEIGHT // 2 + 30),
        (THUMBNAIL_WIDTH // 2 - 50, THUMBNAIL_HEIGHT // 2),
        (THUMBNAIL_WIDTH * 3 // 4, THUMBNAIL_HEIGHT // 2 - 30),
        (THUMBNAIL_WIDTH * 3 // 4, THUMBNAIL_HEIGHT // 2 + 30)
    ]
    
    for i, (x, y) in enumerate(player_positions):
        team_color = (0, 0, 200) if i < 3 else (200, 0, 0)  # Blue vs Red
        
        # Draw player
        pygame.draw.circle(
            surface,
            team_color,
            (x, y),
            8
        )
        
        # Draw player number
        font = pygame.font.SysFont("Arial", 8)
        number_text = font.render(str(i + 1), True, (255, 255, 255))
        number_rect = number_text.get_rect(center=(x, y))
        surface.blit(number_text, number_rect)
    
    # Draw digital effects
    for _ in range(20):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(0, THUMBNAIL_HEIGHT)
        size = random.randint(1, 3)
        
        pygame.draw.circle(
            surface,
            (0, 255, 0, 100),
            (x, y),
            size
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("CYBER SOCCER", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_extreme_racing_thumbnail():
    """Generate a thumbnail for Extreme Racing game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['extreme_racing']
    
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
    
    # Draw race track (curved)
    track_points = []
    track_width = 60
    
    # Generate track centerline
    for angle in range(0, 360, 5):
        rad_angle = math.radians(angle)
        radius = 80 + 20 * math.sin(rad_angle * 2)
        x = THUMBNAIL_WIDTH // 2 + int(radius * math.cos(rad_angle))
        y = THUMBNAIL_HEIGHT // 2 + int(radius * math.sin(rad_angle))
        track_points.append((x, y))
    
    # Draw outer track
    pygame.draw.lines(
        surface,
        colors['secondary'],
        True,
        track_points,
        track_width
    )
    
    # Draw track markings
    pygame.draw.lines(
        surface,
        colors['accent'],
        True,
        track_points,
        2
    )
    
    # Draw start/finish line
    start_x = THUMBNAIL_WIDTH // 2
    start_y = THUMBNAIL_HEIGHT // 2 - 100
    
    pygame.draw.rect(
        surface,
        (255, 255, 255),
        pygame.Rect(start_x - 20, start_y - 5, 40, 10),
        0
    )
    
    # Draw checkered pattern on start/finish
    square_size = 5
    for i in range(8):
        for j in range(2):
            if (i + j) % 2 == 0:
                pygame.draw.rect(
                    surface,
                    (0, 0, 0),
                    pygame.Rect(start_x - 20 + i * square_size, start_y - 5 + j * square_size, square_size, square_size)
                )
    
    # Draw race cars
    car_positions = [
        (start_x, start_y + 20),  # Leader
        (start_x - 10, start_y + 40),  # Second
        (start_x + 15, start_y + 60)  # Third
    ]
    
    car_colors = [
        (255, 0, 0),  # Red
        (0, 0, 255),  # Blue
        (255, 255, 0)  # Yellow
    ]
    
    for (x, y), color in zip(car_positions, car_colors):
        # Draw car body
        pygame.draw.rect(
            surface,
            color,
            pygame.Rect(x - 8, y - 12, 16, 24),
            0,
            border_radius=5
        )
        
        # Draw wheels
        pygame.draw.circle(surface, (0, 0, 0), (x - 8, y - 8), 4)
        pygame.draw.circle(surface, (0, 0, 0), (x + 8, y - 8), 4)
        pygame.draw.circle(surface, (0, 0, 0), (x - 8, y + 8), 4)
        pygame.draw.circle(surface, (0, 0, 0), (x + 8, y + 8), 4)
    
    # Draw speed lines
    for _ in range(10):
        start_x = random.randint(0, THUMBNAIL_WIDTH)
        start_y = random.randint(0, THUMBNAIL_HEIGHT)
        length = random.randint(20, 50)
        
        pygame.draw.line(
            surface,
            colors['accent'],
            (start_x, start_y),
            (start_x - length, start_y),
            2
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("EXTREME RACING", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_space_basketball_thumbnail():
    """Generate a thumbnail for Space Basketball game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['space_basketball']
    
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
    
    # Draw stars in background
    for _ in range(50):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(0, THUMBNAIL_HEIGHT)
        size = random.randint(1, 3)
        
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (x, y),
            size
        )
    
    # Draw basketball court
    court_rect = pygame.Rect(50, 50, THUMBNAIL_WIDTH - 100, THUMBNAIL_HEIGHT - 100)
    pygame.draw.rect(
        surface,
        colors['primary'],
        court_rect
    )
    
    # Draw court lines
    # Center circle
    pygame.draw.circle(
        surface,
        colors['secondary'],
        (THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT // 2),
        30,
        2
    )
    
    # Center line
    pygame.draw.line(
        surface,
        colors['secondary'],
        (court_rect.left, THUMBNAIL_HEIGHT // 2),
        (court_rect.right, THUMBNAIL_HEIGHT // 2),
        2
    )
    
    # Draw hoops
    hoop_y = THUMBNAIL_HEIGHT // 2
    
    # Left hoop
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(court_rect.left - 5, hoop_y - 15, 5, 30)
    )
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(court_rect.left - 20, hoop_y - 10, 15, 5)
    )
    pygame.draw.circle(
        surface,
        colors['accent'],
        (court_rect.left - 10, hoop_y),
        10,
        2
    )
    
    # Right hoop
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(court_rect.right, hoop_y - 15, 5, 30)
    )
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(court_rect.right + 5, hoop_y - 10, 15, 5)
    )
    pygame.draw.circle(
        surface,
        colors['accent'],
        (court_rect.right + 10, hoop_y),
        10,
        2
    )
    
    # Draw basketball
    ball_x = THUMBNAIL_WIDTH // 2 + 30
    ball_y = THUMBNAIL_HEIGHT // 2 - 20
    ball_radius = 10
    
    pygame.draw.circle(
        surface,
        colors['secondary'],
        (ball_x, ball_y),
        ball_radius
    )
    
    # Draw ball lines
    pygame.draw.line(
        surface,
        (0, 0, 0),
        (ball_x - ball_radius, ball_y),
        (ball_x + ball_radius, ball_y),
        1
    )
    pygame.draw.line(
        surface,
        (0, 0, 0),
        (ball_x, ball_y - ball_radius),
        (ball_x, ball_y + ball_radius),
        1
    )
    
    # Draw players (simplified as astronauts)
    player_positions = [
        (THUMBNAIL_WIDTH // 4, THUMBNAIL_HEIGHT // 2),
        (THUMBNAIL_WIDTH * 3 // 4, THUMBNAIL_HEIGHT // 2 - 20)
    ]
    
    for x, y in player_positions:
        # Draw spacesuit
        pygame.draw.circle(
            surface,
            (200, 200, 200),
            (x, y - 10),
            10  # Head
        )
        pygame.draw.rect(
            surface,
            (200, 200, 200),
            pygame.Rect(x - 8, y, 16, 20)  # Body
        )
        
        # Draw visor
        pygame.draw.rect(
            surface,
            (100, 200, 255),
            pygame.Rect(x - 5, y - 15, 10, 5)
        )
        
        # Draw team color
        team_color = (0, 0, 200) if x < THUMBNAIL_WIDTH // 2 else (200, 0, 0)
        pygame.draw.rect(
            surface,
            team_color,
            pygame.Rect(x - 8, y + 5, 16, 5)
        )
    
    # Draw zero-gravity effect (motion lines)
    for _ in range(15):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(0, THUMBNAIL_HEIGHT)
        length = random.randint(5, 15)
        angle = random.uniform(0, math.pi * 2)
        
        end_x = x + int(math.cos(angle) * length)
        end_y = y + int(math.sin(angle) * length)
        
        pygame.draw.line(
            surface,
            (100, 100, 255, 100),
            (x, y),
            (end_x, end_y),
            1
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("SPACE BASKETBALL", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface
def generate_virtual_tennis_thumbnail():
    """Generate a thumbnail for Virtual Tennis game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['virtual_tennis']
    
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
    
    # Draw tennis court
    court_rect = pygame.Rect(20, 40, THUMBNAIL_WIDTH - 40, THUMBNAIL_HEIGHT - 80)
    pygame.draw.rect(
        surface,
        colors['primary'],
        court_rect
    )
    
    # Draw court lines
    # Center line
    pygame.draw.line(
        surface,
        colors['accent'],
        (THUMBNAIL_WIDTH // 2, court_rect.top),
        (THUMBNAIL_WIDTH // 2, court_rect.bottom),
        2
    )
    
    # Baseline
    pygame.draw.line(
        surface,
        colors['accent'],
        (court_rect.left, court_rect.top),
        (court_rect.right, court_rect.top),
        2
    )
    pygame.draw.line(
        surface,
        colors['accent'],
        (court_rect.left, court_rect.bottom),
        (court_rect.right, court_rect.bottom),
        2
    )
    
    # Service lines
    service_y_top = court_rect.top + court_rect.height // 3
    service_y_bottom = court_rect.bottom - court_rect.height // 3
    
    pygame.draw.line(
        surface,
        colors['accent'],
        (court_rect.left, service_y_top),
        (court_rect.right, service_y_top),
        2
    )
    pygame.draw.line(
        surface,
        colors['accent'],
        (court_rect.left, service_y_bottom),
        (court_rect.right, service_y_bottom),
        2
    )
    
    # Draw net
    pygame.draw.rect(
        surface,
        colors['accent'],
        pygame.Rect(THUMBNAIL_WIDTH // 2 - 1, court_rect.top, 2, court_rect.height)
    )
    
    # Draw tennis ball
    ball_x = THUMBNAIL_WIDTH // 2 + 40
    ball_y = THUMBNAIL_HEIGHT // 2 - 20
    ball_radius = 8
    
    pygame.draw.circle(
        surface,
        colors['secondary'],
        (ball_x, ball_y),
        ball_radius
    )
    
    # Draw curved line on ball
    pygame.draw.arc(
        surface,
        (255, 255, 255),
        pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2),
        0,
        math.pi,
        1
    )
    
    # Draw players (simplified)
    player1_x = THUMBNAIL_WIDTH // 4
    player1_y = THUMBNAIL_HEIGHT // 2 + 20
    
    player2_x = THUMBNAIL_WIDTH * 3 // 4
    player2_y = THUMBNAIL_HEIGHT // 2 - 20
    
    # Player 1
    pygame.draw.circle(
        surface,
        (255, 200, 150),  # Skin tone
        (player1_x, player1_y - 15),
        8  # Head
    )
    pygame.draw.rect(
        surface,
        (255, 0, 0),  # Red shirt
        pygame.Rect(player1_x - 10, player1_y - 5, 20, 25)
    )
    
    # Player 1 racket
    racket_angle = math.pi / 4
    racket_length = 25
    racket_end_x = player1_x + int(math.cos(racket_angle) * racket_length)
    racket_end_y = player1_y + int(math.sin(racket_angle) * racket_length)
    
    pygame.draw.line(
        surface,
        (150, 75, 0),  # Brown handle
        (player1_x + 5, player1_y),
        (racket_end_x, racket_end_y),
        3
    )
    
    pygame.draw.ellipse(
        surface,
        (150, 75, 0),
        pygame.Rect(racket_end_x - 8, racket_end_y - 12, 16, 24),
        2
    )
    
    # Player 2
    pygame.draw.circle(
        surface,
        (255, 200, 150),  # Skin tone
        (player2_x, player2_y - 15),
        8  # Head
    )
    pygame.draw.rect(
        surface,
        (0, 0, 255),  # Blue shirt
        pygame.Rect(player2_x - 10, player2_y - 5, 20, 25)
    )
    
    # Player 2 racket
    racket_angle = -math.pi / 4
    racket_length = 25
    racket_end_x = player2_x + int(math.cos(racket_angle) * racket_length)
    racket_end_y = player2_y + int(math.sin(racket_angle) * racket_length)
    
    pygame.draw.line(
        surface,
        (150, 75, 0),  # Brown handle
        (player2_x - 5, player2_y),
        (racket_end_x, racket_end_y),
        3
    )
    
    pygame.draw.ellipse(
        surface,
        (150, 75, 0),
        pygame.Rect(racket_end_x - 8, racket_end_y - 12, 16, 24),
        2
    )
    
    # Draw virtual reality elements
    for _ in range(20):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(0, THUMBNAIL_HEIGHT)
        size = random.randint(1, 3)
        
        pygame.draw.circle(
            surface,
            (0, 255, 0, 100),
            (x, y),
            size
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("VIRTUAL TENNIS", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_mech_boxing_thumbnail():
    """Generate a thumbnail for Mech Boxing game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['mech_boxing']
    
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
    
    # Draw boxing ring
    ring_rect = pygame.Rect(40, 40, THUMBNAIL_WIDTH - 80, THUMBNAIL_HEIGHT - 80)
    pygame.draw.rect(
        surface,
        (150, 150, 150),  # Gray canvas
        ring_rect
    )
    
    # Draw ring ropes
    rope_heights = [ring_rect.top, ring_rect.top + 20, ring_rect.top + 40]
    for y in rope_heights:
        pygame.draw.line(
            surface,
            colors['secondary'],
            (ring_rect.left, y),
            (ring_rect.right, y),
            3
        )
        pygame.draw.line(
            surface,
            colors['secondary'],
            (ring_rect.left, ring_rect.bottom - (y - ring_rect.top)),
            (ring_rect.right, ring_rect.bottom - (y - ring_rect.top)),
            3
        )
    
    # Draw ring posts
    post_positions = [
        (ring_rect.left, ring_rect.top),
        (ring_rect.right, ring_rect.top),
        (ring_rect.left, ring_rect.bottom),
        (ring_rect.right, ring_rect.bottom)
    ]
    
    for x, y in post_positions:
        pygame.draw.rect(
            surface,
            (100, 100, 100),
            pygame.Rect(x - 5, y - 5, 10, 10)
        )
    
    # Draw mech boxers
    mech1_x = THUMBNAIL_WIDTH // 3
    mech1_y = THUMBNAIL_HEIGHT // 2
    
    mech2_x = THUMBNAIL_WIDTH * 2 // 3
    mech2_y = THUMBNAIL_HEIGHT // 2
    
    # Mech 1 (left)
    # Body
    pygame.draw.rect(
        surface,
        (200, 0, 0),  # Red
        pygame.Rect(mech1_x - 20, mech1_y - 30, 40, 60),
        0,
        border_radius=5
    )
    
    # Head
    pygame.draw.rect(
        surface,
        (200, 0, 0),
        pygame.Rect(mech1_x - 10, mech1_y - 45, 20, 15),
        0,
        border_radius=3
    )
    
    # Eye
    pygame.draw.rect(
        surface,
        (255, 255, 0),
        pygame.Rect(mech1_x - 5, mech1_y - 40, 10, 5)
    )
    
    # Arms
    pygame.draw.rect(
        surface,
        (150, 0, 0),
        pygame.Rect(mech1_x - 30, mech1_y - 25, 10, 40),
        0,
        border_radius=3
    )
    
    # Boxing glove
    pygame.draw.circle(
        surface,
        (255, 0, 0),
        (mech1_x - 25, mech1_y + 25),
        12
    )
    
    # Extended arm (punching)
    pygame.draw.rect(
        surface,
        (150, 0, 0),
        pygame.Rect(mech1_x + 20, mech1_y - 10, 40, 10),
        0,
        border_radius=3
    )
    
    # Boxing glove (punching)
    pygame.draw.circle(
        surface,
        (255, 0, 0),
        (mech1_x + 65, mech1_y - 5),
        15
    )
    
    # Mech 2 (right)
    # Body
    pygame.draw.rect(
        surface,
        (0, 0, 200),  # Blue
        pygame.Rect(mech2_x - 20, mech2_y - 30, 40, 60),
        0,
        border_radius=5
    )
    
    # Head
    pygame.draw.rect(
        surface,
        (0, 0, 200),
        pygame.Rect(mech2_x - 10, mech2_y - 45, 20, 15),
        0,
        border_radius=3
    )
    
    # Eye
    pygame.draw.rect(
        surface,
        (0, 255, 255),
        pygame.Rect(mech2_x - 5, mech2_y - 40, 10, 5)
    )
    
    # Arms
    pygame.draw.rect(
        surface,
        (0, 0, 150),
        pygame.Rect(mech2_x + 20, mech2_y - 25, 10, 40),
        0,
        border_radius=3
    )
    
    # Boxing glove
    pygame.draw.circle(
        surface,
        (0, 0, 255),
        (mech2_x + 25, mech2_y + 25),
        12
    )
    
    # Defensive arm
    pygame.draw.rect(
        surface,
        (0, 0, 150),
        pygame.Rect(mech2_x - 40, mech2_y - 20, 20, 10),
        0,
        border_radius=3
    )
    
    # Boxing glove (defensive)
    pygame.draw.circle(
        surface,
        (0, 0, 255),
        (mech2_x - 45, mech2_y - 15),
        15
    )
    
    # Draw impact effect
    pygame.draw.circle(
        surface,
        (255, 255, 255, 150),
        (mech2_x - 30, mech2_y - 5),
        20,
        0
    )
    
    for i in range(8):
        angle = i * math.pi / 4
        length = 15
        end_x = mech2_x - 30 + int(math.cos(angle) * length)
        end_y = mech2_y - 5 + int(math.sin(angle) * length)
        
        pygame.draw.line(
            surface,
            (255, 255, 0),
            (mech2_x - 30, mech2_y - 5),
            (end_x, end_y),
            2
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("MECH BOXING", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_cyber_surfing_thumbnail():
    """Generate a thumbnail for Cyber Surfing game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['cyber_surfing']
    
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
    
    # Draw digital ocean
    ocean_height = THUMBNAIL_HEIGHT * 2 // 3
    
    # Draw waves
    wave_points = []
    for x in range(0, THUMBNAIL_WIDTH, 5):
        y = ocean_height + int(10 * math.sin(x * 0.05))
        wave_points.append((x, y))
    
    # Fill ocean
    ocean_polygon = wave_points + [(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), (0, THUMBNAIL_HEIGHT)]
    pygame.draw.polygon(
        surface,
        colors['primary'],
        ocean_polygon
    )
    
    # Draw wave line
    pygame.draw.lines(
        surface,
        colors['secondary'],
        False,
        wave_points,
        3
    )
    
    # Draw digital grid on ocean
    for x in range(0, THUMBNAIL_WIDTH, 20):
        pygame.draw.line(
            surface,
            (*colors['secondary'], 50),
            (x, ocean_height),
            (x, THUMBNAIL_HEIGHT),
            1
        )
    
    for y in range(ocean_height, THUMBNAIL_HEIGHT, 20):
        pygame.draw.line(
            surface,
            (*colors['secondary'], 50),
            (0, y),
            (THUMBNAIL_WIDTH, y),
            1
        )
    
    # Draw surfer
    surfer_x = THUMBNAIL_WIDTH // 3
    surfer_y = ocean_height - 10
    
    # Draw surfboard
    pygame.draw.ellipse(
        surface,
        (200, 100, 0),
        pygame.Rect(surfer_x - 30, surfer_y, 60, 15)
    )
    
    # Draw surfer body
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        pygame.Rect(surfer_x - 5, surfer_y - 30, 10, 30),
        0,
        border_radius=3
    )
    
    # Draw surfer head
    pygame.draw.circle(
        surface,
        (255, 200, 150),
        (surfer_x, surfer_y - 35),
        8
    )
    
    # Draw surfer arms
    pygame.draw.line(
        surface,
        (0, 0, 0),
        (surfer_x, surfer_y - 25),
        (surfer_x + 15, surfer_y - 15),
        3
    )
    pygame.draw.line(
        surface,
        (0, 0, 0),
        (surfer_x, surfer_y - 20),
        (surfer_x - 15, surfer_y - 10),
        3
    )
    
    # Draw digital effects
    for _ in range(30):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(ocean_height, THUMBNAIL_HEIGHT)
        size = random.randint(1, 3)
        
        pygame.draw.circle(
            surface,
            colors['secondary'],
            (x, y),
            size
        )
    
    # Draw splash effect
    splash_points = []
    for i in range(10):
        angle = math.pi / 2 - math.pi / 4 + i * math.pi / 20
        length = random.randint(10, 20)
        x = surfer_x - 20 + int(math.cos(angle) * length)
        y = surfer_y + int(math.sin(angle) * length)
        splash_points.append((x, y))
    
    pygame.draw.lines(
        surface,
        colors['accent'],
        False,
        splash_points,
        2
    )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("CYBER SURFING", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface

def main():
    """Generate all thumbnails."""
    # Create thumbnails
    thumbnails = {
        'cyber_soccer': generate_cyber_soccer_thumbnail(),
        'extreme_racing': generate_extreme_racing_thumbnail(),
        'space_basketball': generate_space_basketball_thumbnail(),
        'virtual_tennis': generate_virtual_tennis_thumbnail(),
        'mech_boxing': generate_mech_boxing_thumbnail(),
        'cyber_surfing': generate_cyber_surfing_thumbnail()
    }
    
    # Save thumbnails
    for game_id, surface in thumbnails.items():
        output_path = os.path.join(OUTPUT_DIR, f"{game_id}.png")
        pygame.image.save(surface, output_path)
        print(f"Generated thumbnail for {game_id}: {output_path}")

if __name__ == "__main__":
    main()
    pygame.quit()
