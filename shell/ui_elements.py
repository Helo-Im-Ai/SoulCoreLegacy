"""
SoulCoreLegacy Arcade - UI Elements
----------------------------------
This module provides UI elements for the shell interface.
"""

import pygame
import math
from core.asset_loader import load_font, create_rounded_rect_image

class Button:
    """A clickable button UI element."""
    
    def __init__(self, text, x, y, width, height, color, text_color, action=None, background_image=None, font_size=24):
        """
        Initialize a button.
        
        Args:
            text (str): The text to display on the button
            x (int): The x-coordinate of the button
            y (int): The y-coordinate of the button
            width (int): The width of the button
            height (int): The height of the button
            color (tuple): The RGB color of the button
            text_color (tuple): The RGB color of the text
            action (function): The function to call when the button is clicked
            background_image (pygame.Surface): Optional custom background image
            font_size (int): The size of the font
        """
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.action = action
        self.background_image = background_image
        
        # Create the font
        self.font = load_font("Arial", font_size)
        
        # Create the rect
        self.rect = pygame.Rect(x, y, width, height)
        
        # Hover state
        self.is_hovered = False
        
        # Animation properties
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.2
        
        # Create default background if none provided
        if not self.background_image:
            self.background_image = create_rounded_rect_image(width, height, color, radius=10)
            self.hover_background = create_rounded_rect_image(
                width, height, 
                tuple(min(c + 30, 255) for c in color),  # Lighter color
                radius=10
            )
        else:
            # If a custom background was provided, create a hover version
            self.hover_background = self.background_image.copy()
            # Add a slight glow effect
            pygame.draw.rect(
                self.hover_background,
                (255, 255, 255, 50),  # Semi-transparent white
                pygame.Rect(0, 0, width, height),
                border_radius=10
            )
    
    def check_click(self, pos):
        """
        Check if the button was clicked.
        
        Args:
            pos (tuple): The (x, y) position of the click
            
        Returns:
            bool: True if the button was clicked, False otherwise
        """
        if self.rect.collidepoint(pos):
            if self.action:
                self.action()
            return True
        return False
    
    def update(self, mouse_pos):
        """
        Update the button state.
        
        Args:
            mouse_pos (tuple): The current mouse position
        """
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Set target scale based on hover state
        if self.is_hovered:
            self.target_scale = 1.05
        else:
            self.target_scale = 1.0
        
        # Animate scale
        if self.scale != self.target_scale:
            self.scale += (self.target_scale - self.scale) * self.scale_speed
    
    def draw(self, screen):
        """
        Draw the button.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Calculate scaled dimensions
        scaled_width = int(self.width * self.scale)
        scaled_height = int(self.height * self.scale)
        
        # Calculate position to keep button centered during scaling
        scaled_x = self.x + (self.width - scaled_width) // 2
        scaled_y = self.y + (self.height - scaled_height) // 2
        
        # Create scaled rect
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Draw the button background
        if self.background_image:
            # Scale the background image
            bg_to_use = self.hover_background if self.is_hovered else self.background_image
            try:
                scaled_bg = pygame.transform.scale(bg_to_use, (scaled_width, scaled_height))
                screen.blit(scaled_bg, scaled_rect)
            except (pygame.error, ValueError):
                # Fallback if scaling fails
                if self.is_hovered:
                    hover_color = tuple(min(c + 30, 255) for c in self.color)
                    pygame.draw.rect(screen, hover_color, scaled_rect, border_radius=10)
                else:
                    pygame.draw.rect(screen, self.color, scaled_rect, border_radius=10)
        else:
            # Draw a simple rectangle if no background image
            if self.is_hovered:
                # Lighten the color when hovered
                hover_color = tuple(min(c + 30, 255) for c in self.color)
                pygame.draw.rect(screen, hover_color, scaled_rect, border_radius=10)
            else:
                pygame.draw.rect(screen, self.color, scaled_rect, border_radius=10)
            
            # Draw the button border
            pygame.draw.rect(screen, (255, 255, 255), scaled_rect, 2, border_radius=10)
        
        # Draw the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        screen.blit(text_surface, text_rect)

class TextLabel:
    """A text label UI element."""
    
    def __init__(self, text, font, color, x, y, align="center"):
        """
        Initialize a text label.
        
        Args:
            text (str): The text to display
            font (pygame.font.Font): The font to use
            color (tuple): The RGB color of the text
            x (int): The x-coordinate of the label
            y (int): The y-coordinate of the label
            align (str): The alignment of the text ("left", "center", or "right")
        """
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.align = align
        
        # Create the text surface
        self.text_surface = self.font.render(self.text, True, self.color)
        
        # Create the text rect
        self.text_rect = self.text_surface.get_rect()
        
        # Set the position based on the alignment
        if align == "left":
            self.text_rect.topleft = (x, y)
        elif align == "center":
            self.text_rect.midtop = (x, y)
        elif align == "right":
            self.text_rect.topright = (x, y)
        
        # Animation properties
        self.alpha = 255
        self.target_alpha = 255
        self.alpha_speed = 0.1
        self.pulse_time = 0
    
    def update_text(self, text):
        """
        Update the text of the label.
        
        Args:
            text (str): The new text to display
        """
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color)
        
        # Update the position
        if self.align == "left":
            self.text_rect = self.text_surface.get_rect(topleft=(self.x, self.y))
        elif self.align == "center":
            self.text_rect = self.text_surface.get_rect(midtop=(self.x, self.y))
        elif self.align == "right":
            self.text_rect = self.text_surface.get_rect(topright=(self.x, self.y))
    
    def update(self):
        """Update the label state."""
        # Animate alpha
        if self.alpha != self.target_alpha:
            self.alpha += (self.target_alpha - self.alpha) * self.alpha_speed
        
        # Pulse effect
        self.pulse_time += 0.05
        pulse_factor = (math.sin(self.pulse_time) + 1) * 0.5  # 0 to 1
        self.alpha = 200 + int(55 * pulse_factor)  # 200 to 255
    
    def draw(self, screen):
        """
        Draw the label.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Create a copy of the text surface with the current alpha
        alpha_surface = self.text_surface.copy()
        alpha_surface.set_alpha(self.alpha)
        
        # Draw the text
        screen.blit(alpha_surface, self.text_rect)

class GameCard:
    """A game card UI element for the shell menu."""
    
    def __init__(self, game_info, x, y, width, height, action=None):
        """
        Initialize a game card.
        
        Args:
            game_info (dict): Information about the game
            x (int): The x-coordinate of the card
            y (int): The y-coordinate of the card
            width (int): The width of the card
            height (int): The height of the card
            action (function): The function to call when the card is clicked
        """
        self.game_info = game_info
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        
        # Create the rect
        self.rect = pygame.Rect(x, y, width, height)
        
        # Hover state
        self.is_hovered = False
        
        # Animation properties
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.2
        
        # Load the thumbnail
        self.thumbnail = None
        self._load_thumbnail()
        
        # Create fonts
        self.title_font = load_font("Arial", 18)
        self.desc_font = load_font("Arial", 14)
        
        # Create the background
        self.background = create_rounded_rect_image(width, height, (30, 30, 60), radius=10)
        self.hover_background = create_rounded_rect_image(
            width, height, 
            (40, 40, 80),  # Lighter color
            radius=10
        )
        
        # Create the "Not Implemented" overlay if needed
        self.not_implemented = not game_info.get("implemented", False)
        if self.not_implemented:
            self.overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            self.overlay.fill((0, 0, 0, 128))  # Semi-transparent black
            
            # Add "Coming Soon" text
            coming_soon_font = load_font("Arial", 16)
            coming_soon_text = coming_soon_font.render("Coming Soon", True, (255, 255, 255))
            coming_soon_rect = coming_soon_text.get_rect(center=(width // 2, height // 2))
            self.overlay.blit(coming_soon_text, coming_soon_rect)
    
    def _load_thumbnail(self):
        """Load the thumbnail image."""
        try:
            import os
            from core.asset_loader import load_image
            
            # Try to load the thumbnail
            thumbnail_path = os.path.join("games", self.game_info["id"], "assets", "thumbnail.png")
            if os.path.exists(thumbnail_path):
                self.thumbnail = pygame.image.load(thumbnail_path)
            else:
                # Create a placeholder thumbnail
                self.thumbnail = pygame.Surface((160, 120))
                self.thumbnail.fill((50, 50, 80))
                
                # Add the game name
                font = pygame.font.SysFont("Arial", 18)
                text = font.render(self.game_info["name"], True, (255, 255, 255))
                text_rect = text.get_rect(center=(80, 60))
                self.thumbnail.blit(text, text_rect)
        except Exception as e:
            print(f"Error loading thumbnail for {self.game_info['name']}: {e}")
            # Create a placeholder thumbnail
            self.thumbnail = pygame.Surface((160, 120))
            self.thumbnail.fill((50, 50, 80))
    
    def check_click(self, pos):
        """
        Check if the card was clicked.
        
        Args:
            pos (tuple): The (x, y) position of the click
            
        Returns:
            bool: True if the card was clicked, False otherwise
        """
        if self.rect.collidepoint(pos) and not self.not_implemented:
            if self.action:
                self.action(self.game_info["id"])
            return True
        return False
    
    def update(self, mouse_pos):
        """
        Update the card state.
        
        Args:
            mouse_pos (tuple): The current mouse position
        """
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Set target scale based on hover state
        if self.is_hovered and not self.not_implemented:
            self.target_scale = 1.05
        else:
            self.target_scale = 1.0
        
        # Animate scale
        if self.scale != self.target_scale:
            self.scale += (self.target_scale - self.scale) * self.scale_speed
    
    def draw(self, screen):
        """
        Draw the card.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Calculate scaled dimensions
        scaled_width = int(self.width * self.scale)
        scaled_height = int(self.height * self.scale)
        
        # Calculate position to keep card centered during scaling
        scaled_x = self.x + (self.width - scaled_width) // 2
        scaled_y = self.y + (self.height - scaled_height) // 2
        
        # Create scaled rect
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Draw the card background
        bg_to_use = self.hover_background if self.is_hovered else self.background
        try:
            scaled_bg = pygame.transform.scale(bg_to_use, (scaled_width, scaled_height))
            screen.blit(scaled_bg, scaled_rect)
        except (pygame.error, ValueError):
            # Fallback if scaling fails
            pygame.draw.rect(screen, (30, 30, 60), scaled_rect, border_radius=10)
        
        # Draw the thumbnail
        if self.thumbnail:
            # Scale the thumbnail
            thumbnail_width = int(160 * self.scale)
            thumbnail_height = int(120 * self.scale)
            try:
                scaled_thumbnail = pygame.transform.scale(self.thumbnail, (thumbnail_width, thumbnail_height))
                thumbnail_x = scaled_x + (scaled_width - thumbnail_width) // 2
                thumbnail_y = scaled_y + 10
                screen.blit(scaled_thumbnail, (thumbnail_x, thumbnail_y))
            except (pygame.error, ValueError):
                # Fallback if scaling fails
                pass
        
        # Draw the title
        title_text = self.title_font.render(self.game_info["name"], True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(scaled_x + scaled_width // 2, scaled_y + scaled_height - 40))
        screen.blit(title_text, title_rect)
        
        # Draw the description
        desc_text = self.desc_font.render(self.game_info["description"], True, (200, 200, 200))
        desc_rect = desc_text.get_rect(center=(scaled_x + scaled_width // 2, scaled_y + scaled_height - 20))
        screen.blit(desc_text, desc_rect)
        
        # Draw the "Not Implemented" overlay if needed
        if self.not_implemented:
            try:
                scaled_overlay = pygame.transform.scale(self.overlay, (scaled_width, scaled_height))
                screen.blit(scaled_overlay, scaled_rect)
            except (pygame.error, ValueError):
                # Fallback if scaling fails
                pass
