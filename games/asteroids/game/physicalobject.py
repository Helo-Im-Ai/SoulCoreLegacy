"""
SoulCoreLegacy Arcade - Asteroids Game Physical Object
---------------------------------------------------
This module defines the base class for all physical objects in the game.
"""

import pyglet
from . import util

class PhysicalObject(pyglet.sprite.Sprite):
    """
    A sprite with physical properties such as velocity and collision detection.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Physical properties
        self.velocity_x, self.velocity_y = 0.0, 0.0
        
        # Game state
        self.dead = False
        self.new_objects = []
        
        # Collision properties
        self.reacts_to_bullets = True
        self.is_bullet = False
    
    def update(self, dt):
        """
        Update the object's position based on its velocity.
        
        Args:
            dt (float): The time step
        """
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()
    
    def check_bounds(self):
        """
        Wrap the object around the screen if it goes off the edge.
        """
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = 800 + self.image.width / 2
        max_y = 600 + self.image.height / 2
        
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y
    
    def collides_with(self, other_object):
        """
        Check if this object collides with another object.
        
        Args:
            other_object (PhysicalObject): The object to check collision with
            
        Returns:
            bool: True if the objects collide, False otherwise
        """
        # Skip collision checks for bullets if needed
        if not self.reacts_to_bullets and other_object.is_bullet:
            return False
        if self.is_bullet and not other_object.reacts_to_bullets:
            return False
        
        # Calculate collision distance
        collision_distance = self.image.width/2 + other_object.image.width/2
        actual_distance = util.distance(self.position, other_object.position)
        
        return actual_distance <= collision_distance
    
    def handle_collision_with(self, other_object):
        """
        Handle collision with another object.
        
        Args:
            other_object (PhysicalObject): The object collided with
        """
        if other_object.__class__ == self.__class__:
            self.dead = False
        else:
            self.dead = True
