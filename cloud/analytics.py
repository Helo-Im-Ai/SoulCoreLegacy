"""
SoulCoreLegacy Arcade - Analytics Service
---------------------------------------
This module provides analytics services for the SoulCoreLegacy Arcade.
"""

import json
import time
import uuid
import os
from pathlib import Path
from queue import Queue
import threading

class AnalyticsService:
    """Analytics service for cloud integration."""
    
    def __init__(self, config):
        """
        Initialize the analytics service.
        
        Args:
            config (CloudConfig): The cloud configuration
        """
        self.config = config
        self.service_config = config.get_service_config('analytics')
        self.enabled = self.service_config.get('enabled', False)
        self.provider = self.service_config.get('provider', 'kinesis')
        self.stream_name = self.service_config.get('stream_name', 'soulcorelegacy-analytics')
        
        # Local storage path for offline mode
        self.local_storage_path = Path(os.path.expanduser('~/.soulcorelegacy/analytics'))
        self.local_storage_path.mkdir(parents=True, exist_ok=True)
        
        # Event queue for batch processing
        self.event_queue = Queue()
        self.batch_size = 10
        self.flush_interval = 60  # seconds
        self.last_flush_time = time.time()
        
        # Session information
        self.session_id = str(uuid.uuid4())
        self.user_id = None
        
        # Background thread for processing events
        self.processing_thread = None
        self.processing_running = False
        
        # Initialize the appropriate client based on the provider
        self._init_client()
        
        # Start the processing thread
        self._start_processing_thread()
    
    def _init_client(self):
        """Initialize the analytics client."""
        if not self.enabled:
            print("Analytics service is disabled. Using local storage.")
            self.client = None
            return
        
        if self.provider == 'kinesis':
            try:
                import boto3
                self.client = boto3.client('kinesis', region_name=self.config.get('region'))
                print("Initialized Kinesis analytics client.")
            except ImportError:
                print("Warning: boto3 is not installed. Cloud analytics will not be available.")
                self.client = None
            except Exception as e:
                print(f"Error initializing Kinesis client: {e}")
                self.client = None
        else:
            print(f"Warning: Unsupported analytics provider: {self.provider}")
            self.client = None
    
    def _start_processing_thread(self):
        """Start the background thread for processing events."""
        if self.processing_thread is not None:
            return
        
        self.processing_running = True
        self.processing_thread = threading.Thread(target=self._process_events)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def _stop_processing_thread(self):
        """Stop the background thread for processing events."""
        if self.processing_thread is None:
            return
        
        self.processing_running = False
        self.processing_thread.join(timeout=2.0)
        self.processing_thread = None
    
    def _process_events(self):
        """Process events in the background."""
        while self.processing_running:
            # Check if it's time to flush events
            current_time = time.time()
            if current_time - self.last_flush_time >= self.flush_interval:
                self.flush_events()
                self.last_flush_time = current_time
            
            # Sleep for a short time
            time.sleep(1.0)
    
    def set_user_id(self, user_id):
        """
        Set the user ID for analytics events.
        
        Args:
            user_id (str): The user ID
        """
        self.user_id = user_id
    
    def track_event(self, event_type, event_data=None):
        """
        Track an analytics event.
        
        Args:
            event_type (str): The type of event
            event_data (dict): Additional event data
            
        Returns:
            bool: True if the event was queued, False otherwise
        """
        if event_data is None:
            event_data = {}
        
        # Create the event
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': event_type,
            'timestamp': int(time.time()),
            'session_id': self.session_id,
            'user_id': self.user_id or 'anonymous',
            'data': event_data
        }
        
        # Add the event to the queue
        self.event_queue.put(event)
        
        # Flush events if the queue is full
        if self.event_queue.qsize() >= self.batch_size:
            self.flush_events()
        
        return True
    
    def track_game_start(self, game_id, game_mode=None):
        """
        Track a game start event.
        
        Args:
            game_id (str): The ID of the game
            game_mode (str): The game mode
            
        Returns:
            bool: True if the event was tracked, False otherwise
        """
        event_data = {
            'game_id': game_id
        }
        
        if game_mode:
            event_data['game_mode'] = game_mode
        
        return self.track_event('game_start', event_data)
    
    def track_game_end(self, game_id, score=None, duration=None, outcome=None):
        """
        Track a game end event.
        
        Args:
            game_id (str): The ID of the game
            score (int): The score
            duration (int): The duration in seconds
            outcome (str): The outcome (e.g., 'win', 'loss', 'draw')
            
        Returns:
            bool: True if the event was tracked, False otherwise
        """
        event_data = {
            'game_id': game_id
        }
        
        if score is not None:
            event_data['score'] = score
        
        if duration is not None:
            event_data['duration'] = duration
        
        if outcome:
            event_data['outcome'] = outcome
        
        return self.track_event('game_end', event_data)
    
    def track_level_start(self, game_id, level_id):
        """
        Track a level start event.
        
        Args:
            game_id (str): The ID of the game
            level_id (str): The ID of the level
            
        Returns:
            bool: True if the event was tracked, False otherwise
        """
        event_data = {
            'game_id': game_id,
            'level_id': level_id
        }
        
        return self.track_event('level_start', event_data)
    
    def track_level_end(self, game_id, level_id, score=None, duration=None, outcome=None):
        """
        Track a level end event.
        
        Args:
            game_id (str): The ID of the game
            level_id (str): The ID of the level
            score (int): The score
            duration (int): The duration in seconds
            outcome (str): The outcome (e.g., 'win', 'loss', 'draw')
            
        Returns:
            bool: True if the event was tracked, False otherwise
        """
        event_data = {
            'game_id': game_id,
            'level_id': level_id
        }
        
        if score is not None:
            event_data['score'] = score
        
        if duration is not None:
            event_data['duration'] = duration
        
        if outcome:
            event_data['outcome'] = outcome
        
        return self.track_event('level_end', event_data)
    
    def track_achievement(self, game_id, achievement_id):
        """
        Track an achievement event.
        
        Args:
            game_id (str): The ID of the game
            achievement_id (str): The ID of the achievement
            
        Returns:
            bool: True if the event was tracked, False otherwise
        """
        event_data = {
            'game_id': game_id,
            'achievement_id': achievement_id
        }
        
        return self.track_event('achievement', event_data)
    
    def track_error(self, error_type, error_message, error_data=None):
        """
        Track an error event.
        
        Args:
            error_type (str): The type of error
            error_message (str): The error message
            error_data (dict): Additional error data
            
        Returns:
            bool: True if the event was tracked, False otherwise
        """
        if error_data is None:
            error_data = {}
        
        event_data = {
            'error_type': error_type,
            'error_message': error_message,
            **error_data
        }
        
        return self.track_event('error', event_data)
    
    def flush_events(self):
        """
        Flush queued events to storage.
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Get all events from the queue
        events = []
        while not self.event_queue.empty():
            events.append(self.event_queue.get())
        
        if not events:
            return True
        
        # Send events to cloud storage if available
        if self.enabled and self.client:
            try:
                # Batch the events
                records = []
                for event in events:
                    records.append({
                        'Data': json.dumps(event).encode('utf-8'),
                        'PartitionKey': event['event_id']
                    })
                
                # Send to Kinesis
                response = self.client.put_records(
                    StreamName=self.stream_name,
                    Records=records
                )
                
                # Check for failed records
                failed_count = response.get('FailedRecordCount', 0)
                if failed_count > 0:
                    print(f"Warning: {failed_count} records failed to be sent to Kinesis.")
                    # Fall back to local storage for failed records
                    failed_records = []
                    for i, record in enumerate(response.get('Records', [])):
                        if 'ErrorCode' in record:
                            failed_records.append(events[i])
                    
                    if failed_records:
                        self._save_events_locally(failed_records)
                
                print(f"Sent {len(events) - failed_count} events to Kinesis.")
                return True
            except Exception as e:
                print(f"Error sending events to Kinesis: {e}")
                # Fall back to local storage
        
        # Save events locally
        return self._save_events_locally(events)
    
    def _save_events_locally(self, events):
        """
        Save events to local storage.
        
        Args:
            events (list): The events to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create a filename based on the current timestamp
            timestamp = int(time.time())
            filename = f"events_{timestamp}.json"
            filepath = self.local_storage_path / filename
            
            # Save the events
            with open(filepath, 'w') as f:
                json.dump(events, f)
            
            print(f"Saved {len(events)} events to local storage: {filepath}")
            return True
        except Exception as e:
            print(f"Error saving events to local storage: {e}")
            return False
