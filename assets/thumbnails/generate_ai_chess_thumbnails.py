"""
Generate AI Chess-themed thumbnail images for SoulCoreLegacy Arcade.
This script creates visually distinct thumbnails for AI Chess game variants.
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

# Define colors for AI Chess games
COLORS = {
    'ai_chess_partner': {  # AI as your partner
        'bg': (0, 20, 40),  # Dark blue
        'primary': (0, 80, 150),  # Blue
        'secondary': (0, 120, 200),  # Light blue
        'accent': (0, 255, 255),  # Cyan
    },
    'ai_chess_mentor': {  # AI as mentor/guide
        'bg': (0, 30, 20),  # Dark green
        'primary': (0, 100, 50),  # Green
        'secondary': (0, 150, 80),  # Light green
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

def generate_ai_chess_partner_thumbnail():
    """Generate a thumbnail for AI Chess Partner game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['ai_chess_partner']
    
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
    
    # Draw digital circuit patterns
    for i in range(10):
        start_x = random.randint(0, THUMBNAIL_WIDTH)
        start_y = random.randint(0, THUMBNAIL_HEIGHT)
        
        # Draw circuit line
        line_length = random.randint(20, 50)
        direction = random.choice(["horizontal", "vertical"])
        
        if direction == "horizontal":
            end_x = start_x + line_length
            end_y = start_y
        else:
            end_x = start_x
            end_y = start_y + line_length
        
        pygame.draw.line(
            surface,
            (*colors['secondary'], 50),
            (start_x, start_y),
            (end_x, end_y),
            1
        )
        
        # Draw circuit node
        pygame.draw.circle(
            surface,
            (*colors['secondary'], 100),
            (start_x, start_y),
            3
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
    
    # Mid-game position
    pieces = [
        {'type': 'king', 'row': 7, 'col': 6, 'color': 'white'},
        {'type': 'queen', 'row': 5, 'col': 3, 'color': 'white'},
        {'type': 'rook', 'row': 7, 'col': 0, 'color': 'white'},
        {'type': 'bishop', 'row': 4, 'col': 2, 'color': 'white'},
        {'type': 'knight', 'row': 5, 'col': 5, 'color': 'white'},
        {'type': 'pawn', 'row': 6, 'col': 0, 'color': 'white'},
        {'type': 'pawn', 'row': 6, 'col': 7, 'color': 'white'},
        {'type': 'pawn', 'row': 5, 'col': 1, 'color': 'white'},
        
        {'type': 'king', 'row': 0, 'col': 6, 'color': 'black'},
        {'type': 'queen', 'row': 2, 'col': 7, 'color': 'black'},
        {'type': 'rook', 'row': 0, 'col': 0, 'color': 'black'},
        {'type': 'bishop', 'row': 2, 'col': 5, 'color': 'black'},
        {'type': 'knight', 'row': 3, 'col': 2, 'color': 'black'},
        {'type': 'pawn', 'row': 1, 'col': 0, 'color': 'black'},
        {'type': 'pawn', 'row': 3, 'col': 3, 'color': 'black'},
        {'type': 'pawn', 'row': 1, 'col': 7, 'color': 'black'}
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
    
    # Draw player avatar
    player_x = 50
    player_y = 50
    avatar_size = 40
    
    # Avatar circle
    pygame.draw.circle(
        surface,
        (200, 200, 200),  # Light gray
        (player_x, player_y),
        avatar_size // 2
    )
    
    # Avatar border
    pygame.draw.circle(
        surface,
        (255, 255, 255),
        (player_x, player_y),
        avatar_size // 2,
        2
    )
    
    # Simple face
    eye_offset = 5
    pygame.draw.circle(
        surface,
        (0, 0, 0),
        (player_x - eye_offset, player_y - 5),
        3
    )
    pygame.draw.circle(
        surface,
        (0, 0, 0),
        (player_x + eye_offset, player_y - 5),
        3
    )
    
    pygame.draw.arc(
        surface,
        (0, 0, 0),
        pygame.Rect(player_x - 10, player_y, 20, 10),
        0, math.pi,
        2
    )
    
    # Draw AI avatar
    ai_x = THUMBNAIL_WIDTH - 50
    ai_y = 50
    
    # AI circle
    pygame.draw.circle(
        surface,
        colors['primary'],
        (ai_x, ai_y),
        avatar_size // 2
    )
    
    # AI border
    pygame.draw.circle(
        surface,
        colors['accent'],
        (ai_x, ai_y),
        avatar_size // 2,
        2
    )
    
    # AI face (more digital)
    # Eyes
    pygame.draw.rect(
        surface,
        colors['accent'],
        pygame.Rect(ai_x - 10, ai_y - 10, 5, 5)
    )
    pygame.draw.rect(
        surface,
        colors['accent'],
        pygame.Rect(ai_x + 5, ai_y - 10, 5, 5)
    )
    
    # Mouth
    for i in range(3):
        pygame.draw.rect(
            surface,
            colors['accent'],
            pygame.Rect(ai_x - 10 + i * 7, ai_y + 5, 5, 2)
        )
    
    # Draw connection between player and AI
    pygame.draw.line(
        surface,
        colors['accent'],
        (player_x + avatar_size // 2, player_y),
        (ai_x - avatar_size // 2, ai_y),
        2
    )
    
    # Draw "TEAM" text in the middle of the connection
    font = pygame.font.SysFont("Arial", 14, bold=True)
    team_text = font.render("TEAM", True, colors['accent'])
    team_rect = team_text.get_rect(center=((player_x + ai_x) // 2, (player_y + ai_y) // 2 - 10))
    surface.blit(team_text, team_rect)
    
    # Draw move suggestion
    suggestion_square_col = 5
    suggestion_square_row = 4
    suggestion_square_x = board_x + suggestion_square_col * square_size
    suggestion_square_y = board_y + suggestion_square_row * square_size
    
    # Highlight suggested move
    pygame.draw.rect(
        surface,
        (*colors['accent'], 150),
        pygame.Rect(suggestion_square_x, suggestion_square_y, square_size, square_size),
        0
    )
    
    # Draw suggestion arrow
    start_x = board_x + 3 * square_size + square_size // 2
    start_y = board_y + 5 * square_size + square_size // 2
    end_x = suggestion_square_x + square_size // 2
    end_y = suggestion_square_y + square_size // 2
    
    pygame.draw.line(
        surface,
        colors['accent'],
        (start_x, start_y),
        (end_x, end_y),
        2
    )
    
    # Draw arrowhead
    arrow_size = 8
    angle = math.atan2(end_y - start_y, end_x - start_x)
    pygame.draw.polygon(
        surface,
        colors['accent'],
        [
            (end_x, end_y),
            (end_x - arrow_size * math.cos(angle - math.pi/6), end_y - arrow_size * math.sin(angle - math.pi/6)),
            (end_x - arrow_size * math.cos(angle + math.pi/6), end_y - arrow_size * math.sin(angle + math.pi/6))
        ]
    )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("AI CHESS PARTNER", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT - 20))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_ai_chess_mentor_thumbnail():
    """Generate a thumbnail for AI Chess Mentor game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['ai_chess_mentor']
    
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
    
    # Draw digital brain patterns
    for i in range(5):
        center_x = random.randint(0, THUMBNAIL_WIDTH)
        center_y = random.randint(0, THUMBNAIL_HEIGHT)
        size = random.randint(10, 30)
        
        # Draw neural network node
        pygame.draw.circle(
            surface,
            (*colors['secondary'], 50),
            (center_x, center_y),
            size,
            1
        )
        
        # Draw connections
        for j in range(3):
            end_x = center_x + random.randint(-50, 50)
            end_y = center_y + random.randint(-50, 50)
            
            pygame.draw.line(
                surface,
                (*colors['secondary'], 30),
                (center_x, center_y),
                (end_x, end_y),
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
        (240, 240, 240),  # Light squares
        (100, 100, 100),  # Dark squares
        colors['accent']  # Border
    )
    
    # Draw some chess pieces
    square_size = board_size // 8
    
    # Mid-game position
    pieces = [
        {'type': 'king', 'row': 7, 'col': 7, 'color': 'white'},
        {'type': 'queen', 'row': 7, 'col': 3, 'color': 'white'},
        {'type': 'rook', 'row': 7, 'col': 0, 'color': 'white'},
        {'type': 'bishop', 'row': 7, 'col': 2, 'color': 'white'},
        {'type': 'knight', 'row': 7, 'col': 1, 'color': 'white'},
        {'type': 'pawn', 'row': 6, 'col': 0, 'color': 'white'},
        {'type': 'pawn', 'row': 6, 'col': 1, 'color': 'white'},
        {'type': 'pawn', 'row': 4, 'col': 3, 'color': 'white'},
        
        {'type': 'king', 'row': 0, 'col': 7, 'color': 'black'},
        {'type': 'queen', 'row': 0, 'col': 3, 'color': 'black'},
        {'type': 'rook', 'row': 0, 'col': 0, 'color': 'black'},
        {'type': 'bishop', 'row': 0, 'col': 2, 'color': 'black'},
        {'type': 'knight', 'row': 0, 'col': 1, 'color': 'black'},
        {'type': 'pawn', 'row': 1, 'col': 0, 'color': 'black'},
        {'type': 'pawn', 'row': 1, 'col': 1, 'color': 'black'},
        {'type': 'pawn', 'row': 3, 'col': 2, 'color': 'black'}
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
    
    # Draw multiple move suggestions
    suggestions = [
        {'from_col': 3, 'from_row': 4, 'to_col': 3, 'to_row': 3, 'quality': 'good'},
        {'from_col': 3, 'from_row': 4, 'to_col': 2, 'to_row': 3, 'quality': 'better'},
        {'from_col': 3, 'from_row': 4, 'to_col': 4, 'to_row': 3, 'quality': 'best'}
    ]
    
    suggestion_colors = {
        'good': (0, 150, 0),      # Green
        'better': (0, 200, 0),    # Brighter green
        'best': (0, 255, 0)       # Brightest green
    }
    
    for suggestion in suggestions:
        from_x = board_x + suggestion['from_col'] * square_size + square_size // 2
        from_y = board_y + suggestion['from_row'] * square_size + square_size // 2
        to_x = board_x + suggestion['to_col'] * square_size + square_size // 2
        to_y = board_y + suggestion['to_row'] * square_size + square_size // 2
        
        # Highlight destination square
        pygame.draw.rect(
            surface,
            (*suggestion_colors[suggestion['quality']], 100),
            pygame.Rect(
                board_x + suggestion['to_col'] * square_size,
                board_y + suggestion['to_row'] * square_size,
                square_size,
                square_size
            ),
            0
        )
        
        # Draw arrow
        pygame.draw.line(
            surface,
            suggestion_colors[suggestion['quality']],
            (from_x, from_y),
            (to_x, to_y),
            2
        )
        
        # Draw arrowhead
        arrow_size = 8
        angle = math.atan2(to_y - from_y, to_x - from_x)
        pygame.draw.polygon(
            surface,
            suggestion_colors[suggestion['quality']],
            [
                (to_x, to_y),
                (to_x - arrow_size * math.cos(angle - math.pi/6), to_y - arrow_size * math.sin(angle - math.pi/6)),
                (to_x - arrow_size * math.cos(angle + math.pi/6), to_y - arrow_size * math.sin(angle + math.pi/6))
            ]
        )
    
    # Draw AI mentor
    ai_x = THUMBNAIL_WIDTH - 50
    ai_y = 50
    avatar_size = 40
    
    # AI circle
    pygame.draw.circle(
        surface,
        colors['primary'],
        (ai_x, ai_y),
        avatar_size // 2
    )
    
    # AI border
    pygame.draw.circle(
        surface,
        colors['accent'],
        (ai_x, ai_y),
        avatar_size // 2,
        2
    )
    
    # AI face (more digital)
    # Eyes
    pygame.draw.rect(
        surface,
        colors['accent'],
        pygame.Rect(ai_x - 10, ai_y - 10, 5, 5)
    )
    pygame.draw.rect(
        surface,
        colors['accent'],
        pygame.Rect(ai_x + 5, ai_y - 10, 5, 5)
    )
    
    # Mouth
    for i in range(3):
        pygame.draw.rect(
            surface,
            colors['accent'],
            pygame.Rect(ai_x - 10 + i * 7, ai_y + 5, 5, 2)
        )
    
    # Draw speech bubble
    bubble_width = 100
    bubble_height = 50
    bubble_x = ai_x - bubble_width
    bubble_y = ai_y - bubble_height // 2
    
    # Bubble background
    pygame.draw.rect(
        surface,
        (255, 255, 255, 200),
        pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height),
        0,
        border_radius=10
    )
    
    # Bubble border
    pygame.draw.rect(
        surface,
        colors['primary'],
        pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height),
        2,
        border_radius=10
    )
    
    # Bubble pointer
    pygame.draw.polygon(
        surface,
        (255, 255, 255, 200),
        [
            (bubble_x + bubble_width, bubble_y + bubble_height // 2),
            (bubble_x + bubble_width + 10, bubble_y + bubble_height // 2 - 10),
            (bubble_x + bubble_width + 10, bubble_y + bubble_height // 2 + 10)
        ]
    )
    
    pygame.draw.line(
        surface,
        colors['primary'],
        (bubble_x + bubble_width, bubble_y + bubble_height // 2 - 10),
        (bubble_x + bubble_width + 10, bubble_y + bubble_height // 2 - 10),
        2
    )
    
    pygame.draw.line(
        surface,
        colors['primary'],
        (bubble_x + bubble_width + 10, bubble_y + bubble_height // 2 - 10),
        (bubble_x + bubble_width + 10, bubble_y + bubble_height // 2 + 10),
        2
    )
    
    pygame.draw.line(
        surface,
        colors['primary'],
        (bubble_x + bubble_width + 10, bubble_y + bubble_height // 2 + 10),
        (bubble_x + bubble_width, bubble_y + bubble_height // 2 + 10),
        2
    )
    
    # Bubble text
    font = pygame.font.SysFont("Arial", 10)
    text1 = font.render("Consider these moves:", True, (0, 0, 0))
    text2 = font.render("The rightmost option gives", True, (0, 0, 0))
    text3 = font.render("you a strong position.", True, (0, 0, 0))
    
    surface.blit(text1, (bubble_x + 10, bubble_y + 10))
    surface.blit(text2, (bubble_x + 10, bubble_y + 25))
    surface.blit(text3, (bubble_x + 10, bubble_y + 40))
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("AI CHESS MENTOR", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT - 20))
    surface.blit(title_text, title_rect)
    
    return surface

def main():
    """Generate all thumbnails."""
    # Create thumbnails
    thumbnails = {
        'ai_chess_partner': generate_ai_chess_partner_thumbnail(),
        'ai_chess_mentor': generate_ai_chess_mentor_thumbnail()
    }
    
    # Save thumbnails
    for game_id, surface in thumbnails.items():
        output_path = os.path.join(OUTPUT_DIR, f"{game_id}.png")
        pygame.image.save(surface, output_path)
        print(f"Generated thumbnail for {game_id}: {output_path}")

if __name__ == "__main__":
    main()
    pygame.quit()
