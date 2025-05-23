"""
SoulCoreLegacy Arcade - Storage Service
-------------------------------------
This module provides cloud storage services for the SoulCoreLegacy Arcade.
"""

import json
import os
from pathlib import Path

class StorageService:
    """Storage service for cloud integration."""
    
    def __init__(self, config):
        """
        Initialize the storage service.
        
        Args:
            config (CloudConfig): The cloud configuration
        """
        self.config = config
        self.service_config = config.get_service_config('storage')
        self.enabled = self.service_config.get('enabled', False)
        self.provider = self.service_config.get('provider', 's3')
        self.bucket_name = self.service_config.get('bucket_name', 'soulcorelegacy-storage')
        self.table_name = self.service_config.get('table_name', 'soulcorelegacy-data')
        
        # Local storage path for offline mode
        self.local_storage_path = Path(os.path.expanduser('~/.soulcorelegacy/storage'))
        self.local_storage_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize the appropriate client based on the provider
        self._init_client()
    
    def _init_client(self):
        """Initialize the storage client."""
        if not self.enabled:
            print("Storage service is disabled. Using local storage.")
            self.s3_client = None
            self.dynamodb_client = None
            return
        
        if self.provider == 's3':
            try:
                import boto3
                self.s3_client = boto3.client('s3', region_name=self.config.get('region'))
                self.dynamodb_client = boto3.client('dynamodb', region_name=self.config.get('region'))
                print("Initialized S3 and DynamoDB storage clients.")
            except ImportError:
                print("Warning: boto3 is not installed. Cloud storage will not be available.")
                self.s3_client = None
                self.dynamodb_client = None
            except Exception as e:
                print(f"Error initializing storage clients: {e}")
                self.s3_client = None
                self.dynamodb_client = None
        else:
            print(f"Warning: Unsupported storage provider: {self.provider}")
            self.s3_client = None
            self.dynamodb_client = None
    
    def save_game_state(self, game_id, user_id, state_data):
        """
        Save a game state.
        
        Args:
            game_id (str): The ID of the game
            user_id (str): The ID of the user
            state_data (dict): The game state data
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Create a unique key for the game state
        key = f"states/{game_id}/{user_id}/latest.json"
        
        # Convert the state data to JSON
        try:
            state_json = json.dumps(state_data)
        except Exception as e:
            print(f"Error serializing game state: {e}")
            return False
        
        # Save to cloud storage if available
        if self.enabled and self.s3_client:
            try:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=state_json,
                    ContentType='application/json'
                )
                print(f"Game state saved to cloud storage: {key}")
                return True
            except Exception as e:
                print(f"Error saving game state to cloud storage: {e}")
                # Fall back to local storage
        
        # Save to local storage
        try:
            local_path = self.local_storage_path / game_id / user_id
            local_path.mkdir(parents=True, exist_ok=True)
            
            with open(local_path / 'latest.json', 'w') as f:
                f.write(state_json)
            
            print(f"Game state saved to local storage: {local_path / 'latest.json'}")
            return True
        except Exception as e:
            print(f"Error saving game state to local storage: {e}")
            return False
    
    def load_game_state(self, game_id, user_id):
        """
        Load a game state.
        
        Args:
            game_id (str): The ID of the game
            user_id (str): The ID of the user
            
        Returns:
            dict: The game state data, or None if not found
        """
        # Create a unique key for the game state
        key = f"states/{game_id}/{user_id}/latest.json"
        
        # Try to load from cloud storage if available
        if self.enabled and self.s3_client:
            try:
                response = self.s3_client.get_object(
                    Bucket=self.bucket_name,
                    Key=key
                )
                state_json = response['Body'].read().decode('utf-8')
                state_data = json.loads(state_json)
                print(f"Game state loaded from cloud storage: {key}")
                return state_data
            except Exception as e:
                print(f"Error loading game state from cloud storage: {e}")
                # Fall back to local storage
        
        # Try to load from local storage
        try:
            local_path = self.local_storage_path / game_id / user_id / 'latest.json'
            
            if not local_path.exists():
                print(f"Game state not found in local storage: {local_path}")
                return None
            
            with open(local_path, 'r') as f:
                state_json = f.read()
            
            state_data = json.loads(state_json)
            print(f"Game state loaded from local storage: {local_path}")
            return state_data
        except Exception as e:
            print(f"Error loading game state from local storage: {e}")
            return None
    
    def save_high_score(self, game_id, user_id, score, metadata=None):
        """
        Save a high score.
        
        Args:
            game_id (str): The ID of the game
            user_id (str): The ID of the user
            score (int): The score
            metadata (dict): Additional metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        if metadata is None:
            metadata = {}
        
        # Save to cloud storage if available
        if self.enabled and self.dynamodb_client:
            try:
                import time
                timestamp = int(time.time())
                
                item = {
                    'GameId': {'S': game_id},
                    'UserId': {'S': user_id},
                    'Score': {'N': str(score)},
                    'Timestamp': {'N': str(timestamp)}
                }
                
                # Add metadata
                for key, value in metadata.items():
                    if isinstance(value, str):
                        item[key] = {'S': value}
                    elif isinstance(value, (int, float)):
                        item[key] = {'N': str(value)}
                    elif isinstance(value, bool):
                        item[key] = {'BOOL': value}
                
                self.dynamodb_client.put_item(
                    TableName=self.table_name,
                    Item=item
                )
                
                print(f"High score saved to cloud storage: {game_id}/{user_id}/{score}")
                return True
            except Exception as e:
                print(f"Error saving high score to cloud storage: {e}")
                # Fall back to local storage
        
        # Save to local storage
        try:
            local_path = self.local_storage_path / 'scores'
            local_path.mkdir(parents=True, exist_ok=True)
            
            scores_file = local_path / f"{game_id}_scores.json"
            
            # Load existing scores
            scores = []
            if scores_file.exists():
                with open(scores_file, 'r') as f:
                    scores = json.load(f)
            
            # Add the new score
            import time
            timestamp = int(time.time())
            
            scores.append({
                'user_id': user_id,
                'score': score,
                'timestamp': timestamp,
                **metadata
            })
            
            # Sort scores by score (descending)
            scores.sort(key=lambda x: x['score'], reverse=True)
            
            # Save scores
            with open(scores_file, 'w') as f:
                json.dump(scores, f)
            
            print(f"High score saved to local storage: {scores_file}")
            return True
        except Exception as e:
            print(f"Error saving high score to local storage: {e}")
            return False
    
    def get_high_scores(self, game_id, limit=10):
        """
        Get high scores for a game.
        
        Args:
            game_id (str): The ID of the game
            limit (int): The maximum number of scores to return
            
        Returns:
            list: The high scores
        """
        # Try to get from cloud storage if available
        if self.enabled and self.dynamodb_client:
            try:
                response = self.dynamodb_client.query(
                    TableName=self.table_name,
                    KeyConditionExpression='GameId = :game_id',
                    ExpressionAttributeValues={
                        ':game_id': {'S': game_id}
                    },
                    Limit=limit,
                    ScanIndexForward=False  # Sort by score (descending)
                )
                
                scores = []
                for item in response.get('Items', []):
                    score_data = {
                        'user_id': item['UserId']['S'],
                        'score': int(item['Score']['N']),
                        'timestamp': int(item['Timestamp']['N'])
                    }
                    
                    # Add metadata
                    for key, value in item.items():
                        if key not in ['GameId', 'UserId', 'Score', 'Timestamp']:
                            if 'S' in value:
                                score_data[key] = value['S']
                            elif 'N' in value:
                                score_data[key] = float(value['N'])
                            elif 'BOOL' in value:
                                score_data[key] = value['BOOL']
                    
                    scores.append(score_data)
                
                print(f"High scores loaded from cloud storage: {game_id}")
                return scores
            except Exception as e:
                print(f"Error loading high scores from cloud storage: {e}")
                # Fall back to local storage
        
        # Try to get from local storage
        try:
            local_path = self.local_storage_path / 'scores' / f"{game_id}_scores.json"
            
            if not local_path.exists():
                print(f"High scores not found in local storage: {local_path}")
                return []
            
            with open(local_path, 'r') as f:
                scores = json.load(f)
            
            # Sort scores by score (descending)
            scores.sort(key=lambda x: x['score'], reverse=True)
            
            # Limit the number of scores
            scores = scores[:limit]
            
            print(f"High scores loaded from local storage: {local_path}")
            return scores
        except Exception as e:
            print(f"Error loading high scores from local storage: {e}")
            return []
