# SoulCoreLegacy Arcade - Quick Start Guide

This guide will help you run and play the SoulCoreLegacy Arcade games on your system.

## Prerequisites

- Python 3.6 or higher
- Pygame library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Helo-Im-Ai/SoulCoreLegacy.git
   cd SoulCoreLegacy
   ```

2. Install dependencies:
   ```bash
   pip install pygame pyyaml
   ```

## Running the Arcade

### Option 1: Using the run script (recommended)

```bash
./run_game.sh
```

If the script isn't executable, make it executable first:
```bash
chmod +x run_game.sh
./run_game.sh
```

### Option 2: Running directly with Python

```bash
python3 main.py
```

## Playing the Games

1. **Main Menu Navigation**:
   - Use your mouse to select games from the menu
   - Click on a game card to start playing

2. **In-Game Controls**:

   **Pong**:
   - UP/DOWN arrow keys: Move paddle
   - SPACE: Start game / Restart after game over
   - ESC: Return to main menu
   - S: Save game state
   - L: Load game state
   - M: Start multiplayer (requires cloud setup)

   **Snake**:
   - UP/DOWN/LEFT/RIGHT arrow keys: Change direction
   - SPACE: Start game / Restart after game over
   - ESC: Return to main menu
   - S: Save game state
   - L: Load game state
   - W: Toggle wrap-around mode
   - +/-: Adjust game speed

   **Tic-Tac-Toe**:
   - Mouse: Click on cells to place X
   - SPACE: Start game / Restart after game over
   - ESC: Return to main menu
   - S: Save game state
   - L: Load game state
   - A: Toggle AI on/off
   - 1/2/3: Change AI difficulty

   **Photon Racer**:
   - LEFT/RIGHT arrow keys: Move ship
   - SPACE: Start game / Restart after game over
   - ESC: Return to main menu
   - S: Save game state
   - L: Load game state
   - +/-: Adjust game speed

   **NFT Artisan**:
   - Mouse: Navigate menus and select options
   - SPACE: Start game / Generate new art
   - ESC: Return to main menu / Return to previous screen
   - S: Save collection
   - L: Load collection
   - LEFT/RIGHT: Navigate collection (when viewing)

## Troubleshooting

If you encounter any issues:

1. **Missing dependencies**:
   ```bash
   pip install pygame pyyaml
   ```

2. **Permission issues with run script**:
   ```bash
   chmod +x run_game.sh
   ```

3. **Display issues**:
   - Make sure your system supports the default resolution (800x600)
   - You can modify the resolution in `core/config.py` if needed

4. **Performance issues**:
   - Close other applications to free up resources
   - Reduce the game's FPS in `core/config.py` if needed

## Enjoy!

Have fun playing the SoulCoreLegacy Arcade games! The collection currently includes:
- Pong
- Snake
- Tic-Tac-Toe
- Photon Racer
- NFT Artisan
