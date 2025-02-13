# Quick Setup Guide

## Initial Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/BeyondHorizon_Twitter.git
   cd BeyondHorizon_Twitter
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   
   # Windows (Command Prompt)
   .venv\Scripts\activate
   
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   
   # Unix/MacOS
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a new file `config/.env` with the following structure:
     ```
     # Twitter API Configuration
     TWITTER_API_KEY=your_api_key_here
     TWITTER_API_SECRET=your_api_secret_here
     TWITTER_ACCESS_TOKEN=your_access_token_here
     TWITTER_ACCESS_SECRET=your_access_secret_here

     # Development Settings
     ENVIRONMENT=development  # or production
     DEBUG=true

     # Scheduling Configuration
     SCHEDULED_DAYS_INTERVAL=3     # Days between tweets (1-14)
     SCHEDULED_RANDOM_MINUTES=10   # Max random wait before posting (1-15)
     ```

## Testing the Setup

1. **Test Tweet Generation**
   ```bash
   # Show tweet preview without posting
   python src/tweet_manager.py --dry-run

   # Test with specific preset location
   python src/tweet_manager.py --dry-run --preset "Mount Everest to Kanchenjunga"

   # List all available presets
   python src/tweet_manager.py --list-presets

   # View tweet history
   python src/tweet_manager.py --show-history

   # Test with random preset
   python src/tweet_manager.py --dry-run --random

   # Test scheduled tweet runner
   DRY_RUN=true python src/scheduled_tweet_runner.py
   ```

## Project Structure

```
BeyondHorizon_Twitter/
├── config/
│   └── .env                  # Environment variables (not in git)
├── data/
│   └── tweet_history_*.db    # SQLite databases for different environments
├── docs/
│   ├── quickstart.md         # This guide
│   └── preset_manager.md     # Preset management documentation
├── src/
│   ├── location_manager.py   # Location data management
│   ├── preset_manager.py     # Preset rotation and history
│   ├── scheduled_tweet_runner.py  # Automated tweet scheduling
│   ├── tweet_db.py          # Database operations
│   └── tweet_manager.py     # Tweet generation and posting
└── requirements.txt         # Python dependencies
```

## Deployment to PythonAnywhere

1. **Log into PythonAnywhere**
   - Go to your PythonAnywhere dashboard
   - Open a Bash console

2. **Clone the Repository**
   ```bash
   # Clone the repository
   git clone https://github.com/your-username/BeyondHorizon_Twitter.git
   cd BeyondHorizon_Twitter
   ```

3. **Set Up Virtual Environment**
   ```bash
   # Create and activate virtual environment
   python -m venv .venv
   source .venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   # Create and edit .env file
   mkdir -p config
   nano config/.env
   ```
   Add your configuration (same as local setup)

5. **Set Up Scheduled Task**
   - Go to PythonAnywhere Tasks tab
   - Add a new scheduled task
   - Command to run: `/home/your-username/BeyondHorizon_Twitter/.venv/bin/python /home/your-username/BeyondHorizon_Twitter/src/scheduled_tweet_runner.py`
   - Set schedule (e.g., daily at a specific time)

6. **Update Deployment**
   To update your deployment with latest changes:
   ```bash
   cd BeyondHorizon_Twitter
   git pull origin main
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

7. **Verify Setup**
   ```bash
   # Test the setup with dry run
   python src/tweet_manager.py --dry-run
   ```

Note: Make sure to whitelist api.twitter.com in PythonAnywhere (required for free accounts).

## Recent Updates

### Automated Tweet Scheduling
- Added scheduled tweet runner with configurable intervals
- Implemented random wait times for natural posting
- Added comprehensive logging system
- Support for dry run testing

### Preset Management System
- Added SQLite database for tweet history tracking
- Implemented continuous preset rotation
- Added comprehensive testing tools

### Tweet Management
- Simplified tweet preview functionality
- Improved error handling and validation
- Added support for dry runs and testing

## Current Status

1. **Working Features**
   - Automated tweet scheduling
   - Tweet generation and posting
   - Preset management and rotation
   - History tracking
   - Comprehensive testing options

2. **Scheduling Features**
   - Configurable posting intervals (1-14 days)
   - Random wait times (1-15 minutes)
   - Detailed logging
   - Dry run mode for testing
   - PythonAnywhere deployment support

## Troubleshooting

1. **Database Issues**
   - Check environment setting in `.env`
   - Verify database file exists in `data/` directory
   - Use `--clear-history` to reset test database
   - Check file permissions

2. **Tweet Generation Issues**
   - Use `--dry-run` to test without posting
   - Check Twitter API credentials
   - Review history with `--show-history`

## Getting Help

- Check `docs/preset_manager.md` for detailed system documentation
- Review test outputs for detailed error messages
- Use `--list-presets` to verify available locations
