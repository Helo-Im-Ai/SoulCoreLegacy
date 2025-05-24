"""
SoulCoreLegacy Arcade - Debug Test Script
---------------------------------------
This script tests various components of the SoulCoreLegacy Arcade to identify and fix issues.
"""

import pygame
import sys
import os
import importlib
import traceback

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.config import GAME_LIST

def print_header(text):
    """Print a header with the given text."""
    print("\n" + "=" * 80)
    print(f" {text} ".center(80, "="))
    print("=" * 80)

def print_result(test_name, success, message=""):
    """Print the result of a test."""
    if success:
        print(f"✅ {test_name}: PASSED")
    else:
        print(f"❌ {test_name}: FAILED - {message}")

def test_pygame_initialization():
    """Test pygame initialization."""
    print_header("Testing Pygame Initialization")
    try:
        pygame.init()
        print_result("Pygame initialization", True)
        
        # Check display module
        try:
            screen = pygame.display.set_mode((100, 100))
            pygame.display.set_caption("Test")
            print_result("Display module", True)
        except Exception as e:
            print_result("Display module", False, str(e))
        
        # Check font module
        try:
            font = pygame.font.SysFont("Arial", 24)
            text = font.render("Test", True, (255, 255, 255))
            print_result("Font module", True)
        except Exception as e:
            print_result("Font module", False, str(e))
        
        pygame.quit()
    except Exception as e:
        print_result("Pygame initialization", False, str(e))

def test_core_modules():
    """Test core modules."""
    print_header("Testing Core Modules")
    
    # Test config module
    try:
        from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_LIST
        print_result("Config module", True)
    except Exception as e:
        print_result("Config module", False, str(e))
    
    # Test asset_loader module
    try:
        from core.asset_loader import load_font, create_gradient_background
        print_result("Asset loader module", True)
    except Exception as e:
        print_result("Asset loader module", False, str(e))
    
    # Test game_manager module
    try:
        from core.game_manager import GameManager
        print_result("Game manager module", True)
    except Exception as e:
        print_result("Game manager module", False, str(e))

def test_shell_modules():
    """Test shell modules."""
    print_header("Testing Shell Modules")
    
    # Test menu module
    try:
        from shell.menu import ShellMenu
        print_result("Menu module", True)
    except Exception as e:
        print_result("Menu module", False, str(e))
    
    # Test ui_elements module
    try:
        from shell.ui_elements import Button, TextLabel, GameCard
        print_result("UI elements module", True)
    except Exception as e:
        print_result("UI elements module", False, str(e))

def test_game_modules():
    """Test game modules."""
    print_header("Testing Game Modules")
    
    for game in GAME_LIST:
        if game["implemented"]:
            game_id = game["id"]
            try:
                # Try to import the game module
                module_path = f"games.{game_id}.game"
                game_module = importlib.import_module(module_path)
                
                # Try to get the game class
                game_class_name = f"{game_id.capitalize()}Game"
                if game_id == "nft_artisan":
                    game_class_name = "NFTArtisanGame"
                elif game_id == "tic_tac_toe":
                    game_class_name = "TicTacToeGame"
                
                game_class = getattr(game_module, game_class_name)
                print_result(f"{game_id} module", True)
                
                # Check if the thumbnail exists
                thumbnail_path = os.path.join("games", game_id, "assets", "thumbnail.png")
                if os.path.exists(thumbnail_path):
                    print_result(f"{game_id} thumbnail", True)
                else:
                    print_result(f"{game_id} thumbnail", False, "Thumbnail not found")
            except ImportError as e:
                print_result(f"{game_id} module", False, f"Import error: {str(e)}")
            except AttributeError as e:
                print_result(f"{game_id} module", False, f"Class not found: {str(e)}")
            except Exception as e:
                print_result(f"{game_id} module", False, str(e))

def test_cloud_modules():
    """Test cloud modules."""
    print_header("Testing Cloud Modules")
    
    # Test cloud config module
    try:
        from cloud.config import CloudConfig
        print_result("Cloud config module", True)
    except Exception as e:
        print_result("Cloud config module", False, str(e))
    
    # Test cloud auth module
    try:
        from cloud.auth import AuthService
        print_result("Cloud auth module", True)
    except Exception as e:
        print_result("Cloud auth module", False, str(e))
    
    # Test cloud storage module
    try:
        from cloud.storage import StorageService
        print_result("Cloud storage module", True)
    except Exception as e:
        print_result("Cloud storage module", False, str(e))
    
    # Test cloud multiplayer module
    try:
        from cloud.multiplayer import MultiplayerService
        print_result("Cloud multiplayer module", True)
    except Exception as e:
        print_result("Cloud multiplayer module", False, str(e))
    
    # Test cloud analytics module
    try:
        from cloud.analytics import AnalyticsService
        print_result("Cloud analytics module", True)
    except Exception as e:
        print_result("Cloud analytics module", False, str(e))

def test_nft_artisan_game():
    """Test the NFT Artisan game specifically."""
    print_header("Testing NFT Artisan Game")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        
        # Import the game module
        from games.nft_artisan.game import NFTArtisanGame
        
        # Create a mock game manager
        class MockGameManager:
            def __init__(self):
                self.cloud_services = None
            
            def get_cloud_service(self, service_name):
                return None
        
        # Create the game
        game = NFTArtisanGame(MockGameManager())
        print_result("Game initialization", True)
        
        # Test game methods
        try:
            game.reset()
            print_result("Game reset", True)
        except Exception as e:
            print_result("Game reset", False, str(e))
        
        try:
            game.render(screen)
            print_result("Game render", True)
        except Exception as e:
            print_result("Game render", False, str(e))
        
        try:
            game.generate_nft()
            print_result("NFT generation", True)
        except Exception as e:
            print_result("NFT generation", False, str(e))
        
        pygame.quit()
    except Exception as e:
        print_result("NFT Artisan game", False, str(e))
        traceback.print_exc()

def main():
    """Run all tests."""
    print_header("SoulCoreLegacy Arcade Debug Tests")
    
    test_pygame_initialization()
    test_core_modules()
    test_shell_modules()
    test_game_modules()
    test_cloud_modules()
    test_nft_artisan_game()
    
    print_header("Debug Tests Complete")

if __name__ == "__main__":
    main()
