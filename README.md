# SoulCoreLegacy Arcade

A collection of classic and original arcade games with a modern twist, featuring AI opponents and a sleek interface.

## Project Structure

The project follows a modular architecture:

```
soulcorelegacy/
|
+-- main.py               # Main entry point
|
+-- core/                 # Core functionality
|   |-- config.py         # Global settings
|   |-- asset_loader.py   # Asset management
|   +-- game_manager.py   # Game switching logic
|
+-- shell/                # Main menu interface
|   |-- menu.py           # Menu display
|   |-- ui_elements.py    # UI components
|   +-- assets/           # Shell assets
|
+-- games/                # Individual games
    |
    +-- pong/             # Pong game implementation
        |-- __init__.py
        |-- game.py       # Main game loop
        |-- logic.py      # Game mechanics
        |-- ai.py         # AI opponent
        +-- assets/       # Game-specific assets
```

## Phase 1 Implementation (Current)

- [x] Core shell interface
- [x] Game manager for switching between games
- [x] Basic UI elements (buttons, labels)
- [x] Pong game implementation
  - [x] Player-controlled paddle
  - [x] AI opponent
  - [x] Ball physics
  - [x] Scoring system

## Future Phases

### Phase 2
- [ ] Snake game
- [ ] Tic-Tac-Toe game
- [ ] Photon Racer (original game)
- [ ] Enhanced shell interface

### Phase 3
- [ ] Breakout game
- [ ] Space Invaders game
- [ ] Code Cracker game
- [ ] Gravity Drop game
- [ ] Connect Four game
- [ ] Hangman game

### Phase 4
- [ ] Asteroids game
- [ ] Pac-Man (simplified)
- [ ] AI Duel game
- [ ] Synth Grid game
- [ ] Checkers game
- [ ] Minesweeper game
- [ ] Frogger game
- [ ] Tetris game
- [ ] Galaga game
- [ ] Donkey Kong (simplified)

## Running the Game

To run the game:

```bash
cd /path/to/soulcorelegacy
python main.py
```

## Controls

### Shell
- Mouse: Select games from the menu

### Pong
- Up/Down Arrow Keys: Move paddle up/down
- Escape: Return to shell
- Space: Restart game (after game over)

## Dependencies

- Python 3.x
- Pygame
