"""
SoulCoreLegacy Arcade - Multiplayer Service
-----------------------------------------
This module provides multiplayer services for the SoulCoreLegacy Arcade.
"""

import socket
import threading
import json
import time
import uuid
from queue import Queue

class MultiplayerService:
    """Multiplayer service for cloud integration."""
    
    def __init__(self, config):
        """
        Initialize the multiplayer service.
        
        Args:
            config (CloudConfig): The cloud configuration
        """
        self.config = config
        self.service_config = config.get_service_config('multiplayer')
        self.enabled = self.service_config.get('enabled', False)
        self.provider = self.service_config.get('provider', 'gamelift')
        self.fleet_id = self.service_config.get('fleet_id', '')
        self.max_players = self.service_config.get('max_players', 4)
        
        # Local server for offline mode
        self.local_server = None
        self.local_server_thread = None
        self.local_server_running = False
        self.local_server_port = 12345
        
        # Client connection
        self.client_socket = None
        self.client_thread = None
        self.client_running = False
        self.message_queue = Queue()
        self.session_id = None
        self.player_id = None
        
        # Game state
        self.game_state = {}
        self.players = {}
        
        # Initialize the appropriate client based on the provider
        self._init_client()
    
    def _init_client(self):
        """Initialize the multiplayer client."""
        if not self.enabled:
            print("Multiplayer service is disabled.")
            return
        
        if self.provider == 'gamelift':
            try:
                import boto3
                self.client = boto3.client('gamelift', region_name=self.config.get('region'))
                print("Initialized GameLift multiplayer client.")
            except ImportError:
                print("Warning: boto3 is not installed. GameLift multiplayer will not be available.")
                self.client = None
            except Exception as e:
                print(f"Error initializing GameLift client: {e}")
                self.client = None
        else:
            print(f"Warning: Unsupported multiplayer provider: {self.provider}")
            self.client = None
    
    def create_session(self, game_id, max_players=None):
        """
        Create a multiplayer session.
        
        Args:
            game_id (str): The ID of the game
            max_players (int): The maximum number of players
            
        Returns:
            str: The session ID, or None if failed
        """
        if max_players is None:
            max_players = self.max_players
        
        # Try to create a cloud session if available
        if self.enabled and self.client and self.fleet_id:
            try:
                response = self.client.create_game_session(
                    FleetId=self.fleet_id,
                    MaximumPlayerSessionCount=max_players,
                    Name=f"{game_id}-{uuid.uuid4()}",
                    GameProperties=[
                        {
                            'Key': 'game_id',
                            'Value': game_id
                        }
                    ]
                )
                
                session = response.get('GameSession', {})
                session_id = session.get('GameSessionId')
                
                if session_id:
                    print(f"Created cloud multiplayer session: {session_id}")
                    self.session_id = session_id
                    return session_id
                else:
                    print("Failed to create cloud multiplayer session.")
                    # Fall back to local server
            except Exception as e:
                print(f"Error creating cloud multiplayer session: {e}")
                # Fall back to local server
        
        # Start a local server
        try:
            self.start_local_server(game_id, max_players)
            session_id = f"local-{uuid.uuid4()}"
            self.session_id = session_id
            print(f"Created local multiplayer session: {session_id}")
            return session_id
        except Exception as e:
            print(f"Error creating local multiplayer session: {e}")
            return None
    
    def join_session(self, session_id, player_name):
        """
        Join a multiplayer session.
        
        Args:
            session_id (str): The session ID
            player_name (str): The player name
            
        Returns:
            str: The player ID, or None if failed
        """
        # Try to join a cloud session if available
        if self.enabled and self.client and session_id.startswith('arn:'):
            try:
                response = self.client.create_player_session(
                    GameSessionId=session_id,
                    PlayerId=str(uuid.uuid4()),
                    PlayerData=json.dumps({'name': player_name})
                )
                
                player_session = response.get('PlayerSession', {})
                player_id = player_session.get('PlayerId')
                
                if player_id:
                    print(f"Joined cloud multiplayer session: {session_id}")
                    self.session_id = session_id
                    self.player_id = player_id
                    return player_id
                else:
                    print("Failed to join cloud multiplayer session.")
                    # Fall back to local client
            except Exception as e:
                print(f"Error joining cloud multiplayer session: {e}")
                # Fall back to local client
        
        # Connect to a local server
        try:
            self.connect_to_local_server(player_name)
            player_id = str(uuid.uuid4())
            self.player_id = player_id
            print(f"Joined local multiplayer session: {session_id}")
            return player_id
        except Exception as e:
            print(f"Error joining local multiplayer session: {e}")
            return None
    
    def leave_session(self):
        """
        Leave the current multiplayer session.
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Try to leave a cloud session if available
        if self.enabled and self.client and self.session_id and self.player_id:
            try:
                # There's no explicit "leave session" API in GameLift,
                # but we can update the player data to indicate they've left
                print(f"Left cloud multiplayer session: {self.session_id}")
                self.session_id = None
                self.player_id = None
                return True
            except Exception as e:
                print(f"Error leaving cloud multiplayer session: {e}")
                # Fall back to disconnecting from local server
        
        # Disconnect from the local server
        try:
            self.disconnect_from_local_server()
            self.session_id = None
            self.player_id = None
            print("Left local multiplayer session.")
            return True
        except Exception as e:
            print(f"Error leaving local multiplayer session: {e}")
            return False
    
    def send_game_state(self, state_data):
        """
        Send game state to other players.
        
        Args:
            state_data (dict): The game state data
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.session_id or not self.player_id:
            print("Not connected to a multiplayer session.")
            return False
        
        # Add player ID to the state data
        state_data['player_id'] = self.player_id
        
        # Try to send to cloud session if available
        if self.enabled and self.client and self.session_id.startswith('arn:'):
            try:
                # There's no direct way to send game state in GameLift,
                # but we can use the real-time servers or a custom solution
                print("Cloud game state synchronization not implemented yet.")
                return False
            except Exception as e:
                print(f"Error sending game state to cloud session: {e}")
                # Fall back to local server
        
        # Send to local server
        try:
            if self.client_socket:
                message = {
                    'type': 'game_state',
                    'data': state_data
                }
                self.client_socket.sendall(json.dumps(message).encode('utf-8'))
                print("Game state sent to local server.")
                return True
            else:
                print("Not connected to local server.")
                return False
        except Exception as e:
            print(f"Error sending game state to local server: {e}")
            return False
    
    def receive_game_state(self):
        """
        Receive game state from other players.
        
        Returns:
            dict: The game state data, or None if no new state
        """
        if not self.message_queue.empty():
            message = self.message_queue.get()
            if message.get('type') == 'game_state':
                return message.get('data')
        
        return None
    
    def start_local_server(self, game_id, max_players):
        """
        Start a local multiplayer server.
        
        Args:
            game_id (str): The ID of the game
            max_players (int): The maximum number of players
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.local_server_running:
            print("Local server is already running.")
            return True
        
        try:
            self.local_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.local_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.local_server.bind(('localhost', self.local_server_port))
            self.local_server.listen(max_players)
            
            self.local_server_running = True
            self.local_server_thread = threading.Thread(target=self._local_server_loop)
            self.local_server_thread.daemon = True
            self.local_server_thread.start()
            
            print(f"Local server started on port {self.local_server_port}")
            return True
        except Exception as e:
            print(f"Error starting local server: {e}")
            return False
    
    def stop_local_server(self):
        """
        Stop the local multiplayer server.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.local_server_running:
            print("Local server is not running.")
            return True
        
        try:
            self.local_server_running = False
            if self.local_server:
                self.local_server.close()
            
            if self.local_server_thread:
                self.local_server_thread.join(timeout=1.0)
            
            print("Local server stopped.")
            return True
        except Exception as e:
            print(f"Error stopping local server: {e}")
            return False
    
    def connect_to_local_server(self, player_name):
        """
        Connect to a local multiplayer server.
        
        Args:
            player_name (str): The player name
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.client_running:
            print("Already connected to a server.")
            return True
        
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', self.local_server_port))
            
            # Send player information
            message = {
                'type': 'join',
                'data': {
                    'name': player_name,
                    'id': str(uuid.uuid4())
                }
            }
            self.client_socket.sendall(json.dumps(message).encode('utf-8'))
            
            self.client_running = True
            self.client_thread = threading.Thread(target=self._client_loop)
            self.client_thread.daemon = True
            self.client_thread.start()
            
            print("Connected to local server.")
            return True
        except Exception as e:
            print(f"Error connecting to local server: {e}")
            return False
    
    def disconnect_from_local_server(self):
        """
        Disconnect from the local multiplayer server.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client_running:
            print("Not connected to a server.")
            return True
        
        try:
            self.client_running = False
            if self.client_socket:
                self.client_socket.close()
            
            if self.client_thread:
                self.client_thread.join(timeout=1.0)
            
            print("Disconnected from local server.")
            return True
        except Exception as e:
            print(f"Error disconnecting from local server: {e}")
            return False
    
    def _local_server_loop(self):
        """Local server main loop."""
        clients = []
        
        while self.local_server_running:
            try:
                # Accept new connections
                self.local_server.settimeout(1.0)
                try:
                    client_socket, client_address = self.local_server.accept()
                    clients.append(client_socket)
                    print(f"Client connected: {client_address}")
                except socket.timeout:
                    pass
                
                # Process client messages
                for client in clients[:]:
                    try:
                        client.settimeout(0.0)
                        data = client.recv(4096)
                        if data:
                            # Broadcast the message to all other clients
                            message = data.decode('utf-8')
                            for other_client in clients:
                                if other_client != client:
                                    other_client.sendall(data)
                        else:
                            # Client disconnected
                            clients.remove(client)
                            client.close()
                            print("Client disconnected.")
                    except socket.timeout:
                        pass
                    except ConnectionResetError:
                        # Client disconnected
                        clients.remove(client)
                        client.close()
                        print("Client disconnected.")
                    except Exception as e:
                        print(f"Error processing client message: {e}")
            except Exception as e:
                print(f"Error in local server loop: {e}")
            
            time.sleep(0.01)
        
        # Close all client connections
        for client in clients:
            try:
                client.close()
            except:
                pass
    
    def _client_loop(self):
        """Client main loop."""
        buffer = b''
        
        while self.client_running:
            try:
                # Receive data
                self.client_socket.settimeout(1.0)
                try:
                    data = self.client_socket.recv(4096)
                    if data:
                        buffer += data
                        
                        # Process complete messages
                        while b'\n' in buffer:
                            message, buffer = buffer.split(b'\n', 1)
                            try:
                                message_data = json.loads(message.decode('utf-8'))
                                self.message_queue.put(message_data)
                            except json.JSONDecodeError:
                                print("Received invalid JSON message.")
                    else:
                        # Server disconnected
                        print("Disconnected from server.")
                        self.client_running = False
                        break
                except socket.timeout:
                    pass
            except Exception as e:
                print(f"Error in client loop: {e}")
                self.client_running = False
                break
            
            time.sleep(0.01)
