"""
SoulCoreLegacy Arcade - Asteroids Game Bullet
-------------------------------------------
This module defines the bullets fired by the player.
"""

import pyglet
from . import physicalobject, resources

class Bullet(physicalobject.PhysicalObject):
    """
    Bullets fired by the player.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.bullet_image, *args, **kwargs)
        
        # Set bullet properties
        self.is_bullet = True
        
        # Schedule bullet to die after 0.5 seconds
        pyglet.clock.schedule_once(self.die, 0.5)
    
    def die(self, dt):
        """
        Mark the bullet as dead after its lifespan.
        
        Args:
            dt (float): The time step
        """
        self.dead = True
