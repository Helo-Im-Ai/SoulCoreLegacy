"""
SoulCoreLegacy Arcade - Pong AI
------------------------------
This module implements the AI for the Pong game.
"""

import random
from core.config import SCREEN_HEIGHT

class PongAI:
    """
    A simple AI for the Pong game.
    """
    
    def __init__(self, paddle, ball):
        """
        Initialize the AI.
        
        Args:
            paddle (Paddle): The AI's paddle
            ball (Ball): The ball object
        """
        self.paddle = paddle
        self.ball = ball
        
        # Reaction speed (lower = faster)
        self.reaction_speed = 0.1
        
        # Difficulty level (0.0 to 1.0)
        self.difficulty = 0.7
    
    def update(self):
        """Update the AI's paddle position based on the ball's position."""
        # Only move if the ball is moving towards the AI's paddle
        if self.ball.velocity_x > 0:
            # Calculate the target y position
            target_y = self.predict_ball_y()
            
            # Move the paddle towards the target position
            if self.paddle.y + self.paddle.height / 2 < target_y - 10:
                self.paddle.moving_up = False
                self.paddle.moving_down = True
            elif self.paddle.y + self.paddle.height / 2 > target_y + 10:
                self.paddle.moving_up = True
                self.paddle.moving_down = False
            else:
                self.paddle.moving_up = False
                self.paddle.moving_down = False
        else:
            # Move towards the center when the ball is moving away
            if self.paddle.y + self.paddle.height / 2 < self.ball.initial_y - 10:
                self.paddle.moving_up = False
                self.paddle.moving_down = True
            elif self.paddle.y + self.paddle.height / 2 > self.ball.initial_y + 10:
                self.paddle.moving_up = True
                self.paddle.moving_down = False
            else:
                self.paddle.moving_up = False
                self.paddle.moving_down = False
    
    def predict_ball_y(self):
        """
        Predict where the ball will be when it reaches the AI's paddle.
        
        Returns:
            float: The predicted y-coordinate of the ball
        """
        # If the ball is moving away from the AI, return the center
        if self.ball.velocity_x <= 0:
            return self.ball.initial_y
        
        # Calculate time to reach the paddle
        distance_x = self.paddle.x - self.ball.x
        if self.ball.velocity_x == 0:  # Avoid division by zero
            return self.ball.y
            
        time_to_reach = distance_x / self.ball.velocity_x
        
        # Predict the y position
        predicted_y = self.ball.y + self.ball.velocity_y * time_to_reach
        
        # Account for bounces off the top and bottom walls
        screen_height = SCREEN_HEIGHT
        while predicted_y < 0 or predicted_y > screen_height:
            if predicted_y < 0:
                predicted_y = -predicted_y
            elif predicted_y > screen_height:
                predicted_y = 2 * screen_height - predicted_y
        
        # Add some randomness based on difficulty
        # Lower difficulty means more randomness
        if self.difficulty < 1.0:
            max_error = (1.0 - self.difficulty) * self.paddle.height
            error = random.uniform(-max_error, max_error)
            predicted_y += error
        
        return predicted_y
