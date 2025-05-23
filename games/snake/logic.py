"""
SoulCoreLegacy Arcade - Snake Game Logic
--------------------------------------
This module implements the logic for the Snake game.
"""

import random
import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Snake:
    """
    Represents the snake in the Snake game.
    """
    
    def __init__(self, x, y, block_size, color):
        """
        Initialize the snake.
        
        Args:
            x (int): The x-coordinate of the snake's head
            y (int): The y-coordinate of the snake's head
            block_size (int): The size of each snake segment
            color (tuple): The RGB color of the snake
        """
        self.block_size = block_size
        self.color = color
        self.speed = block_size
        
        # Initial position and direction
        self.x_change = 0
        self.y_change = 0
        self.direction = "RIGHT"
        
        # Create the snake body (list of positions)
        self.body = []
        self.head = [x, y]
        self.body.append(self.head)
        
        # Add two more segments to start with
        self.body.append([x - block_size, y])
        self.body.append([x - 2 * block_size, y])
        
        # Track the length
        self.length = 3
    
    def update(self):
        """
        Update the snake's position.
        
        Returns:
            bool: True if the snake is still alive, False if it collided with itself
        """
        # Update the head position based on the current direction
        new_head = [self.head[0] + self.x_change, self.head[1] + self.y_change]
        
        # Check for collision with self
        if new_head in self.body[1:]:
            return False
        
        # Add the new head to the body
        self.body.insert(0, new_head)
        self.head = new_head
        
        # Remove the tail if the snake hasn't grown
        if len(self.body) > self.length:
            self.body.pop()
        
        return True
    
    def grow(self):
        """Increase the length of the snake."""
        self.length += 1
    
    def change_direction(self, direction):
        """
        Change the direction of the snake.
        
        Args:
            direction (str): The new direction ("UP", "DOWN", "LEFT", "RIGHT")
        """
        # Prevent the snake from reversing direction
        if direction == "UP" and self.direction != "DOWN":
            self.x_change = 0
            self.y_change = -self.speed
            self.direction = "UP"
        elif direction == "DOWN" and self.direction != "UP":
            self.x_change = 0
            self.y_change = self.speed
            self.direction = "DOWN"
        elif direction == "LEFT" and self.direction != "RIGHT":
            self.x_change = -self.speed
            self.y_change = 0
            self.direction = "LEFT"
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.x_change = self.speed
            self.y_change = 0
            self.direction = "RIGHT"
    
    def check_boundary_collision(self, wrap_around=False):
        """
        Check if the snake has collided with the boundaries.
        
        Args:
            wrap_around (bool): If True, the snake wraps around the screen
            
        Returns:
            bool: True if the snake is still alive, False if it collided with the boundary
        """
        if wrap_around:
            # Wrap around the screen
            if self.head[0] >= SCREEN_WIDTH:
                self.head[0] = 0
            elif self.head[0] < 0:
                self.head[0] = SCREEN_WIDTH - self.block_size
            
            if self.head[1] >= SCREEN_HEIGHT:
                self.head[1] = 0
            elif self.head[1] < 0:
                self.head[1] = SCREEN_HEIGHT - self.block_size
            
            # Update the body[0] (head) with the wrapped position
            self.body[0] = self.head
            
            return True
        else:
            # Check for boundary collision
            if (self.head[0] >= SCREEN_WIDTH or self.head[0] < 0 or
                self.head[1] >= SCREEN_HEIGHT or self.head[1] < 0):
                return False
            
            return True
    
    def draw(self, screen):
        """
        Draw the snake.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Draw each segment of the snake
        for i, segment in enumerate(self.body):
            # Draw the head in a slightly different color
            if i == 0:
                # Make the head a bit brighter
                head_color = tuple(min(c + 50, 255) for c in self.color)
                pygame.draw.rect(screen, head_color, [segment[0], segment[1], self.block_size, self.block_size])
                
                # Draw eyes
                eye_size = max(2, self.block_size // 5)
                eye_offset = self.block_size // 4
                
                if self.direction == "RIGHT":
                    pygame.draw.circle(screen, (0, 0, 0), (segment[0] + self.block_size - eye_offset, segment[1] + eye_offset), eye_size)
                    pygame.draw.circle(screen, (0, 0, 0), (segment[0] + self.block_size - eye_offset, segment[1] + self.block_size - eye_offset), eye_size)
                elif self.direction == "LEFT":
                    pygame.draw.circle(screen, (0, 0, 0), (segment[0] + eye_offset, segment[1] + eye_offset), eye_size)
                    pygame.draw.circle(screen, (0, 0, 0), (segment[0] + eye_offset, segment[1] + self.block_size - eye_offset), eye_size)
                elif self.direction == "UP":
                    pygame.draw.circle(screen, (0, 0, 0), (segment[0] + eye_offset, segment[1] + eye_offset), eye_size)
                    pygame.draw.circle(screen, (0, 0, 0), (segment[0] + self.block_size - eye_offset, segment[1] + eye_offset), eye_size)
                elif self.direction == "DOWN":
                    pygame.draw.circle(screen, (0, 0, 0), (segment[0] + eye_offset, segment[1] + self.block_size - eye_offset), eye_size)
                    pygame.draw.circle(screen, (0, 0, 0), (segment[0] + self.block_size - eye_offset, segment[1] + self.block_size - eye_offset), eye_size)
            else:
                pygame.draw.rect(screen, self.color, [segment[0], segment[1], self.block_size, self.block_size])
            
            # Add a small border to each segment
            pygame.draw.rect(screen, (0, 0, 0), [segment[0], segment[1], self.block_size, self.block_size], 1)

class Food:
    """
    Represents the food in the Snake game.
    """
    
    def __init__(self, block_size, color):
        """
        Initialize the food.
        
        Args:
            block_size (int): The size of the food
            color (tuple): The RGB color of the food
        """
        self.block_size = block_size
        self.color = color
        self.position = [0, 0]
        self.respawn()
    
    def respawn(self, snake_body=None):
        """
        Respawn the food at a random position.
        
        Args:
            snake_body (list): The snake's body to avoid spawning food on the snake
        """
        # Calculate the number of possible positions
        grid_width = SCREEN_WIDTH // self.block_size
        grid_height = SCREEN_HEIGHT // self.block_size
        
        # Generate a random position
        x = random.randint(0, grid_width - 1) * self.block_size
        y = random.randint(0, grid_height - 1) * self.block_size
        
        # Make sure the food doesn't spawn on the snake
        if snake_body:
            while [x, y] in snake_body:
                x = random.randint(0, grid_width - 1) * self.block_size
                y = random.randint(0, grid_height - 1) * self.block_size
        
        self.position = [x, y]
    
    def draw(self, screen):
        """
        Draw the food.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Draw the food as a circle
        center_x = self.position[0] + self.block_size // 2
        center_y = self.position[1] + self.block_size // 2
        radius = self.block_size // 2
        
        pygame.draw.circle(screen, self.color, (center_x, center_y), radius)
        
        # Add a small shine effect
        shine_radius = radius // 2
        shine_offset = radius // 3
        pygame.draw.circle(screen, (255, 255, 255), (center_x - shine_offset, center_y - shine_offset), shine_radius)

class SnakeLogic:
    """
    Implements the game logic for Snake.
    """
    
    def __init__(self, block_size, snake_color, food_color, wrap_around=False):
        """
        Initialize the game logic.
        
        Args:
            block_size (int): The size of each snake segment and food
            snake_color (tuple): The RGB color of the snake
            food_color (tuple): The RGB color of the food
            wrap_around (bool): If True, the snake wraps around the screen
        """
        # Calculate the grid size
        self.grid_width = SCREEN_WIDTH // block_size
        self.grid_height = SCREEN_HEIGHT // block_size
        self.block_size = block_size
        
        # Create the snake at the center of the screen
        start_x = (self.grid_width // 2) * block_size
        start_y = (self.grid_height // 2) * block_size
        self.snake = Snake(start_x, start_y, block_size, snake_color)
        
        # Create the food
        self.food = Food(block_size, food_color)
        self.food.respawn(self.snake.body)
        
        # Game settings
        self.wrap_around = wrap_around
        self.score = 0
        self.game_over = False
    
    def update(self):
        """
        Update the game state.
        
        Returns:
            bool: True if the game is still running, False if game over
        """
        if self.game_over:
            return False
        
        # Update the snake
        if not self.snake.update():
            self.game_over = True
            return False
        
        # Check for boundary collision
        if not self.snake.check_boundary_collision(self.wrap_around):
            self.game_over = True
            return False
        
        # Check for food collision
        if self.snake.head == self.food.position:
            self.snake.grow()
            self.food.respawn(self.snake.body)
            self.score += 1
        
        return True
    
    def change_direction(self, direction):
        """
        Change the direction of the snake.
        
        Args:
            direction (str): The new direction ("UP", "DOWN", "LEFT", "RIGHT")
        """
        self.snake.change_direction(direction)
    
    def draw(self, screen):
        """
        Draw the game.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Draw the snake
        self.snake.draw(screen)
        
        # Draw the food
        self.food.draw(screen)
    
    def reset(self):
        """Reset the game state."""
        # Calculate the grid size
        self.grid_width = SCREEN_WIDTH // self.block_size
        self.grid_height = SCREEN_HEIGHT // self.block_size
        
        # Create the snake at the center of the screen
        start_x = (self.grid_width // 2) * self.block_size
        start_y = (self.grid_height // 2) * self.block_size
        self.snake = Snake(start_x, start_y, self.block_size, self.snake.color)
        
        # Create the food
        self.food.respawn(self.snake.body)
        
        # Reset game state
        self.score = 0
        self.game_over = False
