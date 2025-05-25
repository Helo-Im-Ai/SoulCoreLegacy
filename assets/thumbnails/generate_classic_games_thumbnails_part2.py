"""
Generate classic games thumbnail images for SoulCoreLegacy Arcade (Part 2).
This script creates visually distinct thumbnails for Neo Blackjack, Quantum Solitaire, and AI Soul Society.
"""

import pygame
import os
import math
import random
import sys

# Initialize pygame
pygame.init()

# Define constants
THUMBNAIL_WIDTH = 300
THUMBNAIL_HEIGHT = 200
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define colors for classic games
COLORS = {
    'neo_blackjack': {  # 21 Blackjack
        'bg': (20, 0, 0),  # Dark red
        'primary': (80, 0, 0),  # Red
        'secondary': (150, 0, 0),  # Bright red
        'accent': (255, 215, 0),  # Gold
    },
    'quantum_solitaire': {  # Solitaire
        'bg': (0, 20, 0),  # Dark green
        'primary': (0, 80, 0),  # Green
        'secondary': (0, 150, 0),  # Bright green
        'accent': (255, 255, 255),  # White
    },
    'ai_soul_society': {  # AI Soul Society
        'bg': (30, 0, 50),  # Dark purple
        'primary': (100, 0, 150),  # Purple
        'secondary': (150, 100, 255),  # Light purple
        'accent': (255, 200, 0),  # Gold
    }
}

def generate_neo_blackjack_thumbnail():
    """Generate a thumbnail for Neo Blackjack game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['neo_blackjack']
    
    # Fill background with gradient
    for y in range(THUMBNAIL_HEIGHT):
        # Calculate color for this line
        progress = y / THUMBNAIL_HEIGHT
        color_top = colors['bg']
        color_bottom = tuple(max(0, c - 10) for c in colors['bg'])
        
        color = tuple(
            int(color_top[i] * (1 - progress) + color_bottom[i] * progress)
            for i in range(3)
        )
        
        # Draw horizontal line with this color
        pygame.draw.line(
            surface,
            color,
            (0, y),
            (THUMBNAIL_WIDTH - 1, y)
        )
    
    # Draw blackjack table
    table_rect = pygame.Rect(20, 40, THUMBNAIL_WIDTH - 40, THUMBNAIL_HEIGHT - 80)
    pygame.draw.rect(
        surface,
        colors['primary'],
        table_rect,
        0,
        border_radius=20
    )
    
    # Draw table border
    pygame.draw.rect(
        surface,
        colors['accent'],
        table_rect,
        2,
        border_radius=20
    )
    
    # Draw dealer area
    dealer_area = pygame.Rect(table_rect.left + 20, table_rect.top + 10, table_rect.width - 40, 30)
    pygame.draw.rect(
        surface,
        colors['secondary'],
        dealer_area,
        0,
        border_radius=10
    )
    
    # Draw dealer label
    font = pygame.font.SysFont("Arial", 14)
    dealer_text = font.render("DEALER", True, colors['accent'])
    dealer_rect = dealer_text.get_rect(center=(THUMBNAIL_WIDTH // 2, dealer_area.top + 15))
    surface.blit(dealer_text, dealer_rect)
    
    # Draw player area
    player_area = pygame.Rect(table_rect.left + 20, table_rect.bottom - 40, table_rect.width - 40, 30)
    pygame.draw.rect(
        surface,
        colors['secondary'],
        player_area,
        0,
        border_radius=10
    )
    
    # Draw player label
    font = pygame.font.SysFont("Arial", 14)
    player_text = font.render("PLAYER", True, colors['accent'])
    player_rect = player_text.get_rect(center=(THUMBNAIL_WIDTH // 2, player_area.top + 15))
    surface.blit(player_text, player_rect)
    
    # Draw cards
    card_width = 40
    card_height = 60
    
    # Dealer's cards
    dealer_cards = [
        (THUMBNAIL_WIDTH // 2 - 25, table_rect.top + 60),
        (THUMBNAIL_WIDTH // 2 + 25, table_rect.top + 60)
    ]
    
    for i, (x, y) in enumerate(dealer_cards):
        # Card background
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            pygame.Rect(x - card_width // 2, y - card_height // 2, card_width, card_height),
            0,
            border_radius=3
        )
        
        # Card border
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            pygame.Rect(x - card_width // 2, y - card_height // 2, card_width, card_height),
            1,
            border_radius=3
        )
        
        # If it's the second card, draw face down
        if i == 1:
            # Card back pattern
            for j in range(5):
                for k in range(8):
                    pygame.draw.rect(
                        surface,
                        colors['secondary'],
                        pygame.Rect(
                            x - card_width // 2 + 5 + j * 7,
                            y - card_height // 2 + 5 + k * 7,
                            5, 5
                        )
                    )
        else:
            # Draw card value
            font = pygame.font.SysFont("Arial", 16, bold=True)
            value_text = font.render("10", True, (0, 0, 0))
            value_rect = value_text.get_rect(center=(x, y))
            surface.blit(value_text, value_rect)
    
    # Player's cards
    player_cards = [
        (THUMBNAIL_WIDTH // 2 - 50, table_rect.bottom - 60),
        (THUMBNAIL_WIDTH // 2, table_rect.bottom - 60),
        (THUMBNAIL_WIDTH // 2 + 50, table_rect.bottom - 60)
    ]
    
    card_values = ["A", "J", "10"]
    card_colors = [(255, 0, 0), (0, 0, 0), (0, 0, 0)]
    
    for (x, y), value, color in zip(player_cards, card_values, card_colors):
        # Card background
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            pygame.Rect(x - card_width // 2, y - card_height // 2, card_width, card_height),
            0,
            border_radius=3
        )
        
        # Card border
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            pygame.Rect(x - card_width // 2, y - card_height // 2, card_width, card_height),
            1,
            border_radius=3
        )
        
        # Draw card value
        font = pygame.font.SysFont("Arial", 16, bold=True)
        value_text = font.render(value, True, color)
        value_rect = value_text.get_rect(center=(x, y))
        surface.blit(value_text, value_rect)
    
    # Draw chips
    chip_positions = [
        (THUMBNAIL_WIDTH // 2 - 70, THUMBNAIL_HEIGHT // 2),
        (THUMBNAIL_WIDTH // 2 - 60, THUMBNAIL_HEIGHT // 2 - 10),
        (THUMBNAIL_WIDTH // 2 - 80, THUMBNAIL_HEIGHT // 2 - 5)
    ]
    
    chip_colors = [
        (255, 0, 0),    # Red
        (0, 0, 255),    # Blue
        (255, 215, 0)   # Gold
    ]
    
    for (x, y), color in zip(chip_positions, chip_colors):
        # Draw chip
        pygame.draw.circle(
            surface,
            color,
            (x, y),
            10
        )
        
        # Draw chip border
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (x, y),
            10,
            2
        )
        
        # Draw chip pattern
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (x, y),
            6,
            1
        )
    
    # Draw digital effects
    for _ in range(15):
        x = random.randint(0, THUMBNAIL_WIDTH)
        y = random.randint(0, THUMBNAIL_HEIGHT)
        size = random.randint(1, 3)
        
        pygame.draw.circle(
            surface,
            colors['accent'],
            (x, y),
            size
        )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("NEO BLACKJACK", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_quantum_solitaire_thumbnail():
    """Generate a thumbnail for Quantum Solitaire game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['quantum_solitaire']
    
    # Fill background with gradient
    for y in range(THUMBNAIL_HEIGHT):
        # Calculate color for this line
        progress = y / THUMBNAIL_HEIGHT
        color_top = colors['bg']
        color_bottom = tuple(max(0, c - 10) for c in colors['bg'])
        
        color = tuple(
            int(color_top[i] * (1 - progress) + color_bottom[i] * progress)
            for i in range(3)
        )
        
        # Draw horizontal line with this color
        pygame.draw.line(
            surface,
            color,
            (0, y),
            (THUMBNAIL_WIDTH - 1, y)
        )
    
    # Draw solitaire table
    table_rect = pygame.Rect(20, 40, THUMBNAIL_WIDTH - 40, THUMBNAIL_HEIGHT - 80)
    pygame.draw.rect(
        surface,
        colors['primary'],
        table_rect,
        0,
        border_radius=20
    )
    
    # Draw table border
    pygame.draw.rect(
        surface,
        colors['secondary'],
        table_rect,
        2,
        border_radius=20
    )
    
    # Draw card dimensions
    card_width = 30
    card_height = 45
    
    # Draw foundation piles (top right)
    foundation_positions = [
        (THUMBNAIL_WIDTH - 60, 60),
        (THUMBNAIL_WIDTH - 90, 60),
        (THUMBNAIL_WIDTH - 120, 60),
        (THUMBNAIL_WIDTH - 150, 60)
    ]
    
    for x, y in foundation_positions:
        # Draw foundation outline
        pygame.draw.rect(
            surface,
            colors['secondary'],
            pygame.Rect(x - card_width // 2, y - card_height // 2, card_width, card_height),
            1,
            border_radius=3
        )
    
    # Draw stock pile (top left)
    stock_x = 60
    stock_y = 60
    
    # Draw stock outline
    pygame.draw.rect(
        surface,
        colors['secondary'],
        pygame.Rect(stock_x - card_width // 2, stock_y - card_height // 2, card_width, card_height),
        1,
        border_radius=3
    )
    
    # Draw waste pile (next to stock)
    waste_x = 100
    waste_y = 60
    
    # Draw some cards in the waste pile
    for i in range(3):
        offset = i * 10
        
        # Card background
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            pygame.Rect(waste_x - card_width // 2 + offset, waste_y - card_height // 2, card_width, card_height),
            0,
            border_radius=3
        )
        
        # Card border
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            pygame.Rect(waste_x - card_width // 2 + offset, waste_y - card_height // 2, card_width, card_height),
            1,
            border_radius=3
        )
    
    # Draw top card in waste pile
    top_card_x = waste_x + 20
    top_card_y = waste_y
    
    # Draw heart symbol
    heart_size = 8
    pygame.draw.polygon(
        surface,
        (255, 0, 0),
        [
            (top_card_x, top_card_y + heart_size // 2),
            (top_card_x - heart_size // 2, top_card_y - heart_size // 4),
            (top_card_x, top_card_y - heart_size),
            (top_card_x + heart_size // 2, top_card_y - heart_size // 4)
        ]
    )
    
    # Draw card value
    font = pygame.font.SysFont("Arial", 12, bold=True)
    value_text = font.render("A", True, (255, 0, 0))
    value_rect = value_text.get_rect(center=(top_card_x - 10, top_card_y - 15))
    surface.blit(value_text, value_rect)
    
    # Draw tableau piles (bottom)
    tableau_positions = []
    for i in range(7):
        tableau_positions.append((50 + i * 40, 120))
    
    # Draw cards in tableau
    for i, (x, y) in enumerate(tableau_positions):
        # Draw cards in the pile
        for j in range(i + 1):
            card_y = y + j * 15
            
            # Card background
            pygame.draw.rect(
                surface,
                (255, 255, 255),
                pygame.Rect(x - card_width // 2, card_y - card_height // 2, card_width, card_height),
                0,
                border_radius=3
            )
            
            # Card border
            pygame.draw.rect(
                surface,
                (0, 0, 0),
                pygame.Rect(x - card_width // 2, card_y - card_height // 2, card_width, card_height),
                1,
                border_radius=3
            )
            
            # If it's not the last card, draw face down
            if j < i:
                # Card back pattern
                for k in range(3):
                    for l in range(5):
                        pygame.draw.rect(
                            surface,
                            colors['secondary'],
                            pygame.Rect(
                                x - card_width // 2 + 5 + k * 7,
                                card_y - card_height // 2 + 5 + l * 7,
                                5, 5
                            )
                        )
            else:
                # Draw a random card face
                suit = random.choice(["♠", "♥", "♦", "♣"])
                value = random.choice(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"])
                color = (0, 0, 0) if suit in ["♠", "♣"] else (255, 0, 0)
                
                # Draw card value
                font = pygame.font.SysFont("Arial", 12, bold=True)
                value_text = font.render(value, True, color)
                value_rect = value_text.get_rect(center=(x - 8, card_y - 15))
                surface.blit(value_text, value_rect)
                
                # Draw suit
                font = pygame.font.SysFont("Arial", 12, bold=True)
                suit_text = font.render(suit, True, color)
                suit_rect = suit_text.get_rect(center=(x, card_y))
                surface.blit(suit_text, suit_rect)
    
    # Draw quantum effects
    for _ in range(10):
        effect_x = random.randint(0, THUMBNAIL_WIDTH)
        effect_y = random.randint(0, THUMBNAIL_HEIGHT)
        effect_size = random.randint(5, 15)
        
        # Draw quantum circle
        for i in range(3):
            pygame.draw.circle(
                surface,
                (*colors['secondary'], 100 - i * 30),
                (effect_x, effect_y),
                effect_size + i * 3,
                1
            )
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("QUANTUM SOLITAIRE", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface

def generate_ai_soul_society_thumbnail():
    """Generate a thumbnail for AI Soul Society game."""
    surface = pygame.Surface((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    colors = COLORS['ai_soul_society']
    
    # Fill background with gradient
    for y in range(THUMBNAIL_HEIGHT):
        # Calculate color for this line
        progress = y / THUMBNAIL_HEIGHT
        color_top = colors['bg']
        color_bottom = tuple(max(0, c - 10) for c in colors['bg'])
        
        color = tuple(
            int(color_top[i] * (1 - progress) + color_bottom[i] * progress)
            for i in range(3)
        )
        
        # Draw horizontal line with this color
        pygame.draw.line(
            surface,
            color,
            (0, y),
            (THUMBNAIL_WIDTH - 1, y)
        )
    
    # Draw digital grid
    for x in range(0, THUMBNAIL_WIDTH, 20):
        pygame.draw.line(
            surface,
            (*colors['primary'], 30),
            (x, 0),
            (x, THUMBNAIL_HEIGHT),
            1
        )
    
    for y in range(0, THUMBNAIL_HEIGHT, 20):
        pygame.draw.line(
            surface,
            (*colors['primary'], 30),
            (0, y),
            (THUMBNAIL_WIDTH, y),
            1
        )
    
    # Draw AI souls (simplified as glowing orbs with faces)
    ai_positions = [
        (THUMBNAIL_WIDTH // 4, THUMBNAIL_HEIGHT // 3),
        (THUMBNAIL_WIDTH // 2, THUMBNAIL_HEIGHT // 2),
        (THUMBNAIL_WIDTH * 3 // 4, THUMBNAIL_HEIGHT // 3 + 20),
        (THUMBNAIL_WIDTH // 3, THUMBNAIL_HEIGHT * 2 // 3),
        (THUMBNAIL_WIDTH * 2 // 3, THUMBNAIL_HEIGHT * 2 // 3 - 20)
    ]
    
    ai_colors = [
        (255, 100, 100),  # Red
        (100, 100, 255),  # Blue
        (100, 255, 100),  # Green
        (255, 255, 100),  # Yellow
        (255, 100, 255)   # Pink
    ]
    
    for (x, y), color in zip(ai_positions, ai_colors):
        # Draw glowing orb
        for i in range(4):
            pygame.draw.circle(
                surface,
                (*color, 150 - i * 30),
                (x, y),
                20 + i * 5
            )
        
        # Draw core
        pygame.draw.circle(
            surface,
            color,
            (x, y),
            15
        )
        
        # Draw face
        # Eyes
        eye_offset = 5
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (x - eye_offset, y - 3),
            3
        )
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (x + eye_offset, y - 3),
            3
        )
        
        # Pupils
        pygame.draw.circle(
            surface,
            (0, 0, 0),
            (x - eye_offset, y - 3),
            1
        )
        pygame.draw.circle(
            surface,
            (0, 0, 0),
            (x + eye_offset, y - 3),
            1
        )
        
        # Mouth (random expressions)
        expression = random.choice(["smile", "neutral", "surprise"])
        
        if expression == "smile":
            pygame.draw.arc(
                surface,
                (255, 255, 255),
                pygame.Rect(x - 5, y, 10, 10),
                0, math.pi,
                2
            )
        elif expression == "neutral":
            pygame.draw.line(
                surface,
                (255, 255, 255),
                (x - 5, y + 5),
                (x + 5, y + 5),
                2
            )
        else:  # surprise
            pygame.draw.circle(
                surface,
                (255, 255, 255),
                (x, y + 5),
                3,
                1
            )
    
    # Draw connections between AIs
    for i in range(len(ai_positions)):
        for j in range(i + 1, len(ai_positions)):
            if random.random() < 0.7:  # 70% chance to draw a connection
                start_x, start_y = ai_positions[i]
                end_x, end_y = ai_positions[j]
                
                # Draw connection line
                for k in range(3):
                    pygame.draw.line(
                        surface,
                        (*colors['secondary'], 100 - k * 30),
                        (start_x, start_y),
                        (end_x, end_y),
                        3 - k
                    )
    
    # Draw UI elements (simplified)
    # Status bar
    status_rect = pygame.Rect(20, THUMBNAIL_HEIGHT - 30, THUMBNAIL_WIDTH - 40, 20)
    pygame.draw.rect(
        surface,
        colors['primary'],
        status_rect,
        0,
        border_radius=5
    )
    
    # Status indicators
    indicators = ["HAPPINESS", "ENERGY", "SOCIAL"]
    indicator_values = [0.8, 0.6, 0.9]  # 0.0 to 1.0
    indicator_colors = [(255, 255, 0), (0, 255, 0), (0, 100, 255)]
    
    indicator_width = (status_rect.width - 20) // len(indicators)
    
    for i, (label, value, color) in enumerate(zip(indicators, indicator_values, indicator_colors)):
        # Indicator background
        indicator_rect = pygame.Rect(
            status_rect.left + 10 + i * indicator_width,
            status_rect.top + 5,
            indicator_width - 10,
            10
        )
        pygame.draw.rect(
            surface,
            (50, 50, 50),
            indicator_rect,
            0,
            border_radius=5
        )
        
        # Indicator fill
        fill_rect = pygame.Rect(
            indicator_rect.left,
            indicator_rect.top,
            int(indicator_rect.width * value),
            indicator_rect.height
        )
        pygame.draw.rect(
            surface,
            color,
            fill_rect,
            0,
            border_radius=5
        )
        
        # Indicator label
        font = pygame.font.SysFont("Arial", 8)
        label_text = font.render(label, True, (255, 255, 255))
        label_rect = label_text.get_rect(center=(indicator_rect.centerx, indicator_rect.top - 5))
        surface.blit(label_text, label_rect)
    
    # Draw floating icons (representing activities)
    icons = [
        {"pos": (50, 50), "color": (255, 100, 100), "symbol": "♥"},  # Love
        {"pos": (250, 60), "color": (100, 100, 255), "symbol": "✓"},  # Task
        {"pos": (150, 40), "color": (255, 255, 0), "symbol": "★"},    # Star
        {"pos": (80, 150), "color": (0, 255, 0), "symbol": "✚"}       # Health
    ]
    
    for icon in icons:
        # Draw icon background
        pygame.draw.circle(
            surface,
            icon["color"],
            icon["pos"],
            12
        )
        
        # Draw icon symbol
        font = pygame.font.SysFont("Arial", 14, bold=True)
        symbol_text = font.render(icon["symbol"], True, (255, 255, 255))
        symbol_rect = symbol_text.get_rect(center=icon["pos"])
        surface.blit(symbol_text, symbol_rect)
    
    # Draw game title
    font = pygame.font.SysFont("Arial", 24, bold=True)
    title_text = font.render("AI SOUL SOCIETY", True, colors['accent'])
    title_rect = title_text.get_rect(center=(THUMBNAIL_WIDTH // 2, 20))
    surface.blit(title_text, title_rect)
    
    return surface

def main():
    """Generate all thumbnails."""
    # Create thumbnails
    thumbnails = {
        'neo_blackjack': generate_neo_blackjack_thumbnail(),
        'quantum_solitaire': generate_quantum_solitaire_thumbnail(),
        'ai_soul_society': generate_ai_soul_society_thumbnail()
    }
    
    # Save thumbnails
    for game_id, surface in thumbnails.items():
        output_path = os.path.join(OUTPUT_DIR, f"{game_id}.png")
        pygame.image.save(surface, output_path)
        print(f"Generated thumbnail for {game_id}: {output_path}")

if __name__ == "__main__":
    main()
    pygame.quit()
