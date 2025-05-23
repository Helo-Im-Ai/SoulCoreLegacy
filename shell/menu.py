"""
SoulCoreLegacy Arcade - Shell Menu
---------------------------------
This module implements the main menu interface for the arcade.
"""

import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, GAME_LIST
from core.asset_loader import load_font, create_gradient_background, create_rounded_rect_image
from shell.ui_elements import Button, TextLabel, GameCard

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
        self.game_cards = []
        
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
            40
        )
        self.labels.append(title_label)
        
        # Create subtitle label
        subtitle_font = load_font("Arial", 24)
        subtitle_label = TextLabel(
            "Select a game to play",
            subtitle_font,
            SECONDARY_COLOR,
            SCREEN_WIDTH // 2,
            100
        )
        self.labels.append(subtitle_label)
        
        # Create game cards
        self._create_game_cards()
        
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
    
    def _create_game_cards(self):
        """Create cards for each available game."""
        self.game_cards = []
        
        card_width = 200
        card_height = 220
        card_margin = 20
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
            
            # Create the card
            card = GameCard(
                game,
                x,
                y,
                card_width,
                card_height,
                self.game_manager.start_game
            )
            
            # Add the card to the list
            self.game_cards.append(card)
    
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
            
            for card in self.game_cards:
                card.check_click(event.pos)
        
        # Update button hover states
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.update(event.pos)
            
            for card in self.game_cards:
                card.update(event.pos)
    
    def update(self):
        """Update the menu state."""
        # Update labels
        for label in self.labels:
            label.update()
    
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
        
        # Draw the game cards
        for card in self.game_cards:
            card.draw(screen)
    
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
            pygame.Rect(0, 0, SCREEN_WIDTH, 120),
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
