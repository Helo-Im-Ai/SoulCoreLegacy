"""
SoulCoreLegacy Arcade - Asteroids Thumbnail Generator
--------------------------------------------------
This script generates a thumbnail for the Asteroids game.
"""

import pygame
import os
import sys
import random
import math

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.config import PRIMARY_COLOR, SECONDARY_COLOR, WHITE

def generate_thumbnail():
    """Generate a thumbnail for the Asteroids game."""
    # Create a surface
    width, height = 200, 150
    surface = pygame.Surface((width, height))
    
    # Fill the background with stars
    surface.fill((0, 0, 20))  # Dark blue background
    
    # Draw some stars
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 2)
        brightness = random.randint(150, 255)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(surface, color, (x, y), size)
    
    # Draw some asteroids
    for _ in range(3):
        x = random.randint(20, width - 20)
        y = random.randint(20, height - 20)
        size = random.randint(10, 20)
        
        # Draw a polygon for the asteroid
        points = []
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            point_x = x + math.cos(angle) * (size + random.randint(-5, 5))
            point_y = y + math.sin(angle) * (size + random.randint(-5, 5))
            points.append((point_x, point_y))
        
        pygame.draw.polygon(surface, (100, 100, 100), points)
        pygame.draw.polygon(surface, (150, 150, 150), points, 1)
    
    # Draw the player's ship
    ship_x = width // 2
    ship_y = height // 2
    ship_size = 15
    
    # Ship points
    ship_points = [
        (ship_x + ship_size, ship_y),
        (ship_x - ship_size / 2, ship_y - ship_size / 2),
        (ship_x - ship_size / 2, ship_y + ship_size / 2)
    ]
    
    # Draw the ship
    pygame.draw.polygon(surface, WHITE, ship_points)
    
    # Draw a bullet
    bullet_x = ship_x + ship_size + 10
    bullet_y = ship_y
    pygame.draw.circle(surface, PRIMARY_COLOR, (bullet_x, bullet_y), 3)
    
    # Draw the game title
    font = pygame.font.SysFont("Arial", 18)
    title_text = font.render("Asteroids", True, WHITE)
    title_rect = title_text.get_rect(center=(width // 2, 20))
    surface.blit(title_text, title_rect)
    
    # Draw a border
    pygame.draw.rect(
        surface,
        SECONDARY_COLOR,
        pygame.Rect(0, 0, width, height),
        2
    )
    
    # Save the thumbnail
    pygame.image.save(surface, os.path.join(os.path.dirname(__file__), "thumbnail.png"))
    
    print("Asteroids thumbnail generated successfully.")

if __name__ == "__main__":
    pygame.init()
    generate_thumbnail()
    pygame.quit()
