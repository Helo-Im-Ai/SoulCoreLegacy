# SoulCoreLegacy Cloud Integration

This module provides cloud integration for the SoulCoreLegacy Arcade, leveraging AWS Cloud Game Development Toolkit.

## Overview

The cloud integration module provides the following services:

- **Authentication**: User management and authentication
- **Storage**: Cloud storage for game states and high scores
- **Multiplayer**: Real-time multiplayer functionality
- **Analytics**: Game analytics and event tracking

## Architecture

The cloud integration is designed to work both online (with AWS services) and offline (with local fallbacks):

```
SoulCoreLegacy
└── cloud/
    ├── __init__.py       # Main entry point
    ├── config.py         # Configuration management
    ├── auth.py           # Authentication service (AWS Cognito)
    ├── storage.py        # Storage service (S3/DynamoDB)
    ├── multiplayer.py    # Multiplayer service (GameLift)
    └── analytics.py      # Analytics service (Kinesis)
```

## Usage

### Initialization

```python
from cloud import initialize_cloud_services

# Initialize all cloud services
services = initialize_cloud_services()

# Access individual services
auth_service = services['auth']
storage_service = services['storage']
multiplayer_service = services['multiplayer']
analytics_service = services['analytics']
```

### Authentication

```python
# Sign up a new user
auth_service.sign_up('username', 'password', 'email@example.com')

# Confirm sign up
auth_service.confirm_sign_up('username', 'confirmation_code')

# Sign in
auth_service.sign_in('username', 'password')

# Check if authenticated
if auth_service.is_authenticated():
    user = auth_service.get_current_user()
    print(f"Signed in as {user['username']}")

# Sign out
auth_service.sign_out()
```

### Storage

```python
# Save game state
storage_service.save_game_state('pong', 'user123', {
    'score': 10,
    'level': 2,
    'position': [100, 200]
})

# Load game state
state = storage_service.load_game_state('pong', 'user123')

# Save high score
storage_service.save_high_score('pong', 'user123', 100, {
    'difficulty': 'hard',
    'time_played': 120
})

# Get high scores
scores = storage_service.get_high_scores('pong', limit=10)
```

### Multiplayer

```python
# Create a multiplayer session
session_id = multiplayer_service.create_session('pong', max_players=2)

# Join a session
player_id = multiplayer_service.join_session(session_id, 'Player 1')

# Send game state
multiplayer_service.send_game_state({
    'paddle_position': 150,
    'ball_position': [200, 300],
    'score': 5
})

# Receive game state
state = multiplayer_service.receive_game_state()

# Leave session
multiplayer_service.leave_session()
```

### Analytics

```python
# Set user ID
analytics_service.set_user_id('user123')

# Track game start
analytics_service.track_game_start('pong', game_mode='single_player')

# Track game end
analytics_service.track_game_end('pong', score=100, duration=120, outcome='win')

# Track achievement
analytics_service.track_achievement('pong', 'first_win')

# Track custom event
analytics_service.track_event('button_click', {
    'button_id': 'start_game',
    'screen': 'main_menu'
})

# Flush events immediately
analytics_service.flush_events()
```

## Configuration

The cloud integration can be configured using environment variables or a configuration file:

### Environment Variables

```
# Region
AWS_REGION=us-west-2
SOULCORE_ENV=development

# Authentication
SOULCORE_AUTH_ENABLED=true
SOULCORE_AUTH_PROVIDER=cognito
SOULCORE_AUTH_USER_POOL_ID=us-west-2_abcdef123
SOULCORE_AUTH_CLIENT_ID=1234567890abcdef

# Storage
SOULCORE_STORAGE_ENABLED=true
SOULCORE_STORAGE_PROVIDER=s3
SOULCORE_STORAGE_BUCKET=soulcorelegacy-storage
SOULCORE_STORAGE_TABLE=soulcorelegacy-data

# Multiplayer
SOULCORE_MULTIPLAYER_ENABLED=true
SOULCORE_MULTIPLAYER_PROVIDER=gamelift
SOULCORE_MULTIPLAYER_FLEET_ID=fleet-1234567890

# Analytics
SOULCORE_ANALYTICS_ENABLED=true
SOULCORE_ANALYTICS_PROVIDER=kinesis
SOULCORE_ANALYTICS_STREAM=soulcorelegacy-analytics
```

### Configuration File

```json
{
  "region": "us-west-2",
  "environment": "development",
  "services": {
    "auth": {
      "enabled": true,
      "provider": "cognito",
      "user_pool_id": "us-west-2_abcdef123",
      "client_id": "1234567890abcdef"
    },
    "storage": {
      "enabled": true,
      "provider": "s3",
      "bucket_name": "soulcorelegacy-storage",
      "table_name": "soulcorelegacy-data"
    },
    "multiplayer": {
      "enabled": true,
      "provider": "gamelift",
      "fleet_id": "fleet-1234567890",
      "max_players": 4
    },
    "analytics": {
      "enabled": true,
      "provider": "kinesis",
      "stream_name": "soulcorelegacy-analytics"
    }
  }
}
```

## Dependencies

- `boto3`: AWS SDK for Python
- `pyjwt`: JWT token handling
- `pyyaml`: YAML configuration parsing

## Offline Mode

All services have offline fallbacks that work without an internet connection:

- **Authentication**: Simulated authentication with local user storage
- **Storage**: Local file-based storage for game states and high scores
- **Multiplayer**: Local socket-based server for multiplayer functionality
- **Analytics**: Local file-based storage for analytics events

This ensures that the game remains fully functional even without cloud connectivity.
