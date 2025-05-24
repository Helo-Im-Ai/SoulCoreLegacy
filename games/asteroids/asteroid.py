"""
SoulCoreLegacy Arcade - Asteroids Game
------------------------------------
This module implements the classic Asteroids game.
"""

import pyglet
import time
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, WHITE, PRIMARY_COLOR, SECONDARY_COLOR
from core.asset_loader import load_font
from games.asteroids.game import resources, load, player, asteroid

class AsteroidsGame:
    """
    Implementation of the classic Asteroids game.
    """
    
    def __init__(self, game_manager):
        """
        Initialize the Asteroids game.
        
        Args:
            game_manager (GameManager): Reference to the game manager
        """
        self.game_manager = game_manager
        
        # Game state
        self.score = 0
        self.level = 1
        self.lives = 3
        self.game_over = False
        self.paused = False
        self.waiting_for_start = True
        self.start_time = None
        
        # Create batch for drawing
        self.main_batch = pyglet.graphics.Batch()
        
        # Create labels
        self.score_label = pyglet.text.Label(
            text="Score: 0",
            x=10, y=575,
            batch=self.main_batch
        )
        
        self.level_label = pyglet.text.Label(
            text="Asteroids",
            x=SCREEN_WIDTH//2, y=575,
            anchor_x='center',
            batch=self.main_batch
        )
        
        # Create the player
        self.player_ship = player.Player(
            x=SCREEN_WIDTH//2,
            y=SCREEN_HEIGHT//2,
            batch=self.main_batch
        )
        
        # Create asteroids
        self.asteroids = load.asteroids(3, self.player_ship.position, self.main_batch)
        
        # Create player lives display
        self.life_icons = load.player_lives(self.lives, self.main_batch)
        
        # List of all game objects
        self.game_objects = [self.player_ship] + self.asteroids
        
        # Get cloud services
        self.storage_service = self.game_manager.get_cloud_service('storage')
        self.analytics_service = self.game_manager.get_cloud_service('analytics')
        
        # Load high score
        self.high_score = 0
        self.load_high_score()
        
        # Reset the game
        self.reset()
    
    def reset(self):
        """Reset the game state."""
        # Clear game objects
        for obj in self.game_objects:
            obj.delete()
        
        # Reset game state
        self.score = 0
        self.level = 1
        self.lives = 3
        self.game_over = False
        self.paused = False
        self.waiting_for_start = True
        self.start_time = time.time()
        
        # Update score label
        self.score_label.text = f"Score: {self.score}"
        
        # Create the player
        self.player_ship = player.Player(
            x=SCREEN_WIDTH//2,
            y=SCREEN_HEIGHT//2,
            batch=self.main_batch
        )
        
        # Create asteroids
        self.asteroids = load.asteroids(3, self.player_ship.position, self.main_batch)
        
        # Update life icons
        for icon in self.life_icons:
            icon.delete()
        self.life_icons = load.player_lives(self.lives, self.main_batch)
        
        # Update game objects list
        self.game_objects = [self.player_ship] + self.asteroids
        
        # Track game start
        if hasattr(self, 'analytics_service') and self.analytics_service:
            self.analytics_service.track_game_start('asteroids', 'classic')
    
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        # Handle key press events
        if event.type == pyglet.window.key.KeyPress:
            # Start the game
            if event.key == pyglet.window.key.SPACE:
                if self.waiting_for_start:
                    self.waiting_for_start = False
                    self.start_time = time.time()
                elif self.game_over:
                    self.reset()
                else:
                    self.paused = not self.paused
            
            # Pass the event to the player
            if not self.game_over and not self.waiting_for_start:
                self.player_ship.on_key_press(event.key, event.modifiers)
        
        # Push the player's key handler
        self.game_manager.game_window.push_handlers(self.player_ship.key_handler)
    
    def update(self, dt):
        """Update the game state."""
        # Don't update if the game is paused, over, or waiting to start
        if self.paused or self.game_over or self.waiting_for_start:
            return
        
        # List for new objects
        to_add = []
        
        # Update all objects
        for obj in self.game_objects:
            obj.update(dt)
            to_add.extend(obj.new_objects)
            obj.new_objects = []
        
        # Check for collisions
        for i in range(len(self.game_objects)):
            for j in range(i+1, len(self.game_objects)):
                obj_1 = self.game_objects[i]
                obj_2 = self.game_objects[j]
                
                # Skip if either object is already dead
                if obj_1.dead or obj_2.dead:
                    continue
                
                # Check for collision
                if obj_1.collides_with(obj_2):
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)
                    
                    # Update score if an asteroid was hit by a bullet
                    if (isinstance(obj_1, asteroid.Asteroid) and obj_2.is_bullet) or \
                       (isinstance(obj_2, asteroid.Asteroid) and obj_1.is_bullet):
                        self.score += 10
                        self.score_label.text = f"Score: {self.score}"
        
        # Remove dead objects
        for to_remove in [obj for obj in self.game_objects if obj.dead]:
            # Check if the player died
            if to_remove == self.player_ship:
                self.lives -= 1
                
                # Update life icons
                if self.life_icons:
                    self.life_icons[-1].delete()
                    self.life_icons.pop()
                
                # Check for game over
                if self.lives <= 0:
                    self.game_over = True
                    
                    # Update high score
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
                    
                    # Track game end
                    self.track_game_end('loss')
                else:
                    # Respawn the player
                    self.player_ship = player.Player(
                        x=SCREEN_WIDTH//2,
                        y=SCREEN_HEIGHT//2,
                        batch=self.main_batch
                    )
                    to_add.append(self.player_ship)
            
            # Remove the object
            to_remove.delete()
            self.game_objects.remove(to_remove)
        
        # Add new objects
        self.game_objects.extend(to_add)
        
        # Check if all asteroids are gone
        if not any(isinstance(obj, asteroid.Asteroid) for obj in self.game_objects):
            # Advance to the next level
            self.level += 1
            
            # Add more asteroids
            new_asteroids = load.asteroids(
                3 + self.level,
                self.player_ship.position,
                self.main_batch
            )
            self.game_objects.extend(new_asteroids)
    
    def render(self, screen):
        """
        Render the game.
        
        Args:
            screen (pygame.Surface): The surface to render on
        """
        # Clear the screen
        screen.fill(BG_COLOR)
        
        # Draw all objects
        self.main_batch.draw()
        
        # Draw waiting for start message
        if self.waiting_for_start:
            message_font = load_font("Arial", 24)
            message = message_font.render("Press SPACE to start", True, WHITE)
            message_rect = message.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(message, message_rect)
            
            # Draw instructions
            instructions_font = load_font("Arial", 18)
            instructions = [
                "Arrow keys to move and rotate",
                "SPACE to fire",
                "ESC to return to menu"
            ]
            
            for i, instruction in enumerate(instructions):
                instr_text = instructions_font.render(instruction, True, WHITE)
                instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40 + i*30))
                screen.blit(instr_text, instr_rect)
        
        # Draw game over message
        elif self.game_over:
            message_font = load_font("Arial", 36)
            message = message_font.render("GAME OVER", True, PRIMARY_COLOR)
            message_rect = message.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            screen.blit(message, message_rect)
            
            # Draw final score
            score_font = load_font("Arial", 24)
            score_text = score_font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(score_text, score_rect)
            
            # Draw high score
            high_score_font = load_font("Arial", 24)
            high_score_text = high_score_font.render(f"High Score: {self.high_score}", True, SECONDARY_COLOR)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            screen.blit(high_score_text, high_score_rect)
            
            # Draw restart message
            restart_font = load_font("Arial", 18)
            restart_text = restart_font.render("Press SPACE to play again", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
            screen.blit(restart_text, restart_rect)
        
        # Draw paused message
        elif self.paused:
            message_font = load_font("Arial", 36)
            message = message_font.render("PAUSED", True, WHITE)
            message_rect = message.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(message, message_rect)
            
            # Draw resume message
            resume_font = load_font("Arial", 18)
            resume_text = resume_font.render("Press SPACE to resume", True, WHITE)
            resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            screen.blit(resume_text, resume_rect)
    
    def load_high_score(self):
        """Load the high score."""
        if not self.storage_service:
            return
        
        try:
            # Use 'anonymous' as user_id if not available
            user_id = 'anonymous'
            auth_service = self.game_manager.get_cloud_service('auth')
            if auth_service and auth_service.is_authenticated():
                user = auth_service.get_current_user()
                if user:
                    user_id = user.get('sub', 'anonymous')
            
            # Load high scores
            scores = self.storage_service.get_high_scores('asteroids', limit=1)
            
            if scores and len(scores) > 0:
                self.high_score = scores[0].get('score', 0)
        except Exception as e:
            print(f"Error loading high score: {e}")
            self.high_score = 0
    
    def save_high_score(self):
        """Save the high score."""
        if not self.storage_service:
            return
        
        try:
            # Use 'anonymous' as user_id if not available
            user_id = 'anonymous'
            auth_service = self.game_manager.get_cloud_service('auth')
            if auth_service and auth_service.is_authenticated():
                user = auth_service.get_current_user()
                if user:
                    user_id = user.get('sub', 'anonymous')
            
            # Save the high score
            self.storage_service.save_high_score('asteroids', user_id, self.high_score)
        except Exception as e:
            print(f"Error saving high score: {e}")
    
    def track_game_end(self, outcome):
        """
        Track game end analytics.
        
        Args:
            outcome (str): The outcome of the game ('win', 'loss', 'draw')
        """
        if hasattr(self, 'analytics_service') and self.analytics_service:
            # Calculate duration
            duration = int(time.time() - self.start_time)
            
            # Track game end
            self.analytics_service.track_game_end(
                'asteroids',
                score=self.score,
                duration=duration,
                outcome=outcome
            )
