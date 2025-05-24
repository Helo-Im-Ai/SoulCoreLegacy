"""
SoulCoreLegacy Arcade - Tic-Tac-Toe Game
--------------------------------------
This module implements the classic Tic-Tac-Toe game.
"""

import pygame
import time
import random
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, WHITE, PRIMARY_COLOR, SECONDARY_COLOR
from core.asset_loader import load_font, create_gradient_background

class Tic_tac_toeGame:
    """
    Implementation of the classic Tic-Tac-Toe game.
    """
    
    def __init__(self, game_manager):
        """
        Initialize the Tic-Tac-Toe game.
        
        Args:
            game_manager (GameManager): Reference to the game manager
        """
        self.game_manager = game_manager
        
        # Game settings
        self.board_size = 3
        self.cell_size = 100
        self.board_margin = 50
        self.x_color = PRIMARY_COLOR
        self.o_color = SECONDARY_COLOR
        self.grid_color = (100, 100, 100)
        
        # Calculate board position
        self.board_width = self.board_size * self.cell_size
        self.board_height = self.board_size * self.cell_size
        self.board_x = (SCREEN_WIDTH - self.board_width) // 2
        self.board_y = (SCREEN_HEIGHT - self.board_height) // 2
        
        # Game state
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.tie = False
        self.start_time = None
        self.waiting_for_start = True
        self.player_score = 0
        self.ai_score = 0
        self.ties = 0
        
        # AI settings
        self.ai_enabled = True
        self.ai_difficulty = 1  # 0: Easy, 1: Medium, 2: Hard
        
        # Create fonts
        self.font = load_font("Arial", 36)
        self.message_font = load_font("Arial", 24)
        self.small_font = load_font("Arial", 18)
        
        # Create background
        self.background = create_gradient_background(
            SCREEN_WIDTH, 
            SCREEN_HEIGHT, 
            (30, 30, 50),  # Dark blue-gray
            (50, 50, 80)   # Slightly lighter blue-gray
        )
        
        # Get cloud services
        self.storage_service = self.game_manager.get_cloud_service('storage')
        self.analytics_service = self.game_manager.get_cloud_service('analytics')
        
        # Reset the game
        self.reset()
    
    def reset(self):
        """Reset the game state."""
        # Clear the board
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Reset game state
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.tie = False
        self.waiting_for_start = True
        self.start_time = time.time()
        
        # Track game start
        if self.analytics_service:
            self.analytics_service.track_game_start('tic_tac_toe', 'classic')
    
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
            
            # Save/load keys
            elif event.key == pygame.K_s:
                self.save_game_state()
            elif event.key == pygame.K_l:
                self.load_game_state()
            
            # Toggle AI
            elif event.key == pygame.K_a:
                self.ai_enabled = not self.ai_enabled
            
            # Change AI difficulty
            elif event.key == pygame.K_1:
                self.ai_difficulty = 0  # Easy
            elif event.key == pygame.K_2:
                self.ai_difficulty = 1  # Medium
            elif event.key == pygame.K_3:
                self.ai_difficulty = 2  # Hard
        
        # Handle mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.waiting_for_start and not self.game_over:
            # Get the mouse position
            mouse_x, mouse_y = event.pos
            
            # Check if the click is within the board
            if (self.board_x <= mouse_x <= self.board_x + self.board_width and
                self.board_y <= mouse_y <= self.board_y + self.board_height):
                
                # Calculate the cell coordinates
                cell_x = (mouse_x - self.board_x) // self.cell_size
                cell_y = (mouse_y - self.board_y) // self.cell_size
                
                # Make a move if the cell is empty
                if self.board[cell_y][cell_x] is None and self.current_player == 'X':
                    self.make_move(cell_x, cell_y)
    
    def make_move(self, x, y):
        """
        Make a move on the board.
        
        Args:
            x (int): The x-coordinate of the cell
            y (int): The y-coordinate of the cell
        """
        # Place the current player's mark
        self.board[y][x] = self.current_player
        
        # Check for a win or tie
        if self.check_win():
            self.game_over = True
            self.winner = self.current_player
            
            # Update scores
            if self.winner == 'X':
                self.player_score += 1
                self.track_game_end('win')
            else:
                self.ai_score += 1
                self.track_game_end('loss')
        elif self.check_tie():
            self.game_over = True
            self.tie = True
            self.ties += 1
            self.track_game_end('tie')
        else:
            # Switch players
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            # AI's turn
            if self.current_player == 'O' and self.ai_enabled and not self.game_over:
                self.ai_move()
    
    def ai_move(self):
        """Make an AI move."""
        # Easy: Random move
        if self.ai_difficulty == 0:
            self.ai_move_random()
        # Medium: Block player wins, otherwise random
        elif self.ai_difficulty == 1:
            if not self.ai_move_block():
                self.ai_move_random()
        # Hard: Try to win, block player wins, otherwise strategic
        else:
            if not self.ai_move_win():
                if not self.ai_move_block():
                    if not self.ai_move_strategic():
                        self.ai_move_random()
    
    def ai_move_random(self):
        """Make a random AI move."""
        # Get all empty cells
        empty_cells = []
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] is None:
                    empty_cells.append((x, y))
        
        # Make a random move
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.make_move(x, y)
    
    def ai_move_block(self):
        """Try to block the player from winning."""
        # Check each empty cell
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] is None:
                    # Try placing an X here
                    self.board[y][x] = 'X'
                    
                    # Check if this would be a winning move for the player
                    if self.check_win():
                        # Block it by placing an O here
                        self.board[y][x] = 'O'
                        
                        # Check for a win or tie
                        if self.check_win():
                            self.game_over = True
                            self.winner = 'O'
                            self.ai_score += 1
                            self.track_game_end('loss')
                        elif self.check_tie():
                            self.game_over = True
                            self.tie = True
                            self.ties += 1
                            self.track_game_end('tie')
                        else:
                            self.current_player = 'X'
                        
                        return True
                    
                    # Undo the test move
                    self.board[y][x] = None
        
        return False
    
    def ai_move_win(self):
        """Try to make a winning move."""
        # Check each empty cell
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] is None:
                    # Try placing an O here
                    self.board[y][x] = 'O'
                    
                    # Check if this would be a winning move
                    if self.check_win():
                        # This is a winning move
                        self.game_over = True
                        self.winner = 'O'
                        self.ai_score += 1
                        self.track_game_end('loss')
                        return True
                    
                    # Undo the test move
                    self.board[y][x] = None
        
        return False
    
    def ai_move_strategic(self):
        """Make a strategic move."""
        # Take center if available
        if self.board[1][1] is None:
            self.make_move(1, 1)
            return True
        
        # Take corners if available
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        empty_corners = [corner for corner in corners if self.board[corner[1]][corner[0]] is None]
        if empty_corners:
            x, y = random.choice(empty_corners)
            self.make_move(x, y)
            return True
        
        # Take sides if available
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        empty_sides = [side for side in sides if self.board[side[1]][side[0]] is None]
        if empty_sides:
            x, y = random.choice(empty_sides)
            self.make_move(x, y)
            return True
        
        return False
    
    def check_win(self):
        """
        Check if the current player has won.
        
        Returns:
            bool: True if the current player has won, False otherwise
        """
        # Check rows
        for y in range(self.board_size):
            if all(self.board[y][x] == self.current_player for x in range(self.board_size)):
                return True
        
        # Check columns
        for x in range(self.board_size):
            if all(self.board[y][x] == self.current_player for y in range(self.board_size)):
                return True
        
        # Check diagonals
        if all(self.board[i][i] == self.current_player for i in range(self.board_size)):
            return True
        
        if all(self.board[i][self.board_size - 1 - i] == self.current_player for i in range(self.board_size)):
            return True
        
        return False
    
    def check_tie(self):
        """
        Check if the game is a tie.
        
        Returns:
            bool: True if the game is a tie, False otherwise
        """
        # Check if the board is full
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] is None:
                    return False
        
        return True
    
    def update(self):
        """Update the game state."""
        # Nothing to update in this game
        pass
    
    def render(self, screen):
        """
        Render the game.
        
        Args:
            screen (pygame.Surface): The surface to render on
        """
        # Draw the background
        screen.blit(self.background, (0, 0))
        
        # Draw the board
        self.draw_board(screen)
        
        # Draw the scores
        score_text = self.font.render(f"Player: {self.player_score}  Ties: {self.ties}  AI: {self.ai_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(score_text, score_rect)
        
        # Draw AI status
        ai_status = "AI: ON" if self.ai_enabled else "AI: OFF"
        ai_difficulty = ["Easy", "Medium", "Hard"][self.ai_difficulty]
        ai_text = self.small_font.render(f"{ai_status} ({ai_difficulty})", True, SECONDARY_COLOR)
        screen.blit(ai_text, (10, 10))
        
        # Draw waiting for start message
        if self.waiting_for_start:
            message = "Press SPACE to start"
            message_text = self.message_font.render(message, True, WHITE)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
            screen.blit(message_text, message_rect)
            
            # Draw instructions
            instructions = [
                "Click on a cell to place your X",
                "Press A to toggle AI",
                "Press 1-3 to change AI difficulty"
            ]
            
            for i, instruction in enumerate(instructions):
                instruction_text = self.small_font.render(instruction, True, WHITE)
                instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100 + i * 30))
                screen.blit(instruction_text, instruction_rect)
        
        # Draw game over message
        elif self.game_over:
            if self.tie:
                message = "It's a tie!"
            else:
                message = f"{self.winner} wins!"
            
            message_text = self.message_font.render(message, True, WHITE)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            screen.blit(message_text, message_rect)
            
            # Draw restart message
            restart_text = self.small_font.render("Press SPACE to play again", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70))
            screen.blit(restart_text, restart_rect)
        
        # Draw current player
        elif not self.waiting_for_start:
            message = f"Current player: {self.current_player}"
            message_text = self.message_font.render(message, True, WHITE)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            screen.blit(message_text, message_rect)
        
        # Draw controls help
        controls_text = self.small_font.render("S: Save  L: Load  A: Toggle AI  1-3: AI Difficulty", True, WHITE)
        screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, SCREEN_HEIGHT - 30))
    
    def draw_board(self, screen):
        """
        Draw the game board.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Draw the grid
        for i in range(1, self.board_size):
            # Vertical lines
            pygame.draw.line(
                screen,
                self.grid_color,
                (self.board_x + i * self.cell_size, self.board_y),
                (self.board_x + i * self.cell_size, self.board_y + self.board_height),
                3
            )
            
            # Horizontal lines
            pygame.draw.line(
                screen,
                self.grid_color,
                (self.board_x, self.board_y + i * self.cell_size),
                (self.board_x + self.board_width, self.board_y + i * self.cell_size),
                3
            )
        
        # Draw the X's and O's
        for y in range(self.board_size):
            for x in range(self.board_size):
                cell_value = self.board[y][x]
                if cell_value:
                    cell_x = self.board_x + x * self.cell_size + self.cell_size // 2
                    cell_y = self.board_y + y * self.cell_size + self.cell_size // 2
                    
                    if cell_value == 'X':
                        self.draw_x(screen, cell_x, cell_y)
                    else:
                        self.draw_o(screen, cell_x, cell_y)
    
    def draw_x(self, screen, x, y):
        """
        Draw an X at the specified position.
        
        Args:
            screen (pygame.Surface): The surface to draw on
            x (int): The x-coordinate of the center of the X
            y (int): The y-coordinate of the center of the X
        """
        size = self.cell_size // 2 - 10
        pygame.draw.line(screen, self.x_color, (x - size, y - size), (x + size, y + size), 5)
        pygame.draw.line(screen, self.x_color, (x + size, y - size), (x - size, y + size), 5)
    
    def draw_o(self, screen, x, y):
        """
        Draw an O at the specified position.
        
        Args:
            screen (pygame.Surface): The surface to draw on
            x (int): The x-coordinate of the center of the O
            y (int): The y-coordinate of the center of the O
        """
        size = self.cell_size // 2 - 10
        pygame.draw.circle(screen, self.o_color, (x, y), size, 5)
    
    def save_game_state(self):
        """Save the current game state."""
        if not self.storage_service:
            print("Storage service not available.")
            return
        
        # Convert the board to a serializable format
        serialized_board = []
        for row in self.board:
            serialized_board.append([cell if cell is not None else "" for cell in row])
        
        state = {
            'board': serialized_board,
            'current_player': self.current_player,
            'winner': self.winner,
            'game_over': self.game_over,
            'tie': self.tie,
            'waiting_for_start': self.waiting_for_start,
            'player_score': self.player_score,
            'ai_score': self.ai_score,
            'ties': self.ties,
            'ai_enabled': self.ai_enabled,
            'ai_difficulty': self.ai_difficulty
        }
        
        # Use 'anonymous' as user_id if not available
        user_id = 'anonymous'
        auth_service = self.game_manager.get_cloud_service('auth')
        if auth_service and auth_service.is_authenticated():
            user = auth_service.get_current_user()
            if user:
                user_id = user.get('sub', 'anonymous')
        
        success = self.storage_service.save_game_state('tic_tac_toe', user_id, state)
        
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
        
        state = self.storage_service.load_game_state('tic_tac_toe', user_id)
        
        if not state:
            print("No saved game state found.")
            return
        
        # Restore the board
        serialized_board = state.get('board', [])
        if serialized_board:
            self.board = []
            for row in serialized_board:
                self.board.append([cell if cell else None for cell in row])
        
        # Restore game state
        self.current_player = state.get('current_player', 'X')
        self.winner = state.get('winner', None)
        self.game_over = state.get('game_over', False)
        self.tie = state.get('tie', False)
        self.waiting_for_start = state.get('waiting_for_start', True)
        self.player_score = state.get('player_score', 0)
        self.ai_score = state.get('ai_score', 0)
        self.ties = state.get('ties', 0)
        self.ai_enabled = state.get('ai_enabled', True)
        self.ai_difficulty = state.get('ai_difficulty', 1)
        
        print("Game state loaded successfully.")
    
    def track_game_end(self, outcome):
        """
        Track game end analytics.
        
        Args:
            outcome (str): The outcome of the game ('win', 'loss', 'tie')
        """
        if not self.analytics_service:
            return
        
        # Calculate duration
        duration = int(time.time() - self.start_time)
        
        # Track game end
        self.analytics_service.track_game_end(
            'tic_tac_toe',
            score=1 if outcome == 'win' else 0,
            duration=duration,
            outcome=outcome
        )
