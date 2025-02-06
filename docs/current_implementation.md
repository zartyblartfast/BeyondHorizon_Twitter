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
   ```bash
   # Create virtual environment (if not already created)
   python -m venv venv
   
   # Activate virtual environment (choose one):
   .\venv\Scripts\activate     # Windows PowerShell
   .\venv\Scripts\activate.bat # Windows CMD
   source venv/bin/activate    # Linux/Mac
   
   # Your prompt should show (venv), example:
   # (venv) PS C:\Users\username\BeyondHorizon_Twitter>
   ```

2. Run test script:
   ```bash
   # Preview tweet without posting
   python src/test_tweet.py --dry-run
   
   # Post actual tweet (respects rate limits)
   python src/test_tweet.py
   ```

> **Note**: The virtual environment isolates project dependencies. If you see import errors or unexpected behavior, make sure:
> 1. You see `(venv)` in your prompt
> 2. You've installed dependencies: `pip install -r requirements.txt`
> 3. You're in the project root directory

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

## Next Steps

### 1. Azure Functions Integration (Priority)
- Set up Azure Functions API for calculations
- Required calculations:
  * Distance to Horizon
  * Horizon Dip Angle
  * Hidden Height
  * Visible Height
- Integration points:
  * API endpoint configuration
  * Authentication setup
  * Response handling
  * Fallback to pre-calculated results

### 2. Visual Content Enhancement
- Maps integration:
  * Static maps showing LoS path
  * Target location images
  * Image caching system
- Twitter card preview optimization
- Image attribution handling

### 3. Deployment Setup
- PythonAnywhere configuration:
  * Environment setup
  * Domain whitelisting
  * Scheduled tasks
  * Error monitoring
- Production environment variables
- Logging and monitoring

### 4. Community Features
- Location submission process:
  * Verification workflow
  * Contributor recognition
  * Attribution tracking
- Web calculator integration:
  * Cross-linking
  * Custom calculation support
  * Result sharing

### Timeline
1. Week 1-2: Azure Functions setup and integration
2. Week 3: Visual content system
3. Week 4: PythonAnywhere deployment
4. Week 5+: Community features rollout

### Dependencies Required
- Azure Functions subscription
- Google Maps API key
- PythonAnywhere paid account (for whitelist support)
- Additional Python packages (TBD based on Azure Functions requirements)
