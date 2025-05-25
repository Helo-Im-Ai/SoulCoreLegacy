import pygame
import pygame_gui
import sys
import os
import time
import random
import math
from typing import List, Dict, Tuple, Callable, Optional

# Define constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Define colors
BACKGROUND_COLOR = (10, 5, 30)  # Deep space black with hint of purple

# Define paths
THUMBNAIL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "thumbnails")

# Game list for the arcade
GAME_LIST = [
    {
        "id": "cosmic_racer",
        "name": "Cosmic Racer",
        "description": "Race through the cosmos at breakneck speeds, avoiding asteroids and collecting stardust.",
        "implemented": True,
        "popularity": 8,
        "new_release": False,
        "featured": True,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "cosmic_racer.png"),
        "category": "Racing"
    },
    {
        "id": "dungeon_delver",
        "name": "Dungeon Delver",
        "description": "Explore mysterious dungeons, battle monsters, and collect treasure in this roguelike adventure.",
        "implemented": True,
        "popularity": 6,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "dungeon_delver.png"),
        "category": "Adventure"
    },
    {
        "id": "nft_artisan",
        "name": "NFT Artisan",
        "description": "Create, trade, and collect unique digital art pieces in this creative sandbox.",
        "implemented": True,
        "popularity": 7,
        "new_release": False,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "nft_artisan.png"),
        "category": "Creative"
    },
    {
        "id": "snake",
        "name": "Quantum Snake",
        "description": "Guide your snake through a quantum realm where walls are merely suggestions.",
        "implemented": True,
        "popularity": 5,
        "new_release": False,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "snake.png"),
        "category": "Arcade"
    },
    {
        "id": "pong",
        "name": "Neon Pong",
        "description": "The classic game reimagined with neon visuals and power-ups.",
        "implemented": True,
        "popularity": 4,
        "new_release": False,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "pong.png"),
        "category": "Sports"
    },
    {
        "id": "asteroids",
        "name": "Asteroids Annihilation",
        "description": "Destroy asteroids and alien ships in this enhanced version of the classic.",
        "implemented": True,
        "popularity": 7,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "asteroids.png"),
        "category": "Arcade"
    },
    {
        "id": "cyber_defense",
        "name": "Cyber Defense",
        "description": "Protect your network from incoming cyber attacks in this strategic tower defense game.",
        "implemented": True,
        "popularity": 9,
        "new_release": True,
        "featured": True,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "cyber_defense.png"),
        "category": "Strategy"
    },
    {
        "id": "quantum_puzzler",
        "name": "Quantum Puzzler",
        "description": "Solve mind-bending puzzles using quantum mechanics principles and parallel realities.",
        "implemented": True,
        "popularity": 7,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "quantum_puzzler.png"),
        "category": "Puzzle"
    },
    {
        "id": "rhythm_master",
        "name": "Rhythm Master",
        "description": "Test your rhythm and timing in this music-based game with increasing difficulty levels.",
        "implemented": True,
        "popularity": 8,
        "new_release": False,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "rhythm_master.png"),
        "category": "Music"
    },
    {
        "id": "mech_commander",
        "name": "Mech Commander",
        "description": "Command a squad of customizable mechs in tactical turn-based combat scenarios.",
        "implemented": True,
        "popularity": 6,
        "new_release": False,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "mech_commander.png"),
        "category": "Strategy"
    },
    {
        "id": "crypto_tycoon",
        "name": "Crypto Tycoon",
        "description": "Build your crypto empire by trading, mining, and investing in this economic simulation.",
        "implemented": True,
        "popularity": 8,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "crypto_tycoon.png"),
        "category": "Simulation"
    },
    {
        "id": "vr_explorer",
        "name": "VR Explorer",
        "description": "Explore stunning virtual worlds and solve environmental puzzles in this immersive adventure.",
        "implemented": True,
        "popularity": 9,
        "new_release": True,
        "featured": True,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "vr_explorer.png"),
        "category": "Adventure"
    },
    {
        "id": "cyber_soccer",
        "name": "Cyber Soccer",
        "description": "Play futuristic soccer with enhanced abilities, power-ups, and dynamic playing fields.",
        "implemented": True,
        "popularity": 8,
        "new_release": True,
        "featured": True,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "cyber_soccer.png"),
        "category": "Sports"
    },
    {
        "id": "extreme_racing",
        "name": "Extreme Racing",
        "description": "Race on impossible tracks with gravity-defying vehicles and strategic power-ups.",
        "implemented": True,
        "popularity": 9,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "extreme_racing.png"),
        "category": "Sports"
    },
    {
        "id": "space_basketball",
        "name": "Space Basketball",
        "description": "Play basketball in zero gravity with unique physics and special abilities.",
        "implemented": True,
        "popularity": 7,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "space_basketball.png"),
        "category": "Sports"
    },
    {
        "id": "virtual_tennis",
        "name": "Virtual Tennis",
        "description": "Experience tennis with dynamic courts, power shots, and customizable players.",
        "implemented": True,
        "popularity": 6,
        "new_release": False,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "virtual_tennis.png"),
        "category": "Sports"
    },
    {
        "id": "mech_boxing",
        "name": "Mech Boxing",
        "description": "Control giant robots in intense boxing matches with upgradeable parts and special moves.",
        "implemented": True,
        "popularity": 8,
        "new_release": True,
        "featured": True,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "mech_boxing.png"),
        "category": "Sports"
    },
    {
        "id": "cyber_surfing",
        "name": "Cyber Surfing",
        "description": "Surf on digital waves in a neon cyberspace with tricks, combos, and obstacles.",
        "implemented": True,
        "popularity": 7,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "cyber_surfing.png"),
        "category": "Sports"
    },
    {
        "id": "quantum_leap",
        "name": "Quantum Leap",
        "description": "Navigate through dangerous roads and rivers while manipulating quantum physics to teleport.",
        "implemented": True,
        "popularity": 8,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "quantum_leap.png"),
        "category": "Arcade"
    },
    {
        "id": "neon_blocks",
        "name": "Neon Blocks",
        "description": "Arrange falling neon blocks to create complete lines in this addictive puzzle game.",
        "implemented": True,
        "popularity": 9,
        "new_release": False,
        "featured": True,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "neon_blocks.png"),
        "category": "Puzzle"
    },
    {
        "id": "cyber_spades",
        "name": "Cyber Spades",
        "description": "Play the classic card game Spades with futuristic twists and special card abilities.",
        "implemented": True,
        "popularity": 6,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "cyber_spades.png"),
        "category": "Card"
    },
    {
        "id": "neo_blackjack",
        "name": "Neo Blackjack",
        "description": "Test your luck and strategy in this enhanced version of Blackjack with special powers.",
        "implemented": True,
        "popularity": 7,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "neo_blackjack.png"),
        "category": "Card"
    },
    {
        "id": "quantum_solitaire",
        "name": "Quantum Solitaire",
        "description": "Play solitaire where cards exist in multiple states until observed, adding strategic depth.",
        "implemented": True,
        "popularity": 5,
        "new_release": False,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "quantum_solitaire.png"),
        "category": "Card"
    },
    {
        "id": "ai_soul_society",
        "name": "AI Soul Society",
        "description": "Create, nurture, and evolve digital AI beings in a virtual society with emergent behaviors.",
        "implemented": True,
        "popularity": 10,
        "new_release": True,
        "featured": True,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "ai_soul_society.png"),
        "category": "Simulation"
    },
    {
        "id": "pixel_quest",
        "name": "Pixel Quest",
        "description": "Embark on a retro-style RPG adventure with turn-based combat and pixel art graphics.",
        "implemented": True,
        "popularity": 8,
        "new_release": False,
        "featured": True,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "pixel_quest.png"),
        "category": "RPG"
    },
    {
        "id": "cyber_knights",
        "name": "Cyber Knights",
        "description": "Lead a team of cybernetically enhanced knights in a dystopian future RPG.",
        "implemented": True,
        "popularity": 7,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "cyber_knights.png"),
        "category": "RPG"
    },
    {
        "id": "dragon_realm",
        "name": "Dragon Realm",
        "description": "Explore a vast fantasy world filled with dragons, magic, and epic quests.",
        "implemented": True,
        "popularity": 9,
        "new_release": True,
        "featured": True,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "dragon_realm.png"),
        "category": "RPG"
    },
    {
        "id": "space_commander",
        "name": "Space Commander",
        "description": "Command a fleet of starships in strategic space battles across the galaxy.",
        "implemented": True,
        "popularity": 8,
        "new_release": False,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "space_commander.png"),
        "category": "Strategy"
    },
    {
        "id": "quantum_tactics",
        "name": "Quantum Tactics",
        "description": "Deploy tactical units in turn-based combat with quantum mechanics altering the battlefield.",
        "implemented": True,
        "popularity": 7,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "quantum_tactics.png"),
        "category": "Strategy"
    },
    {
        "id": "civilization_nexus",
        "name": "Civilization Nexus",
        "description": "Build, expand, and conquer in this 4X strategy game spanning multiple eras of development.",
        "implemented": True,
        "popularity": 9,
        "new_release": True,
        "featured": True,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "civilization_nexus.png"),
        "category": "Strategy"
    },
    {
        "id": "quantum_chess",
        "name": "Quantum Chess",
        "description": "Play chess with a timer where pieces can exist in quantum superposition until observed.",
        "implemented": True,
        "popularity": 8,
        "new_release": True,
        "featured": True,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "quantum_chess.png"),
        "category": "Chess"
    },
    {
        "id": "zen_chess",
        "name": "Zen Chess",
        "description": "Experience a meditative approach to chess with no time pressure and beautiful aesthetics.",
        "implemented": True,
        "popularity": 6,
        "new_release": False,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "zen_chess.png"),
        "category": "Chess"
    },
    {
        "id": "team_chess_arena",
        "name": "Team Chess Arena",
        "description": "Compete in 2v2 team chess matches where coordination and strategy are key to victory.",
        "implemented": True,
        "popularity": 7,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "team_chess_arena.png"),
        "category": "Chess"
    },
    {
        "id": "ai_chess_partner",
        "name": "AI Chess Partner",
        "description": "Play chess with an AI partner that suggests moves and helps you develop winning strategies.",
        "implemented": True,
        "popularity": 9,
        "new_release": True,
        "featured": True,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "ai_chess_partner.png"),
        "category": "Chess"
    },
    {
        "id": "ai_chess_mentor",
        "name": "AI Chess Mentor",
        "description": "Learn chess from an AI mentor that guides your moves but lets you make the final decisions.",
        "implemented": True,
        "popularity": 8,
        "new_release": True,
        "featured": False,
        "thumbnail": os.path.join(THUMBNAIL_PATH, "ai_chess_mentor.png"),
        "category": "Chess"
    }
]

class ParticleSystem:
    """Particle system for background effects."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize the particle system."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particles = []
        self.create_particles(50)  # Start with 50 particles
    
    def create_particles(self, count: int):
        """Create a number of particles."""
        for _ in range(count):
            self.particles.append({
                'x': random.randint(0, self.screen_width),
                'y': random.randint(0, self.screen_height),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.2, 1.0),
                'direction': random.uniform(0, math.pi * 2),
                'lifetime': random.uniform(5, 15),
                'age': random.uniform(0, 5),  # Start at different ages for variety
                'color': self._get_random_color()
            })
    
    def _get_random_color(self) -> Tuple[int, int, int]:
        """Get a random color for particles."""
        colors = [
            (100, 100, 255),  # Blue
            (150, 100, 255),  # Purple
            (255, 100, 255),  # Pink
            (100, 255, 255),  # Cyan
            (255, 255, 100),  # Yellow
            (255, 100, 100)   # Red
        ]
        return random.choice(colors)
    
    def update(self, delta_time: float):
        """Update all particles."""
        # Update existing particles
        for i in range(len(self.particles) - 1, -1, -1):
            particle = self.particles[i]
            
            # Update age
            particle['age'] += delta_time
            
            # Remove old particles
            if particle['age'] >= particle['lifetime']:
                self.particles.pop(i)
                continue
            
            # Move particle
            particle['x'] += math.cos(particle['direction']) * particle['speed'] * delta_time * 60
            particle['y'] += math.sin(particle['direction']) * particle['speed'] * delta_time * 60
            
            # Wrap around screen edges
            if particle['x'] < 0:
                particle['x'] = self.screen_width
            elif particle['x'] > self.screen_width:
                particle['x'] = 0
                
            if particle['y'] < 0:
                particle['y'] = self.screen_height
            elif particle['y'] > self.screen_height:
                particle['y'] = 0
        
        # Add new particles if needed
        if len(self.particles) < 50:
            self.create_particles(1)
    
    def draw(self, surface: pygame.Surface):
        """Draw all particles."""
        for particle in self.particles:
            # Calculate alpha based on age
            progress = particle['age'] / particle['lifetime']
            alpha = int(255 * (1 - progress))
            
            # Create a surface with alpha
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            
            # Draw particle with glow effect
            pygame.draw.circle(
                particle_surface,
                (*particle['color'], alpha),
                (particle['size'], particle['size']),
                particle['size']
            )
            
            # Draw the particle
            surface.blit(
                particle_surface, 
                (int(particle['x']) - particle['size'], 
                 int(particle['y']) - particle['size'])
            )

class GridBackground:
    """Grid background with tech-inspired design."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize the grid background."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = 40
        self.grid_color = (40, 40, 80, 20)  # Semi-transparent
        self.animation_time = 0
        
        # Create the background surface
        self.background = self._create_background()
        
        # Create nodes
        self.nodes = []
        for _ in range(20):
            self.nodes.append({
                'x': random.randint(0, self.screen_width),
                'y': random.randint(0, self.screen_height),
                'size': random.randint(2, 5),
                'pulse_speed': random.uniform(1.0, 3.0),
                'color': (100, 100, 255)  # Blue
            })
        
        # Create connections between nodes
        self.connections = []
        for i in range(len(self.nodes)):
            # Connect to 1-3 other nodes
            for _ in range(random.randint(1, 3)):
                j = random.randint(0, len(self.nodes) - 1)
                if i != j:
                    self.connections.append({
                        'start': i,
                        'end': j,
                        'color': (100, 100, 255, 100)  # Semi-transparent blue
                    })
    
    def _create_background(self) -> pygame.Surface:
        """Create the background surface with gradient."""
        background = pygame.Surface((self.screen_width, self.screen_height))
        
        # Fill with gradient
        for y in range(self.screen_height):
            # Calculate color for this line
            progress = y / self.screen_height
            color_top = (10, 5, 30)  # Dark purple
            color_bottom = (5, 0, 20)  # Darker purple
            
            color = tuple(
                int(color_top[i] * (1 - progress) + color_bottom[i] * progress)
                for i in range(3)
            )
            
            # Draw horizontal line with this color
            pygame.draw.line(
                background,
                color,
                (0, y),
                (self.screen_width - 1, y)
            )
        
        return background
    
    def update(self, delta_time: float):
        """Update the grid background."""
        self.animation_time += delta_time
    
    def draw(self, surface: pygame.Surface):
        """Draw the grid background."""
        # Draw the background
        surface.blit(self.background, (0, 0))
        
        # Draw grid lines
        grid_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        
        # Horizontal grid lines
        for y in range(0, self.screen_height, self.grid_size):
            pygame.draw.line(
                grid_surface,
                self.grid_color,
                (0, y),
                (self.screen_width, y)
            )
        
        # Vertical grid lines
        for x in range(0, self.screen_width, self.grid_size):
            pygame.draw.line(
                grid_surface,
                self.grid_color,
                (x, 0),
                (x, self.screen_height)
            )
        
        # Draw grid
        surface.blit(grid_surface, (0, 0))
        
        # Draw connections between nodes
        for connection in self.connections:
            start_node = self.nodes[connection['start']]
            end_node = self.nodes[connection['end']]
            
            # Calculate alpha based on animation
            alpha = int(100 + 50 * math.sin(self.animation_time * 2))
            color = (*connection['color'][:3], alpha)
            
            # Draw line with alpha
            connection_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            pygame.draw.line(
                connection_surface,
                color,
                (start_node['x'], start_node['y']),
                (end_node['x'], end_node['y']),
                1
            )
            surface.blit(connection_surface, (0, 0))
        
        # Draw nodes
        for node in self.nodes:
            # Calculate pulse effect
            pulse = (math.sin(self.animation_time * node['pulse_speed']) + 1) * 0.5  # 0 to 1
            size = node['size'] + pulse * 2
            
            # Draw node with glow
            glow_surface = pygame.Surface((int(size * 4), int(size * 4)), pygame.SRCALPHA)
            
            # Draw outer glow
            pygame.draw.circle(
                glow_surface,
                (*node['color'], 50),  # Semi-transparent
                (int(size * 2), int(size * 2)),
                int(size * 2)
            )
            
            # Draw inner glow
            pygame.draw.circle(
                glow_surface,
                (*node['color'], 100),  # More opaque
                (int(size * 2), int(size * 2)),
                int(size * 1.5)
            )
            
            # Draw core
            pygame.draw.circle(
                glow_surface,
                node['color'],
                (int(size * 2), int(size * 2)),
                int(size)
            )
            
            # Draw the node
            surface.blit(
                glow_surface, 
                (node['x'] - int(size * 2), node['y'] - int(size * 2))
            )

class GameCard:
    """Game card UI element for pygame_gui."""
    
    def __init__(self, ui_manager: pygame_gui.UIManager, game_info: Dict, rect: pygame.Rect, 
                 on_click: Callable[[str], None]):
        """
        Initialize a game card.
        
        Args:
            ui_manager: The pygame_gui UIManager
            game_info: Information about the game
            rect: The rectangle for the card
            on_click: Function to call when clicked
        """
        self.ui_manager = ui_manager
        self.game_info = game_info
        self.rect = rect
        self.on_click = on_click
        
        # Create the panel
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=rect,
            manager=ui_manager,
            starting_height=1,
            margins={'left': 1, 'right': 1, 'top': 1, 'bottom': 1},
            object_id=f"#game_card_{game_info['id']}"
        )
        
        # Load thumbnail if available
        self.thumbnail = None
        thumbnail_path = game_info.get('thumbnail')
        if thumbnail_path and os.path.exists(thumbnail_path):
            try:
                # Load the thumbnail image
                self.thumbnail = pygame.image.load(thumbnail_path)
                
                # Create thumbnail image element
                thumbnail_rect = pygame.Rect(10, 10, rect.width - 20, 80)  # Reduced height
                
                # Scale the thumbnail to fit
                scaled_thumbnail = pygame.transform.scale(self.thumbnail, (thumbnail_rect.width, thumbnail_rect.height))
                
                # Create the image element
                self.thumbnail_element = pygame_gui.elements.UIImage(
                    relative_rect=thumbnail_rect,
                    image_surface=scaled_thumbnail,
                    manager=ui_manager,
                    container=self.panel,
                    object_id=f"#game_card_{game_info['id']}_thumbnail"
                )
                
                # Adjust layout for thumbnail
                title_y = 95  # Adjusted position
            except Exception as e:
                print(f"Error loading thumbnail for {game_info['id']}: {e}")
                title_y = 10
        else:
            title_y = 10
        
        # Create the title
        title_rect = pygame.Rect(0, title_y, rect.width - 20, 25)  # Reduced height
        self.title = pygame_gui.elements.UILabel(
            relative_rect=title_rect,
            text=game_info['name'],
            manager=ui_manager,
            container=self.panel,
            object_id=f"#game_card_{game_info['id']}_title"
        )
        
        # Create the description
        desc_rect = pygame.Rect(10, title_y + 30, rect.width - 20, 50)  # Reduced height
        self.description = pygame_gui.elements.UITextBox(
            html_text=game_info['description'],
            relative_rect=desc_rect,
            manager=ui_manager,
            container=self.panel,
            object_id=f"#game_card_{game_info['id']}_description"
        )
        
        # Create the play button
        button_rect = pygame.Rect((rect.width - 100) // 2, rect.height - 40, 100, 30)
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=button_rect,
            text="PLAY",
            manager=ui_manager,
            container=self.panel,
            object_id=f"#game_card_{game_info['id']}_button"
        )
        
        # Add badges if needed
        self.badges = []
        
        # New release badge
        if game_info.get('new_release', False):
            new_badge_rect = pygame.Rect(rect.width - 60, 10, 50, 20)
            new_badge = pygame_gui.elements.UILabel(
                relative_rect=new_badge_rect,
                text="NEW!",
                manager=ui_manager,
                container=self.panel,
                object_id="#new_badge"
            )
            self.badges.append(new_badge)
        
        # Featured badge
        if game_info.get('featured', False):
            featured_badge_rect = pygame.Rect(10, 10, 70, 20)
            featured_badge = pygame_gui.elements.UILabel(
                relative_rect=featured_badge_rect,
                text="FEATURED",
                manager=ui_manager,
                container=self.panel,
                object_id="#featured_badge"
            )
            self.badges.append(featured_badge)
        
        # Create popularity stars
        self.stars = []
        popularity = game_info.get('popularity', 0)
        star_count = min(5, max(0, popularity // 2))  # 0-10 scale to 0-5 stars
        
        for i in range(5):
            star_rect = pygame.Rect(10 + i * 15, rect.height - 60, 10, 10)  # Smaller stars, adjusted position
            star_filled = i < star_count
            star = pygame_gui.elements.UIImage(
                relative_rect=star_rect,
                image_surface=self._create_star_image(filled=star_filled, size=10),  # Smaller stars
                manager=ui_manager,
                container=self.panel,
                object_id="#star_filled" if star_filled else "#star_empty"
            )
            self.stars.append(star)
    
    def _create_star_image(self, filled: bool = True, size: int = 15) -> pygame.Surface:
        """
        Create a star image.
        
        Args:
            filled: Whether the star is filled
            size: Size of the star image
            
        Returns:
            Star image surface
        """
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        if filled:
            color = (255, 215, 0)  # Gold
        else:
            color = (100, 100, 100)  # Gray
        
        # Draw a simple star
        points = []
        for i in range(5):
            # Outer points
            angle_outer = math.pi / 2 + i * 2 * math.pi / 5
            x_outer = size / 2 + size / 2 * 0.9 * math.cos(angle_outer)
            y_outer = size / 2 - size / 2 * 0.9 * math.sin(angle_outer)
            points.append((x_outer, y_outer))
            
            # Inner points
            angle_inner = math.pi / 2 + (i + 0.5) * 2 * math.pi / 5
            x_inner = size / 2 + size / 2 * 0.4 * math.cos(angle_inner)
            y_inner = size / 2 - size / 2 * 0.4 * math.sin(angle_inner)
            points.append((x_inner, y_inner))
        
        if filled:
            pygame.draw.polygon(surface, color, points)
        else:
            pygame.draw.polygon(surface, color, points, 1)
        
        return surface
    
    def process_event(self, event: pygame.event.Event) -> bool:
        """
        Process events for this card.
        
        Args:
            event: The event to process
            
        Returns:
            True if the event was handled
        """
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_button:
                self.on_click(self.game_info['id'])
                return True
        
        return False
    
    def update(self, delta_time: float):
        """
        Update the card.
        
        Args:
            delta_time: Time since last update
        """
        pass
    
    def kill(self):
        """Destroy the card and all its elements."""
        for star in self.stars:
            star.kill()
        
        for badge in self.badges:
            badge.kill()
        
        self.play_button.kill()
        self.description.kill()
        self.title.kill()
        
        if hasattr(self, 'thumbnail_element'):
            self.thumbnail_element.kill()
            
        self.panel.kill()

class ProfessionalMenu:
    """Professional menu interface using pygame_gui."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize the professional menu.
        
        Args:
            screen_width: Width of the screen
            screen_height: Height of the screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("SoulCoreLegacy Arcade")
        
        # Create clock
        self.clock = pygame.time.Clock()
        
        # Create UI manager with theme
        self.ui_manager = pygame_gui.UIManager((screen_width, screen_height), 'pygame_gui_theme.json')
        
        # Create background effects
        self.grid_background = GridBackground(screen_width, screen_height)
        self.particle_system = ParticleSystem(screen_width, screen_height)
        
        # Create UI elements
        self._create_ui_elements()
        
        # Game cards
        self.game_cards = []
        self._create_game_cards()
        
        # Add scrollbar for vertical scrolling if needed
        self.scrollbar = None
        self.setup_scrolling()
    
    def _create_ui_elements(self):
        """Create the UI elements."""
        # Create title
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen_width - 500) // 2, 30, 500, 50),
            text="SoulCoreLegacy Arcade",
            manager=self.ui_manager,
            object_id="#title_label"
        )
        
        # Create subtitle
        self.subtitle_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen_width - 300) // 2, 80, 300, 30),
            text="Select a game to play",
            manager=self.ui_manager,
            object_id="#subtitle_label"
        )
        
        # Create footer
        self.footer_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen_width - 400) // 2, self.screen_height - 40, 400, 30),
            text="Press ESC to return to menu from any game",
            manager=self.ui_manager,
            object_id="#footer_label"
        )
        
        # Create settings button
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.screen_width - 150, 20, 130, 40),
            text="Settings",
            manager=self.ui_manager,
            object_id="#settings_button"
        )
        
        # Create quit button
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(20, 20, 100, 40),
            text="Quit",
            manager=self.ui_manager,
            object_id="#quit_button"
        )
    
    def _create_game_cards(self):
        """Create game cards for each game."""
        # Clear existing cards
        for card in self.game_cards:
            card.kill()
        
        self.game_cards = []
        
        # Calculate card layout
        card_width = 300
        card_height = 250  # Reduced height to fit screen better
        cards_per_row = 3
        horizontal_spacing = 30
        vertical_spacing = 20  # Reduced vertical spacing
        
        # Calculate starting position
        start_x = (self.screen_width - (cards_per_row * card_width + (cards_per_row - 1) * horizontal_spacing)) // 2
        start_y = 130  # Moved up slightly
        
        # Create a card for each game
        for i, game in enumerate(GAME_LIST):
            # Calculate position
            row = i // cards_per_row
            col = i % cards_per_row
            x = start_x + col * (card_width + horizontal_spacing)
            y = start_y + row * (card_height + vertical_spacing)
            
            # Create the card
            card = GameCard(
                ui_manager=self.ui_manager,
                game_info=game,
                rect=pygame.Rect(x, y, card_width, card_height),
                on_click=self._on_game_selected
            )
            
            # Add the card to the list
            self.game_cards.append(card)
    
    def _on_game_selected(self, game_id: str):
        """
        Handle game selection.
        
        Args:
            game_id: ID of the selected game
        """
        print(f"Game selected: {game_id}")
    
    def setup_scrolling(self):
        """Set up scrolling for the game cards if needed."""
        # Calculate total height needed
        if len(self.game_cards) > 0:
            last_card = self.game_cards[-1]
            total_content_height = last_card.rect.bottom + 50  # Add some padding
            
            # If content exceeds screen height, add scrollbar
            if total_content_height > self.screen_height:
                self.scrollbar = pygame_gui.elements.UIVerticalScrollBar(
                    relative_rect=pygame.Rect(self.screen_width - 20, 120, 20, self.screen_height - 160),
                    visible_percentage=(self.screen_height - 160) / total_content_height,
                    manager=self.ui_manager
                )
    
    def handle_scrolling(self, event):
        """Handle scrolling events."""
        if hasattr(self, 'scrollbar') and self.scrollbar:
            # Check for mouse wheel events
            if event.type == pygame.MOUSEWHEEL:
                scroll_amount = event.y * -0.1  # Adjust scroll speed
                self.scrollbar.scroll_position = max(0.0, min(1.0, self.scrollbar.scroll_position + scroll_amount))
                self.update_card_positions()
            
            # Check for scrollbar movement using a more generic approach
            if event.type == pygame.USEREVENT:
                if hasattr(event, 'ui_element') and event.ui_element == self.scrollbar:
                    self.update_card_positions()
            
            # Check for mouse clicks on scrollbar arrows
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if clicked on up arrow (top of scrollbar)
                scrollbar_rect = self.scrollbar.rect
                up_arrow_rect = pygame.Rect(scrollbar_rect.x, scrollbar_rect.y, scrollbar_rect.width, 20)
                if up_arrow_rect.collidepoint(mouse_pos):
                    self.scrollbar.scroll_position = max(0.0, self.scrollbar.scroll_position - 0.1)
                    self.update_card_positions()
                
                # Check if clicked on down arrow (bottom of scrollbar)
                down_arrow_rect = pygame.Rect(scrollbar_rect.x, scrollbar_rect.bottom - 20, scrollbar_rect.width, 20)
                if down_arrow_rect.collidepoint(mouse_pos):
                    self.scrollbar.scroll_position = min(1.0, self.scrollbar.scroll_position + 0.1)
                    self.update_card_positions()
                
                # Check if clicked on scrollbar track
                track_rect = pygame.Rect(scrollbar_rect.x, scrollbar_rect.y + 20, 
                                        scrollbar_rect.width, scrollbar_rect.height - 40)
                if track_rect.collidepoint(mouse_pos):
                    # Calculate relative position in track
                    relative_pos = (mouse_pos[1] - track_rect.y) / track_rect.height
                    self.scrollbar.scroll_position = max(0.0, min(1.0, relative_pos))
                    self.update_card_positions()
    
    def update_card_positions(self):
        """Update card positions based on scroll position."""
        if not hasattr(self, 'scrollbar') or not self.scrollbar or not self.game_cards:
            return
            
        # Calculate total height needed
        last_card = self.game_cards[-1]
        total_content_height = last_card.rect.bottom + 50
        
        # Calculate scroll offset
        scroll_height = total_content_height - (self.screen_height - 160)
        scroll_offset = int(self.scrollbar.scroll_position * scroll_height)
        
        # Apply offset to all cards
        for card in self.game_cards:
            # Get the original y position (without scrolling)
            original_y = card.rect.y
            
            # Apply scroll offset
            card.panel.set_position((card.rect.x, original_y - scroll_offset))
    
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event: The event to handle
        """
        # Handle scrolling
        self.handle_scrolling(event)
        
        # Process UI events
        self.ui_manager.process_events(event)
        
        # Process game card events
        for card in self.game_cards:
            card.process_event(event)
        
        # Handle button events
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.quit_button:
                return False  # Signal to quit
            elif event.ui_element == self.settings_button:
                print("Settings button pressed")
        
        return True  # Continue running
    
    def update(self, time_delta: float):
        """
        Update the menu state.
        
        Args:
            time_delta: Time since last update
        """
        # Update background effects
        self.grid_background.update(time_delta)
        self.particle_system.update(time_delta)
        
        # Update UI
        self.ui_manager.update(time_delta)
    
    def draw(self, surface: pygame.Surface):
        """
        Draw the menu.
        
        Args:
            surface: Surface to draw on
        """
        # Draw background effects
        self.grid_background.draw(surface)
        self.particle_system.draw(surface)
        
        # Draw UI
        self.ui_manager.draw_ui(surface)
    
    def run(self):
        """Run the menu loop."""
        running = True
        
        while running:
            # Calculate delta time
            time_delta = self.clock.tick(FPS) / 1000.0
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle events
                if not self.handle_event(event):
                    running = False
            
            # Update
            self.update(time_delta)
            
            # Draw
            self.draw(self.screen)
            
            # Update display
            pygame.display.update()
        
        # Clean up
        pygame.quit()

if __name__ == "__main__":
    menu = ProfessionalMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
    menu.run()
