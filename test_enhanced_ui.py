"""
SoulCoreLegacy Arcade - Enhanced UI Test
---------------------------------------
This script tests the enhanced UI components.
"""

import pygame
import sys
import os
import time
import random
from typing import List, Dict, Tuple

# Import enhanced UI components
from shell.enhanced_ui_elements import UITheme, EnhancedButton, EnhancedTextLabel, EnhancedGameCard, MouseController

def test_enhanced_ui():
    """Test the enhanced UI components."""
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("SoulCoreLegacy Arcade - Enhanced UI Test")
    
    # Create theme
    theme = UITheme("cosmic")  # Try different themes: cosmic, network, quantum, synthwave
    
    # Create mouse controller
    mouse = MouseController(800, 600)
    
    # Create buttons
    buttons = []
    
    play_button = EnhancedButton(
        rect=pygame.Rect(50, 50, 200, 50),
        text="Play Game",
        theme=theme,
        on_click=lambda: print("Play clicked!"),
        importance="high"
    )
    buttons.append(play_button)
    
    options_button = EnhancedButton(
        rect=pygame.Rect(50, 120, 200, 50),
        text="Options",
        theme=theme,
        on_click=lambda: print("Options clicked!")
    )
    buttons.append(options_button)
    
    quit_button = EnhancedButton(
        rect=pygame.Rect(50, 190, 200, 50),
        text="Quit",
        theme=theme,
        on_click=lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))
    )
    buttons.append(quit_button)
    
    # Register buttons with mouse controller
    mouse.register_clickable("play", play_button.rect, play_button.on_click)
    mouse.register_clickable("options", options_button.rect, options_button.on_click)
    mouse.register_clickable("quit", quit_button.rect, quit_button.on_click)
    
    # Create labels
    labels = []
    
    title_label = EnhancedTextLabel(
        rect=pygame.Rect(400, 50, 300, 50),
        text="SoulCoreLegacy Arcade",
        theme=theme,
        font_size="title",
        align="center",
        importance="high"
    )
    labels.append(title_label)
    
    subtitle_label = EnhancedTextLabel(
        rect=pygame.Rect(400, 100, 300, 30),
        text="Enhanced UI Test",
        theme=theme,
        font_size="medium",
        align="center"
    )
    labels.append(subtitle_label)
    
    # Create game cards
    game_cards = []
    
    # Create a tech-themed thumbnail
    thumbnail1 = pygame.Surface((150, 100))
    thumbnail1.fill((20, 10, 40))  # Dark purple background
    
    # Add tech grid pattern
    grid_color = (100, 0, 255, 50)  # Semi-transparent purple
    for y in range(0, 100, 10):
        pygame.draw.line(thumbnail1, grid_color, (0, y), (150, y), 1)
    for x in range(0, 150, 10):
        pygame.draw.line(thumbnail1, grid_color, (x, 0), (x, 100), 1)
    
    # Add some "nodes" in the grid
    for _ in range(8):
        x = random.randint(5, 145)
        y = random.randint(5, 95)
        radius = random.randint(2, 4)
        pygame.draw.circle(thumbnail1, (0, 200, 255), (x, y), radius)
    
    # Create a second thumbnail with different pattern
    thumbnail2 = pygame.Surface((150, 100))
    thumbnail2.fill((0, 10, 30))  # Dark blue background
    
    # Add space-themed elements
    for _ in range(50):
        x = random.randint(0, 150)
        y = random.randint(0, 100)
        radius = random.randint(1, 2)
        brightness = random.randint(150, 255)
        pygame.draw.circle(thumbnail2, (brightness, brightness, brightness), (x, y), radius)
    
    # Add a planet
    pygame.draw.circle(thumbnail2, (0, 100, 200), (120, 30), 20)
    pygame.draw.circle(thumbnail2, (0, 150, 255), (120, 30), 18)
    
    # Add a ring around the planet
    pygame.draw.ellipse(thumbnail2, (200, 200, 255), (100, 25, 40, 10), 1)
    
    # Create game cards
    game1_info = {
        "id": "cosmic_racer",
        "name": "Cosmic Racer",
        "description": "Race through the cosmos at breakneck speeds, avoiding asteroids and collecting stardust.",
        "implemented": True,
        "popularity": 8,
        "new_release": False
    }
    
    game2_info = {
        "id": "dungeon_delver",
        "name": "Dungeon Delver",
        "description": "Explore mysterious dungeons, battle monsters, and collect treasure in this roguelike adventure.",
        "implemented": True,
        "popularity": 6,
        "new_release": True
    }
    
    game1_card = EnhancedGameCard(
        game_info=game1_info,
        x=300,
        y=200,
        width=200,
        height=300,
        theme=theme,
        action=lambda game_id: print(f"Game {game_id} clicked!"),
        featured=True
    )
    game1_card.thumbnail = thumbnail1
    game1_card.scaled_thumbnail = pygame.transform.scale(
        thumbnail1, 
        (game1_card.thumbnail_rect.width, game1_card.thumbnail_rect.height)
    )
    game_cards.append(game1_card)
    
    game2_card = EnhancedGameCard(
        game_info=game2_info,
        x=550,
        y=200,
        width=200,
        height=300,
        theme=theme,
        action=lambda game_id: print(f"Game {game_id} clicked!")
    )
    game2_card.thumbnail = thumbnail2
    game2_card.scaled_thumbnail = pygame.transform.scale(
        thumbnail2, 
        (game2_card.thumbnail_rect.width, game2_card.thumbnail_rect.height)
    )
    game_cards.append(game2_card)
    
    # Register game cards with mouse controller
    mouse.register_clickable(
        "game1",
        game1_card.rect,
        lambda: print(f"Game {game1_info['id']} clicked!")
    )
    mouse.register_clickable(
        "game2",
        game2_card.rect,
        lambda: print(f"Game {game2_info['id']} clicked!")
    )
    
    # Create background
    background = pygame.Surface((800, 600))
    
    # Fill with gradient
    for y in range(600):
        # Calculate color for this line
        progress = y / 600
        color_top = theme.get_color("background")
        color_bottom = tuple(max(0, c - 15) for c in color_top)  # Slightly darker
        
        color = tuple(
            int(color_top[i] * (1 - progress) + color_bottom[i] * progress)
            for i in range(3)
        )
        
        # Draw horizontal line with this color
        pygame.draw.line(
            background,
            color,
            (0, y),
            (799, y)
        )
    
    # Draw grid lines
    grid_color = (*theme.get_color("primary"), 20)  # Very transparent
    
    # Horizontal grid lines
    for y in range(0, 600, 40):
        pygame.draw.line(
            background,
            grid_color,
            (0, y),
            (800, y)
        )
    
    # Vertical grid lines
    for x in range(0, 800, 40):
        pygame.draw.line(
            background,
            grid_color,
            (x, 0),
            (x, 600)
        )
    
    # Create particles
    particles = []
    for _ in range(50):
        x = random.randint(0, 800)
        y = random.randint(0, 600)
        size = random.randint(1, 3)
        speed = random.uniform(0.2, 1.0)
        direction = random.uniform(0, 6.28)
        lifetime = random.uniform(5, 15)
        
        # Choose a color based on particle size
        if size == 1:
            color = theme.get_color("text_secondary")
        elif size == 2:
            color = theme.get_color("secondary")
        else:
            color = theme.get_color("accent")
        
        particles.append({
            'x': x,
            'y': y,
            'size': size,
            'speed': speed,
            'direction': direction,
            'lifetime': lifetime,
            'age': 0,
            'color': color
        })
    
    # Main game loop
    running = True
    clock = pygame.time.Clock()
    animation_time = 0
    
    print("Enhanced UI Test launched! Close the window to exit.")
    
    try:
        while running:
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            
            # Update mouse controller
            mouse_info = mouse.update(events)
            mouse_pos = mouse_info["position"]
            mouse_pressed = mouse_info["buttons"][0]
            
            # Update buttons
            for button in buttons:
                button.update(mouse_pos, mouse_pressed, mouse)
            
            # Update labels
            for label in labels:
                label.update()
            
            # Update game cards
            for card in game_cards:
                card.update(mouse_pos, mouse_pressed, mouse)
            
            # Update particles
            for i in range(len(particles) - 1, -1, -1):
                particle = particles[i]
                
                # Update age
                particle['age'] += 0.016  # Approximately 60 FPS
                
                # Remove old particles
                if particle['age'] >= particle['lifetime']:
                    particles.pop(i)
                    
                    # Add a new particle to replace it
                    x = random.randint(0, 800)
                    y = random.randint(0, 600)
                    size = random.randint(1, 3)
                    speed = random.uniform(0.2, 1.0)
                    direction = random.uniform(0, 6.28)
                    lifetime = random.uniform(5, 15)
                    
                    # Choose a color based on particle size
                    if size == 1:
                        color = theme.get_color("text_secondary")
                    elif size == 2:
                        color = theme.get_color("secondary")
                    else:
                        color = theme.get_color("accent")
                    
                    particles.append({
                        'x': x,
                        'y': y,
                        'size': size,
                        'speed': speed,
                        'direction': direction,
                        'lifetime': lifetime,
                        'age': 0,
                        'color': color
                    })
                    
                    continue
                
                # Move particle
                particle['x'] += math.cos(particle['direction']) * particle['speed']
                particle['y'] += math.sin(particle['direction']) * particle['speed']
                
                # Wrap around screen edges
                if particle['x'] < 0:
                    particle['x'] = 800
                elif particle['x'] > 800:
                    particle['x'] = 0
                    
                if particle['y'] < 0:
                    particle['y'] = 600
                elif particle['y'] > 600:
                    particle['y'] = 0
            
            # Update animation time
            animation_time += 0.01
            
            # Clear screen
            screen.blit(background, (0, 0))
            
            # Draw particles
            for particle in particles:
                # Calculate alpha based on age
                progress = particle['age'] / particle['lifetime']
                alpha = int(255 * (1 - progress))
                
                # Draw particle
                pygame.draw.circle(
                    screen,
                    (*particle['color'], alpha),
                    (int(particle['x']), int(particle['y'])),
                    particle['size']
                )
            
            # Draw animated circles on the left
            for i in range(5):
                radius = 5 + i * 3
                pulse = (math.sin(animation_time * 2 + i * 0.5) + 1) * 0.5  # 0 to 1
                alpha = int(100 + pulse * 100)  # 100 to 200
                
                pygame.draw.circle(
                    screen,
                    (*theme.get_color("accent"), alpha),
                    (50, 50),
                    radius,
                    2
                )
            
            # Draw animated circles on the right
            for i in range(5):
                radius = 5 + i * 3
                pulse = (math.sin(animation_time * 2 + i * 0.5 + 3.14) + 1) * 0.5  # 0 to 1
                alpha = int(100 + pulse * 100)  # 100 to 200
                
                pygame.draw.circle(
                    screen,
                    (*theme.get_color("secondary"), alpha),
                    (750, 50),
                    radius,
                    2
                )
            
            # Draw UI elements
            for button in buttons:
                button.draw(screen)
            
            for label in labels:
                label.draw(screen)
            
            for card in game_cards:
                card.draw(screen)
            
            # Draw mouse effects
            mouse.draw_effects(screen)
            
            # Update display
            pygame.display.flip()
            clock.tick(60)
    except Exception as e:
        print(f"Error in game loop: {e}")
    finally:
        pygame.quit()
        print("Test closed.")

if __name__ == "__main__":
    test_enhanced_ui()
