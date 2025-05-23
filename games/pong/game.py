"""
SoulCoreLegacy Arcade - Pong Game
--------------------------------
This module implements the classic Pong game.
"""

import pygame
import time
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, WHITE, PRIMARY_COLOR, SECONDARY_COLOR
from core.asset_loader import load_font
from games.pong.logic import Ball, Paddle, PongLogic
from games.pong.ai import PongAI

class PongGame:
    """
    Implementation of the classic Pong game.
    """
    
    def __init__(self, game_manager):
        """
        Initialize the Pong game.
        
        Args:
            game_manager (GameManager): Reference to the game manager
        """
        self.game_manager = game_manager
        
        # Game state
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.start_time = None
        
        # Create the game objects
        self.reset()
        
        # Create the font for score display
        self.font = load_font("Arial", 36)
        
        # Create the font for messages
        self.message_font = load_font("Arial", 24)
        
        # Get cloud services
        self.storage_service = self.game_manager.get_cloud_service('storage')
        self.analytics_service = self.game_manager.get_cloud_service('analytics')
        self.multiplayer_service = self.game_manager.get_cloud_service('multiplayer')
        
        # Multiplayer state
        self.is_multiplayer = False
        self.session_id = None
        self.player_id = None
    
    def reset(self):
        """Reset the game state."""
        # Create the paddles
        paddle_width = 10
        paddle_height = 100
        paddle_margin = 20
        
        self.player_paddle = Paddle(
            paddle_margin,
            SCREEN_HEIGHT // 2 - paddle_height // 2,
            paddle_width,
            paddle_height,
            WHITE
        )
        
        self.ai_paddle = Paddle(
            SCREEN_WIDTH - paddle_margin - paddle_width,
            SCREEN_HEIGHT // 2 - paddle_height // 2,
            paddle_width,
            paddle_height,
            WHITE
        )
        
        # Create the ball
        self.ball = Ball(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            10,
            WHITE
        )
        
        # Create the game logic
        self.logic = PongLogic(self.ball, self.player_paddle, self.ai_paddle)
        
        # Create the AI
        self.ai = PongAI(self.ai_paddle, self.ball)
        
        # Reset scores
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.start_time = time.time()
        
        # Track game start
        if self.analytics_service:
            self.analytics_service.track_game_start('pong', 'single_player')
    
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        # Handle key presses for paddle movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player_paddle.moving_up = True
            elif event.key == pygame.K_DOWN:
                self.player_paddle.moving_down = True
            # Restart the game if it's over
            elif event.key == pygame.K_SPACE and self.game_over:
                self.reset()
            # Save game state
            elif event.key == pygame.K_s:
                self.save_game_state()
            # Load game state
            elif event.key == pygame.K_l:
                self.load_game_state()
            # Start multiplayer
            elif event.key == pygame.K_m and not self.is_multiplayer:
                self.start_multiplayer()
        
        # Handle key releases for paddle movement
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.player_paddle.moving_up = False
            elif event.key == pygame.K_DOWN:
                self.player_paddle.moving_down = False
    
    def update(self):
        """Update the game state."""
        if not self.game_over:
            # Update the AI if not in multiplayer mode
            if not self.is_multiplayer:
                self.ai.update()
            
            # Update the game logic
            result = self.logic.update()
            
            # Check for scoring
            if result == "player_scored":
                self.player_score += 1
                self.ball.reset()
                
                # Track score event
                if self.analytics_service:
                    self.analytics_service.track_event('player_scored', {
                        'game_id': 'pong',
                        'score': self.player_score
                    })
            elif result == "ai_scored":
                self.ai_score += 1
                self.ball.reset()
                
                # Track score event
                if self.analytics_service:
                    self.analytics_service.track_event('ai_scored', {
                        'game_id': 'pong',
                        'score': self.ai_score
                    })
            
            # Check for game over
            if self.player_score >= 5:
                self.game_over = True
                self.winner = "Player"
                self.track_game_end('win')
            elif self.ai_score >= 5:
                self.game_over = True
                self.winner = "AI"
                self.track_game_end('loss')
            
            # Update multiplayer state
            if self.is_multiplayer and self.multiplayer_service:
                # Send game state
                self.send_multiplayer_state()
                
                # Receive game state
                self.receive_multiplayer_state()
    
    def render(self, screen):
        """
        Render the game.
        
        Args:
            screen (pygame.Surface): The surface to render on
        """
        # Clear the screen
        screen.fill(BG_COLOR)
        
        # Draw the center line
        pygame.draw.aaline(
            screen,
            WHITE,
            (SCREEN_WIDTH // 2, 0),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT)
        )
        
        # Draw the paddles
        self.player_paddle.draw(screen)
        self.ai_paddle.draw(screen)
        
        # Draw the ball
        self.ball.draw(screen)
        
        # Draw the scores
        player_score_text = self.font.render(str(self.player_score), True, PRIMARY_COLOR)
        ai_score_text = self.font.render(str(self.ai_score), True, SECONDARY_COLOR)
        
        screen.blit(player_score_text, (SCREEN_WIDTH // 4, 20))
        screen.blit(ai_score_text, (3 * SCREEN_WIDTH // 4, 20))
        
        # Draw game over message if the game is over
        if self.game_over:
            message = f"{self.winner} wins! Press SPACE to restart."
            message_text = self.message_font.render(message, True, WHITE)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(message_text, message_rect)
        
        # Draw multiplayer status
        if self.is_multiplayer:
            multiplayer_text = self.message_font.render("Multiplayer Mode", True, SECONDARY_COLOR)
            screen.blit(multiplayer_text, (SCREEN_WIDTH // 2 - multiplayer_text.get_width() // 2, 50))
        
        # Draw controls help
        controls_text = self.message_font.render("S: Save  L: Load  M: Multiplayer", True, WHITE)
        screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, SCREEN_HEIGHT - 30))
    
    def save_game_state(self):
        """Save the current game state."""
        if not self.storage_service:
            print("Storage service not available.")
            return
        
        state = {
            'player_score': self.player_score,
            'ai_score': self.ai_score,
            'ball_x': self.ball.x,
            'ball_y': self.ball.y,
            'ball_velocity_x': self.ball.velocity_x,
            'ball_velocity_y': self.ball.velocity_y,
            'player_paddle_y': self.player_paddle.y,
            'ai_paddle_y': self.ai_paddle.y,
            'game_over': self.game_over,
            'winner': self.winner
        }
        
        # Use 'anonymous' as user_id if not available
        user_id = 'anonymous'
        auth_service = self.game_manager.get_cloud_service('auth')
        if auth_service and auth_service.is_authenticated():
            user = auth_service.get_current_user()
            if user:
                user_id = user.get('sub', 'anonymous')
        
        success = self.storage_service.save_game_state('pong', user_id, state)
        
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
        
        state = self.storage_service.load_game_state('pong', user_id)
        
        if not state:
            print("No saved game state found.")
            return
        
        # Restore game state
        self.player_score = state.get('player_score', 0)
        self.ai_score = state.get('ai_score', 0)
        self.ball.x = state.get('ball_x', SCREEN_WIDTH // 2)
        self.ball.y = state.get('ball_y', SCREEN_HEIGHT // 2)
        self.ball.velocity_x = state.get('ball_velocity_x', 5)
        self.ball.velocity_y = state.get('ball_velocity_y', 0)
        self.player_paddle.y = state.get('player_paddle_y', SCREEN_HEIGHT // 2 - self.player_paddle.height // 2)
        self.ai_paddle.y = state.get('ai_paddle_y', SCREEN_HEIGHT // 2 - self.ai_paddle.height // 2)
        self.game_over = state.get('game_over', False)
        self.winner = state.get('winner', None)
        
        # Update paddle rects
        self.player_paddle.rect.y = self.player_paddle.y
        self.ai_paddle.rect.y = self.ai_paddle.y
        
        print("Game state loaded successfully.")
    
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
            'pong',
            score=self.player_score,
            duration=duration,
            outcome=outcome
        )
        
        # Save high score
        storage_service = self.game_manager.get_cloud_service('storage')
        if storage_service:
            # Use 'anonymous' as user_id if not available
            user_id = 'anonymous'
            auth_service = self.game_manager.get_cloud_service('auth')
            if auth_service and auth_service.is_authenticated():
                user = auth_service.get_current_user()
                if user:
                    user_id = user.get('sub', 'anonymous')
            
            storage_service.save_high_score('pong', user_id, self.player_score, {
                'duration': duration,
                'outcome': outcome
            })
    
    def start_multiplayer(self):
        """Start a multiplayer session."""
        if not self.multiplayer_service:
            print("Multiplayer service not available.")
            return
        
        # Create a session
        session_id = self.multiplayer_service.create_session('pong', 2)
        if not session_id:
            print("Failed to create multiplayer session.")
            return
        
        # Join the session
        player_id = self.multiplayer_service.join_session(session_id, "Player 1")
        if not player_id:
            print("Failed to join multiplayer session.")
            return
        
        self.is_multiplayer = True
        self.session_id = session_id
        self.player_id = player_id
        
        print(f"Started multiplayer session: {session_id}")
        
        # Track multiplayer start
        if self.analytics_service:
            self.analytics_service.track_game_start('pong', 'multiplayer')
    
    def send_multiplayer_state(self):
        """Send the current game state to other players."""
        if not self.is_multiplayer or not self.multiplayer_service:
            return
        
        state = {
            'player_paddle_y': self.player_paddle.y,
            'ball_x': self.ball.x,
            'ball_y': self.ball.y,
            'ball_velocity_x': self.ball.velocity_x,
            'ball_velocity_y': self.ball.velocity_y,
            'player_score': self.player_score,
            'ai_score': self.ai_score
        }
        
        self.multiplayer_service.send_game_state(state)
    
    def receive_multiplayer_state(self):
        """Receive game state from other players."""
        if not self.is_multiplayer or not self.multiplayer_service:
            return
        
        state = self.multiplayer_service.receive_game_state()
        if not state:
            return
        
        # Update opponent paddle position
        if 'player_paddle_y' in state:
            self.ai_paddle.y = state['player_paddle_y']
            self.ai_paddle.rect.y = self.ai_paddle.y
        
        # If we're the second player, update ball position
        if state.get('player_id') != self.player_id:
            if 'ball_x' in state and 'ball_y' in state:
                self.ball.x = SCREEN_WIDTH - state['ball_x']  # Mirror X position
                self.ball.y = state['ball_y']
            
            if 'ball_velocity_x' in state and 'ball_velocity_y' in state:
                self.ball.velocity_x = -state['ball_velocity_x']  # Reverse X velocity
                self.ball.velocity_y = state['ball_velocity_y']
            
            # Update scores
            if 'player_score' in state and 'ai_score' in state:
                self.ai_score = state['player_score']
                self.player_score = state['ai_score']
