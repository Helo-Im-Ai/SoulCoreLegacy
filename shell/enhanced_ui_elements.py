"""
SoulCoreLegacy Arcade - Enhanced UI Elements
-------------------------------------------
This module provides enhanced UI elements with improved UX design principles.
"""

import pygame
import math
import time
import random
from typing import Tuple, List, Dict, Callable, Optional, Union
from enum import Enum

class MouseState(Enum):
    """Enum representing different mouse states for visual feedback."""
    NORMAL = 0
    HOVER = 1
    CLICK = 2
    DRAG = 3
    DISABLED = 4

class FeedbackType(Enum):
    """Types of feedback that can be provided to the user."""
    VISUAL = 0
    AUDIO = 1
    HAPTIC = 2
    ANIMATION = 3

class UITheme:
    """
    Theme manager for UI elements to ensure consistent styling.
    Implements Aesthetic-Usability Effect by providing visually pleasing themes.
    """
    
    def __init__(self, name: str = "cosmic"):
        """
        Initialize a UI theme.
        
        Args:
            name: Theme name
        """
        self.name = name
        
        # Define color schemes with vibrant tech-inspired gradients
        self.color_schemes = {
            "cosmic": {
                "background": (5, 0, 20),   # Deep space black
                "primary": (100, 0, 255),   # Deep purple
                "secondary": (0, 200, 255), # Bright blue
                "accent": (255, 215, 0),    # Gold
                "text": (255, 255, 255),    # Pure white
                "text_secondary": (180, 180, 255), # Light purple
                "hover": (150, 50, 255),    # Brighter purple
                "active": (180, 80, 255),   # Even brighter purple
                "disabled": (40, 20, 60),   # Muted purple
                "success": (0, 255, 150),   # Neon green
                "warning": (255, 200, 0),   # Gold
                "error": (255, 0, 100)      # Hot pink
            },
            "network": {
                "background": (0, 10, 25),  # Deep blue-black
                "primary": (0, 150, 255),   # Bright blue
                "secondary": (100, 0, 255), # Deep purple
                "accent": (0, 255, 200),    # Neon teal
                "text": (220, 240, 255),    # Light blue-white
                "text_secondary": (150, 200, 255), # Light blue
                "hover": (50, 180, 255),    # Brighter blue
                "active": (100, 200, 255),  # Even brighter blue
                "disabled": (30, 60, 80),   # Muted blue
                "success": (0, 255, 150),   # Neon green
                "warning": (255, 200, 0),   # Gold
                "error": (255, 50, 100)     # Hot pink
            },
            "quantum": {
                "background": (5, 0, 15),   # Near-black
                "primary": (140, 0, 255),   # Deep purple
                "secondary": (0, 200, 255), # Bright blue
                "accent": (255, 0, 150),    # Hot pink
                "text": (255, 255, 255),    # Pure white
                "text_secondary": (200, 180, 255), # Light purple
                "hover": (180, 50, 255),    # Brighter purple
                "active": (200, 100, 255),  # Even brighter purple
                "disabled": (50, 30, 70),   # Muted purple
                "success": (0, 255, 170),   # Neon teal
                "warning": (255, 215, 0),   # Gold
                "error": (255, 0, 100)      # Hot pink
            },
            "synthwave": {
                "background": (20, 0, 40),  # Deep purple
                "primary": (255, 0, 150),   # Hot pink
                "secondary": (0, 200, 255), # Bright blue
                "accent": (255, 215, 0),    # Gold
                "text": (255, 255, 255),    # Pure white
                "text_secondary": (200, 200, 255), # Light purple
                "hover": (255, 50, 180),    # Brighter pink
                "active": (255, 100, 200),  # Even brighter pink
                "disabled": (80, 30, 80),   # Muted purple-pink
                "success": (0, 255, 170),   # Neon teal
                "warning": (255, 215, 0),   # Gold
                "error": (255, 50, 50)      # Bright red
            },
            "default": {
                "background": (10, 5, 30),  # Deep space black with hint of purple
                "primary": (80, 70, 220),   # Rich purple
                "secondary": (0, 180, 255), # Bright cyan
                "accent": (255, 215, 0),    # Gold
                "text": (255, 255, 255),    # Pure white
                "text_secondary": (200, 200, 255), # Light purple
                "hover": (120, 90, 255),    # Brighter purple
                "active": (140, 110, 255),  # Even brighter purple
                "disabled": (50, 50, 80),   # Muted purple
                "success": (0, 255, 170),   # Neon teal
                "warning": (255, 215, 0),   # Gold
                "error": (255, 50, 120)     # Hot pink
            }
        }
        
        # Set the current color scheme
        self.colors = self.color_schemes[name] if name in self.color_schemes else self.color_schemes["cosmic"]
        
        # Define fonts
        self.fonts = {
            "small": pygame.font.SysFont(None, 18),
            "medium": pygame.font.SysFont(None, 24),
            "large": pygame.font.SysFont(None, 32),
            "title": pygame.font.SysFont(None, 48),
            "header": pygame.font.SysFont(None, 36)
        }
        
        # Define spacing
        self.spacing = {
            "tiny": 4,
            "small": 8,
            "medium": 16,
            "large": 24,
            "xlarge": 32
        }
        
        # Define animation durations (in seconds)
        self.animation = {
            "fast": 0.1,
            "medium": 0.2,
            "slow": 0.3
        }
        
        # Define border radius
        self.border_radius = 5
        
        # Define shadow properties
        self.shadow = {
            "enabled": True,
            "offset": (2, 2),
            "blur": 5,
            "color": (0, 0, 0, 128)  # RGBA
        }
    
    def set_theme(self, name: str):
        """
        Change the current theme.
        
        Args:
            name: Theme name
        """
        if name in self.color_schemes:
            self.name = name
            self.colors = self.color_schemes[name]
    
    def get_color(self, name: str) -> Tuple[int, int, int]:
        """
        Get a color from the current theme.
        
        Args:
            name: Color name
            
        Returns:
            RGB color tuple
        """
        return self.colors.get(name, self.colors["primary"])
    
    def get_font(self, size: str) -> pygame.font.Font:
        """
        Get a font from the current theme.
        
        Args:
            size: Font size name
            
        Returns:
            Pygame font
        """
        return self.fonts.get(size, self.fonts["medium"])
    
    def get_spacing(self, size: str) -> int:
        """
        Get spacing value from the current theme.
        
        Args:
            size: Spacing size name
            
        Returns:
            Spacing value in pixels
        """
        return self.spacing.get(size, self.spacing["medium"])
    
    def get_animation_duration(self, speed: str) -> float:
        """
        Get animation duration from the current theme.
        
        Args:
            speed: Animation speed name
            
        Returns:
            Animation duration in seconds
        """
        return self.animation.get(speed, self.animation["medium"])

class EnhancedButton:
    """
    Enhanced button class with animations and effects.
    Implements multiple UX principles:
    - Fitts's Law: Optimized target size
    - Aesthetic-Usability Effect: Visual appeal
    - Doherty Threshold: Responsive feedback
    """
    
    def __init__(self, rect: pygame.Rect, text: str, 
                theme: UITheme, 
                on_click: Callable = None,
                icon: pygame.Surface = None,
                tooltip: str = None,
                disabled: bool = False,
                importance: str = "normal"):
        """
        Initialize an enhanced button.
        
        Args:
            rect: Button rectangle
            text: Button text
            theme: UI theme
            on_click: Function to call when clicked
            icon: Optional icon to display
            tooltip: Optional tooltip text
            disabled: Whether the button is disabled
            importance: Button importance ("low", "normal", "high")
        """
        self.rect = rect
        self.text = text
        self.theme = theme
        self.on_click = on_click
        self.icon = icon
        self.tooltip = tooltip
        self.disabled = disabled
        self.importance = importance
        
        # State
        self.hovered = False
        self.pressed = False
        self.focused = False
        
        # Animation properties
        self.animation_progress = 0.0
        self.animation_start_time = 0
        self.animation_duration = theme.get_animation_duration("medium")
        self.animation_target = 0.0
        
        # Visual effects
        self.glow_effect = importance == "high"  # Apply glow effect to high importance buttons
        self.pulse_effect = False
        self.ripple_effects = []
        
        # Accessibility
        self.keyboard_shortcut = None
        
        # Von Restorff Effect - make important buttons stand out
        if importance == "high":
            # Make high importance buttons slightly larger
            self.rect.inflate_ip(10, 6)
    
    def update(self, mouse_pos: Tuple[int, int], mouse_pressed: bool, 
              mouse_controller = None) -> bool:
        """
        Update button state based on mouse input.
        
        Args:
            mouse_pos: Current mouse position
            mouse_pressed: Whether the mouse button is pressed
            mouse_controller: Optional mouse controller for enhanced effects
            
        Returns:
            True if the button was clicked
        """
        if self.disabled:
            return False
        
        old_hovered = self.hovered
        old_pressed = self.pressed
        
        # Check if mouse is over button
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Update pressed state
        if self.hovered and mouse_pressed:
            self.pressed = True
        else:
            # Check if button was clicked (released while hovering)
            clicked = self.pressed and self.hovered and not mouse_pressed
            self.pressed = False
            
            if clicked and self.on_click:
                # Start click animation
                self._start_animation(1.0)
                
                # Add ripple effect
                self._add_ripple_effect(mouse_pos)
                
                # Call click handler
                self.on_click()
                
                return True
        
        # Start hover animation if hover state changed
        if old_hovered != self.hovered:
            self._start_animation(1.0 if self.hovered else 0.0)
            
            # Register with mouse controller if available
            if mouse_controller and self.hovered:
                mouse_controller.set_cursor(MouseState.HOVER)
            elif mouse_controller and not self.hovered and old_hovered:
                mouse_controller.set_cursor(MouseState.NORMAL)
        
        # Update animations
        self._update_animations()
        
        return False
    
    def draw(self, surface: pygame.Surface):
        """
        Draw the button on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Determine colors based on state
        if self.disabled:
            bg_color = self.theme.get_color("disabled")
            text_color = self.theme.get_color("text_secondary")
        else:
            if self.pressed:
                bg_color = self.theme.get_color("active")
            elif self.hovered:
                bg_color = self.theme.get_color("hover")
            else:
                bg_color = self.theme.get_color("primary")
            
            # Apply Von Restorff Effect for high importance buttons
            if self.importance == "high" and not self.pressed:
                bg_color = self.theme.get_color("accent")
            
            text_color = self.theme.get_color("text")
        
        # Draw shadow (if enabled)
        if self.theme.shadow["enabled"] and not self.disabled:
            shadow_rect = self.rect.copy()
            shadow_rect.x += self.theme.shadow["offset"][0]
            shadow_rect.y += self.theme.shadow["offset"][1]
            
            # Create shadow surface with alpha
            shadow_surface = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(
                shadow_surface,
                self.theme.shadow["color"],
                pygame.Rect(0, 0, shadow_rect.width, shadow_rect.height),
                border_radius=self.theme.border_radius
            )
            
            # Draw shadow
            surface.blit(shadow_surface, shadow_rect)
        
        # Draw ripple effects
        for ripple in self.ripple_effects:
            # Create ripple surface with alpha
            ripple_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            
            # Calculate ripple properties
            progress = (time.time() - ripple["start_time"]) / ripple["duration"]
            radius = int(ripple["max_radius"] * progress)
            alpha = int(255 * (1 - progress))
            
            # Draw ripple circle
            pygame.draw.circle(
                ripple_surface,
                (*self.theme.get_color("text"), alpha),  # RGBA
                (ripple["pos"][0] - self.rect.x, ripple["pos"][1] - self.rect.y),
                radius
            )
            
            # Draw ripple
            surface.blit(ripple_surface, self.rect)
        
        # Create gradient background
        gradient_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        
        # Get gradient colors
        if self.disabled:
            color_top = self.theme.get_color("disabled")
            color_bottom = tuple(max(0, c - 20) for c in color_top)
        else:
            if self.pressed:
                color_top = self.theme.get_color("active")
                color_bottom = tuple(max(0, c - 30) for c in color_top)
            elif self.hovered:
                color_top = self.theme.get_color("hover")
                color_bottom = tuple(min(255, c + 20) for c in color_top)
            else:
                color_top = self.theme.get_color("primary")
                color_bottom = tuple(max(0, c - 40) for c in color_top)
            
            # Apply Von Restorff Effect for high importance buttons
            if self.importance == "high" and not self.pressed:
                color_top = self.theme.get_color("accent")
                color_bottom = tuple(max(0, c - 40) for c in color_top)
        
        # Draw vertical gradient
        for y in range(self.rect.height):
            # Calculate color for this line
            progress = y / self.rect.height
            color = tuple(
                int(color_top[i] * (1 - progress) + color_bottom[i] * progress)
                for i in range(3)
            )
            
            # Draw horizontal line with this color
            pygame.draw.line(
                gradient_surface,
                color,
                (0, y),
                (self.rect.width - 1, y)
            )
        
        # Apply rounded corners by drawing a rect with border radius
        pygame.draw.rect(
            gradient_surface,
            (255, 255, 255, 0),  # Transparent
            pygame.Rect(0, 0, self.rect.width, self.rect.height),
            border_radius=self.theme.border_radius
        )
        
        # Draw button background
        surface.blit(gradient_surface, self.rect)
        
        # Add subtle inner border
        pygame.draw.rect(
            surface,
            (*color_top, 150),  # Semi-transparent
            self.rect,
            border_radius=self.theme.border_radius,
            width=1
        )
        
        # Draw glow effect for high importance buttons
        if self.glow_effect and not self.disabled:
            glow_rect = self.rect.inflate(6, 6)
            
            # Create glow surface with alpha
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            
            # Get glow color
            glow_color = self.theme.get_color("accent")
            
            # Draw multiple rects with decreasing alpha for glow effect
            for i in range(3):
                pygame.draw.rect(
                    glow_surface,
                    (*glow_color, 100 - i * 30),  # Decreasing alpha
                    pygame.Rect(i, i, glow_rect.width - i * 2, glow_rect.height - i * 2),
                    border_radius=self.theme.border_radius + 3,
                    width=2
                )
            
            # Draw glow
            surface.blit(glow_surface, glow_rect)
        
        # Draw button text
        font = self.theme.get_font("medium")
        text_surf = font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # Adjust text position when pressed
        if self.pressed:
            text_rect.y += 1
            
        surface.blit(text_surf, text_rect)
        
        # Draw icon if available
        if self.icon:
            icon_rect = self.icon.get_rect()
            icon_rect.centery = self.rect.centery
            icon_rect.x = self.rect.x + self.theme.get_spacing("medium")
            
            # Adjust text position to make room for icon
            text_rect.x += icon_rect.width + self.theme.get_spacing("small")
            
            surface.blit(self.icon, icon_rect)
    
    def _start_animation(self, target: float):
        """
        Start a new animation.
        
        Args:
            target: Target animation value
        """
        self.animation_start_time = time.time()
        self.animation_target = target
    
    def _update_animations(self):
        """Update all animations."""
        current_time = time.time()
        
        # Update main animation
        elapsed = current_time - self.animation_start_time
        progress = min(1.0, elapsed / self.animation_duration)
        
        # Smooth easing function
        eased_progress = progress * (2 - progress)
        
        # Update animation progress
        start_value = self.animation_progress
        target_value = self.animation_target
        self.animation_progress = start_value + (target_value - start_value) * eased_progress
        
        # Update ripple effects
        for i in range(len(self.ripple_effects) - 1, -1, -1):
            ripple = self.ripple_effects[i]
            if current_time - ripple["start_time"] >= ripple["duration"]:
                self.ripple_effects.pop(i)
    
    def _add_ripple_effect(self, pos: Tuple[int, int]):
        """
        Add a ripple effect at the specified position.
        
        Args:
            pos: Position for the ripple effect
        """
        self.ripple_effects.append({
            "pos": pos,
            "start_time": time.time(),
            "duration": self.theme.get_animation_duration("slow"),
            "max_radius": max(self.rect.width, self.rect.height)
        })
class EnhancedTextLabel:
    """
    Enhanced text label with animations and effects.
    Implements Aesthetic-Usability Effect for improved visual appeal.
    """
    
    def __init__(self, rect: pygame.Rect, text: str, 
                theme: UITheme,
                font_size: str = "medium",
                color: str = "text",
                align: str = "left",
                multiline: bool = False,
                max_width: int = None,
                animate_in: bool = False,
                importance: str = "normal"):
        """
        Initialize an enhanced text label.
        
        Args:
            rect: Label rectangle
            text: Label text
            theme: UI theme
            font_size: Font size name
            color: Color name
            align: Text alignment ("left", "center", "right")
            multiline: Whether to allow multiple lines
            max_width: Maximum width for text wrapping
            animate_in: Whether to animate the label when first shown
            importance: Label importance ("low", "normal", "high")
        """
        self.rect = rect
        self.text = text
        self.theme = theme
        self.font_size = font_size
        self.color_name = color
        self.align = align
        self.multiline = multiline
        self.max_width = max_width or rect.width
        self.importance = importance
        
        # Animation properties
        self.visible = not animate_in  # Start invisible if animating in
        self.animation_progress = 0.0 if animate_in else 1.0
        self.animation_start_time = time.time() if animate_in else 0
        self.animation_duration = theme.get_animation_duration("medium")
        
        # Split text into lines if multiline
        self.lines = []
        if multiline:
            self._wrap_text()
        
        # Apply Von Restorff Effect for high importance labels
        self.highlight = importance == "high"
        self.glow_effect = importance == "high"
    
    def set_text(self, text: str):
        """
        Set the label text.
        
        Args:
            text: New text
        """
        if self.text != text:
            self.text = text
            if self.multiline:
                self._wrap_text()
    
    def update(self):
        """Update label animations."""
        if not self.visible and self.animation_progress < 1.0:
            # Update animation progress
            elapsed = time.time() - self.animation_start_time
            progress = min(1.0, elapsed / self.animation_duration)
            
            # Smooth easing function
            eased_progress = progress * (2 - progress)
            
            self.animation_progress = eased_progress
            
            # Make visible once animation starts
            self.visible = True
    
    def draw(self, surface: pygame.Surface):
        """
        Draw the label on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        if not self.visible:
            return
        
        # Get font and color
        font = self.theme.get_font(self.font_size)
        color = self.theme.get_color(self.color_name)
        
        # Apply Von Restorff Effect for high importance labels
        if self.highlight:
            # Draw highlight background
            highlight_rect = self.rect.inflate(10, 4)
            pygame.draw.rect(
                surface,
                self.theme.get_color("accent"),
                highlight_rect,
                border_radius=self.theme.border_radius
            )
            
            # Use contrasting text color
            color = self.theme.get_color("text")
        
        # Apply glow effect
        if self.glow_effect:
            glow_color = (*self.theme.get_color("accent"), 100)  # Semi-transparent
            glow_font = self.theme.get_font(self.font_size)
            
            # Draw glow (simplified)
            for offset_x, offset_y in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                if self.multiline:
                    y_offset = 0
                    for line in self.lines:
                        text_surf = glow_font.render(line, True, glow_color)
                        
                        if self.align == "center":
                            text_rect = text_surf.get_rect(midtop=(self.rect.centerx + offset_x, self.rect.y + y_offset + offset_y))
                        elif self.align == "right":
                            text_rect = text_surf.get_rect(topright=(self.rect.right + offset_x, self.rect.y + y_offset + offset_y))
                        else:  # left
                            text_rect = text_surf.get_rect(topleft=(self.rect.x + offset_x, self.rect.y + y_offset + offset_y))
                        
                        surface.blit(text_surf, text_rect)
                        y_offset += font.get_linesize()
                else:
                    text_surf = glow_font.render(self.text, True, glow_color)
                    
                    if self.align == "center":
                        text_rect = text_surf.get_rect(center=(self.rect.centerx + offset_x, self.rect.centery + offset_y))
                    elif self.align == "right":
                        text_rect = text_surf.get_rect(midright=(self.rect.right + offset_x, self.rect.centery + offset_y))
                    else:  # left
                        text_rect = text_surf.get_rect(midleft=(self.rect.x + offset_x, self.rect.centery + offset_y))
                    
                    surface.blit(text_surf, text_rect)
        
        # Apply animation
        alpha = int(255 * self.animation_progress)
        
        # Draw text
        if self.multiline:
            y_offset = 0
            for line in self.lines:
                text_surf = font.render(line, True, color)
                
                # Apply animation
                if self.animation_progress < 1.0:
                    # Create a surface with alpha
                    alpha_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
                    alpha_surf.fill((255, 255, 255, alpha))
                    text_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
                if self.align == "center":
                    text_rect = text_surf.get_rect(midtop=(self.rect.centerx, self.rect.y + y_offset))
                elif self.align == "right":
                    text_rect = text_surf.get_rect(topright=(self.rect.right, self.rect.y + y_offset))
                else:  # left
                    text_rect = text_surf.get_rect(topleft=(self.rect.x, self.rect.y + y_offset))
                
                surface.blit(text_surf, text_rect)
                y_offset += font.get_linesize()
        else:
            text_surf = font.render(self.text, True, color)
            
            # Apply animation
            if self.animation_progress < 1.0:
                # Create a surface with alpha
                alpha_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
                alpha_surf.fill((255, 255, 255, alpha))
                text_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            if self.align == "center":
                text_rect = text_surf.get_rect(center=self.rect.center)
            elif self.align == "right":
                text_rect = text_surf.get_rect(midright=(self.rect.right, self.rect.centery))
            else:  # left
                text_rect = text_surf.get_rect(midleft=(self.rect.x, self.rect.centery))
            
            surface.blit(text_surf, text_rect)
    
    def _wrap_text(self):
        """Wrap text to fit within max_width."""
        self.lines = []
        font = self.theme.get_font(self.font_size)
        
        words = self.text.split(' ')
        current_line = []
        current_width = 0
        
        for word in words:
            word_surface = font.render(word + ' ', True, (0, 0, 0))
            word_width = word_surface.get_width()
            
            if current_width + word_width > self.max_width:
                # Line is full, start a new one
                self.lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
            else:
                # Add word to current line
                current_line.append(word)
                current_width += word_width
        
        # Add the last line
        if current_line:
            self.lines.append(' '.join(current_line))
class EnhancedGameCard:
    """
    Enhanced game card for game selection screens.
    Implements multiple UX principles:
    - Aesthetic-Usability Effect: Visual appeal
    - Fitts's Law: Optimized target size
    - Von Restorff Effect: Making important games stand out
    """
    
    def __init__(self, game_info: Dict, 
                x: int, y: int, 
                width: int, height: int,
                theme: UITheme,
                action: Callable = None,
                featured: bool = False):
        """
        Initialize an enhanced game card.
        
        Args:
            game_info: Information about the game
            x: X-coordinate of the card
            y: Y-coordinate of the card
            width: Width of the card
            height: Height of the card
            theme: UI theme
            action: Function to call when clicked
            featured: Whether this is a featured game
        """
        self.game_info = game_info
        self.rect = pygame.Rect(x, y, width, height)
        self.theme = theme
        self.action = action
        self.featured = featured
        
        # Determine if this is a new release
        self.new_release = game_info.get("new_release", False)
        
        # Determine if this game is implemented
        self.implemented = game_info.get("implemented", False)
        
        # Determine popularity (0-10 scale)
        self.popularity = game_info.get("popularity", 5)
        
        # State
        self.hovered = False
        self.pressed = False
        
        # Animation properties
        self.animation_progress = 0.0
        self.animation_start_time = 0
        self.animation_duration = theme.get_animation_duration("medium")
        self.animation_target = 0.0
        
        # Visual effects
        self.glow_effect = featured  # Apply glow effect to featured games
        self.pulse_effect = self.new_release  # Apply pulse effect to new releases
        self.pulse_time = 0
        
        # Apply Von Restorff Effect based on importance
        self.importance = "high" if featured else "normal"
        if featured:
            # Make featured games slightly larger
            self.rect.inflate_ip(20, 20)
        
        # Load the thumbnail
        self.thumbnail = self._load_thumbnail()
        
        # Thumbnail properties
        self.thumbnail_rect = pygame.Rect(
            self.rect.x + theme.get_spacing("medium"),
            self.rect.y + theme.get_spacing("medium"),
            self.rect.width - theme.get_spacing("medium") * 2,
            self.rect.height * 0.6
        )
        
        # Scale thumbnail to fit
        if self.thumbnail:
            self.scaled_thumbnail = pygame.transform.scale(
                self.thumbnail, 
                (self.thumbnail_rect.width, self.thumbnail_rect.height)
            )
    
    def _load_thumbnail(self) -> pygame.Surface:
        """
        Load the thumbnail image.
        
        Returns:
            Pygame surface with the thumbnail
        """
        try:
            import os
            
            # Try to load the thumbnail
            thumbnail_path = os.path.join("games", self.game_info["id"], "assets", "thumbnail.png")
            if os.path.exists(thumbnail_path):
                return pygame.image.load(thumbnail_path)
            else:
                # Create a placeholder thumbnail with tech pattern
                thumbnail = pygame.Surface((160, 120))
                thumbnail.fill(self.theme.get_color("background"))
                
                # Add tech grid pattern
                grid_color = (*self.theme.get_color("primary"), 50)  # Semi-transparent
                for y in range(0, 120, 10):
                    pygame.draw.line(thumbnail, grid_color, (0, y), (160, y), 1)
                for x in range(0, 160, 10):
                    pygame.draw.line(thumbnail, grid_color, (x, 0), (x, 120), 1)
                
                # Add some "nodes" in the grid
                for _ in range(8):
                    x = random.randint(5, 155)
                    y = random.randint(5, 115)
                    radius = random.randint(2, 4)
                    pygame.draw.circle(thumbnail, self.theme.get_color("accent"), (x, y), radius)
                
                # Add some "connections" between nodes
                for _ in range(5):
                    x1 = random.randint(5, 155)
                    y1 = random.randint(5, 115)
                    x2 = random.randint(5, 155)
                    y2 = random.randint(5, 115)
                    pygame.draw.line(thumbnail, self.theme.get_color("secondary"), (x1, y1), (x2, y2), 1)
                
                # Add the game name
                font = pygame.font.SysFont("Arial", 18)
                text = font.render(self.game_info["name"], True, self.theme.get_color("text"))
                text_rect = text.get_rect(center=(80, 60))
                thumbnail.blit(text, text_rect)
                
                return thumbnail
        except Exception as e:
            print(f"Error loading thumbnail for {self.game_info['name']}: {e}")
            # Create a simple placeholder thumbnail
            thumbnail = pygame.Surface((160, 120))
            thumbnail.fill(self.theme.get_color("primary"))
            return thumbnail
    
    def update(self, mouse_pos: Tuple[int, int], mouse_pressed: bool, 
              mouse_controller = None) -> bool:
        """
        Update card state based on mouse input.
        
        Args:
            mouse_pos: Current mouse position
            mouse_pressed: Whether the mouse button is pressed
            mouse_controller: Optional mouse controller for enhanced effects
            
        Returns:
            True if the card was clicked
        """
        if not self.implemented:
            return False
            
        old_hovered = self.hovered
        old_pressed = self.pressed
        
        # Check if mouse is over card
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Update pressed state
        if self.hovered and mouse_pressed:
            self.pressed = True
        else:
            # Check if card was clicked (released while hovering)
            clicked = self.pressed and self.hovered and not mouse_pressed
            self.pressed = False
            
            if clicked and self.action:
                # Start click animation
                self._start_animation(1.0)
                
                # Call click handler
                self.action(self.game_info["id"])
                
                return True
        
        # Start hover animation if hover state changed
        if old_hovered != self.hovered:
            self._start_animation(1.0 if self.hovered else 0.0)
            
            # Register with mouse controller if available
            if mouse_controller and self.hovered:
                mouse_controller.set_cursor(MouseState.HOVER)
            elif mouse_controller and not self.hovered and old_hovered:
                mouse_controller.set_cursor(MouseState.NORMAL)
        
        # Update animations
        self._update_animations()
        
        return False
    
    def draw(self, surface: pygame.Surface):
        """
        Draw the game card on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Determine colors based on state
        if self.pressed:
            bg_color = self.theme.get_color("active")
        elif self.hovered:
            bg_color = self.theme.get_color("hover")
        else:
            bg_color = self.theme.get_color("primary")
        
        # Apply Von Restorff Effect for featured games
        if self.featured and not self.pressed:
            bg_color = self.theme.get_color("accent")
        
        # Draw shadow (if enabled)
        if self.theme.shadow["enabled"]:
            shadow_rect = self.rect.copy()
            shadow_rect.x += self.theme.shadow["offset"][0]
            shadow_rect.y += self.theme.shadow["offset"][1]
            
            # Create shadow surface with alpha
            shadow_surface = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(
                shadow_surface,
                self.theme.shadow["color"],
                pygame.Rect(0, 0, shadow_rect.width, shadow_rect.height),
                border_radius=self.theme.border_radius
            )
            
            # Draw shadow
            surface.blit(shadow_surface, shadow_rect)
        
        # Create gradient background
        gradient_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        
        # Get gradient colors
        if self.pressed:
            color_top = self.theme.get_color("active")
            color_bottom = tuple(max(0, c - 30) for c in color_top)
        elif self.hovered:
            color_top = self.theme.get_color("hover")
            color_bottom = tuple(max(0, c - 40) for c in color_top)
        else:
            color_top = self.theme.get_color("primary")
            color_bottom = tuple(max(0, c - 50) for c in color_top)
        
        # Apply Von Restorff Effect for featured games
        if self.featured and not self.pressed:
            color_top = self.theme.get_color("accent")
            color_bottom = tuple(max(0, c - 50) for c in color_top)
        
        # Draw vertical gradient
        for y in range(self.rect.height):
            # Calculate color for this line
            progress = y / self.rect.height
            color = tuple(
                int(color_top[i] * (1 - progress) + color_bottom[i] * progress)
                for i in range(3)
            )
            
            # Draw horizontal line with this color
            pygame.draw.line(
                gradient_surface,
                color,
                (0, y),
                (self.rect.width - 1, y)
            )
        
        # Apply rounded corners by drawing a rect with border radius
        pygame.draw.rect(
            gradient_surface,
            (255, 255, 255, 0),  # Transparent
            pygame.Rect(0, 0, self.rect.width, self.rect.height),
            border_radius=self.theme.border_radius
        )
        
        # Draw card background
        surface.blit(gradient_surface, self.rect)
        
        # Add subtle inner border
        pygame.draw.rect(
            surface,
            (*color_top, 150),  # Semi-transparent
            self.rect,
            border_radius=self.theme.border_radius,
            width=1
        )
        
        # Draw glow effect for featured games
        if self.glow_effect:
            glow_rect = self.rect.inflate(10, 10)
            
            # Create glow surface with alpha
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            
            # Pulse the glow for new releases
            if self.pulse_effect:
                pulse_value = (math.sin(self.pulse_time * 5) + 1) / 2  # 0 to 1
                glow_alpha = int(100 + pulse_value * 100)  # 100 to 200
            else:
                glow_alpha = 150
            
            # Get glow color
            glow_color = self.theme.get_color("accent")
            
            # Draw multiple rects with decreasing alpha for glow effect
            for i in range(4):
                pygame.draw.rect(
                    glow_surface,
                    (*glow_color, glow_alpha - i * 30),  # Decreasing alpha
                    pygame.Rect(i, i, glow_rect.width - i * 2, glow_rect.height - i * 2),
                    border_radius=self.theme.border_radius + 5,
                    width=2
                )
            
            # Draw glow
            surface.blit(glow_surface, glow_rect)
        
        # Create thumbnail background with tech pattern
        thumbnail_bg = pygame.Surface(self.thumbnail_rect.size, pygame.SRCALPHA)
        thumbnail_bg.fill((0, 0, 0, 200))  # Semi-transparent black
        
        # Draw tech pattern (grid lines)
        grid_color = (self.theme.get_color("primary")[0], 
                     self.theme.get_color("primary")[1], 
                     self.theme.get_color("primary")[2], 50)  # Semi-transparent
        
        # Horizontal grid lines
        for y in range(0, self.thumbnail_rect.height, 10):
            pygame.draw.line(
                thumbnail_bg,
                grid_color,
                (0, y),
                (self.thumbnail_rect.width, y),
                1
            )
        
        # Vertical grid lines
        for x in range(0, self.thumbnail_rect.width, 10):
            pygame.draw.line(
                thumbnail_bg,
                grid_color,
                (x, 0),
                (x, self.thumbnail_rect.height),
                1
            )
        
        # Draw some random "nodes" in the grid
        for _ in range(10):
            x = random.randint(5, self.thumbnail_rect.width - 5)
            y = random.randint(5, self.thumbnail_rect.height - 5)
            radius = random.randint(2, 4)
            
            pygame.draw.circle(
                thumbnail_bg,
                (self.theme.get_color("accent")[0],
                 self.theme.get_color("accent")[1],
                 self.theme.get_color("accent")[2], 150),
                (x, y),
                radius
            )
        
        # Draw thumbnail background
        surface.blit(thumbnail_bg, self.thumbnail_rect)
        
        # Draw thumbnail with slight transparency
        if hasattr(self, 'scaled_thumbnail') and self.scaled_thumbnail:
            thumbnail_alpha = pygame.Surface(self.scaled_thumbnail.get_size(), pygame.SRCALPHA)
            thumbnail_alpha.fill((255, 255, 255, 220))  # Slight transparency
            
            # Apply thumbnail
            thumbnail_copy = self.scaled_thumbnail.copy()
            thumbnail_copy.blit(thumbnail_alpha, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(thumbnail_copy, self.thumbnail_rect)
        
        # Draw thumbnail border
        pygame.draw.rect(
            surface,
            self.theme.get_color("primary"),
            self.thumbnail_rect,
            width=1,
            border_radius=3
        )
        
        # Draw title with tech-inspired style
        title_font = self.theme.get_font("large")
        title_surf = title_font.render(self.game_info["name"], True, self.theme.get_color("text"))
        title_rect = title_surf.get_rect(
            topleft=(
                self.rect.x + self.theme.get_spacing("medium"),
                self.thumbnail_rect.bottom + self.theme.get_spacing("medium")
            )
        )
        
        # Draw title glow for featured games
        if self.featured:
            # Create glow surface
            glow_surf = title_font.render(self.game_info["name"], True, self.theme.get_color("accent"))
            glow_rect = glow_surf.get_rect(center=title_rect.center)
            
            # Apply blur (simplified)
            for offset_x, offset_y in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                offset_rect = glow_rect.copy()
                offset_rect.x += offset_x
                offset_rect.y += offset_y
                surface.blit(glow_surf, offset_rect, special_flags=pygame.BLEND_RGB_ADD)
        
        surface.blit(title_surf, title_rect)
        
        # Draw description
        desc_font = self.theme.get_font("small")
        desc_rect = pygame.Rect(
            self.rect.x + self.theme.get_spacing("medium"),
            title_rect.bottom + self.theme.get_spacing("small"),
            self.rect.width - self.theme.get_spacing("medium") * 2,
            self.rect.bottom - title_rect.bottom - self.theme.get_spacing("medium") * 2
        )
        
        # Get description text
        description = self.game_info.get("description", "")
        
        # Wrap description text
        words = description.split(' ')
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_surface = desc_font.render(word + ' ', True, (0, 0, 0))
            word_width = word_surface.get_width()
            
            if current_width + word_width > desc_rect.width:
                # Line is full, start a new one
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
            else:
                # Add word to current line
                current_line.append(word)
                current_width += word_width
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw description lines
        y_offset = 0
        for i, line in enumerate(lines):
            if y_offset + desc_font.get_linesize() > desc_rect.height:
                # Not enough space for more lines
                if i < len(lines) - 1:
                    # Add ellipsis to indicate truncation
                    line = line[:-3] + "..."
                line_surf = desc_font.render(line, True, self.theme.get_color("text_secondary"))
                surface.blit(line_surf, (desc_rect.x, desc_rect.y + y_offset))
                break
            
            line_surf = desc_font.render(line, True, self.theme.get_color("text_secondary"))
            surface.blit(line_surf, (desc_rect.x, desc_rect.y + y_offset))
            y_offset += desc_font.get_linesize()
        
        # Draw "New!" badge for new releases
        if self.new_release:
            badge_font = self.theme.get_font("small")
            badge_text = "NEW!"
            badge_surf = badge_font.render(badge_text, True, self.theme.get_color("text"))
            badge_bg_rect = badge_surf.get_rect(
                topright=(
                    self.rect.right - self.theme.get_spacing("small"),
                    self.rect.y + self.theme.get_spacing("small")
                )
            )
            badge_bg_rect.inflate_ip(10, 6)
            
            # Create gradient for badge
            badge_gradient = pygame.Surface(badge_bg_rect.size, pygame.SRCALPHA)
            
            # Get gradient colors
            badge_color_top = self.theme.get_color("warning")
            badge_color_bottom = tuple(max(0, c - 40) for c in badge_color_top)
            
            # Draw vertical gradient
            for y in range(badge_bg_rect.height):
                # Calculate color for this line
                progress = y / badge_bg_rect.height
                color = tuple(
                    int(badge_color_top[i] * (1 - progress) + badge_color_bottom[i] * progress)
                    for i in range(3)
                )
                
                # Draw horizontal line with this color
                pygame.draw.line(
                    badge_gradient,
                    color,
                    (0, y),
                    (badge_bg_rect.width - 1, y)
                )
            
            # Apply rounded corners
            pygame.draw.rect(
                badge_gradient,
                (255, 255, 255, 0),  # Transparent
                pygame.Rect(0, 0, badge_bg_rect.width, badge_bg_rect.height),
                border_radius=self.theme.border_radius
            )
            
            # Draw badge background
            surface.blit(badge_gradient, badge_bg_rect)
            
            # Add subtle border
            pygame.draw.rect(
                surface,
                (*badge_color_top, 150),  # Semi-transparent
                badge_bg_rect,
                border_radius=self.theme.border_radius,
                width=1
            )
            
            # Draw badge text
            badge_rect = badge_surf.get_rect(center=badge_bg_rect.center)
            surface.blit(badge_surf, badge_rect)
        
        # Draw "Coming Soon" overlay if not implemented
        if not self.implemented:
            # Create overlay
            overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Semi-transparent black
            
            # Add "Coming Soon" text
            coming_soon_font = self.theme.get_font("large")
            coming_soon_text = coming_soon_font.render("Coming Soon", True, self.theme.get_color("text"))
            coming_soon_rect = coming_soon_text.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
            overlay.blit(coming_soon_text, coming_soon_rect)
            
            # Draw overlay
            surface.blit(overlay, self.rect)
        
        # Draw popularity stars
        if self.popularity > 0:
            star_size = 12
            star_spacing = 2
            total_width = (star_size + star_spacing) * 5 - star_spacing
            
            star_start_x = self.rect.right - self.theme.get_spacing("medium") - total_width
            star_y = title_rect.centery
            
            for i in range(5):
                star_rect = pygame.Rect(
                    star_start_x + (star_size + star_spacing) * i,
                    star_y - star_size // 2,
                    star_size,
                    star_size
                )
                
                # Determine if this star should be filled
                filled = (i + 1) * 2 <= self.popularity
                half_filled = (i * 2 < self.popularity < (i + 1) * 2)
                
                if filled:
                    # Draw filled star with gradient
                    star_gradient = pygame.Surface((star_size, star_size), pygame.SRCALPHA)
                    
                    # Get gradient colors
                    star_color_top = self.theme.get_color("warning")
                    star_color_bottom = tuple(max(0, c - 30) for c in star_color_top)
                    
                    # Draw vertical gradient
                    for y in range(star_size):
                        # Calculate color for this line
                        progress = y / star_size
                        color = tuple(
                            int(star_color_top[i] * (1 - progress) + star_color_bottom[i] * progress)
                            for i in range(3)
                        )
                        
                        # Draw horizontal line with this color
                        pygame.draw.line(
                            star_gradient,
                            color,
                            (0, y),
                            (star_size - 1, y)
                        )
                    
                    # Draw star shape
                    pygame.draw.polygon(
                        star_gradient,
                        (255, 255, 255, 0),  # Transparent
                        self._get_star_points(pygame.Rect(0, 0, star_size, star_size))
                    )
                    
                    # Draw star
                    surface.blit(star_gradient, star_rect)
                    
                    # Add subtle border
                    pygame.draw.polygon(
                        surface,
                        self.theme.get_color("warning"),
                        self._get_star_points(star_rect),
                        1
                    )
                elif half_filled:
                    # Draw half-filled star (simplified)
                    pygame.draw.polygon(
                        surface,
                        self.theme.get_color("warning"),
                        self._get_star_points(star_rect),
                        1
                    )
                    
                    # Draw half fill
                    half_rect = pygame.Rect(
                        star_rect.x,
                        star_rect.y,
                        star_rect.width // 2,
                        star_rect.height
                    )
                    
                    # Create half star surface
                    half_star = pygame.Surface((star_size, star_size), pygame.SRCALPHA)
                    
                    # Draw star shape
                    pygame.draw.polygon(
                        half_star,
                        self.theme.get_color("warning"),
                        self._get_star_points(pygame.Rect(0, 0, star_size, star_size))
                    )
                    
                    # Create mask for left half
                    mask = pygame.Surface((star_size, star_size), pygame.SRCALPHA)
                    pygame.draw.rect(
                        mask,
                        (255, 255, 255, 255),
                        pygame.Rect(0, 0, star_size // 2, star_size)
                    )
                    
                    # Apply mask
                    half_star.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    
                    # Draw half star
                    surface.blit(half_star, star_rect)
                else:
                    # Draw empty star
                    pygame.draw.polygon(
                        surface,
                        self.theme.get_color("text_secondary"),
                        self._get_star_points(star_rect),
                        1
                    )
    
    def _start_animation(self, target: float):
        """
        Start a new animation.
        
        Args:
            target: Target animation value
        """
        self.animation_start_time = time.time()
        self.animation_target = target
    
    def _update_animations(self):
        """Update all animations."""
        current_time = time.time()
        
        # Update main animation
        elapsed = current_time - self.animation_start_time
        progress = min(1.0, elapsed / self.animation_duration)
        
        # Smooth easing function
        eased_progress = progress * (2 - progress)
        
        # Update animation progress
        start_value = self.animation_progress
        target_value = self.animation_target
        self.animation_progress = start_value + (target_value - start_value) * eased_progress
        
        # Update pulse effect
        self.pulse_time = current_time
    
    def _get_star_points(self, rect: pygame.Rect) -> List[Tuple[int, int]]:
        """
        Get the points for drawing a star.
        
        Args:
            rect: Rectangle containing the star
            
        Returns:
            List of points for drawing the star
        """
        cx, cy = rect.centerx, rect.centery
        r_outer = rect.width / 2
        r_inner = r_outer * 0.4
        
        points = []
        for i in range(5):
            # Outer points
            angle_outer = math.pi / 2 + i * 2 * math.pi / 5
            x_outer = cx + r_outer * math.cos(angle_outer)
            y_outer = cy - r_outer * math.sin(angle_outer)
            points.append((x_outer, y_outer))
            
            # Inner points
            angle_inner = math.pi / 2 + (i + 0.5) * 2 * math.pi / 5
            x_inner = cx + r_inner * math.cos(angle_inner)
            y_inner = cy - r_inner * math.sin(angle_inner)
            points.append((x_inner, y_inner))
        
        return points
class MouseController:
    """
    Enhanced mouse controller that implements UX design principles
    for a more immersive and intuitive arcade experience.
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize the MouseController with screen dimensions.
        
        Args:
            screen_width: Width of the game screen
            screen_height: Height of the game screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_state = MouseState.NORMAL
        self.hover_elements = []
        self.clickable_elements = []
        self.draggable_elements = []
        
        # Custom cursors for different states
        self.cursors = {}
        self.current_cursor = None
        
        # Feedback mechanisms
        self.visual_feedback_enabled = True
        self.audio_feedback_enabled = True
        self.haptic_feedback_enabled = False  # Default off as not all systems support it
        
        # Tracking for animations and effects
        self.last_click_time = 0
        self.last_click_position = (0, 0)
        self.click_animations = []
        
        # Performance tracking (for Doherty Threshold)
        self.interaction_start_time = 0
        self.response_times = []
        
        # Load default cursors
        self._load_default_cursors()
    
    def _load_default_cursors(self):
        """
        Load default cursor images for different mouse states.
        Implements Aesthetic-Usability Effect by using visually pleasing cursors.
        """
        # In a real implementation, these would load actual cursor images
        # For now, we'll use pygame's system cursors
        self.cursors[MouseState.NORMAL] = pygame.SYSTEM_CURSOR_ARROW
        self.cursors[MouseState.HOVER] = pygame.SYSTEM_CURSOR_HAND
        self.cursors[MouseState.CLICK] = pygame.SYSTEM_CURSOR_HAND
        self.cursors[MouseState.DRAG] = pygame.SYSTEM_CURSOR_SIZEALL
        self.cursors[MouseState.DISABLED] = pygame.SYSTEM_CURSOR_NO
        
        # Set the default cursor
        self.set_cursor(MouseState.NORMAL)
    
    def set_cursor(self, state: MouseState):
        """
        Set the cursor based on the current mouse state.
        
        Args:
            state: The MouseState to set the cursor to
        """
        if state in self.cursors:
            pygame.mouse.set_cursor(self.cursors[state])
            self.current_state = state
    
    def register_hoverable(self, element_id: str, rect: pygame.Rect, 
                          hover_callback: Callable = None):
        """
        Register an element that can be hovered over.
        Implements Fitts's Law by tracking interactive elements.
        
        Args:
            element_id: Unique identifier for the element
            rect: The rectangle defining the element's boundaries
            hover_callback: Function to call when element is hovered
        """
        self.hover_elements.append({
            'id': element_id,
            'rect': rect,
            'callback': hover_callback,
            'is_hovered': False
        })
    
    def register_clickable(self, element_id: str, rect: pygame.Rect, 
                          click_callback: Callable, 
                          hover_callback: Callable = None,
                          sound_effect: str = None):
        """
        Register an element that can be clicked.
        Implements multiple UX laws:
        - Fitts's Law: Tracks clickable areas
        - Doherty Threshold: Will measure response time
        - Peak-End Rule: Can provide special effects on click
        
        Args:
            element_id: Unique identifier for the element
            rect: The rectangle defining the element's boundaries
            click_callback: Function to call when element is clicked
            hover_callback: Function to call when element is hovered
            sound_effect: Path to sound effect file to play on click
        """
        self.clickable_elements.append({
            'id': element_id,
            'rect': rect,
            'click_callback': click_callback,
            'hover_callback': hover_callback,
            'sound_effect': sound_effect,
            'is_hovered': False,
            'is_clicked': False,
            'last_click_time': 0
        })
        
        # Also register as hoverable if it has a hover callback
        if hover_callback:
            self.register_hoverable(element_id, rect, hover_callback)
    
    def register_draggable(self, element_id: str, rect: pygame.Rect,
                          drag_start_callback: Callable = None,
                          drag_callback: Callable = None,
                          drag_end_callback: Callable = None):
        """
        Register an element that can be dragged.
        Implements Postel's Law by making interfaces more forgiving with drag operations.
        
        Args:
            element_id: Unique identifier for the element
            rect: The rectangle defining the element's boundaries
            drag_start_callback: Function to call when drag starts
            drag_callback: Function to call during dragging
            drag_end_callback: Function to call when drag ends
        """
        self.draggable_elements.append({
            'id': element_id,
            'rect': rect,
            'drag_start_callback': drag_start_callback,
            'drag_callback': drag_callback,
            'drag_end_callback': drag_end_callback,
            'is_dragging': False,
            'drag_offset': (0, 0)
        })
    
    def update(self, events: List[pygame.event.Event]) -> Dict:
        """
        Update the mouse controller state based on pygame events.
        Implements Doherty Threshold by ensuring responsive feedback.
        
        Args:
            events: List of pygame events to process
            
        Returns:
            Dictionary containing information about mouse interactions
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        
        # Track interactions for performance metrics
        current_time = time.time()
        
        # Process events
        clicked_elements = []
        hovered_elements = []
        dragged_elements = []
        
        # Check for hover events (Jakob's Law - familiar patterns of interaction)
        for element in self.hover_elements:
            was_hovered = element['is_hovered']
            is_hovered = element['rect'].collidepoint(mouse_pos)
            
            if is_hovered != was_hovered:
                element['is_hovered'] = is_hovered
                if is_hovered:
                    hovered_elements.append(element['id'])
                    if element['callback']:
                        element['callback'](True)
                    # Change cursor to hover state
                    self.set_cursor(MouseState.HOVER)
                else:
                    if element['callback']:
                        element['callback'](False)
                    # Reset cursor if not hovering over anything
                    if not any(e['is_hovered'] for e in self.hover_elements):
                        self.set_cursor(MouseState.NORMAL)
        
        # Process mouse events
        for event in events:
            # Click events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.interaction_start_time = current_time
                self.last_click_position = mouse_pos
                
                # Check for clicks on elements
                for element in self.clickable_elements:
                    if element['rect'].collidepoint(mouse_pos):
                        element['is_clicked'] = True
                        self.set_cursor(MouseState.CLICK)
                        
                        # Start measuring response time (Doherty Threshold)
                        start_time = time.time()
                        
                        # Execute callback
                        if element['click_callback']:
                            element['click_callback']()
                        
                        # Play sound effect if available
                        if element['sound_effect'] and self.audio_feedback_enabled:
                            # In a real implementation, this would play the sound
                            pass
                        
                        # Add visual feedback (Aesthetic-Usability Effect)
                        if self.visual_feedback_enabled:
                            self._add_click_animation(mouse_pos)
                        
                        # Record response time
                        response_time = (time.time() - start_time) * 1000  # ms
                        self.response_times.append(response_time)
                        
                        clicked_elements.append(element['id'])
                
                # Check for drag starts
                for element in self.draggable_elements:
                    if element['rect'].collidepoint(mouse_pos):
                        element['is_dragging'] = True
                        element['drag_offset'] = (
                            mouse_pos[0] - element['rect'].x,
                            mouse_pos[1] - element['rect'].y
                        )
                        self.set_cursor(MouseState.DRAG)
                        
                        if element['drag_start_callback']:
                            element['drag_start_callback'](mouse_pos)
            
            # Release events
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Reset click states
                for element in self.clickable_elements:
                    element['is_clicked'] = False
                
                # End drags
                for element in self.draggable_elements:
                    if element['is_dragging']:
                        element['is_dragging'] = False
                        if element['drag_end_callback']:
                            element['drag_end_callback'](mouse_pos)
                        dragged_elements.append(element['id'])
                
                # Reset cursor based on hover state
                if any(e['is_hovered'] for e in self.hover_elements):
                    self.set_cursor(MouseState.HOVER)
                else:
                    self.set_cursor(MouseState.NORMAL)
        
        # Handle dragging (Postel's Law - forgiving interfaces)
        for element in self.draggable_elements:
            if element['is_dragging']:
                new_x = mouse_pos[0] - element['drag_offset'][0]
                new_y = mouse_pos[1] - element['drag_offset'][1]
                
                # Apply constraints to keep within screen (Postel's Law)
                new_x = max(0, min(self.screen_width - element['rect'].width, new_x))
                new_y = max(0, min(self.screen_height - element['rect'].height, new_y))
                
                element['rect'].x = new_x
                element['rect'].y = new_y
                
                if element['drag_callback']:
                    element['drag_callback'](mouse_pos, (new_x, new_y))
                
                dragged_elements.append(element['id'])
        
        # Update animations
        self._update_animations()
        
        return {
            'clicked': clicked_elements,
            'hovered': hovered_elements,
            'dragged': dragged_elements,
            'position': mouse_pos,
            'buttons': mouse_buttons
        }
    
    def _add_click_animation(self, position: Tuple[int, int]):
        """
        Add a click animation at the specified position.
        Implements Aesthetic-Usability Effect and Peak-End Rule.
        
        Args:
            position: (x, y) position for the animation
        """
        self.click_animations.append({
            'position': position,
            'start_time': time.time(),
            'duration': 0.3,  # seconds
            'radius': 0,
            'max_radius': 30,
            'color': (255, 255, 255, 255)  # RGBA
        })
    
    def _update_animations(self):
        """Update all active animations."""
        current_time = time.time()
        
        # Update click animations
        for i in range(len(self.click_animations) - 1, -1, -1):
            anim = self.click_animations[i]
            elapsed = current_time - anim['start_time']
            
            if elapsed >= anim['duration']:
                # Remove completed animations
                self.click_animations.pop(i)
            else:
                # Update animation properties
                progress = elapsed / anim['duration']
                anim['radius'] = int(anim['max_radius'] * progress)
                # Fade out
                alpha = int(255 * (1 - progress))
                anim['color'] = (anim['color'][0], anim['color'][1], anim['color'][2], alpha)
    
    def draw_effects(self, surface: pygame.Surface):
        """
        Draw all visual effects on the given surface.
        Implements Aesthetic-Usability Effect.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw click animations
        for anim in self.click_animations:
            # Create a surface for the circle with alpha
            anim_surface = pygame.Surface((anim['radius'] * 2, anim['radius'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                anim_surface,
                anim['color'],
                (anim['radius'], anim['radius']),
                anim['radius'],
                2  # Line width
            )
            
            # Position the animation centered on the click
            pos = (
                anim['position'][0] - anim['radius'],
                anim['position'][1] - anim['radius']
            )
            surface.blit(anim_surface, pos)
    
    def get_performance_metrics(self) -> Dict:
        """
        Get performance metrics for UX optimization.
        Implements Doherty Threshold by tracking response times.
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.response_times:
            return {'average_response_time': 0, 'meets_doherty_threshold': True}
        
        avg_response_time = sum(self.response_times) / len(self.response_times)
        meets_threshold = avg_response_time < 400  # Doherty Threshold is 400ms
        
        return {
            'average_response_time': avg_response_time,
            'meets_doherty_threshold': meets_threshold,
            'response_times': self.response_times[-10:]  # Last 10 responses
        }
