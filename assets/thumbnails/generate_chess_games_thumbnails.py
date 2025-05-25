"""
Generate Chess-themed thumbnail images for SoulCoreLegacy Arcade.
This script creates visually distinct thumbnails for Chess game variants.
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

# Define colors for Chess games
COLORS = {
    'quantum_chess': {  # Solo chess with timer
        'bg': (20, 0, 40),  # Dark purple
        'primary': (100, 0, 150),  # Purple
        'secondary': (150, 100, 255),  # Light purple
        'accent': (255, 200, 0),  # Gold
    },
    'zen_chess': {  # Solo chess without timer
        'bg': (0, 30, 40),  # Dark teal
        'primary': (0, 100, 120),  # Teal
        'secondary': (0, 150, 180),  # Light teal
        'accent': (255, 255, 255),  # White
    },
    'team_chess_arena': {  # 2v2 team chess
        'bg': (30, 0, 0),  # Dark red
        'primary': (150, 0, 0),  # Red
        'secondary': (200, 0, 0),  # Light red
        'accent': (255, 255, 0),  # Yellow
    }
}

def draw_chess_board(surface, x, y, size, light_color, dark_color, border_color=None):
    """Draw a chess board on the surface."""
    square_size = size // 8
    
    # Draw border if color is provided
    if border_color:
        pygame.draw.rect(
            surface,
            border_color,
            pygame.Rect(x - 2, y - 2, size + 4, size + 4),
            2
        )
    
    # Draw squares
    for row in range(8):
        for col in range(8):
            square_x = x + col * square_size
            square_y = y + row * square_size
            color = light_color if (row + col) % 2 == 0 else dark_color
            
            pygame.draw.rect(
                surface,
                color,
                pygame.Rect(square_x, square_y, square_size, square_size)
            )

def draw_chess_piece(surface, piece_type, x, y, size, color):
    """Draw a chess piece on the surface."""
    # Map piece types to Unicode chess symbols
    piece_symbols = {
        'king': '♔' if color == 'white' else '♚',
        'queen': '♕' if color == 'white' else '♛',
        'rook': '♖' if color == 'white' else '♜',
        'bishop': '♗' if color == 'white' else '♝',
        'knight': '♘' if color == 'white' else '♞',
        'pawn': '♙' if color == 'white' else '♟'
    }
    
    # Get the symbol for the piece
    symbol = piece_symbols.get(piece_type, '?')
    
    # Create font and render text
    font_size = int(size * 0.8)
    font = pygame.font.SysFont("Arial", font_size, bold=True)
    text_color = (255, 255, 255) if color == 'white' else (0, 0, 0)
    text = font.render(symbol, True, text_color)
    
    # Center the text on the square
    text_rect = text.get_rect(center=(x, y))
    surface.blit(text, text_rect)

def generate_quantum_chess_thumbnail():
    """Generate a thumbnail for Quantum Chess (Solo chess with timer) game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['quantum_chess']
    
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
    
    # Draw chess board
    board_size = 120
    board_x = (THUMBNAIL_WIDTH - board_size) // 2
    board_y = (THUMBNAIL_HEIGHT - board_size) // 2
    
    draw_chess_board(
        surface,
        board_x,
        board_y,
        board_size,
        (240, 240, 240),  # Light squares
        (100, 100, 100),  # Dark squares
        colors['accent']  # Border
    )
    
    # Draw some chess pieces
    square_size = board_size // 8
    
    # White pieces
    pieces = [
        {'type': 'king', 'row': 7, 'col': 4, 'color': 'white'},
        {'type': 'queen', 'row': 7, 'col': 3, 'color': 'white'},
        {'type': 'rook', 'row': 7, 'col': 0, 'color': 'white'},
        {'type': 'rook', 'row': 7, 'col': 7, 'color': 'white'},
        {'type': 'bishop', 'row': 7, 'col': 2, 'color': 'white'},
        {'type': 'bishop', 'row': 7, 'col': 5, 'color': 'white'},
        {'type': 'knight', 'row': 7, 'col': 1, 'color': 'white'},
        {'type': 'knight', 'row': 7, 'col': 6, 'color': 'white'},
        {'type': 'pawn', 'row': 6, 'col': 0, 'color': 'white'},
        {'type': 'pawn', 'row': 6, 'col': 1, 'color': 'white'},
        {'type': 'pawn', 'row': 6, 'col': 2, 'color': 'white'},
        {'type': 'pawn', 'row': 6, 'col': 3, 'color': 'white'},
        {'type': 'pawn', 'row': 6, 'col': 4, 'color': 'white'},
        {'type': 'pawn', 'row': 6, 'col': 5, 'color': 'white'},
        {'type': 'pawn', 'row': 6, 'col': 6, 'color': 'white'},
        {'type': 'pawn', 'row': 6, 'col': 7, 'color': 'white'},
    ]
    
    # Black pieces
    pieces += [
        {'type': 'king', 'row': 0, 'col': 4, 'color': 'black'},
        {'type': 'queen', 'row': 0, 'col': 3, 'color': 'black'},
        {'type': 'rook', 'row': 0, 'col': 0, 'color': 'black'},
        {'type': 'rook', 'row': 0, 'col': 7, 'color': 'black'},
        {'type': 'bishop', 'row': 0, 'col': 2, 'color': 'black'},
        {'type': 'bishop', 'row': 0, 'col': 5, 'color': 'black'},
        {'type': 'knight', 'row': 0, 'col': 1, 'color': 'black'},
        {'type': 'knight', 'row': 0, 'col': 6, 'color': 'black'},
        {'type': 'pawn', 'row': 1, 'col': 0, 'color': 'black'},
        {'type': 'pawn', 'row': 1, 'col': 1, 'color': 'black'},
        {'type': 'pawn', 'row': 1, 'col': 2, 'color': 'black'},
        {'type': 'pawn', 'row': 1, 'col': 3, 'color': 'black'},
        {'type': 'pawn', 'row': 1, 'col': 4, 'color': 'black'},
        {'type': 'pawn', 'row': 1, 'col': 5, 'color': 'black'},
        {'type': 'pawn', 'row': 1, 'col': 6, 'color': 'black'},
        {'type': 'pawn', 'row': 1, 'col': 7, 'color': 'black'},
    ]
    
    # Draw only some pieces to avoid clutter
    selected_pieces = random.sample(pieces, 10)
    
    for piece in selected_pieces:
        piece_x = board_x + piece['col'] * square_size + square_size // 2
        piece_y = board_y + piece['row'] * square_size + square_size // 2
        
        draw_chess_piece(
            surface,
            piece['type'],
            piece_x,
            piece_y,
            square_size,
            piece['color']
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
    
    # Draw timer
    timer_rect = pygame.Rect(THUMBNAIL_WIDTH - 80, 20, 60, 30)
    pygame.draw.rect(
        surface,
        (0, 0, 0, 150),
        timer_rect,
        0,
        border_radius=5
    )
    pygame.draw.rect(
        surface,
        colors['accent'],
        timer_rect,
        1,
        border_radius=5
    )
    
    # Timer text
    font = pygame.font.SysFont("Arial", 16, bold=True)
    timer_text = font.render("05:00", True, colors['accent'])
    timer_rect = timer_text.get_rect(center=(THUMBNAIL_WIDTH - 50, 35))
    surface.blit(timer_text, timer_rect)
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("QUANTUM CHESS", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    # Draw subtitle
    font = pygame.font.SysFont("Arial", 14)
    subtitle_text = font.render("TIMED SOLO CHALLENGE", True, (200, 200, 200))
    subtitle_rect = subtitle_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 45))
    surface.blit(subtitle_text, subtitle_rect)
    
    return surface

def generate_zen_chess_thumbnail():
    """Generate a thumbnail for Zen Chess (Solo chess without timer) game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['zen_chess']
    
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
    
    # Draw zen-like circles
    for i in range(5):
        radius = 100 + i * 20
        pygame.draw.circle(
            surface,
            (*colors['secondary'], 20),
            (THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT // 2),
            radius,
            1
        )
    
    # Draw chess board
    board_size = 120
    board_x = (THUMBNAIL_WIDTH - board_size) // 2
    board_y = (THUMBNAIL_HEIGHT - board_size) // 2
    
    draw_chess_board(
        surface,
        board_x,
        board_y,
        board_size,
        (220, 220, 220),  # Light squares (slightly darker for zen feel)
        (80, 80, 80),     # Dark squares
        colors['accent']  # Border
    )
    
    # Draw fewer chess pieces for a minimalist feel
    square_size = board_size // 8
    
    # Just a few key pieces
    pieces = [
        {'type': 'king', 'row': 7, 'col': 4, 'color': 'white'},
        {'type': 'queen', 'row': 0, 'col': 3, 'color': 'black'},
        {'type': 'knight', 'row': 5, 'col': 2, 'color': 'white'},
        {'type': 'bishop', 'row': 2, 'col': 5, 'color': 'black'},
        {'type': 'pawn', 'row': 3, 'col': 4, 'color': 'white'},
        {'type': 'pawn', 'row': 4, 'col': 3, 'color': 'black'}
    ]
    
    for piece in pieces:
        piece_x = board_x + piece['col'] * square_size + square_size // 2
        piece_y = board_y + piece['row'] * square_size + square_size // 2
        
        draw_chess_piece(
            surface,
            piece['type'],
            piece_x,
            piece_y,
            square_size,
            piece['color']
        )
    
    # Draw zen elements
    # Bamboo
    bamboo_x = 50
    bamboo_y = 100
    bamboo_width = 10
    bamboo_height = 80
    
    pygame.draw.rect(
        surface,
        (0, 100, 0),  # Green
        pygame.Rect(bamboo_x - bamboo_width // 2, bamboo_y, bamboo_width, bamboo_height)
    )
    
    # Bamboo segments
    for i in range(1, 4):
        segment_y = bamboo_y + i * bamboo_height // 4
        pygame.draw.line(
            surface,
            (0, 50, 0),  # Darker green
            (bamboo_x - bamboo_width // 2, segment_y),
            (bamboo_x + bamboo_width // 2, segment_y),
            2
        )
    
    # Stone
    stone_x = THUMBNAIL_WIDTH - 60
    stone_y = 120
    stone_radius = 15
    
    pygame.draw.circle(
        surface,
        (150, 150, 150),  # Gray
        (stone_x, stone_y),
        stone_radius
    )
    
    # Stone texture
    for i in range(3):
        pygame.draw.circle(
            surface,
            (170, 170, 170),  # Lighter gray
            (stone_x - 5 + i * 5, stone_y - 5 + i * 3),
            2
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("ZEN CHESS", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    # Draw subtitle
    font = pygame.font.SysFont("Arial", 14)
    subtitle_text = font.render("UNTIMED MEDITATION", True, (200, 200, 200))
    subtitle_rect = subtitle_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 45))
    surface.blit(subtitle_text, subtitle_rect)
    
    # Draw zen quote
    font = pygame.font.SysFont("Arial", 12, italic=True)
    quote_text = font.render('"The journey of a thousand moves begins with a single pawn"', True, (180, 180, 180))
    quote_rect = quote_text.get_rect(center=(THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT - 20))
    surface.blit(quote_text, quote_rect)
    
    return surface

def generate_team_chess_arena_thumbnail():
    """Generate a thumbnail for Team Chess Arena (2v2 team chess) game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['team_chess_arena']
    
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
    
    # Draw arena-like elements
    # Arena circle
    pygame.draw.circle(
        surface,
        (*colors['primary'], 50),
        (THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT // 2),
        100,
        2
    )
    
    # Arena spotlights
    for angle in [30, 150, 270]:
        rad_angle = math.radians(angle)
        start_x = THUMBNAIL_WIDTH // 2 + int(120 * math.cos(rad_angle))
        start_y = THUMBNAIL_HEIGHT // 2 + int(120 * math.sin(rad_angle))
        end_x = THUMBNAIL_WIDTH // 2 + int(80 * math.cos(rad_angle))
        end_y = THUMBNAIL_HEIGHT // 2 + int(80 * math.sin(rad_angle))
        
        pygame.draw.line(
            surface,
            (*colors['accent'], 100),
            (start_x, start_y),
            (end_x, end_y),
            5
        )
    
    # Draw two chess boards side by side
    board_size = 80
    spacing = 20
    
    # Left board
    left_board_x = THUMBNAIL_WIDTH // 2 - board_size - spacing // 2
    left_board_y = THUMBNAIL_HEIGHT // 2 - board_size // 2
    
    draw_chess_board(
        surface,
        left_board_x,
        left_board_y,
        board_size,
        (240, 240, 240),  # Light squares
        (100, 100, 100),  # Dark squares
        (0, 0, 200)       # Blue border for team 1
    )
    
    # Right board
    right_board_x = THUMBNAIL_WIDTH // 2 + spacing // 2
    right_board_y = THUMBNAIL_HEIGHT // 2 - board_size // 2
    
    draw_chess_board(
        surface,
        right_board_x,
        right_board_y,
        board_size,
        (240, 240, 240),  # Light squares
        (100, 100, 100),  # Dark squares
        (200, 0, 0)       # Red border for team 2
    )
    
    # Draw some chess pieces on both boards
    square_size = board_size // 8
    
    # Left board pieces
    left_pieces = [
        {'type': 'king', 'row': 7, 'col': 4, 'color': 'white'},
        {'type': 'queen', 'row': 7, 'col': 3, 'color': 'white'},
        {'type': 'rook', 'row': 7, 'col': 0, 'color': 'white'},
        {'type': 'bishop', 'row': 7, 'col': 2, 'color': 'white'},
        {'type': 'king', 'row': 0, 'col': 4, 'color': 'black'},
        {'type': 'queen', 'row': 0, 'col': 3, 'color': 'black'},
        {'type': 'pawn', 'row': 6, 'col': 3, 'color': 'white'},
        {'type': 'pawn', 'row': 1, 'col': 4, 'color': 'black'}
    ]
    
    for piece in left_pieces:
        piece_x = left_board_x + piece['col'] * square_size + square_size // 2
        piece_y = left_board_y + piece['row'] * square_size + square_size // 2
        
        draw_chess_piece(
            surface,
            piece['type'],
            piece_x,
            piece_y,
            square_size,
            piece['color']
        )
    
    # Right board pieces
    right_pieces = [
        {'type': 'king', 'row': 7, 'col': 4, 'color': 'white'},
        {'type': 'queen', 'row': 7, 'col': 3, 'color': 'white'},
        {'type': 'knight', 'row': 7, 'col': 1, 'color': 'white'},
        {'type': 'bishop', 'row': 7, 'col': 5, 'color': 'white'},
        {'type': 'king', 'row': 0, 'col': 4, 'color': 'black'},
        {'type': 'queen', 'row': 0, 'col': 3, 'color': 'black'},
        {'type': 'pawn', 'row': 6, 'col': 2, 'color': 'white'},
        {'type': 'pawn', 'row': 1, 'col': 5, 'color': 'black'}
    ]
    
    for piece in right_pieces:
        piece_x = right_board_x + piece['col'] * square_size + square_size // 2
        piece_y = right_board_y + piece['row'] * square_size + square_size // 2
        
        draw_chess_piece(
            surface,
            piece['type'],
            piece_x,
            piece_y,
            square_size,
            piece['color']
        )
    
    # Draw player avatars
    avatar_size = 30
    avatar_positions = [
        (left_board_x - avatar_size - 5, left_board_y),  # Team 1, Player 1
        (left_board_x - avatar_size - 5, left_board_y + board_size - avatar_size),  # Team 1, Player 2
        (right_board_x + board_size + 5, right_board_y),  # Team 2, Player 1
        (right_board_x + board_size + 5, right_board_y + board_size - avatar_size)  # Team 2, Player 2
    ]
    
    avatar_colors = [
        (0, 0, 200),  # Blue (Team 1)
        (0, 0, 150),  # Darker Blue (Team 1)
        (200, 0, 0),  # Red (Team 2)
        (150, 0, 0)   # Darker Red (Team 2)
    ]
    
    for (x, y), color in zip(avatar_positions, avatar_colors):
        # Draw avatar circle
        pygame.draw.circle(
            surface,
            color,
            (x + avatar_size // 2, y + avatar_size // 2),
            avatar_size // 2
        )
        
        # Draw avatar border
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (x + avatar_size // 2, y + avatar_size // 2),
            avatar_size // 2,
            2
        )
        
        # Draw simple face
        eye_offset = 5
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (x + avatar_size // 2 - eye_offset, y + avatar_size // 2 - 2),
            3
        )
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (x + avatar_size // 2 + eye_offset, y + avatar_size // 2 - 2),
            3
        )
        
        pygame.draw.arc(
            surface,
            (255, 255, 255),
            pygame.Rect(x + avatar_size // 4, y + avatar_size // 2, avatar_size // 2, avatar_size // 4),
            0, math.pi,
            2
        )
    
    # Draw team score
    score_rect = pygame.Rect(THUMBNAIL_WIDTH // 2 - 40, 20, 80, 30)
    pygame.draw.rect(
        surface,
        (0, 0, 0, 150),
        score_rect,
        0,
        border_radius=5
    )
    pygame.draw.rect(
        surface,
        colors['accent'],
        score_rect,
        1,
        border_radius=5
    )
    
    # Score text
    font = pygame.font.SysFont("Arial", 16, bold=True)
    score_text = font.render("2 - 1", True, colors['accent'])
    score_rect = score_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 35))
    surface.blit(score_text, score_rect)
    
    # Draw team indicators
    team1_rect = pygame.Rect(score_rect.left - 50, score_rect.top, 40, 30)
    pygame.draw.rect(
        surface,
        (0, 0, 200),  # Blue
        team1_rect,
        0,
        border_radius=5
    )
    
    team2_rect = pygame.Rect(score_rect.right + 10, score_rect.top, 40, 30)
    pygame.draw.rect(
        surface,
        (200, 0, 0),  # Red
        team2_rect,
        0,
        border_radius=5
    )
    
    # Team text
    font = pygame.font.SysFont("Arial", 12, bold=True)
    team1_text = font.render("TEAM 1", True, (255, 255, 255))
    team1_rect = team1_text.get_rect(center=(team1_rect.centerx, team1_rect.centery))
    surface.blit(team1_text, team1_rect)
    
    team2_text = font.render("TEAM 2", True, (255, 255, 255))
    team2_rect = team2_text.get_rect(center=(team2_rect.centerx, team2_rect.centery))
    surface.blit(team2_text, team2_rect)
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("TEAM CHESS ARENA", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT - 20))
    surface.blit(title_text, title_rect)
    
    return surface

def main():
    """Generate all thumbnails."""
    # Create thumbnails
    thumbnails = {
        'quantum_chess': generate_quantum_chess_thumbnail(),
        'zen_chess': generate_zen_chess_thumbnail(),
        'team_chess_arena': generate_team_chess_arena_thumbnail()
    }
    
    # Save thumbnails
    for game_id, surface in thumbnails.items():
        output_path = os.path.join(OUTPUT_DIR, f"{game_id}.png")
        pygame.image.save(surface, output_path)
        print(f"Generated thumbnail for {game_id}: {output_path}")

if __name__ == "__main__":
    main()
    pygame.quit()
