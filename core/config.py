"""
SoulCoreLegacy Arcade - Configuration
------------------------------------
This module contains global configuration settings for the SoulCoreLegacy Arcade.
"""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "SoulCoreLegacy Arcade"
FPS = 60

# Color definitions (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Theme colors
PRIMARY_COLOR = (110, 68, 255)  # Purple
SECONDARY_COLOR = (0, 191, 255)  # Deep Sky Blue
ACCENT_COLOR = (255, 149, 0)  # Orange
BG_COLOR = (18, 18, 37)  # Dark Blue-Purple
TEXT_COLOR = WHITE

# Font settings
FONT_NAME = "Arial"
FONT_SIZE_SMALL = 16
FONT_SIZE_MEDIUM = 24
FONT_SIZE_LARGE = 36
FONT_SIZE_TITLE = 48

# Game settings
GAME_LIST = [
    {
        "id": "pong",
        "name": "Pong",
        "description": "Classic paddle and ball game",
        "thumbnail": "pong/assets/thumbnail.png",
        "implemented": True
    },
    {
        "id": "snake",
        "name": "Snake",
        "description": "Grow your snake by eating food",
        "thumbnail": "snake/assets/thumbnail.png",
        "implemented": True
    },
    {
        "id": "tic_tac_toe",
        "name": "Tic-Tac-Toe",
        "description": "Classic X and O game",
        "thumbnail": "tic_tac_toe/assets/thumbnail.png",
        "implemented": True
    },
    {
        "id": "photon_racer",
        "name": "Photon Racer",
        "description": "Guide a light-ship through a winding tunnel",
        "thumbnail": "photon_racer/assets/thumbnail.png",
        "implemented": True
    },
    {
        "id": "nft_artisan",
        "name": "NFT Artisan",
        "description": "Create unique digital art pieces",
        "thumbnail": "nft_artisan/assets/thumbnail.png",
        "implemented": True
    },
    {
        "id": "asteroids",
        "name": "Asteroids",
        "description": "Destroy asteroids in space",
        "thumbnail": "asteroids/assets/thumbnail.png",
        "implemented": True
    },
    {
        "id": "breakout",
        "name": "Breakout",
        "description": "Break bricks with a bouncing ball",
        "thumbnail": "breakout/assets/thumbnail.png",
        "implemented": False
    },
    {
        "id": "space_invaders",
        "name": "Space Invaders",
        "description": "Defend Earth from alien invaders",
        "thumbnail": "space_invaders/assets/thumbnail.png",
        "implemented": False
    }
]

# Development mode (enables debug features)
DEBUG_MODE = True
