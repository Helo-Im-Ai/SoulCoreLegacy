"""
SoulCoreLegacy Arcade - Enhanced Shell Menu
------------------------------------------
This module implements an enhanced main menu interface for the arcade
with improved UX design principles.
"""

import pygame
import math
import random
import time
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_LIST
from shell.enhanced_ui_elements import UITheme, EnhancedButton, EnhancedTextLabel, EnhancedGameCard, MouseController

class EnhancedShellMenu:
    """
    Enhanced main menu interface for the SoulCoreLegacy Arcade.
    Implements multiple UX principles for a more immersive experience.
    """
    
    def __init__(self, game_manager):
        """
        Initialize the enhanced shell menu.
        
        Args:
            game_manager: Reference to the game manager
        """
        self.game_manager = game_manager
        
        # Create theme
        self.theme = UITheme("cosmic")
        
        # Create mouse controller
        self.mouse = MouseController(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # UI elements
        self.buttons = []
        self.labels = []
        self.game_cards = []
        
        # Create background
        self.background = self._create_tech_background()
        
        # Create title label
        title_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 40, 400, 60)
        title_label = EnhancedTextLabel(
            title_rect,
            "SoulCoreLegacy Arcade",
            self.theme,
            font_size="title",
            color="text",
            align="center",
            importance="high"
        )
        self.labels.append(title_label)
        
        # Create subtitle label
        subtitle_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 100, 300, 30)
        subtitle_label = EnhancedTextLabel(
            subtitle_rect,
            "Select a game to play",
            self.theme,
            font_size="medium",
            color="text_secondary",
            align="center"
        )
        self.labels.append(subtitle_label)
        
        # Create game cards
        self._create_game_cards()
        
        # Create footer text
        footer_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 40, 400, 30)
        footer_label = EnhancedTextLabel(
            footer_rect,
            "Press ESC to return to menu from any game",
            self.theme,
            font_size="small",
            color="text_secondary",
            align="center"
        )
        self.labels.append(footer_label)
        
        # Animation properties
        self.animation_time = 0
        
        # Particle effects
        self.particles = []
        for _ in range(50):
            self._add_particle()
    
    def _create_tech_background(self):
        """
        Create a tech-themed background with grid lines and nodes.
        
        Returns:
            Pygame surface with the background
        """
        # Create background surface
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Fill with gradient
        for y in range(SCREEN_HEIGHT):
            # Calculate color for this line
            progress = y / SCREEN_HEIGHT
            color_top = self.theme.get_color("background")
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
                (SCREEN_WIDTH - 1, y)
            )
        
        # Draw grid lines
        grid_color = (*self.theme.get_color("primary"), 20)  # Very transparent
        
        # Horizontal grid lines
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(
                background,
                grid_color,
                (0, y),
                (SCREEN_WIDTH, y)
            )
        
        # Vertical grid lines
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(
                background,
                grid_color,
                (x, 0),
                (x, SCREEN_HEIGHT)
            )
        
        # Draw some "nodes" in the grid
        for _ in range(30):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            radius = random.randint(1, 3)
            
            pygame.draw.circle(
                background,
                self.theme.get_color("accent"),
                (x, y),
                radius
            )
        
        # Draw some "connections" between nodes
        for _ in range(15):
            x1 = random.randint(0, SCREEN_WIDTH)
            y1 = random.randint(0, SCREEN_HEIGHT)
            x2 = random.randint(max(0, x1 - 200), min(SCREEN_WIDTH, x1 + 200))
            y2 = random.randint(max(0, y1 - 200), min(SCREEN_HEIGHT, y1 + 200))
            
            pygame.draw.line(
                background,
                (*self.theme.get_color("secondary"), 40),  # Semi-transparent
                (x1, y1),
                (x2, y2),
                1
            )
        
        return background
    
    def _create_game_cards(self):
        """Create enhanced cards for each available game."""
        self.game_cards = []
        
        card_width = 200
        card_height = 280
        card_margin = 30
        cards_per_row = 3
        
        # Calculate starting position
        start_x = (SCREEN_WIDTH - (cards_per_row * card_width + (cards_per_row - 1) * card_margin)) // 2
        start_y = 150
        
        # Create a card for each game
        for i, game in enumerate(GAME_LIST):
            # Calculate position
            row = i // cards_per_row
            col = i % cards_per_row
            x = start_x + col * (card_width + card_margin)
            y = start_y + row * (card_height + card_margin)
            
            # Determine if this is a featured game
            featured = game.get("featured", False)
            
            # Create the card
            card = EnhancedGameCard(
                game,
                x,
                y,
                card_width,
                card_height,
                self.theme,
                self.game_manager.start_game,
                featured
            )
            
            # Add the card to the list
            self.game_cards.append(card)
            
            # Register with mouse controller
            self.mouse.register_clickable(
                f"game_card_{game['id']}",
                pygame.Rect(x, y, card_width, card_height),
                lambda game_id=game['id']: self.game_manager.start_game(game_id)
            )
    
    def _add_particle(self):
        """Add a floating particle effect."""
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(1, 3)
        speed = random.uniform(0.2, 1.0)
        direction = random.uniform(0, math.pi * 2)
        lifetime = random.uniform(5, 15)
        
        # Choose a color based on particle size
        if size == 1:
            color = self.theme.get_color("text_secondary")
        elif size == 2:
            color = self.theme.get_color("secondary")
        else:
            color = self.theme.get_color("accent")
        
        self.particles.append({
            'x': x,
            'y': y,
            'size': size,
            'speed': speed,
            'direction': direction,
            'lifetime': lifetime,
            'age': 0,
            'color': color
        })
    
    def reset(self):
        """Reset the menu state."""
        # Nothing to reset for now
        pass
    
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event: The event to handle
        """
        # Pass events to mouse controller
        self.mouse.update([event])
        
        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            for card in self.game_cards:
                card.update(mouse_pos, True)
        
        # Handle button releases
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            
            for card in self.game_cards:
                card.update(mouse_pos, False)
        
        # Update hover states
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            
            for card in self.game_cards:
                card.update(mouse_pos, pygame.mouse.get_pressed()[0])
    
    def update(self):
        """Update the menu state."""
        # Update animation time
        self.animation_time += 0.01
        
        # Update labels
        for label in self.labels:
            label.update()
        
        # Update particles
        for i in range(len(self.particles) - 1, -1, -1):
            particle = self.particles[i]
            
            # Update age
            particle['age'] += 0.016  # Approximately 60 FPS
            
            # Remove old particles
            if particle['age'] >= particle['lifetime']:
                self.particles.pop(i)
                self._add_particle()  # Add a new particle to replace it
                continue
            
            # Move particle
            particle['x'] += math.cos(particle['direction']) * particle['speed']
            particle['y'] += math.sin(particle['direction']) * particle['speed']
            
            # Wrap around screen edges
            if particle['x'] < 0:
                particle['x'] = SCREEN_WIDTH
            elif particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
                
            if particle['y'] < 0:
                particle['y'] = SCREEN_HEIGHT
            elif particle['y'] > SCREEN_HEIGHT:
                particle['y'] = 0
    
    def render(self, screen):
        """
        Render the menu.
        
        Args:
            screen: The surface to render on
        """
        # Draw the background
        screen.blit(self.background, (0, 0))
        
        # Draw particles
        for particle in self.particles:
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
        
        # Draw decorative elements
        self._draw_decorations(screen)
        
        # Draw the game cards
        for card in self.game_cards:
            card.draw(screen)
        
        # Draw the labels
        for label in self.labels:
            label.draw(screen)
        
        # Draw mouse effects
        self.mouse.draw_effects(screen)
    
    def _draw_decorations(self, screen):
        """
        Draw decorative elements on the menu.
        
        Args:
            screen: The surface to draw on
        """
        # Draw a header bar with gradient
        header_surface = pygame.Surface((SCREEN_WIDTH, 120), pygame.SRCALPHA)
        
        # Draw gradient
        for y in range(120):
            # Calculate color for this line
            progress = y / 120
            color_top = self.theme.get_color("primary")
            color_bottom = self.theme.get_color("background")
            
            color = tuple(
                int(color_top[i] * (1 - progress) + color_bottom[i] * progress)
                for i in range(3)
            )
            
            # Draw horizontal line with this color
            pygame.draw.line(
                header_surface,
                (*color, 150),  # Semi-transparent
                (0, y),
                (SCREEN_WIDTH - 1, y)
            )
        
        # Apply rounded corners
        pygame.draw.rect(
            header_surface,
            (0, 0, 0, 0),  # Transparent
            pygame.Rect(0, 0, SCREEN_WIDTH, 120),
            border_bottom_left_radius=20,
            border_bottom_right_radius=20
        )
        
        # Draw header
        screen.blit(header_surface, (0, 0))
        
        # Draw animated circles on the left
        for i in range(5):
            radius = 5 + i * 3
            pulse = (math.sin(self.animation_time * 2 + i * 0.5) + 1) * 0.5  # 0 to 1
            alpha = int(100 + pulse * 100)  # 100 to 200
            
            pygame.draw.circle(
                screen,
                (*self.theme.get_color("accent"), alpha),
                (50, 50),
                radius,
                2
            )
        
        # Draw animated circles on the right
        for i in range(5):
            radius = 5 + i * 3
            pulse = (math.sin(self.animation_time * 2 + i * 0.5 + math.pi) + 1) * 0.5  # 0 to 1
            alpha = int(100 + pulse * 100)  # 100 to 200
            
            pygame.draw.circle(
                screen,
                (*self.theme.get_color("secondary"), alpha),
                (SCREEN_WIDTH - 50, 50),
                radius,
                2
            )
