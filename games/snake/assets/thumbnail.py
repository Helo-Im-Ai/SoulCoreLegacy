"""
SoulCoreLegacy Arcade - Snake Thumbnail Generator
----------------------------------------------
This script generates a thumbnail for the Snake game.
"""

import pygame
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.config import PRIMARY_COLOR, SECONDARY_COLOR, WHITE, BLACK, GREEN

def generate_thumbnail():
    """Generate a thumbnail for the Snake game."""
    # Create a surface
    width, height = 200, 150
    surface = pygame.Surface((width, height))
    
    # Fill the background
    surface.fill((18, 18, 37))  # Dark blue-purple
    
    # Draw the snake
    block_size = 15
    snake_color = (0, 200, 0)  # Green
    
    # Snake body segments
    snake_body = [
        [width // 2, height // 2],
        [width // 2 - block_size, height // 2],
        [width // 2 - 2 * block_size, height // 2],
        [width // 2 - 3 * block_size, height // 2],
        [width // 2 - 4 * block_size, height // 2],
        [width // 2 - 4 * block_size, height // 2 + block_size],
        [width // 2 - 4 * block_size, height // 2 + 2 * block_size],
    ]
    
    # Draw each segment of the snake
    for i, segment in enumerate(snake_body):
        # Draw the head in a slightly different color
        if i == 0:
            # Make the head a bit brighter
            head_color = tuple(min(c + 50, 255) for c in snake_color)
            pygame.draw.rect(surface, head_color, [segment[0], segment[1], block_size, block_size])
            
            # Draw eyes
            eye_size = max(2, block_size // 5)
            eye_offset = block_size // 4
            
            pygame.draw.circle(surface, (0, 0, 0), (segment[0] + block_size - eye_offset, segment[1] + eye_offset), eye_size)
            pygame.draw.circle(surface, (0, 0, 0), (segment[0] + block_size - eye_offset, segment[1] + block_size - eye_offset), eye_size)
        else:
            pygame.draw.rect(surface, snake_color, [segment[0], segment[1], block_size, block_size])
        
        # Add a small border to each segment
        pygame.draw.rect(surface, (0, 0, 0), [segment[0], segment[1], block_size, block_size], 1)
    
    # Draw the food
    food_color = (255, 50, 50)  # Red
    food_position = [width // 2 + 3 * block_size, height // 2]
    
    # Draw the food as a circle
    center_x = food_position[0] + block_size // 2
    center_y = food_position[1] + block_size // 2
    radius = block_size // 2
    
    pygame.draw.circle(surface, food_color, (center_x, center_y), radius)
    
    # Add a small shine effect
    shine_radius = radius // 2
    shine_offset = radius // 3
    pygame.draw.circle(surface, (255, 255, 255), (center_x - shine_offset, center_y - shine_offset), shine_radius)
    
    # Draw the score
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render("Score: 7", True, WHITE)
    surface.blit(score_text, (10, 10))
    
    # Draw a border
    pygame.draw.rect(
        surface,
        WHITE,
        pygame.Rect(0, 0, width, height),
        2
    )
    
    # Save the thumbnail
    pygame.image.save(surface, os.path.join(os.path.dirname(__file__), "thumbnail.png"))
    
    print("Snake thumbnail generated successfully.")

if __name__ == "__main__":
    pygame.init()
    generate_thumbnail()
    pygame.quit()
