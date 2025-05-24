"""
SoulCoreLegacy Arcade - NFT Artisan Game
--------------------------------------
This module implements the NFT Artisan game, where players create unique digital art.
"""

import pygame
import time
import random
import math
import uuid
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, WHITE, PRIMARY_COLOR, SECONDARY_COLOR
from core.asset_loader import load_font, create_gradient_background

class NFTArtisanGame:
    """
    Implementation of the NFT Artisan game.
    """
    
    def __init__(self, game_manager):
        """
        Initialize the NFT Artisan game.
        
        Args:
            game_manager (GameManager): Reference to the game manager
        """
        self.game_manager = game_manager
        
        # Game state
        self.current_nft = None
        self.collection = []
        self.max_collection_size = 10
        self.creating = False
        self.viewing_collection = False
        self.current_view_index = 0
        self.waiting_for_start = True
        
        # NFT generation parameters
        self.generation_params = {
            'shape_count': random.randint(5, 15),
            'color_scheme': random.choice(['rainbow', 'monochrome', 'complementary', 'analogous']),
            'background_style': random.choice(['gradient', 'solid', 'pattern']),
            'complexity': random.uniform(0.5, 1.0)
        }
        
        # Create fonts
        self.font = load_font("Arial", 36)
        self.message_font = load_font("Arial", 24)
        self.small_font = load_font("Arial", 18)
        
        # Create background
        self.background = create_gradient_background(
            SCREEN_WIDTH, 
            SCREEN_HEIGHT, 
            (20, 10, 40),  # Dark purple
            (40, 20, 80)   # Medium purple
        )
        
        # Get cloud services
        self.storage_service = self.game_manager.get_cloud_service('storage')
        self.analytics_service = self.game_manager.get_cloud_service('analytics')
        
        # Reset the game
        self.reset()
    
    def reset(self):
        """Reset the game state."""
        self.current_nft = None
        self.creating = False
        self.viewing_collection = False
        self.current_view_index = 0
        self.waiting_for_start = True
        
        # Load collection from storage
        self.load_collection()
        
        # Track game start
        if self.analytics_service:
            self.analytics_service.track_game_start('nft_artisan', 'create')
    
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        if event.type == pygame.KEYDOWN:
            # Start the game
            if event.key == pygame.K_SPACE:
                if self.waiting_for_start:
                    self.waiting_for_start = False
                    self.show_main_menu()
                elif self.creating:
                    self.generate_nft()
            
            # Navigation in collection view
            elif event.key == pygame.K_LEFT and self.viewing_collection:
                self.current_view_index = (self.current_view_index - 1) % len(self.collection)
            elif event.key == pygame.K_RIGHT and self.viewing_collection:
                self.current_view_index = (self.current_view_index + 1) % len(self.collection)
            
            # Return to main menu
            elif event.key == pygame.K_ESCAPE:
                if self.creating or self.viewing_collection:
                    self.show_main_menu()
            
            # Save/load keys
            elif event.key == pygame.K_s:
                self.save_collection()
            elif event.key == pygame.K_l:
                self.load_collection()
        
        # Handle mouse clicks for menu options
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Main menu buttons
            if not self.waiting_for_start and not self.creating and not self.viewing_collection:
                # Create NFT button
                create_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50)
                if create_button_rect.collidepoint(mouse_pos):
                    self.start_creating()
                
                # View Collection button
                view_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 10, 200, 50)
                if view_button_rect.collidepoint(mouse_pos):
                    self.start_viewing_collection()
    
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
        
        # Draw title
        title_text = self.font.render("NFT Artisan", True, PRIMARY_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        # Draw waiting for start message
        if self.waiting_for_start:
            message = "Press SPACE to start"
            message_text = self.message_font.render(message, True, WHITE)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(message_text, message_rect)
            
            # Draw description
            description = "Create unique digital art pieces for your collection"
            desc_text = self.small_font.render(description, True, SECONDARY_COLOR)
            desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(desc_text, desc_rect)
        
        # Draw main menu
        elif not self.creating and not self.viewing_collection:
            self.render_main_menu(screen)
        
        # Draw NFT creation screen
        elif self.creating:
            self.render_creation_screen(screen)
        
        # Draw collection view
        elif self.viewing_collection:
            self.render_collection_view(screen)
        
        # Draw controls help
        controls_text = self.small_font.render("S: Save  L: Load  ESC: Back", True, WHITE)
        screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, SCREEN_HEIGHT - 30))
    
    def render_main_menu(self, screen):
        """
        Render the main menu.
        
        Args:
            screen (pygame.Surface): The surface to render on
        """
        # Draw menu title
        menu_title = "Main Menu"
        menu_title_text = self.message_font.render(menu_title, True, WHITE)
        menu_title_rect = menu_title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(menu_title_text, menu_title_rect)
        
        # Draw Create NFT button
        create_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50)
        pygame.draw.rect(screen, PRIMARY_COLOR, create_button_rect, border_radius=10)
        create_text = self.message_font.render("Create NFT", True, WHITE)
        create_text_rect = create_text.get_rect(center=create_button_rect.center)
        screen.blit(create_text, create_text_rect)
        
        # Draw View Collection button
        view_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 10, 200, 50)
        pygame.draw.rect(screen, SECONDARY_COLOR, view_button_rect, border_radius=10)
        view_text = self.message_font.render("View Collection", True, WHITE)
        view_text_rect = view_text.get_rect(center=view_button_rect.center)
        screen.blit(view_text, view_text_rect)
        
        # Draw collection count
        collection_count = f"Collection: {len(self.collection)}/{self.max_collection_size}"
        count_text = self.small_font.render(collection_count, True, WHITE)
        count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(count_text, count_rect)
    
    def render_creation_screen(self, screen):
        """
        Render the NFT creation screen.
        
        Args:
            screen (pygame.Surface): The surface to render on
        """
        # Draw screen title
        screen_title = "NFT Creation"
        screen_title_text = self.message_font.render(screen_title, True, WHITE)
        screen_title_rect = screen_title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(screen_title_text, screen_title_rect)
        
        # Draw the current NFT if it exists
        if self.current_nft:
            # Draw NFT frame
            nft_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150, 300, 300)
            pygame.draw.rect(screen, (50, 50, 50), nft_rect)
            
            # Draw the NFT
            screen.blit(self.current_nft, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 140))
            
            # Draw save button
            save_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 170, 200, 40)
            pygame.draw.rect(screen, PRIMARY_COLOR, save_button_rect, border_radius=10)
            save_text = self.small_font.render("Save to Collection", True, WHITE)
            save_text_rect = save_text.get_rect(center=save_button_rect.center)
            screen.blit(save_text, save_text_rect)
        else:
            # Draw generate button
            generate_text = self.message_font.render("Press SPACE to Generate NFT", True, WHITE)
            generate_rect = generate_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(generate_text, generate_rect)
    
    def render_collection_view(self, screen):
        """
        Render the collection view.
        
        Args:
            screen (pygame.Surface): The surface to render on
        """
        # Draw screen title
        screen_title = "Your Collection"
        screen_title_text = self.message_font.render(screen_title, True, WHITE)
        screen_title_rect = screen_title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(screen_title_text, screen_title_rect)
        
        if self.collection:
            # Draw NFT frame
            nft_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150, 300, 300)
            pygame.draw.rect(screen, (50, 50, 50), nft_rect)
            
            # Draw the current NFT from collection
            current_nft = self.collection[self.current_view_index]
            screen.blit(current_nft, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 140))
            
            # Draw navigation text
            nav_text = self.small_font.render("< Left / Right >", True, WHITE)
            nav_rect = nav_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 170))
            screen.blit(nav_text, nav_rect)
            
            # Draw index
            index_text = self.small_font.render(f"{self.current_view_index + 1}/{len(self.collection)}", True, WHITE)
            index_rect = index_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))
            screen.blit(index_text, index_rect)
        else:
            # Draw empty collection message
            empty_text = self.message_font.render("Your collection is empty", True, WHITE)
            empty_rect = empty_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(empty_text, empty_rect)
    
    def show_main_menu(self):
        """Show the main menu."""
        self.creating = False
        self.viewing_collection = False
        self.current_nft = None
    
    def start_creating(self):
        """Start creating a new NFT."""
        self.creating = True
        self.viewing_collection = False
        self.current_nft = None
    
    def start_viewing_collection(self):
        """Start viewing the collection."""
        self.creating = False
        self.viewing_collection = True
        self.current_view_index = 0 if self.collection else 0
    
    def generate_nft(self):
        """Generate a new NFT."""
        # Create a surface for the NFT
        nft_surface = pygame.Surface((280, 280))
        nft_surface.fill((0, 0, 0))  # Black background
        
        # Randomize generation parameters
        self.generation_params = {
            'shape_count': random.randint(5, 15),
            'color_scheme': random.choice(['rainbow', 'monochrome', 'complementary', 'analogous']),
            'background_style': random.choice(['gradient', 'solid', 'pattern']),
            'complexity': random.uniform(0.5, 1.0)
        }
        
        # Generate background
        self.generate_background(nft_surface)
        
        # Generate shapes
        self.generate_shapes(nft_surface)
        
        # Add some effects
        self.add_effects(nft_surface)
        
        # Store the generated NFT
        self.current_nft = nft_surface
    
    def generate_background(self, surface):
        """
        Generate a background for the NFT.
        
        Args:
            surface (pygame.Surface): The surface to draw on
        """
        width, height = surface.get_size()
        
        if self.generation_params['background_style'] == 'gradient':
            # Create a gradient background
            color1 = self.get_random_color()
            color2 = self.get_random_color()
            
            for y in range(height):
                # Calculate the ratio of the current position
                ratio = y / height
                
                # Interpolate between the two colors
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                
                # Draw a horizontal line with the calculated color
                pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
        
        elif self.generation_params['background_style'] == 'solid':
            # Create a solid background
            color = self.get_random_color()
            surface.fill(color)
        
        elif self.generation_params['background_style'] == 'pattern':
            # Create a pattern background
            pattern_size = random.randint(10, 30)
            for x in range(0, width, pattern_size):
                for y in range(0, height, pattern_size):
                    color = self.get_random_color()
                    rect = pygame.Rect(x, y, pattern_size, pattern_size)
                    pygame.draw.rect(surface, color, rect)
    
    def generate_shapes(self, surface):
        """
        Generate shapes for the NFT.
        
        Args:
            surface (pygame.Surface): The surface to draw on
        """
        width, height = surface.get_size()
        shape_count = self.generation_params['shape_count']
        
        for _ in range(shape_count):
            shape_type = random.choice(['circle', 'rect', 'polygon', 'line'])
            color = self.get_random_color()
            
            if shape_type == 'circle':
                # Draw a circle
                center_x = random.randint(0, width)
                center_y = random.randint(0, height)
                radius = random.randint(10, 50)
                pygame.draw.circle(surface, color, (center_x, center_y), radius)
            
            elif shape_type == 'rect':
                # Draw a rectangle
                x = random.randint(0, width - 20)
                y = random.randint(0, height - 20)
                w = random.randint(10, 100)
                h = random.randint(10, 100)
                pygame.draw.rect(surface, color, pygame.Rect(x, y, w, h))
            
            elif shape_type == 'polygon':
                # Draw a polygon
                points = []
                point_count = random.randint(3, 6)
                for _ in range(point_count):
                    x = random.randint(0, width)
                    y = random.randint(0, height)
                    points.append((x, y))
                pygame.draw.polygon(surface, color, points)
            
            elif shape_type == 'line':
                # Draw a line
                start_x = random.randint(0, width)
                start_y = random.randint(0, height)
                end_x = random.randint(0, width)
                end_y = random.randint(0, height)
                thickness = random.randint(1, 5)
                pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), thickness)
    
    def add_effects(self, surface):
        """
        Add effects to the NFT.
        
        Args:
            surface (pygame.Surface): The surface to draw on
        """
        width, height = surface.get_size()
        
        # Add some noise
        noise_amount = random.uniform(0, 0.1)
        for x in range(width):
            for y in range(height):
                if random.random() < noise_amount:
                    color = self.get_random_color()
                    surface.set_at((x, y), color)
        
        # Add a border
        border_color = self.get_random_color()
        pygame.draw.rect(surface, border_color, pygame.Rect(0, 0, width, height), 2)
    
    def get_random_color(self):
        """
        Get a random color based on the color scheme.
        
        Returns:
            tuple: RGB color
        """
        if self.generation_params['color_scheme'] == 'rainbow':
            # Return a random color
            return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        elif self.generation_params['color_scheme'] == 'monochrome':
            # Return a monochrome color
            value = random.randint(0, 255)
            return (value, value, value)
        
        elif self.generation_params['color_scheme'] == 'complementary':
            # Return a complementary color
            hue = random.random()
            saturation = random.uniform(0.5, 1.0)
            value = random.uniform(0.5, 1.0)
            r, g, b = self.hsv_to_rgb(hue, saturation, value)
            return (int(r * 255), int(g * 255), int(b * 255))
        
        elif self.generation_params['color_scheme'] == 'analogous':
            # Return an analogous color
            hue = random.random()
            saturation = random.uniform(0.5, 1.0)
            value = random.uniform(0.5, 1.0)
            r, g, b = self.hsv_to_rgb(hue, saturation, value)
            return (int(r * 255), int(g * 255), int(b * 255))
    
    def hsv_to_rgb(self, h, s, v):
        """
        Convert HSV color to RGB.
        
        Args:
            h (float): Hue (0-1)
            s (float): Saturation (0-1)
            v (float): Value (0-1)
            
        Returns:
            tuple: RGB color (0-1)
        """
        if s == 0.0:
            return (v, v, v)
        
        i = int(h * 6)
        f = (h * 6) - i
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        
        i %= 6
        
        if i == 0:
            return (v, t, p)
        elif i == 1:
            return (q, v, p)
        elif i == 2:
            return (p, v, t)
        elif i == 3:
            return (p, q, v)
        elif i == 4:
            return (t, p, v)
        else:
            return (v, p, q)
    
    def save_current_nft(self):
        """Save the current NFT to the collection."""
        if self.current_nft and len(self.collection) < self.max_collection_size:
            self.collection.append(self.current_nft)
            self.current_nft = None
            self.save_collection()
    
    def load_collection(self):
        """Load the NFT collection from storage."""
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
        
        state = self.storage_service.load_game_state('nft_artisan', user_id)
        
        if not state:
            print("No saved collection found.")
            self.collection = []
            return
        
        # For now, just initialize with empty collection
        # In a real implementation, we would deserialize the NFT surfaces
        self.collection = []
    
    def save_collection(self):
        """Save the NFT collection to storage."""
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
        
        # For now, just save the collection count
        # In a real implementation, we would serialize the NFT surfaces
        state = {
            'collection_count': len(self.collection)
        }
        
        success = self.storage_service.save_game_state('nft_artisan', user_id, state)
        
        if success:
            print("Collection saved successfully.")
        else:
            print("Failed to save collection.")
