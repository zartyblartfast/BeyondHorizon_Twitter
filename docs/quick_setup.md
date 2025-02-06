# Quick Setup Guide

This guide contains everything needed to recreate the BeyondHorizon Twitter bot from scratch.

## 1. Prerequisites
1. **Twitter Developer Account**
   - Create account at developer.twitter.com
   - Apply for Elevated access
   - Create new project and app
   - Generate API keys and tokens with OAuth 1.0a

2. **Python Environment**
   - Python 3.8+
   - Virtual environment

## 2. Essential Files

### Project Structure
```
BeyondHorizon_Twitter/
├── config/
│   ├── .env                 # Twitter credentials
│   └── config.template.env  # Template for .env
├── src/
│   ├── location_manager.py  # Handles location data and tweet formatting
│   ├── twitter_client.py    # Twitter API integration
│   └── test_tweet.py       # Test script
└── requirements.txt         # Python dependencies
```

### File Contents

1. **requirements.txt**
```
tweepy>=4.14.0
python-dotenv>=1.0.0
requests>=2.31.0
```

2. **config/config.template.env**
```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

## 3. Setup Steps
1. Clone repository or create directory structure
2. Copy `config.template.env` to `.env` and add Twitter credentials
3. Create and activate virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment (choose one):
   .\venv\Scripts\activate     # Windows PowerShell
   .\venv\Scripts\activate.bat # Windows CMD
   source venv/bin/activate    # Linux/Mac
   
   # Confirm activation - you should see (venv) in your prompt
   # Example: (venv) PS C:\Users\username\BeyondHorizon_Twitter>
   ```
4. Install dependencies:
   ```bash
   # Make sure your virtual environment is activated (see step 3)
   pip install -r requirements.txt
   ```
5. Run test:
   ```bash
   # Make sure your virtual environment is activated (see step 3)
   
   # Preview tweet without posting (dry run)
   python src/test_tweet.py --dry-run

   # Post actual tweet
   python src/test_tweet.py
   ```

> **Important**: Always ensure your virtual environment is activated (you should see `(venv)` in your prompt) before running any Python commands. This isolates the project dependencies and prevents conflicts with your system Python packages.

## 4. Rate Limiting
The Twitter API has rate limits that affect how frequently you can post:
- Maximum 200 tweets per 3-hour window (about 1 tweet per minute)
- Maximum 300 media uploads per 3-hour window

The script automatically handles rate limiting by:
- Waiting 3 minutes between tweets to stay well within limits
- Showing a countdown when waiting due to rate limits
- Providing clear error messages if rate limits are hit

## 5. Key Features
- Formats tweets with location details, distance, and refraction data
- Supports up to 4 images per tweet
- Preview mode (--dry-run) to review tweet content before posting
- Automatic rate limit handling
- Error handling for network and API issues

## 6. Key Dependencies
- Access to BeyondHorizonCalc presets.json for location data
- Twitter API access for posting tweets
- Python packages (tweepy, python-dotenv, requests)

With just these components and the source code files, you can fully recreate the current functionality of posting formatted Long Line of Sight tweets.
