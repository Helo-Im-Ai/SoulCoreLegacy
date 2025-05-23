"""
SoulCoreLegacy Arcade - Cloud Integration
----------------------------------------
This module provides cloud integration for the SoulCoreLegacy Arcade.
"""

# Import submodules for easier access
from cloud.config import CloudConfig
from cloud.auth import AuthService
from cloud.storage import StorageService
from cloud.multiplayer import MultiplayerService
from cloud.analytics import AnalyticsService

# Initialize services
def initialize_cloud_services(config_file=None):
    """
    Initialize all cloud services.
    
    Args:
        config_file (str): Path to the configuration file
        
    Returns:
        dict: Dictionary containing all initialized services
    """
    # Load configuration
    config = CloudConfig(config_file)
    
    # Initialize services
    auth = AuthService(config)
    storage = StorageService(config)
    multiplayer = MultiplayerService(config)
    analytics = AnalyticsService(config)
    
    return {
        'config': config,
        'auth': auth,
        'storage': storage,
        'multiplayer': multiplayer,
        'analytics': analytics
    }
