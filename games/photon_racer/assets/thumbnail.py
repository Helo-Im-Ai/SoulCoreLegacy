"""
SoulCoreLegacy Arcade - Photon Racer Thumbnail Generator
-----------------------------------------------------
This script generates a thumbnail for the Photon Racer game.
"""

import pygame
import os
import sys
import math
import random

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.config import PRIMARY_COLOR, SECONDARY_COLOR, WHITE

def generate_thumbnail():
    """Generate a thumbnail for the Photon Racer game."""
    # Create a surface
    width, height = 200, 150
    surface = pygame.Surface((width, height))
    
    # Fill the background with a gradient
    for y in range(height):
        # Calculate the ratio of the current position
        ratio = y / height
        
        # Interpolate between the two colors
        r = int(0 * (1 - ratio) + 30 * ratio)
        g = int(0 * (1 - ratio) + 0 * ratio)
        b = int(30 * (1 - ratio) + 60 * ratio)
        
        # Draw a horizontal line with the calculated color
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    
    # Draw the tunnel
    tunnel_width = 80
    tunnel_color = (50, 0, 100)  # Dark purple
    tunnel_border_color = (100, 50, 200)  # Light purple
    
    # Generate tunnel points
    tunnel_points = []
    center_x = width // 2
    for y in range(height, -50, -10):
        deviation = math.sin(y / 20) * 30
        tunnel_points.append((center_x + deviation, y))
    
    # Draw tunnel segments
    for i in range(len(tunnel_points) - 1):
        p1 = tunnel_points[i]
        p2 = tunnel_points[i + 1]
        
        # Calculate tunnel edges
        angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0]) + math.pi / 2
        dx = math.cos(angle) * tunnel_width / 2
        dy = math.sin(angle) * tunnel_width / 2
        
        left1 = (p1[0] - dx, p1[1] - dy)
        right1 = (p1[0] + dx, p1[1] + dy)
        left2 = (p2[0] - dx, p2[1] - dy)
        right2 = (p2[0] + dx, p2[1] + dy)
        
        # Draw tunnel interior
        pygame.draw.polygon(surface, tunnel_color, [left1, right1, right2, left2])
        
        # Draw tunnel borders
        pygame.draw.line(surface, tunnel_border_color, left1, left2, 2)
        pygame.draw.line(surface, tunnel_border_color, right1, right2, 2)
    
    # Draw the ship
    ship_x = width // 2
    ship_y = height - 30
    ship_size = 15
    ship_color = (0, 255, 255)  # Cyan
    
    # Draw ship trail
    for i in range(10):
        # Fade the trail based on position
        alpha = int(255 * i / 10)
        radius = int(ship_size / 2 * i / 10)
        trail_y = ship_y + i * 3
        
        # Create a surface for the trail segment
        trail_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(trail_surface, (*ship_color, alpha), (radius, radius), radius)
        
        # Draw the trail segment
        surface.blit(trail_surface, (ship_x - radius, trail_y - radius))
    
    # Draw the ship
    pygame.draw.circle(surface, ship_color, (ship_x, ship_y), ship_size // 2)
    
    # Draw ship details
    pygame.draw.line(surface, WHITE, (ship_x, ship_y - ship_size // 2), (ship_x, ship_y + ship_size // 2), 2)
    pygame.draw.line(surface, WHITE, (ship_x - ship_size // 2, ship_y), (ship_x + ship_size // 2, ship_y), 2)
    
    # Draw the game title
    font = pygame.font.SysFont("Arial", 18)
    title_text = font.render("Photon Racer", True, WHITE)
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
    
    print("Photon Racer thumbnail generated successfully.")

if __name__ == "__main__":
    pygame.init()
    generate_thumbnail()
    pygame.quit()
