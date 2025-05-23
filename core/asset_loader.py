"""
SoulCoreLegacy Arcade - Asset Loader
-----------------------------------
This module provides functions for loading and managing game assets.
"""

import os
import pygame
from pygame import mixer
import io
import base64
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT

# Dictionary to cache loaded assets
_image_cache = {}
_sound_cache = {}
_font_cache = {}

def get_asset_path(game_id, filename):
    """
    Constructs the path to a game asset.
    
    Args:
        game_id (str): The ID of the game (or 'shell' for shell assets)
        filename (str): The filename of the asset
        
    Returns:
        str: The full path to the asset
    """
    if game_id == "shell":
        return os.path.join("shell", "assets", filename)
    else:
        return os.path.join("games", game_id, "assets", filename)

def load_image(game_id, filename, scale=1.0, convert_alpha=True):
    """
    Loads an image asset, with caching.
    
    Args:
        game_id (str): The ID of the game (or 'shell' for shell assets)
        filename (str): The filename of the image
        scale (float): Scale factor to resize the image
        convert_alpha (bool): Whether to convert the image for alpha transparency
        
    Returns:
        pygame.Surface: The loaded image
    """
    # Create a cache key
    cache_key = f"{game_id}:{filename}:{scale}:{convert_alpha}"
    
    # Check if the image is already cached
    if cache_key in _image_cache:
        return _image_cache[cache_key]
    
    # Load the image
    path = get_asset_path(game_id, filename)
    try:
        image = pygame.image.load(path)
        
        # Convert the image for better performance
        if convert_alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
        
        # Scale the image if needed
        if scale != 1.0:
            new_width = int(image.get_width() * scale)
            new_height = int(image.get_height() * scale)
            image = pygame.transform.scale(image, (new_width, new_height))
        
        # Cache the image
        _image_cache[cache_key] = image
        return image
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image {path}: {e}")
        # Return a placeholder image (a colored rectangle)
        placeholder = pygame.Surface((50, 50))
        placeholder.fill((255, 0, 255))  # Magenta for missing textures
        return placeholder

def create_simple_image(width, height, color):
    """
    Creates a simple colored surface.
    
    Args:
        width (int): The width of the image
        height (int): The height of the image
        color (tuple): The RGB color of the image
        
    Returns:
        pygame.Surface: The created image
    """
    image = pygame.Surface((width, height))
    image.fill(color)
    return image

def create_circle_image(radius, color, border_width=0, border_color=None):
    """
    Creates a circular image.
    
    Args:
        radius (int): The radius of the circle
        color (tuple): The RGB color of the circle
        border_width (int): The width of the border (0 for no border)
        border_color (tuple): The RGB color of the border
        
    Returns:
        pygame.Surface: The created image
    """
    diameter = radius * 2
    image = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
    
    # Draw the circle
    pygame.draw.circle(image, color, (radius, radius), radius)
    
    # Draw the border if needed
    if border_width > 0 and border_color:
        pygame.draw.circle(image, border_color, (radius, radius), radius, border_width)
    
    return image

def create_rounded_rect_image(width, height, color, radius=10, border_width=0, border_color=None):
    """
    Creates a rounded rectangle image.
    
    Args:
        width (int): The width of the rectangle
        height (int): The height of the rectangle
        color (tuple): The RGB color of the rectangle
        radius (int): The radius of the corners
        border_width (int): The width of the border (0 for no border)
        border_color (tuple): The RGB color of the border
        
    Returns:
        pygame.Surface: The created image
    """
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    rect = pygame.Rect(0, 0, width, height)
    
    # Draw the rounded rectangle
    pygame.draw.rect(image, color, rect, border_radius=radius)
    
    # Draw the border if needed
    if border_width > 0 and border_color:
        pygame.draw.rect(image, border_color, rect, border_width, border_radius=radius)
    
    return image

def load_sound(game_id, filename):
    """
    Loads a sound asset, with caching.
    
    Args:
        game_id (str): The ID of the game (or 'shell' for shell assets)
        filename (str): The filename of the sound
        
    Returns:
        pygame.mixer.Sound: The loaded sound
    """
    # Create a cache key
    cache_key = f"{game_id}:{filename}"
    
    # Check if the sound is already cached
    if cache_key in _sound_cache:
        return _sound_cache[cache_key]
    
    # Load the sound
    path = get_asset_path(game_id, filename)
    try:
        sound = mixer.Sound(path)
        
        # Cache the sound
        _sound_cache[cache_key] = sound
        return sound
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading sound {path}: {e}")
        return None

def load_font(name, size):
    """
    Loads a font, with caching.
    
    Args:
        name (str): The name of the font
        size (int): The size of the font
        
    Returns:
        pygame.font.Font: The loaded font
    """
    # Create a cache key
    cache_key = f"{name}:{size}"
    
    # Check if the font is already cached
    if cache_key in _font_cache:
        return _font_cache[cache_key]
    
    # Load the font
    try:
        font = pygame.font.SysFont(name, size)
        
        # Cache the font
        _font_cache[cache_key] = font
        return font
    except pygame.error as e:
        print(f"Error loading font {name} at size {size}: {e}")
        # Return a default font
        return pygame.font.SysFont(None, size)

def create_gradient_background(width, height, color1, color2, vertical=True):
    """
    Creates a gradient background.
    
    Args:
        width (int): The width of the background
        height (int): The height of the background
        color1 (tuple): The RGB color at the start of the gradient
        color2 (tuple): The RGB color at the end of the gradient
        vertical (bool): Whether the gradient is vertical (True) or horizontal (False)
        
    Returns:
        pygame.Surface: The created background
    """
    background = pygame.Surface((width, height))
    
    if vertical:
        for y in range(height):
            # Calculate the ratio of the current position
            ratio = y / height
            
            # Interpolate between the two colors
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            
            # Draw a horizontal line with the calculated color
            pygame.draw.line(background, (r, g, b), (0, y), (width, y))
    else:
        for x in range(width):
            # Calculate the ratio of the current position
            ratio = x / width
            
            # Interpolate between the two colors
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            
            # Draw a vertical line with the calculated color
            pygame.draw.line(background, (r, g, b), (x, 0), (x, height))
    
    return background

def clear_cache():
    """Clears all asset caches."""
    _image_cache.clear()
    _sound_cache.clear()
    _font_cache.clear()
