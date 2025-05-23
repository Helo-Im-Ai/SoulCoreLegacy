"""
SoulCoreLegacy Arcade - Authentication Service
--------------------------------------------
This module provides authentication services for the SoulCoreLegacy Arcade.
"""

class AuthService:
    """Authentication service for cloud integration."""
    
    def __init__(self, config):
        """
        Initialize the authentication service.
        
        Args:
            config (CloudConfig): The cloud configuration
        """
        self.config = config
        self.service_config = config.get_service_config('auth')
        self.enabled = self.service_config.get('enabled', False)
        self.provider = self.service_config.get('provider', 'cognito')
        self.user_pool_id = self.service_config.get('user_pool_id', '')
        self.client_id = self.service_config.get('client_id', '')
        
        # Current user information
        self.current_user = None
        self.id_token = None
        self.access_token = None
        self.refresh_token = None
        
        # Initialize the appropriate client based on the provider
        self._init_client()
    
    def _init_client(self):
        """Initialize the authentication client."""
        if not self.enabled:
            print("Authentication service is disabled.")
            return
        
        if self.provider == 'cognito':
            try:
                import boto3
                self.client = boto3.client('cognito-idp', region_name=self.config.get('region'))
                print("Initialized Cognito authentication client.")
            except ImportError:
                print("Warning: boto3 is not installed. Cognito authentication will not be available.")
                self.client = None
            except Exception as e:
                print(f"Error initializing Cognito client: {e}")
                self.client = None
        else:
            print(f"Warning: Unsupported authentication provider: {self.provider}")
            self.client = None
    
    def sign_up(self, username, password, email):
        """
        Sign up a new user.
        
        Args:
            username (str): The username
            password (str): The password
            email (str): The email address
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            print("Authentication service is not available.")
            return False
        
        try:
            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=username,
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    }
                ]
            )
            print(f"User {username} signed up successfully.")
            return True
        except Exception as e:
            print(f"Error signing up user: {e}")
            return False
    
    def confirm_sign_up(self, username, confirmation_code):
        """
        Confirm a user sign up.
        
        Args:
            username (str): The username
            confirmation_code (str): The confirmation code
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            print("Authentication service is not available.")
            return False
        
        try:
            self.client.confirm_sign_up(
                ClientId=self.client_id,
                Username=username,
                ConfirmationCode=confirmation_code
            )
            print(f"User {username} confirmed successfully.")
            return True
        except Exception as e:
            print(f"Error confirming user: {e}")
            return False
    
    def sign_in(self, username, password):
        """
        Sign in a user.
        
        Args:
            username (str): The username
            password (str): The password
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            print("Authentication service is not available.")
            return False
        
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            
            # Store the tokens
            auth_result = response.get('AuthenticationResult', {})
            self.id_token = auth_result.get('IdToken')
            self.access_token = auth_result.get('AccessToken')
            self.refresh_token = auth_result.get('RefreshToken')
            
            # Get user information
            self.current_user = {
                'username': username,
                'sub': self._get_claim_from_token(self.id_token, 'sub'),
                'email': self._get_claim_from_token(self.id_token, 'email')
            }
            
            print(f"User {username} signed in successfully.")
            return True
        except Exception as e:
            print(f"Error signing in: {e}")
            return False
    
    def sign_out(self):
        """
        Sign out the current user.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.enabled or not self.client or not self.current_user:
            print("No user is signed in.")
            return False
        
        try:
            if self.access_token:
                self.client.global_sign_out(
                    AccessToken=self.access_token
                )
            
            # Clear user information
            self.current_user = None
            self.id_token = None
            self.access_token = None
            self.refresh_token = None
            
            print("User signed out successfully.")
            return True
        except Exception as e:
            print(f"Error signing out: {e}")
            return False
    
    def get_current_user(self):
        """
        Get the current user.
        
        Returns:
            dict: The current user information, or None if no user is signed in
        """
        return self.current_user
    
    def is_authenticated(self):
        """
        Check if a user is authenticated.
        
        Returns:
            bool: True if a user is authenticated, False otherwise
        """
        return self.current_user is not None and self.access_token is not None
    
    def _get_claim_from_token(self, token, claim_name):
        """
        Get a claim from a JWT token.
        
        Args:
            token (str): The JWT token
            claim_name (str): The name of the claim
            
        Returns:
            The claim value, or None if the claim is not found
        """
        if not token:
            return None
        
        try:
            import jwt
            decoded = jwt.decode(token, options={"verify_signature": False})
            return decoded.get(claim_name)
        except ImportError:
            print("Warning: PyJWT is not installed. Token decoding is not available.")
            return None
        except Exception as e:
            print(f"Error decoding token: {e}")
            return None
