"""
SoulCoreLegacy Arcade - Asteroids Game Player
-------------------------------------------
This module defines the player's ship in the game.
"""

import math
import pyglet
from pyglet.window import key
from . import physicalobject, resources, bullet

class Player(physicalobject.PhysicalObject):
    """
    The player's ship in the Asteroids game.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.player_image, *args, **kwargs)
        
        # Movement properties
        self.thrust = 300.0
        self.rotate_speed = 200.0
        self.bullet_speed = 700.0
        
        # Set up key handler
        self.key_handler = key.KeyStateHandler()
        
        # Set up engine sprite
        self.engine_sprite = pyglet.sprite.Sprite(
            img=resources.engine_image, *args, **kwargs)
        self.engine_sprite.visible = False
        
        # Player doesn't react to bullets
        self.reacts_to_bullets = False
    
    def update(self, dt):
        """
        Update the player's position and rotation based on input.
        
        Args:
            dt (float): The time step
        """
        # Call the parent update method
        super().update(dt)
        
        # Rotate the ship
        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt
        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt
        
        # Apply thrust
        if self.key_handler[key.UP]:
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt
            self.velocity_x += force_x
            self.velocity_y += force_y
            
            # Update engine sprite
            self.engine_sprite.rotation = self.rotation
            self.engine_sprite.x = self.x
            self.engine_sprite.y = self.y
            self.engine_sprite.visible = True
        else:
            self.engine_sprite.visible = False
    
    def on_key_press(self, symbol, modifiers):
        """
        Handle key press events.
        
        Args:
            symbol (int): The key symbol
            modifiers (int): Key modifiers
        """
        if symbol == key.SPACE:
            self.fire()
    
    def fire(self):
        """
        Fire a bullet from the ship.
        """
        # Calculate bullet position
        angle_radians = -math.radians(self.rotation)
        ship_radius = self.image.width / 2
        bullet_x = self.x + math.cos(angle_radians) * ship_radius
        bullet_y = self.y + math.sin(angle_radians) * ship_radius
        
        # Create the bullet
        new_bullet = bullet.Bullet(bullet_x, bullet_y, batch=self.batch)
        
        # Calculate bullet velocity
        bullet_vx = (
            self.velocity_x +
            math.cos(angle_radians) * self.bullet_speed
        )
        bullet_vy = (
            self.velocity_y +
            math.sin(angle_radians) * self.bullet_speed
        )
        new_bullet.velocity_x = bullet_vx
        new_bullet.velocity_y = bullet_vy
        
        # Add the bullet to new objects
        self.new_objects.append(new_bullet)
    
    def delete(self):
        """
        Delete the player and its engine sprite.
        """
        self.engine_sprite.delete()
        super().delete()
