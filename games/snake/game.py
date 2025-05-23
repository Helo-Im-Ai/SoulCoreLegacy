"""
SoulCoreLegacy Arcade - Snake Game
--------------------------------
This module implements the classic Snake game.
"""

import pygame
import time
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, WHITE, PRIMARY_COLOR, SECONDARY_COLOR
from core.asset_loader import load_font
from games.snake.logic import SnakeLogic

class SnakeGame:
    """
    Implementation of the classic Snake game.
    """
    
    def __init__(self, game_manager):
        """
        Initialize the Snake game.
        
        Args:
            game_manager (GameManager): Reference to the game manager
        """
        self.game_manager = game_manager
        
        # Game settings
        self.block_size = 20
        self.snake_color = (0, 200, 0)  # Green
        self.food_color = (255, 50, 50)  # Red
        self.wrap_around = False  # Whether the snake can wrap around the screen
        self.game_speed = 10  # Frames per second
        
        # Game state
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.paused = False
        self.start_time = None
        
        # Create the game objects
        self.logic = SnakeLogic(self.block_size, self.snake_color, self.food_color, self.wrap_around)
        
        # Create fonts
        self.font = load_font("Arial", 36)
        self.message_font = load_font("Arial", 24)
        self.small_font = load_font("Arial", 18)
        
        # Get cloud services
        self.storage_service = self.game_manager.get_cloud_service('storage')
        self.analytics_service = self.game_manager.get_cloud_service('analytics')
        
        # Load high score
        self.load_high_score()
        
        # Reset the game
        self.reset()
    
    def reset(self):
        """Reset the game state."""
        self.logic.reset()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.start_time = time.time()
        
        # Track game start
        if self.analytics_service:
            self.analytics_service.track_game_start('snake', 'classic')
    
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        if event.type == pygame.KEYDOWN:
            # Game control keys
            if event.key == pygame.K_SPACE:
                if self.game_over:
                    self.reset()
                else:
                    self.paused = not self.paused
            
            # Direction keys
            if not self.paused and not self.game_over:
                if event.key == pygame.K_UP:
                    self.logic.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    self.logic.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.logic.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.logic.change_direction("RIGHT")
            
            # Save/load keys
            if event.key == pygame.K_s:
                self.save_game_state()
            elif event.key == pygame.K_l:
                self.load_game_state()
            
            # Toggle wrap-around mode
            if event.key == pygame.K_w:
                self.wrap_around = not self.wrap_around
                self.logic.wrap_around = self.wrap_around
                
                # Show a message
                print(f"Wrap-around mode: {'ON' if self.wrap_around else 'OFF'}")
            
            # Change game speed
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.game_speed = min(self.game_speed + 1, 20)
                print(f"Game speed: {self.game_speed}")
            elif event.key == pygame.K_MINUS:
                self.game_speed = max(self.game_speed - 1, 5)
                print(f"Game speed: {self.game_speed}")
    
    def update(self):
        """Update the game state."""
        # Don't update if the game is paused or over
        if self.paused or self.game_over:
            return
        
        # Update the game logic at the specified speed
        pygame.time.Clock().tick(self.game_speed)
        
        # Update the game logic
        if self.logic.update():
            # Update the score
            self.score = self.logic.score
            
            # Update high score
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
        else:
            # Game over
            self.game_over = True
            
            # Track game end
            self.track_game_end('loss')
    
    def render(self, screen):
        """
        Render the game.
        
        Args:
            screen (pygame.Surface): The surface to render on
        """
        # Clear the screen
        screen.fill(BG_COLOR)
        
        # Draw the game
        self.logic.draw(screen)
        
        # Draw the score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw the high score
        high_score_text = self.small_font.render(f"High Score: {self.high_score}", True, SECONDARY_COLOR)
        screen.blit(high_score_text, (10, 50))
        
        # Draw game speed
        speed_text = self.small_font.render(f"Speed: {self.game_speed}", True, SECONDARY_COLOR)
        screen.blit(speed_text, (10, 80))
        
        # Draw wrap-around mode
        wrap_text = self.small_font.render(f"Wrap: {'ON' if self.wrap_around else 'OFF'}", True, SECONDARY_COLOR)
        screen.blit(wrap_text, (10, 110))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("Game Over!", True, PRIMARY_COLOR)
            restart_text = self.message_font.render("Press SPACE to restart", True, WHITE)
            
            # Center the text
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            
            # Draw the text
            screen.blit(game_over_text, game_over_rect)
            screen.blit(restart_text, restart_rect)
        
        # Draw paused message
        elif self.paused:
            paused_text = self.font.render("Paused", True, PRIMARY_COLOR)
            resume_text = self.message_font.render("Press SPACE to resume", True, WHITE)
            
            # Center the text
            paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            
            # Draw the text
            screen.blit(paused_text, paused_rect)
            screen.blit(resume_text, resume_rect)
        
        # Draw controls help
        controls_text = self.small_font.render("S: Save  L: Load  W: Toggle Wrap  +/-: Speed", True, WHITE)
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        screen.blit(controls_text, controls_rect)
    
    def save_game_state(self):
        """Save the current game state."""
        if not self.storage_service:
            print("Storage service not available.")
            return
        
        # Create the game state
        state = {
            'score': self.score,
            'snake_body': self.logic.snake.body,
            'snake_direction': self.logic.snake.direction,
            'food_position': self.logic.food.position,
            'wrap_around': self.wrap_around,
            'game_speed': self.game_speed
        }
        
        # Use 'anonymous' as user_id if not available
        user_id = 'anonymous'
        auth_service = self.game_manager.get_cloud_service('auth')
        if auth_service and auth_service.is_authenticated():
            user = auth_service.get_current_user()
            if user:
                user_id = user.get('sub', 'anonymous')
        
        # Save the game state
        success = self.storage_service.save_game_state('snake', user_id, state)
        
        if success:
            print("Game state saved successfully.")
        else:
            print("Failed to save game state.")
    
    def load_game_state(self):
        """Load a saved game state."""
        if not self.storage_service:
            print("Storage service not available.")
            return
        
        # Use 'anonymous' as user_id if not available
        user_id = 'anonymous'
        auth_service = self.game_manager.get_cloud_service('auth')
        if auth_service and auth_service.is_authenticated():
            user = auth_service.get_current_user()
            if user:
                user_id = user.get('sub', 'anonymous')
        
        # Load the game state
        state = self.storage_service.load_game_state('snake', user_id)
        
        if not state:
            print("No saved game state found.")
            return
        
        # Reset the game
        self.logic.reset()
        
        # Restore the game state
        self.score = state.get('score', 0)
        self.logic.score = self.score
        self.wrap_around = state.get('wrap_around', False)
        self.logic.wrap_around = self.wrap_around
        self.game_speed = state.get('game_speed', 10)
        
        # Restore the snake
        snake_body = state.get('snake_body')
        if snake_body and len(snake_body) > 0:
            self.logic.snake.body = snake_body
            self.logic.snake.head = snake_body[0]
            self.logic.snake.length = len(snake_body)
            
            # Restore the direction
            direction = state.get('snake_direction')
            if direction:
                self.logic.snake.direction = direction
                
                # Set the velocity based on the direction
                if direction == "UP":
                    self.logic.snake.x_change = 0
                    self.logic.snake.y_change = -self.logic.snake.speed
                elif direction == "DOWN":
                    self.logic.snake.x_change = 0
                    self.logic.snake.y_change = self.logic.snake.speed
                elif direction == "LEFT":
                    self.logic.snake.x_change = -self.logic.snake.speed
                    self.logic.snake.y_change = 0
                elif direction == "RIGHT":
                    self.logic.snake.x_change = self.logic.snake.speed
                    self.logic.snake.y_change = 0
        
        # Restore the food
        food_position = state.get('food_position')
        if food_position:
            self.logic.food.position = food_position
        
        print("Game state loaded successfully.")
    
    def save_high_score(self):
        """Save the high score."""
        if not self.storage_service:
            return
        
        # Use 'anonymous' as user_id if not available
        user_id = 'anonymous'
        auth_service = self.game_manager.get_cloud_service('auth')
        if auth_service and auth_service.is_authenticated():
            user = auth_service.get_current_user()
            if user:
                user_id = user.get('sub', 'anonymous')
        
        # Save the high score
        self.storage_service.save_high_score('snake', user_id, self.high_score)
    
    def load_high_score(self):
        """Load the high score."""
        if not self.storage_service:
            return
        
        # Use 'anonymous' as user_id if not available
        user_id = 'anonymous'
        auth_service = self.game_manager.get_cloud_service('auth')
        if auth_service and auth_service.is_authenticated():
            user = auth_service.get_current_user()
            if user:
                user_id = user.get('sub', 'anonymous')
        
        # Load high scores
        scores = self.storage_service.get_high_scores('snake', limit=1)
        
        if scores and len(scores) > 0:
            self.high_score = scores[0].get('score', 0)
    
    def track_game_end(self, outcome):
        """
        Track game end analytics.
        
        Args:
            outcome (str): The outcome of the game ('win', 'loss', 'draw')
        """
        if not self.analytics_service:
            return
        
        # Calculate duration
        duration = int(time.time() - self.start_time)
        
        # Track game end
        self.analytics_service.track_game_end(
            'snake',
            score=self.score,
            duration=duration,
            outcome=outcome
        )
