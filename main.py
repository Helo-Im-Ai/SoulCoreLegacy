#!/usr/bin/env python3
"""
SoulCoreLegacy Arcade - Main Entry Point
----------------------------------------
This is the main entry point for the SoulCoreLegacy Arcade application.
It initializes the game manager and starts the shell interface.
"""

import os
import sys
import pygame
from core.game_manager import GameManager

def main():
    """Main function to start the SoulCoreLegacy Arcade."""
    # Initialize pygame
    pygame.init()
    
    # Create game manager instance
    game_manager = GameManager()
    
    # Start the shell (main menu)
    game_manager.start_shell()
    
    # Main game loop
    running = True
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Let the game manager handle events
            game_manager.handle_event(event)
        
        # Update game state
        game_manager.update()
        
        # Render the current screen
        game_manager.render()
        
        # Cap the frame rate
        game_manager.clock.tick(60)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
