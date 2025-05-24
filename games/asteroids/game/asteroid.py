"""
SoulCoreLegacy Arcade - Asteroids Game Asteroid
---------------------------------------------
This module defines the asteroids in the game.
"""

import random
import pyglet
from . import resources, physicalobject

class Asteroid(physicalobject.PhysicalObject):
    """
    Asteroids that float around the screen and split when hit.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.asteroid_image, *args, **kwargs)
        
        # Set random rotation speed
        self.rotate_speed = random.random() * 100.0 - 50.0
    
    def update(self, dt):
        """
        Update the asteroid's position and rotation.
        
        Args:
            dt (float): The time step
        """
        super().update(dt)
        
        # Rotate the asteroid
        self.rotation += self.rotate_speed * dt
    
    def handle_collision_with(self, other_object):
        """
        Handle collision with another object.
        
        Args:
            other_object (PhysicalObject): The object collided with
        """
        # Call the parent method first
        super().handle_collision_with(other_object)
        
        # If the asteroid is dead and big enough, split it
        if self.dead and self.scale > 0.25:
            # Create 2-3 smaller asteroids
            num_asteroids = random.randint(2, 3)
            for i in range(num_asteroids):
                # Create a new asteroid at the same position
                new_asteroid = Asteroid(x=self.x, y=self.y, batch=self.batch)
                
                # Set random rotation and velocity
                new_asteroid.rotation = random.randint(0, 360)
                new_asteroid.velocity_x = random.random() * 70 + self.velocity_x
                new_asteroid.velocity_y = random.random() * 70 + self.velocity_y
                
                # Make it smaller
                new_asteroid.scale = self.scale * 0.5
                
                # Add it to new objects
                self.new_objects.append(new_asteroid)
