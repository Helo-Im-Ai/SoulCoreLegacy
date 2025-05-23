"""
SoulCoreLegacy Arcade - Cloud Configuration
-----------------------------------------
This module provides configuration for cloud services.
"""

import os
import json
import yaml
from pathlib import Path

class CloudConfig:
    """Configuration for cloud services."""
    
    def __init__(self, config_file=None):
        """
        Initialize the cloud configuration.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self.config = {
            # Default configuration
            'region': 'us-west-2',
            'environment': 'development',
            'services': {
                'auth': {
                    'enabled': True,
                    'provider': 'cognito',
                    'user_pool_id': '',
                    'client_id': ''
                },
                'storage': {
                    'enabled': True,
                    'provider': 's3',
                    'bucket_name': 'soulcorelegacy-storage',
                    'table_name': 'soulcorelegacy-data'
                },
                'multiplayer': {
                    'enabled': True,
                    'provider': 'gamelift',
                    'fleet_id': '',
                    'max_players': 4,
                    'matchmaking_config': ''
                },
                'analytics': {
                    'enabled': True,
                    'provider': 'kinesis',
                    'stream_name': 'soulcorelegacy-analytics'
                }
            }
        }
        
        # Load configuration from file if provided
        if config_file:
            self.load_config(config_file)
        
        # Override with environment variables
        self._load_from_env()
    
    def load_config(self, config_file):
        """
        Load configuration from a file.
        
        Args:
            config_file (str): Path to the configuration file
        """
        path = Path(config_file)
        
        if not path.exists():
            print(f"Warning: Configuration file {config_file} not found.")
            return
        
        try:
            if path.suffix == '.json':
                with open(path, 'r') as f:
                    loaded_config = json.load(f)
            elif path.suffix in ['.yaml', '.yml']:
                with open(path, 'r') as f:
                    loaded_config = yaml.safe_load(f)
            else:
                print(f"Warning: Unsupported configuration file format: {path.suffix}")
                return
            
            # Update the configuration
            self._update_config(loaded_config)
            print(f"Loaded configuration from {config_file}")
        except Exception as e:
            print(f"Error loading configuration from {config_file}: {e}")
    
    def _update_config(self, new_config):
        """
        Update the configuration with new values.
        
        Args:
            new_config (dict): New configuration values
        """
        def update_dict(target, source):
            for key, value in source.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    update_dict(target[key], value)
                else:
                    target[key] = value
        
        update_dict(self.config, new_config)
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        # Region
        if 'AWS_REGION' in os.environ:
            self.config['region'] = os.environ['AWS_REGION']
        
        # Environment
        if 'SOULCORE_ENV' in os.environ:
            self.config['environment'] = os.environ['SOULCORE_ENV']
        
        # Auth
        if 'SOULCORE_AUTH_ENABLED' in os.environ:
            self.config['services']['auth']['enabled'] = os.environ['SOULCORE_AUTH_ENABLED'].lower() == 'true'
        if 'SOULCORE_AUTH_PROVIDER' in os.environ:
            self.config['services']['auth']['provider'] = os.environ['SOULCORE_AUTH_PROVIDER']
        if 'SOULCORE_AUTH_USER_POOL_ID' in os.environ:
            self.config['services']['auth']['user_pool_id'] = os.environ['SOULCORE_AUTH_USER_POOL_ID']
        if 'SOULCORE_AUTH_CLIENT_ID' in os.environ:
            self.config['services']['auth']['client_id'] = os.environ['SOULCORE_AUTH_CLIENT_ID']
        
        # Storage
        if 'SOULCORE_STORAGE_ENABLED' in os.environ:
            self.config['services']['storage']['enabled'] = os.environ['SOULCORE_STORAGE_ENABLED'].lower() == 'true'
        if 'SOULCORE_STORAGE_PROVIDER' in os.environ:
            self.config['services']['storage']['provider'] = os.environ['SOULCORE_STORAGE_PROVIDER']
        if 'SOULCORE_STORAGE_BUCKET' in os.environ:
            self.config['services']['storage']['bucket_name'] = os.environ['SOULCORE_STORAGE_BUCKET']
        if 'SOULCORE_STORAGE_TABLE' in os.environ:
            self.config['services']['storage']['table_name'] = os.environ['SOULCORE_STORAGE_TABLE']
        
        # Multiplayer
        if 'SOULCORE_MULTIPLAYER_ENABLED' in os.environ:
            self.config['services']['multiplayer']['enabled'] = os.environ['SOULCORE_MULTIPLAYER_ENABLED'].lower() == 'true'
        if 'SOULCORE_MULTIPLAYER_PROVIDER' in os.environ:
            self.config['services']['multiplayer']['provider'] = os.environ['SOULCORE_MULTIPLAYER_PROVIDER']
        if 'SOULCORE_MULTIPLAYER_FLEET_ID' in os.environ:
            self.config['services']['multiplayer']['fleet_id'] = os.environ['SOULCORE_MULTIPLAYER_FLEET_ID']
        
        # Analytics
        if 'SOULCORE_ANALYTICS_ENABLED' in os.environ:
            self.config['services']['analytics']['enabled'] = os.environ['SOULCORE_ANALYTICS_ENABLED'].lower() == 'true'
        if 'SOULCORE_ANALYTICS_PROVIDER' in os.environ:
            self.config['services']['analytics']['provider'] = os.environ['SOULCORE_ANALYTICS_PROVIDER']
        if 'SOULCORE_ANALYTICS_STREAM' in os.environ:
            self.config['services']['analytics']['stream_name'] = os.environ['SOULCORE_ANALYTICS_STREAM']
    
    def get(self, key, default=None):
        """
        Get a configuration value.
        
        Args:
            key (str): The configuration key
            default: The default value if the key is not found
            
        Returns:
            The configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_service_config(self, service_name):
        """
        Get the configuration for a specific service.
        
        Args:
            service_name (str): The name of the service
            
        Returns:
            dict: The service configuration
        """
        return self.config.get('services', {}).get(service_name, {})
