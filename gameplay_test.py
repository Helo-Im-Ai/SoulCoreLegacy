"""
SoulCoreLegacy Arcade - Gameplay Test Script
------------------------------------------
This script simulates actual gameplay for each game to verify functionality.
"""

import pygame
import sys
import os
import time
import importlib
import traceback
from pygame.locals import *

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.config import GAME_LIST, SCREEN_WIDTH, SCREEN_HEIGHT

class GameplayTester:
    """Class to test gameplay functionality of each game."""
    
    def __init__(self):
        """Initialize the gameplay tester."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("SoulCoreLegacy Gameplay Test")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        
        # Mock game manager
        self.game_manager = self.create_mock_game_manager()
    
    def create_mock_game_manager(self):
        """Create a mock game manager for testing."""
        class MockGameManager:
            def __init__(self):
                self.screen = pygame.display.get_surface()
                self.clock = pygame.time.Clock()
            
            def get_cloud_service(self, service_name):
                return None
            
            def start_game(self, game_id):
                print(f"Starting game: {game_id}")
            
            def start_shell(self):
                print("Returning to shell")
        
        return MockGameManager()
    
    def print_header(self, text):
        """Print a header with the given text."""
        print("\n" + "=" * 80)
        print(f" {text} ".center(80, "="))
        print("=" * 80)
    
    def print_result(self, test_name, success, message=""):
        """Print the result of a test."""
        if success:
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED - {message}")
    
    def test_game(self, game_id):
        """Test a specific game."""
        self.print_header(f"Testing {game_id} Gameplay")
        
        try:
            # Import the game module
            module_path = f"games.{game_id}.game"
            game_module = importlib.import_module(module_path)
            
            # Get the game class name
            game_class_name = f"{game_id.capitalize()}Game"
            if game_id == "nft_artisan":
                game_class_name = "NFTArtisanGame"
            elif game_id == "tic_tac_toe":
                game_class_name = "TicTacToeGame"
            elif game_id == "photon_racer":
                game_class_name = "Photon_racerGame"
            
            # Create the game instance
            game_class = getattr(game_module, game_class_name)
            game = game_class(self.game_manager)
            
            # Test initialization
            self.print_result(f"{game_id} initialization", True)
            
            # Test reset method
            try:
                game.reset()
                self.print_result(f"{game_id} reset", True)
            except Exception as e:
                self.print_result(f"{game_id} reset", False, str(e))
                traceback.print_exc()
            
            # Test rendering
            try:
                game.render(self.screen)
                pygame.display.flip()
                self.print_result(f"{game_id} rendering", True)
            except Exception as e:
                self.print_result(f"{game_id} rendering", False, str(e))
                traceback.print_exc()
            
            # Simulate gameplay
            print(f"\nSimulating {game_id} gameplay...")
            self.simulate_gameplay(game, game_id)
            
        except Exception as e:
            self.print_result(f"{game_id} gameplay", False, str(e))
            traceback.print_exc()
    
    def simulate_gameplay(self, game, game_id):
        """Simulate gameplay for a specific game."""
        # Set up simulation
        simulation_time = 10  # seconds
        start_time = time.time()
        frame_count = 0
        
        # Create a log of events
        event_log = []
        
        # Start the game (exit waiting_for_start state)
        space_event = pygame.event.Event(KEYDOWN, {'key': K_SPACE})
        game.handle_event(space_event)
        event_log.append("Pressed SPACE to start game")
        
        # Game-specific simulations
        if game_id == "pong":
            self.simulate_pong(game, event_log)
        elif game_id == "snake":
            self.simulate_snake(game, event_log)
        elif game_id == "tic_tac_toe":
            self.simulate_tic_tac_toe(game, event_log)
        elif game_id == "photon_racer":
            self.simulate_photon_racer(game, event_log)
        elif game_id == "nft_artisan":
            self.simulate_nft_artisan(game, event_log)
        
        # Main simulation loop
        while time.time() - start_time < simulation_time:
            # Process events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Update game state
            game.update()
            
            # Render the game
            game.render(self.screen)
            
            # Draw simulation info
            self.draw_simulation_info(frame_count, time.time() - start_time, event_log)
            
            # Update the display
            pygame.display.flip()
            
            # Limit the frame rate
            self.clock.tick(60)
            frame_count += 1
        
        # Print simulation results
        avg_fps = frame_count / simulation_time
        print(f"Simulation complete: {frame_count} frames in {simulation_time:.1f} seconds ({avg_fps:.1f} FPS)")
        print(f"Event log: {', '.join(event_log)}")
    
    def draw_simulation_info(self, frame_count, elapsed_time, event_log):
        """Draw simulation information on the screen."""
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, 100))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw simulation info
        fps_text = self.font.render(f"FPS: {frame_count / max(elapsed_time, 0.001):.1f}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
        
        time_text = self.font.render(f"Time: {elapsed_time:.1f}s", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 40))
        
        # Draw the last few events
        if event_log:
            events_text = self.small_font.render(f"Last event: {event_log[-1]}", True, (255, 255, 255))
            self.screen.blit(events_text, (10, 70))
    
    def simulate_pong(self, game, event_log):
        """Simulate Pong gameplay."""
        # Move paddle up
        up_event = pygame.event.Event(KEYDOWN, {'key': K_UP})
        game.handle_event(up_event)
        event_log.append("Pressed UP")
        
        # Wait a bit
        time.sleep(0.5)
        
        # Move paddle down
        down_event = pygame.event.Event(KEYDOWN, {'key': K_DOWN})
        game.handle_event(down_event)
        event_log.append("Pressed DOWN")
        
        # Wait a bit
        time.sleep(0.5)
        
        # Release keys
        up_release = pygame.event.Event(KEYUP, {'key': K_UP})
        game.handle_event(up_release)
        down_release = pygame.event.Event(KEYUP, {'key': K_DOWN})
        game.handle_event(down_release)
        event_log.append("Released keys")
    
    def simulate_snake(self, game, event_log):
        """Simulate Snake gameplay."""
        # Change direction a few times
        directions = [K_UP, K_RIGHT, K_DOWN, K_LEFT]
        for direction in directions:
            dir_event = pygame.event.Event(KEYDOWN, {'key': direction})
            game.handle_event(dir_event)
            event_log.append(f"Changed direction: {pygame.key.name(direction)}")
            time.sleep(0.5)
    
    def simulate_tic_tac_toe(self, game, event_log):
        """Simulate Tic-Tac-Toe gameplay."""
        # Click on a cell
        click_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        click_event = pygame.event.Event(MOUSEBUTTONDOWN, {'pos': click_pos, 'button': 1})
        game.handle_event(click_event)
        event_log.append(f"Clicked at {click_pos}")
    
    def simulate_photon_racer(self, game, event_log):
        """Simulate Photon Racer gameplay."""
        # Move left and right
        left_event = pygame.event.Event(KEYDOWN, {'key': K_LEFT})
        game.handle_event(left_event)
        event_log.append("Pressed LEFT")
        
        time.sleep(0.5)
        
        right_event = pygame.event.Event(KEYDOWN, {'key': K_RIGHT})
        game.handle_event(right_event)
        event_log.append("Pressed RIGHT")
    
    def simulate_nft_artisan(self, game, event_log):
        """Simulate NFT Artisan gameplay."""
        # Click on Create NFT button
        click_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
        click_event = pygame.event.Event(MOUSEBUTTONDOWN, {'pos': click_pos, 'button': 1})
        game.handle_event(click_event)
        event_log.append("Clicked Create NFT")
        
        time.sleep(0.5)
        
        # Generate NFT
        space_event = pygame.event.Event(KEYDOWN, {'key': K_SPACE})
        game.handle_event(space_event)
        event_log.append("Generated NFT")
    
    def run_tests(self):
        """Run gameplay tests for all implemented games."""
        self.print_header("SoulCoreLegacy Arcade Gameplay Tests")
        
        for game in GAME_LIST:
            if game["implemented"]:
                self.test_game(game["id"])
        
        self.print_header("Gameplay Tests Complete")
        pygame.quit()

if __name__ == "__main__":
    tester = GameplayTester()
    tester.run_tests()
