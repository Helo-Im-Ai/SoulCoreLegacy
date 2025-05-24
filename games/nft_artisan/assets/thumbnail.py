"""
SoulCoreLegacy Arcade - NFT Artisan Thumbnail Generator
----------------------------------------------------
This script generates a thumbnail for the NFT Artisan game.
"""

import pygame
import os
import sys
import random

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.config import PRIMARY_COLOR, SECONDARY_COLOR, WHITE

def generate_thumbnail():
    """Generate a thumbnail for the NFT Artisan game."""
    # Create a surface
    width, height = 200, 150
    surface = pygame.Surface((width, height))
    
    # Fill the background with a gradient
    for y in range(height):
        # Calculate the ratio of the current position
        ratio = y / height
        
        # Interpolate between the two colors
        r = int(20 * (1 - ratio) + 40 * ratio)
        g = int(10 * (1 - ratio) + 20 * ratio)
        b = int(40 * (1 - ratio) + 80 * ratio)
        
        # Draw a horizontal line with the calculated color
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    
    # Draw a stylized NFT frame
    frame_rect = pygame.Rect(width // 2 - 50, height // 2 - 40, 100, 80)
    pygame.draw.rect(surface, (50, 50, 50), frame_rect)
    pygame.draw.rect(surface, (100, 100, 100), frame_rect, 2)
    
    # Draw some abstract art inside the frame
    # Circles
    for _ in range(5):
        x = random.randint(frame_rect.left + 10, frame_rect.right - 10)
        y = random.randint(frame_rect.top + 10, frame_rect.bottom - 10)
        radius = random.randint(5, 15)
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        pygame.draw.circle(surface, color, (x, y), radius)
    
    # Lines
    for _ in range(3):
        start_x = random.randint(frame_rect.left + 5, frame_rect.right - 5)
        start_y = random.randint(frame_rect.top + 5, frame_rect.bottom - 5)
        end_x = random.randint(frame_rect.left + 5, frame_rect.right - 5)
        end_y = random.randint(frame_rect.top + 5, frame_rect.bottom - 5)
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), 2)
    
    # Draw the game title
    font = pygame.font.SysFont("Arial", 18)
    title_text = font.render("NFT Artisan", True, WHITE)
    title_rect = title_text.get_rect(center=(width // 2, 20))
    surface.blit(title_text, title_rect)
    
    # Draw a subtitle
    subtitle_font = pygame.font.SysFont("Arial", 12)
    subtitle_text = subtitle_font.render("Create Digital Art", True, SECONDARY_COLOR)
    subtitle_rect = subtitle_text.get_rect(center=(width // 2, height - 15))
    surface.blit(subtitle_text, subtitle_rect)
    
    # Draw a border
    pygame.draw.rect(
        surface,
        WHITE,
        pygame.Rect(0, 0, width, height),
        2
    )
    
    # Save the thumbnail
    pygame.image.save(surface, os.path.join(os.path.dirname(__file__), "thumbnail.png"))
    
    print("NFT Artisan thumbnail generated successfully.")

if __name__ == "__main__":
    pygame.init()
    generate_thumbnail()
    pygame.quit()
