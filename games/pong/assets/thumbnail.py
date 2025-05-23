"""
SoulCoreLegacy Arcade - Pong Thumbnail Generator
----------------------------------------------
This script generates a thumbnail for the Pong game.
"""

import pygame
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.config import PRIMARY_COLOR, SECONDARY_COLOR, WHITE, BLACK

def generate_thumbnail():
    """Generate a thumbnail for the Pong game."""
    # Create a surface
    width, height = 200, 150
    surface = pygame.Surface((width, height))
    
    # Fill the background
    surface.fill((18, 18, 37))  # Dark blue-purple
    
    # Draw the center line
    pygame.draw.aaline(
        surface,
        WHITE,
        (width // 2, 0),
        (width // 2, height)
    )
    
    # Draw the paddles
    paddle_width = 10
    paddle_height = 50
    paddle_margin = 20
    
    pygame.draw.rect(
        surface,
        WHITE,
        pygame.Rect(paddle_margin, height // 2 - paddle_height // 2, paddle_width, paddle_height)
    )
    
    pygame.draw.rect(
        surface,
        WHITE,
        pygame.Rect(width - paddle_margin - paddle_width, height // 2 - paddle_height // 2, paddle_width, paddle_height)
    )
    
    # Draw the ball
    ball_radius = 5
    pygame.draw.circle(
        surface,
        WHITE,
        (width // 2 + 20, height // 2 - 10),
        ball_radius
    )
    
    # Draw the scores
    font = pygame.font.SysFont("Arial", 36)
    player_score_text = font.render("3", True, PRIMARY_COLOR)
    ai_score_text = font.render("2", True, SECONDARY_COLOR)
    
    surface.blit(player_score_text, (width // 4, 20))
    surface.blit(ai_score_text, (3 * width // 4, 20))
    
    # Draw a border
    pygame.draw.rect(
        surface,
        WHITE,
        pygame.Rect(0, 0, width, height),
        2
    )
    
    # Save the thumbnail
    pygame.image.save(surface, os.path.join(os.path.dirname(__file__), "thumbnail.png"))
    
    print("Pong thumbnail generated successfully.")

if __name__ == "__main__":
    pygame.init()
    generate_thumbnail()
    pygame.quit()
