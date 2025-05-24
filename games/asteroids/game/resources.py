"""
SoulCoreLegacy Arcade - Asteroids Game Resources
---------------------------------------------
This module loads and manages resources for the Asteroids game.
"""

import pyglet

# Set the resource path
pyglet.resource.path = ['games/asteroids/assets']
pyglet.resource.reindex()

# Load the images
player_image = pyglet.resource.image("player.png")
bullet_image = pyglet.resource.image("bullet.png")
asteroid_image = pyglet.resource.image("asteroid.png")
engine_image = pyglet.resource.image("engine_flame.png")

# Center the images
def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

center_image(player_image)
center_image(bullet_image)
center_image(asteroid_image)

# Set the engine flame anchor point
engine_image.anchor_x = engine_image.width * 1.5
engine_image.anchor_y = engine_image.height // 2
