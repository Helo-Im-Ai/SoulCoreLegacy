"""
SoulCoreLegacy Arcade - Pong Game Logic
--------------------------------------
This module implements the logic for the Pong game.
"""

import pygame
import random
import math
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Ball:
    """
    Represents the ball in the Pong game.
    """
    
    def __init__(self, x, y, radius, color):
        """
        Initialize the ball.
        
        Args:
            x (int): The x-coordinate of the ball's center
            y (int): The y-coordinate of the ball's center
            radius (int): The radius of the ball
            color (tuple): The RGB color of the ball
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        
        # Initial position for reset
        self.initial_x = x
        self.initial_y = y
        
        # Set initial velocity
        self.reset_velocity()
    
    def reset(self):
        """Reset the ball to its initial position and randomize velocity."""
        self.x = self.initial_x
        self.y = self.initial_y
        self.reset_velocity()
    
    def reset_velocity(self):
        """Randomize the ball's velocity."""
        # Random horizontal direction
        direction = random.choice([-1, 1])
        
        # Set velocity
        self.velocity_x = direction * 5
        self.velocity_y = random.uniform(-3, 3)
    
    def update(self):
        """Update the ball's position."""
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Bounce off the top and bottom walls
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            self.velocity_y = -self.velocity_y
            
            # Ensure the ball stays within bounds
            if self.y - self.radius <= 0:
                self.y = self.radius
            elif self.y + self.radius >= SCREEN_HEIGHT:
                self.y = SCREEN_HEIGHT - self.radius
    
    def draw(self, screen):
        """
        Draw the ball.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Paddle:
    """
    Represents a paddle in the Pong game.
    """
    
    def __init__(self, x, y, width, height, color):
        """
        Initialize the paddle.
        
        Args:
            x (int): The x-coordinate of the paddle's top-left corner
            y (int): The y-coordinate of the paddle's top-left corner
            width (int): The width of the paddle
            height (int): The height of the paddle
            color (tuple): The RGB color of the paddle
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        
        # Movement flags
        self.moving_up = False
        self.moving_down = False
        
        # Movement speed
        self.speed = 7
        
        # Create the rect for collision detection
        self.rect = pygame.Rect(x, y, width, height)
    
    def update(self):
        """Update the paddle's position based on movement flags."""
        if self.moving_up:
            self.y -= self.speed
        if self.moving_down:
            self.y += self.speed
        
        # Keep the paddle within the screen bounds
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height
        
        # Update the rect
        self.rect.y = self.y
    
    def draw(self, screen):
        """
        Draw the paddle.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        pygame.draw.rect(screen, self.color, self.rect)

class PongLogic:
    """
    Implements the game logic for Pong.
    """
    
    def __init__(self, ball, player_paddle, ai_paddle):
        """
        Initialize the game logic.
        
        Args:
            ball (Ball): The ball object
            player_paddle (Paddle): The player's paddle
            ai_paddle (Paddle): The AI's paddle
        """
        self.ball = ball
        self.player_paddle = player_paddle
        self.ai_paddle = ai_paddle
    
    def update(self):
        """
        Update the game state.
        
        Returns:
            str: The result of the update ("player_scored", "ai_scored", or None)
        """
        # Update the paddles
        self.player_paddle.update()
        self.ai_paddle.update()
        
        # Update the ball
        self.ball.update()
        
        # Check for collisions with paddles
        self._check_paddle_collisions()
        
        # Check if the ball went out of bounds
        if self.ball.x - self.ball.radius <= 0:
            # AI scored
            return "ai_scored"
        elif self.ball.x + self.ball.radius >= SCREEN_WIDTH:
            # Player scored
            return "player_scored"
        
        return None
    
    def _check_paddle_collisions(self):
        """Check for collisions between the ball and paddles."""
        # Check collision with player paddle
        if (self.ball.x - self.ball.radius <= self.player_paddle.x + self.player_paddle.width and
            self.ball.y >= self.player_paddle.y and
            self.ball.y <= self.player_paddle.y + self.player_paddle.height and
            self.ball.velocity_x < 0):
            
            # Reverse the horizontal velocity
            self.ball.velocity_x = -self.ball.velocity_x
            
            # Adjust the vertical velocity based on where the ball hit the paddle
            # This creates more interesting bounces
            relative_intersect_y = (self.player_paddle.y + self.player_paddle.height / 2) - self.ball.y
            normalized_relative_intersect_y = relative_intersect_y / (self.player_paddle.height / 2)
            bounce_angle = normalized_relative_intersect_y * (5 * math.pi / 12)  # Max angle: 75 degrees
            self.ball.velocity_y = -self.ball.velocity_x * -math.sin(bounce_angle)
            
            # Increase the speed slightly
            self.ball.velocity_x *= 1.05
        
        # Check collision with AI paddle
        if (self.ball.x + self.ball.radius >= self.ai_paddle.x and
            self.ball.y >= self.ai_paddle.y and
            self.ball.y <= self.ai_paddle.y + self.ai_paddle.height and
            self.ball.velocity_x > 0):
            
            # Reverse the horizontal velocity
            self.ball.velocity_x = -self.ball.velocity_x
            
            # Adjust the vertical velocity based on where the ball hit the paddle
            relative_intersect_y = (self.ai_paddle.y + self.ai_paddle.height / 2) - self.ball.y
            normalized_relative_intersect_y = relative_intersect_y / (self.ai_paddle.height / 2)
            bounce_angle = normalized_relative_intersect_y * (5 * math.pi / 12)  # Max angle: 75 degrees
            self.ball.velocity_y = -self.ball.velocity_x * math.sin(bounce_angle)
            
            # Increase the speed slightly
            self.ball.velocity_x *= 1.05
