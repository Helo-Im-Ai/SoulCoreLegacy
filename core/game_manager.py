"""
SoulCoreLegacy Arcade - Game Manager
-----------------------------------
This module manages the switching between the shell and individual games.
"""

import pygame
import importlib
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, FPS, GAME_LIST
from shell.menu import ShellMenu

class GameManager:
    """
    Manages the overall game state and transitions between the shell and games.
    """
    
    def __init__(self):
        """Initialize the game manager."""
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        
        # Initialize state variables
        self.current_game = None
        self.in_shell = True
        
        # Create the shell menu
        self.shell = ShellMenu(self)
        
        # Dictionary to store loaded game modules
        self.game_modules = {}
        
        # Cloud services
        self.cloud_services = None
        
        # Try to initialize cloud services
        try:
            from cloud import initialize_cloud_services
            self.cloud_services = initialize_cloud_services('cloud/config.yaml')
            print("Cloud services initialized.")
        except ImportError:
            print("Cloud services not available. Running in offline mode.")
        except Exception as e:
            print(f"Error initializing cloud services: {e}")
    
    def start_shell(self):
        """Switch to the shell interface."""
        self.in_shell = True
        self.current_game = None
        self.shell.reset()
    
    def start_game(self, game_id):
        """
        Start a specific game.
        
        Args:
            game_id (str): The ID of the game to start
        """
        # Check if the game is implemented
        game_info = next((game for game in GAME_LIST if game["id"] == game_id), None)
        if not game_info or not game_info.get("implemented", False):
            print(f"Game '{game_id}' is not implemented yet.")
            return
        
        # Try to load the game module
        try:
            if game_id not in self.game_modules:
                # Import the game module
                module_path = f"games.{game_id}.game"
                game_module = importlib.import_module(module_path)
                
                # Create an instance of the game
                game_class = getattr(game_module, f"{game_id.capitalize()}Game")
                self.game_modules[game_id] = game_class(self)
            
            # Switch to the game
            self.current_game = self.game_modules[game_id]
            self.in_shell = False
            self.current_game.reset()
            
            # Track game start if analytics is available
            if self.cloud_services and 'analytics' in self.cloud_services:
                self.cloud_services['analytics'].track_game_start(game_id)
            
            print(f"Started game: {game_id}")
        except (ImportError, AttributeError) as e:
            print(f"Error loading game '{game_id}': {e}")
    
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        # Handle escape key to return to shell
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if not self.in_shell:
                # Track game end if analytics is available
                if self.cloud_services and 'analytics' in self.cloud_services and self.current_game:
                    game_id = self.current_game.__class__.__name__.replace('Game', '').lower()
                    self.cloud_services['analytics'].track_game_end(game_id)
                
                self.start_shell()
                return
        
        # Pass the event to the current context (shell or game)
        if self.in_shell:
            self.shell.handle_event(event)
        elif self.current_game:
            self.current_game.handle_event(event)
    
    def update(self):
        """Update the current game state."""
        if self.in_shell:
            self.shell.update()
        elif self.current_game:
            self.current_game.update()
    
    def render(self):
        """Render the current screen."""
        if self.in_shell:
            self.shell.render(self.screen)
        elif self.current_game:
            self.current_game.render(self.screen)
        
        # Update the display
        pygame.display.flip()
    
    def get_cloud_service(self, service_name):
        """
        Get a cloud service by name.
        
        Args:
            service_name (str): The name of the service
            
        Returns:
            The cloud service, or None if not available
        """
        if not self.cloud_services:
            return None
        
        return self.cloud_services.get(service_name)
