"""
SoulCoreLegacy Arcade - Shell Menu
---------------------------------
This module implements the main menu interface for the arcade.
"""

import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, GAME_LIST
from core.asset_loader import load_font, create_gradient_background, create_rounded_rect_image
from shell.ui_elements import Button, TextLabel

class ShellMenu:
    """
    The main menu interface for the SoulCoreLegacy Arcade.
    """
    
    def __init__(self, game_manager):
        """
        Initialize the shell menu.
        
        Args:
            game_manager (GameManager): Reference to the game manager
        """
        self.game_manager = game_manager
        self.buttons = []
        self.labels = []
        
        # Create background
        self.background = create_gradient_background(
            SCREEN_WIDTH, 
            SCREEN_HEIGHT, 
            (18, 18, 37),  # Dark blue-purple
            (30, 30, 60)   # Slightly lighter blue-purple
        )
        
        # Create title label
        title_font = load_font("Arial", 48)
        title_label = TextLabel(
            "SoulCoreLegacy Arcade",
            title_font,
            PRIMARY_COLOR,
            SCREEN_WIDTH // 2,
            80
        )
        self.labels.append(title_label)
        
        # Create subtitle label
        subtitle_font = load_font("Arial", 24)
        subtitle_label = TextLabel(
            "Select a game to play",
            subtitle_font,
            SECONDARY_COLOR,
            SCREEN_WIDTH // 2,
            130
        )
        self.labels.append(subtitle_label)
        
        # Create game buttons
        self._create_game_buttons()
        
        # Create footer text
        footer_font = load_font("Arial", 16)
        footer_label = TextLabel(
            "Press ESC to return to menu from any game",
            footer_font,
            TEXT_COLOR,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 30
        )
        self.labels.append(footer_label)
    
    def _create_game_buttons(self):
        """Create buttons for each available game."""
        self.buttons = []
        
        button_width = 200
        button_height = 60
        button_margin = 20
        
        # Calculate starting position
        start_y = 200
        
        # Create a button for each game
        for i, game in enumerate(GAME_LIST):
            # Create button background
            button_bg = create_rounded_rect_image(
                button_width,
                button_height,
                PRIMARY_COLOR,
                radius=10
            )
            
            # Create the button
            button = Button(
                game["name"],
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y + i * (button_height + button_margin),
                button_width,
                button_height,
                PRIMARY_COLOR,
                TEXT_COLOR,
                lambda g=game["id"]: self.game_manager.start_game(g),
                button_bg
            )
            
            # Add the button to the list
            self.buttons.append(button)
    
    def reset(self):
        """Reset the menu state."""
        # Nothing to reset for now
        pass
    
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.check_click(event.pos)
        
        # Update button hover states
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.update(event.pos)
    
    def update(self):
        """Update the menu state."""
        # Nothing to update for now
        pass
    
    def render(self, screen):
        """
        Render the menu.
        
        Args:
            screen (pygame.Surface): The surface to render on
        """
        # Draw the background
        screen.blit(self.background, (0, 0))
        
        # Draw decorative elements
        self._draw_decorations(screen)
        
        # Draw the labels
        for label in self.labels:
            label.draw(screen)
        
        # Draw the buttons
        for button in self.buttons:
            button.draw(screen)
    
    def _draw_decorations(self, screen):
        """
        Draw decorative elements on the menu.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Draw a header bar
        pygame.draw.rect(
            screen,
            (30, 30, 60),
            pygame.Rect(0, 0, SCREEN_WIDTH, 150),
            border_bottom_left_radius=20,
            border_bottom_right_radius=20
        )
        
        # Draw some decorative circles
        for i in range(5):
            radius = 5 + i * 3
            pygame.draw.circle(
                screen,
                (110, 68, 255, 50),  # Semi-transparent purple
                (50, 50),
                radius,
                2
            )
            
            pygame.draw.circle(
                screen,
                (0, 191, 255, 50),  # Semi-transparent blue
                (SCREEN_WIDTH - 50, 50),
                radius,
                2
            )
