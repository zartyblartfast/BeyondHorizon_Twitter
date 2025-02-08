# Current Implementation Status

## Prerequisites and Services
1. **Twitter Developer Account**
   - Developer account with Elevated access
   - API Key and Secret
   - Access Token and Secret
   - OAuth 1.0a authentication enabled
   - Tweepy library (>= 4.14.0) for API interaction

2. **Azure Functions API**
   - Local development environment or production endpoint
   - Anonymous authentication (development)
   - API key authentication (production)
   - Exact match with local calculations
   - Automatic fallback to local calculator

3. **PythonAnywhere Account** (for deployment)
   - Free or paid account for hosting
   - Whitelist Twitter API domain
   - Set up virtual environment

4. **GitHub Access**
   - Access to BeyondHorizonCalc repository
   - Presets data from main branch

5. **Local Development**
   - Python 3.8 or higher
   - Git installed
   - Virtual environment capability
   - Required Python packages:
     * tweepy>=4.14.0 (Twitter API)
     * python-dotenv>=1.0.0 (environment variables)
     * requests>=2.31.0 (HTTP requests)
     * azure-functions>=1.14.0 (API integration)

## Components
1. **Location Manager** (`src/location_manager.py`)
   - Fetches presets from `beyondHorizonCalc/main/assets/info/presets.json`
   - Formats refraction levels (None to Extremely High)
   - Generates tweet content

2. **Curvature Calculator** (`src/curvature_calculator.py`)
   - Implements spherical geometry calculations
   - Matches API implementation exactly
   - Supports both local and API-based calculations
   - Automatic fallback from API to local

3. **Twitter Client** (`src/twitter_client.py`)
   - Handles Twitter API authentication
   - Posts tweets

4. **Test Scripts**
   - `src/test_tweet.py`: Tests tweet generation and posting
   - `tests/test_api_integration.py`: Validates API integration

## Configuration
- Environment variables in `config/.env`:
  ```
  # Twitter Configuration
  TWITTER_API_KEY=your_api_key
  TWITTER_API_SECRET=your_api_secret
  TWITTER_ACCESS_TOKEN=your_access_token
  TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret

  # API Configuration
  AZURE_FUNCTION_URL=http://localhost:7071
  AZURE_FUNCTION_KEY=your_function_key  # Optional for local development
  ```

## Current Tweet Format
```
From [Observer] ([Height]m) in [Country] to [Target] ([Height]m) in [Country]
Distance: [Distance]km
Refraction: [Level]([Value])
Hidden Height: [h2]km
Dip Angle: [dip_angle]°
Try your own calculations at https://beyondhorizoncalc.com
#LongLineOfSight #BeyondHorizon
```

## Running Tests
1. Ensure virtual environment is activated:
   ```bash
   # Create virtual environment (if not already created)
   python -m venv venv
   
   # Activate virtual environment (choose one):
   .\venv\Scripts\activate     # Windows PowerShell
   .\venv\Scripts\activate.bat # Windows CMD
   source venv/bin/activate    # Linux/Mac
   ```

2. Run tests:
   ```bash
   # Run API integration tests
   python -m pytest tests/test_api_integration.py -v -s

   # Test tweet generation
   python src/test_tweet.py --dry-run
   
   # Post actual tweet
   python src/test_tweet.py
   ```

## Dependencies
- tweepy>=4.14.0
- python-dotenv>=1.0.0
- requests>=2.31.0
- azure-functions>=1.14.0

## Current Service Dependencies
1. **Azure Functions API** 
   - Integration complete
   - Local and API calculations match
   - Automatic fallback implemented
   - Error handling in place

2. **Image Integration** (Next Phase)
   - Directory structure planned
   - JSON structure defined
   - Implementation pending

## Next Steps
1. Image Integration
   - Create image directory structure
   - Convert images to JPG format
   - Update presets.json with image URLs
   - Implement image posting in tweets

2. Testing Enhancements
   - Add edge case tests
   - Test image posting functionality
   - Improve error handling coverage

3. Documentation Updates
   - Add image handling documentation
   - Update deployment guides
   - Create contributor guidelines
