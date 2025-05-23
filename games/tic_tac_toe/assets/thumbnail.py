"""
SoulCoreLegacy Arcade - Tic-Tac-Toe Thumbnail Generator
----------------------------------------------------
This script generates a thumbnail for the Tic-Tac-Toe game.
"""

import pygame
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.config import PRIMARY_COLOR, SECONDARY_COLOR, WHITE

def generate_thumbnail():
    """Generate a thumbnail for the Tic-Tac-Toe game."""
    # Create a surface
    width, height = 200, 150
    surface = pygame.Surface((width, height))
    
    # Fill the background with a gradient
    for y in range(height):
        # Calculate the ratio of the current position
        ratio = y / height
        
        # Interpolate between the two colors
        r = int(30 * (1 - ratio) + 50 * ratio)
        g = int(30 * (1 - ratio) + 50 * ratio)
        b = int(50 * (1 - ratio) + 80 * ratio)
        
        # Draw a horizontal line with the calculated color
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    
    # Draw the grid
    grid_color = (100, 100, 100)
    cell_size = 40
    board_size = 3
    board_width = board_size * cell_size
    board_height = board_size * cell_size
    board_x = (width - board_width) // 2
    board_y = (height - board_height) // 2
    
    for i in range(1, board_size):
        # Vertical lines
        pygame.draw.line(
            surface,
            grid_color,
            (board_x + i * cell_size, board_y),
            (board_x + i * cell_size, board_y + board_height),
            3
        )
        
        # Horizontal lines
        pygame.draw.line(
            surface,
            grid_color,
            (board_x, board_y + i * cell_size),
            (board_x + board_width, board_y + board_height),
            3
        )
    
    # Draw some X's and O's
    # X in top-left
    draw_x(surface, board_x + cell_size // 2, board_y + cell_size // 2, cell_size, PRIMARY_COLOR)
    
    # O in center
    draw_o(surface, board_x + cell_size * 1.5, board_y + cell_size * 1.5, cell_size, SECONDARY_COLOR)
    
    # X in bottom-right
    draw_x(surface, board_x + cell_size * 2.5, board_y + cell_size * 2.5, cell_size, PRIMARY_COLOR)
    
    # Draw the game title
    font = pygame.font.SysFont("Arial", 18)
    title_text = font.render("Tic-Tac-Toe", True, WHITE)
    title_rect = title_text.get_rect(center=(width // 2, 20))
    surface.blit(title_text, title_rect)
    
    # Draw a border
    pygame.draw.rect(
        surface,
        WHITE,
        pygame.Rect(0, 0, width, height),
        2
    )
    
    # Save the thumbnail
    pygame.image.save(surface, os.path.join(os.path.dirname(__file__), "thumbnail.png"))
    
    print("Tic-Tac-Toe thumbnail generated successfully.")

def draw_x(surface, x, y, cell_size, color):
    """Draw an X at the specified position."""
    size = cell_size // 2 - 10
    pygame.draw.line(surface, color, (x - size, y - size), (x + size, y + size), 5)
    pygame.draw.line(surface, color, (x + size, y - size), (x - size, y + size), 5)

def draw_o(surface, x, y, cell_size, color):
    """Draw an O at the specified position."""
    size = cell_size // 2 - 10
    pygame.draw.circle(surface, color, (x, y), size, 5)

if __name__ == "__main__":
    pygame.init()
    generate_thumbnail()
    pygame.quit()
