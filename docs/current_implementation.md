# Current Implementation Status

## Prerequisites and Services
1. **Twitter Developer Account**
   - Developer account with Elevated access
   - API Key and Secret
   - Access Token and Secret
   - OAuth 1.0a authentication enabled
   - Tweepy library (>= 4.14.0) for API interaction

2. **PythonAnywhere Account** (for deployment)
   - Free or paid account for hosting
   - Whitelist Twitter API domain
   - Set up virtual environment

3. **GitHub Access**
   - Access to BeyondHorizonCalc repository
   - Presets data from main branch

4. **Local Development**
   - Python 3.8 or higher
   - Git installed
   - Virtual environment capability
   - Required Python packages:
     * tweepy>=4.14.0 (Twitter API)
     * python-dotenv>=1.0.0 (environment variables)
     * requests>=2.31.0 (HTTP requests)

## Components
1. **Location Manager** (`src/location_manager.py`)
   - Fetches presets from `beyondHorizonCalc/main/assets/info/presets.json`
   - Formats refraction levels (None to Extremely High)
   - Generates tweet content

2. **Twitter Client** (`src/twitter_client.py`)
   - Handles Twitter API authentication
   - Posts tweets

3. **Test Script** (`src/test_tweet.py`)
   - Tests tweet generation and posting

## Configuration
- Environment variables in `config/.env`:
  ```
  TWITTER_API_KEY=your_api_key
  TWITTER_API_SECRET=your_api_secret
  TWITTER_ACCESS_TOKEN=your_access_token
  TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
  ```

## Current Tweet Format
```
From [Observer] ([Height]m) in [Country] to [Target] ([Height]m) in [Country]
Distance: [Distance]km
Refraction: [Level]([Value])
Try your own calculations at https://beyondhorizoncalc.com
#LongLineOfSight #BeyondHorizon
```

## Running Test Tweet
1. Ensure virtual environment is activated:
   ```
   .\venv\Scripts\activate  # Windows
   ```

2. Run test script:
   ```
   python src/test_tweet.py
   ```

## Dependencies
- tweepy>=4.14.0
- python-dotenv>=1.0.0
- requests>=2.31.0

## Planned Service Dependencies
1. **Azure Functions**
   - For calculation API (pending)
   - Authentication setup required

2. **Google Maps API**
   - For static maps (future)
   - API key will be needed
