"""
SoulCoreLegacy Arcade - Photon Racer Game
---------------------------------------
This module implements the Photon Racer game, where players guide a light-ship through a winding tunnel.
"""

import pygame
import time
import random
import math
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, WHITE, PRIMARY_COLOR, SECONDARY_COLOR
from core.asset_loader import load_font, create_gradient_background

class PhotonRacerGame:
    """
    Implementation of the Photon Racer game.
    """
    
    def __init__(self, game_manager):
        """
        Initialize the Photon Racer game.
        
        Args:
            game_manager (GameManager): Reference to the game manager
        """
        self.game_manager = game_manager
        
        # Game settings
        self.ship_size = 20
        self.ship_color = (0, 255, 255)  # Cyan
        self.tunnel_width = 150
        self.tunnel_color = (50, 0, 100)  # Dark purple
        self.tunnel_border_color = (100, 50, 200)  # Light purple
        self.speed = 5
        self.difficulty = 1.0
        
        # Game state
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.paused = False
        self.start_time = None
        self.waiting_for_start = True
        
        # Ship position and movement
        self.ship_x = SCREEN_WIDTH // 2
        self.ship_y = SCREEN_HEIGHT - 100
        self.ship_trail = []
        self.max_trail_length = 20
        
        # Tunnel path
        self.tunnel_points = []
        self.generate_tunnel()
        
        # Create fonts
        self.font = load_font("Arial", 36)
        self.message_font = load_font("Arial", 24)
        self.small_font = load_font("Arial", 18)
        
        # Create background
        self.background = create_gradient_background(
            SCREEN_WIDTH, 
            SCREEN_HEIGHT, 
            (0, 0, 30),  # Dark blue
            (30, 0, 60)   # Dark purple
        )
        
        # Get cloud services
        self.storage_service = self.game_manager.get_cloud_service('storage')
        self.analytics_service = self.game_manager.get_cloud_service('analytics')
        
        # Load high score
        self.load_high_score()
        
        # Reset the game
        self.reset()
    
    def reset(self):
        """Reset the game state."""
        # Reset ship position
        self.ship_x = SCREEN_WIDTH // 2
        self.ship_y = SCREEN_HEIGHT - 100
        self.ship_trail = []
        
        # Reset game state
        self.score = 0
        self.game_over = False
        self.paused = False
        self.waiting_for_start = True
        self.start_time = time.time()
        
        # Reset tunnel
        self.generate_tunnel()
        
        # Track game start
        if self.analytics_service:
            self.analytics_service.track_game_start('photon_racer', 'classic')
    
    def generate_tunnel(self):
        """Generate a random tunnel path."""
        self.tunnel_points = []
        
        # Start with a straight section
        center_x = SCREEN_WIDTH // 2
        for y in range(0, -1000, -20):
            self.tunnel_points.append((center_x, y))
        
        # Add some random curves
        for i in range(50):
            last_x, last_y = self.tunnel_points[-1]
            new_y = last_y - 20
            max_deviation = 5 + (i // 5)
            new_x = last_x + random.randint(-max_deviation, max_deviation)
            
            # Keep the tunnel within screen bounds
            new_x = max(self.tunnel_width // 2, min(SCREEN_WIDTH - self.tunnel_width // 2, new_x))
            
            self.tunnel_points.append((new_x, new_y))
    
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        if event.type == pygame.KEYDOWN:
            # Game control keys
            if event.key == pygame.K_SPACE:
                if self.waiting_for_start:
                    self.waiting_for_start = False
                elif self.game_over:
                    self.reset()
                else:
                    self.paused = not self.paused
            
            # Ship movement
            elif event.key == pygame.K_LEFT:
                self.ship_x -= 10
            elif event.key == pygame.K_RIGHT:
                self.ship_x += 10
            
            # Save/load keys
            elif event.key == pygame.K_s:
                self.save_game_state()
            elif event.key == pygame.K_l:
                self.load_game_state()
            
            # Difficulty adjustment
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.speed = min(self.speed + 1, 10)
            elif event.key == pygame.K_MINUS:
                self.speed = max(self.speed - 1, 1)
    
    def update(self):
        """Update the game state."""
        # Don't update if the game is paused, over, or waiting to start
        if self.paused or self.game_over or self.waiting_for_start:
            return
        
        # Move the ship based on keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.ship_x -= 5
        if keys[pygame.K_RIGHT]:
            self.ship_x += 5
        
        # Keep the ship within screen bounds
        self.ship_x = max(0, min(SCREEN_WIDTH, self.ship_x))
        
        # Add current position to trail
        self.ship_trail.append((self.ship_x, self.ship_y))
        
        # Limit trail length
        if len(self.ship_trail) > self.max_trail_length:
            self.ship_trail.pop(0)
        
        # Move the tunnel up (simulating ship moving forward)
        for i in range(len(self.tunnel_points)):
            x, y = self.tunnel_points[i]
            self.tunnel_points[i] = (x, y + self.speed)
        
        # Remove tunnel points that are off-screen and add new ones
        while self.tunnel_points and self.tunnel_points[0][1] > SCREEN_HEIGHT + 100:
            self.tunnel_points.pop(0)
            
            # Add a new point at the end
            last_x, last_y = self.tunnel_points[-1]
            new_y = last_y - 20
            max_deviation = 5 + (self.difficulty * 2)
            new_x = last_x + random.randint(-int(max_deviation), int(max_deviation))
            
            # Keep the tunnel within screen bounds
            new_x = max(self.tunnel_width // 2, min(SCREEN_WIDTH - self.tunnel_width // 2, new_x))
            
            self.tunnel_points.append((new_x, new_y))
        
        # Check for collision with tunnel walls
        self.check_collision()
        
        # Increase score
        self.score += self.speed // 5 + 1
        
        # Increase difficulty over time
        if self.score % 1000 == 0:
            self.difficulty = min(self.difficulty + 0.1, 3.0)
    
    def check_collision(self):
        """Check if the ship has collided with the tunnel walls."""
        # Find the closest tunnel segment
        closest_segment = None
        min_distance = float('inf')
        
        for i in range(len(self.tunnel_points) - 1):
            p1 = self.tunnel_points[i]
            p2 = self.tunnel_points[i + 1]
            
            # Calculate distance from ship to segment
            segment_y_avg = (p1[1] + p2[1]) / 2
            distance = abs(segment_y_avg - self.ship_y)
            
            if distance < min_distance:
                min_distance = distance
                closest_segment = (p1, p2)
        
        if closest_segment:
            p1, p2 = closest_segment
            
            # Interpolate tunnel center at ship's y position
            if p2[1] != p1[1]:  # Avoid division by zero
                t = (self.ship_y - p1[1]) / (p2[1] - p1[1])
                tunnel_center_x = p1[0] + t * (p2[0] - p1[0])
            else:
                tunnel_center_x = p1[0]
            
            # Check if ship is outside tunnel
            if abs(self.ship_x - tunnel_center_x) > self.tunnel_width / 2:
                self.game_over = True
                self.track_game_end('loss')
    
    def render(self, screen):
        """
        Render the game.
        
        Args:
            screen (pygame.Surface): The surface to render on
        """
        # Draw the background
        screen.blit(self.background, (0, 0))
        
        # Draw the tunnel
        self.draw_tunnel(screen)
        
        # Draw the ship
        self.draw_ship(screen)
        
        # Draw the score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw the high score
        high_score_text = self.small_font.render(f"High Score: {self.high_score}", True, SECONDARY_COLOR)
        screen.blit(high_score_text, (10, 50))
        
        # Draw speed indicator
        speed_text = self.small_font.render(f"Speed: {self.speed}", True, SECONDARY_COLOR)
        screen.blit(speed_text, (10, 80))
        
        # Draw waiting for start message
        if self.waiting_for_start:
            message = "Press SPACE to start"
            message_text = self.message_font.render(message, True, WHITE)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(message_text, message_rect)
            
            # Draw instructions
            instructions = "Use LEFT/RIGHT arrows to steer your ship"
            instructions_text = self.small_font.render(instructions, True, WHITE)
            instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(instructions_text, instructions_rect)
        
        # Draw game over message
        elif self.game_over:
            message = "Game Over! Press SPACE to restart"
            message_text = self.message_font.render(message, True, WHITE)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(message_text, message_rect)
            
            # Draw final score
            final_score = f"Final Score: {self.score}"
            final_score_text = self.message_font.render(final_score, True, PRIMARY_COLOR)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(final_score_text, final_score_rect)
        
        # Draw paused message
        elif self.paused:
            message = "Paused - Press SPACE to resume"
            message_text = self.message_font.render(message, True, WHITE)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(message_text, message_rect)
        
        # Draw controls help
        controls_text = self.small_font.render("S: Save  L: Load  +/-: Speed  SPACE: Pause", True, WHITE)
        screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, SCREEN_HEIGHT - 30))
    
    def draw_tunnel(self, screen):
        """
        Draw the tunnel.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Draw tunnel segments
        for i in range(len(self.tunnel_points) - 1):
            p1 = self.tunnel_points[i]
            p2 = self.tunnel_points[i + 1]
            
            # Calculate tunnel edges
            angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0]) + math.pi / 2
            dx = math.cos(angle) * self.tunnel_width / 2
            dy = math.sin(angle) * self.tunnel_width / 2
            
            left1 = (p1[0] - dx, p1[1] - dy)
            right1 = (p1[0] + dx, p1[1] + dy)
            left2 = (p2[0] - dx, p2[1] - dy)
            right2 = (p2[0] + dx, p2[1] + dy)
            
            # Draw tunnel interior
            pygame.draw.polygon(screen, self.tunnel_color, [left1, right1, right2, left2])
            
            # Draw tunnel borders
            pygame.draw.line(screen, self.tunnel_border_color, left1, left2, 2)
            pygame.draw.line(screen, self.tunnel_border_color, right1, right2, 2)
    
    def draw_ship(self, screen):
        """
        Draw the ship and its trail.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Draw trail
        for i, (x, y) in enumerate(self.ship_trail):
            # Fade the trail based on position
            alpha = int(255 * i / len(self.ship_trail))
            radius = int(self.ship_size / 2 * i / len(self.ship_trail))
            
            # Create a surface for the trail segment
            trail_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (*self.ship_color, alpha), (radius, radius), radius)
            
            # Draw the trail segment
            screen.blit(trail_surface, (x - radius, y - radius))
        
        # Draw the ship
        pygame.draw.circle(screen, self.ship_color, (int(self.ship_x), int(self.ship_y)), self.ship_size // 2)
        
        # Draw ship details
        ship_rect = pygame.Rect(self.ship_x - self.ship_size // 2, self.ship_y - self.ship_size // 2, self.ship_size, self.ship_size)
        pygame.draw.line(screen, WHITE, (self.ship_x, self.ship_y - self.ship_size // 2), (self.ship_x, self.ship_y + self.ship_size // 2), 2)
        pygame.draw.line(screen, WHITE, (self.ship_x - self.ship_size // 2, self.ship_y), (self.ship_x + self.ship_size // 2, self.ship_y), 2)
    
    def save_game_state(self):
        """Save the current game state."""
        if not self.storage_service:
            print("Storage service not available.")
            return
        
        state = {
            'score': self.score,
            'ship_x': self.ship_x,
            'ship_y': self.ship_y,
            'speed': self.speed,
            'difficulty': self.difficulty,
            'tunnel_points': self.tunnel_points,
            'game_over': self.game_over,
            'paused': self.paused,
            'waiting_for_start': self.waiting_for_start
        }
        
        # Use 'anonymous' as user_id if not available
        user_id = 'anonymous'
        auth_service = self.game_manager.get_cloud_service('auth')
        if auth_service and auth_service.is_authenticated():
            user = auth_service.get_current_user()
            if user:
                user_id = user.get('sub', 'anonymous')
        
        success = self.storage_service.save_game_state('photon_racer', user_id, state)
        
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
        
        state = self.storage_service.load_game_state('photon_racer', user_id)
        
        if not state:
            print("No saved game state found.")
            return
        
        # Restore game state
        self.score = state.get('score', 0)
        self.ship_x = state.get('ship_x', SCREEN_WIDTH // 2)
        self.ship_y = state.get('ship_y', SCREEN_HEIGHT - 100)
        self.speed = state.get('speed', 5)
        self.difficulty = state.get('difficulty', 1.0)
        self.tunnel_points = state.get('tunnel_points', [])
        self.game_over = state.get('game_over', False)
        self.paused = state.get('paused', False)
        self.waiting_for_start = state.get('waiting_for_start', True)
        
        # If no tunnel points were saved, generate a new tunnel
        if not self.tunnel_points:
            self.generate_tunnel()
        
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
        self.storage_service.save_high_score('photon_racer', user_id, self.score)
    
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
        scores = self.storage_service.get_high_scores('photon_racer', limit=1)
        
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
            'photon_racer',
            score=self.score,
            duration=duration,
            outcome=outcome
        )
        
        # Update high score if needed
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
