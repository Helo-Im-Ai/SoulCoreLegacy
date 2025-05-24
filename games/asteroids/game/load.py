"""
SoulCoreLegacy Arcade - Asteroids Game Loader
-------------------------------------------
This module provides functions to load game objects.
"""

import random
from . import asteroid, util

def asteroids(num_asteroids, player_position, batch=None):
    """
    Create a list of asteroids.
    
    Args:
        num_asteroids (int): The number of asteroids to create
        player_position (tuple): The player's position (x, y, z)
        batch (pyglet.graphics.Batch): The batch to add the asteroids to
        
    Returns:
        list: A list of asteroid objects
    """
    asteroids_list = []
    
    for i in range(num_asteroids):
        # Start with the player's position
        asteroid_x, asteroid_y, _ = player_position
        
        # Keep generating positions until we find one far enough from the player
        while util.distance((asteroid_x, asteroid_y), player_position) < 100:
            asteroid_x = random.randint(0, 800)
            asteroid_y = random.randint(0, 600)
        
        # Create the asteroid
        new_asteroid = asteroid.Asteroid(x=asteroid_x, y=asteroid_y, batch=batch)
        
        # Set random rotation and velocity
        new_asteroid.rotation = random.randint(0, 360)
        new_asteroid.velocity_x = random.random() * 40
        new_asteroid.velocity_y = random.random() * 40
        
        # Add to the list
        asteroids_list.append(new_asteroid)
    
    return asteroids_list

def player_lives(num_icons, batch=None):
    """
    Create a list of player life icons.
    
    Args:
        num_icons (int): The number of icons to create
        batch (pyglet.graphics.Batch): The batch to add the icons to
        
    Returns:
        list: A list of player life icons
    """
    from . import resources
    import pyglet
    
    player_lives = []
    
    for i in range(num_icons):
        # Create a new sprite
        new_sprite = pyglet.sprite.Sprite(
            img=resources.player_image,
            x=785-i*30, y=585,
            batch=batch
        )
        
        # Scale it down
        new_sprite.scale = 0.5
        
        # Add to the list
        player_lives.append(new_sprite)
    
    return player_lives
