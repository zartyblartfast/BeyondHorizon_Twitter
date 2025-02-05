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
3. Create virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run test:
   ```bash
   python src/test_tweet.py
   ```

## 4. Key Dependencies
- Access to BeyondHorizonCalc presets.json for location data
- Twitter API access for posting tweets
- Python packages (tweepy, python-dotenv, requests)

With just these components and the source code files, you can fully recreate the current functionality of posting formatted Long Line of Sight tweets.
