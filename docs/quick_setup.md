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
     # Azure Functions API Configuration
     AZURE_FUNCTION_URL=your_function_url_here
     AZURE_FUNCTION_KEY=your_function_key_here

     # Twitter API Configuration
     TWITTER_API_KEY=your_api_key_here
     TWITTER_API_SECRET=your_api_secret_here
     TWITTER_ACCESS_TOKEN=your_access_token_here
     TWITTER_ACCESS_SECRET=your_access_secret_here

     # Development Settings
     ENVIRONMENT=development  # or production
     DEBUG=true
     ```

## Testing the Setup

1. **Test Local Calculations**
   ```bash
   python src/curvature_calculator.py
   ```
   This runs basic validation tests for the local calculation engine.

2. **Test API Integration**
   ```bash
   python src/test_single_location.py
   ```
   This tests the API with a single location (Fort Niagara to Toronto).

3. **Run Batch Tests**
   ```bash
   python src/test_api_comparison.py
   ```
   This compares API and local calculations for all preset locations.

4. **Test Tweet Generation**
   ```bash
   # Show tweet preview without posting (using next preset in sequence)
   python src/test_tweet_v2.py --dry-run

   # Test with specific preset location
   python src/test_tweet_v2.py --dry-run --preset "Mount Everest to Kanchenjunga"

   # List all available presets
   python src/test_tweet_v2.py --list-presets

   # View tweet history
   python src/test_tweet_v2.py --show-history

   # Test with random preset
   python src/test_tweet_v2.py --dry-run --random

   # Record test entries to database
   python src/test_tweet_v2.py --dry-run --test-record

   # Clear test history
   python src/test_tweet_v2.py --clear-history
   ```

5. **Test Database and Managers**
   ```bash
   python src/test_managers.py
   ```
   This tests PresetManager and ReportManager functionality.

## Project Structure

```
BeyondHorizon_Twitter/
├── config/
│   └── .env                  # Environment variables (not in git)
├── data/
│   └── tweet_history_*.db    # SQLite databases for different environments
├── docs/
│   ├── quick_setup.md       # This guide
│   ├── preset_manager.md    # Preset management documentation
│   └── batch_testing.md     # Detailed testing documentation
├── src/
│   ├── curvature_calculator.py    # Core calculation engine
│   ├── location_manager.py        # Location data management
│   ├── preset_manager.py          # Preset rotation and history
│   ├── report_manager.py          # History reporting
│   ├── tweet_db.py               # Database operations
│   ├── test_tweet_v2.py          # Tweet testing and management
│   ├── test_managers.py          # Database testing
│   ├── test_api_comparison.py    # API vs local comparison
│   └── test_single_location.py   # Single location API test
└── requirements.txt              # Python dependencies
```

## Recent Updates

### Preset Management System
- Added SQLite database for tweet history tracking
- Implemented preset rotation with 30-day cooldown
- Added comprehensive testing tools
- Created reporting system for tweet history

### Calculation Engine
- Implemented core curvature calculations
- Added support for:
  - Hidden height calculation
  - Horizon distance
  - Dip angle
  - Visible height
  - Apparent height
  - Perspective scaling

### API Integration
- Added Azure Function API integration
- Implemented field mapping between API and local calculations
- Added comprehensive error handling and validation

### Testing Framework
- Created test scripts for:
  - Tweet generation and posting
  - Preset management
  - Database operations
  - Single location testing
  - Batch comparison testing
- Added CSV output for detailed comparisons

## Current Status

1. **Working Features**
   - Local curvature calculations
   - API integration
   - Tweet generation and testing
   - Preset management and rotation
   - History tracking and reporting
   - Batch testing framework

2. **Under Development**
   - Automated tweet scheduling
   - Email reporting system
   - Enhanced error handling

3. **Next Steps**
   - Implement automated scheduler
   - Add email notifications
   - Deploy to production environment

## Troubleshooting

1. **Database Issues**
   - Check environment setting in `.env`
   - Verify database file exists in `data/` directory
   - Use `--clear-history` to reset test database
   - Check file permissions

2. **API Connection Issues**
   - Verify Azure Function URL and key in `.env`
   - Check Azure Function status
   - Review error messages in test output

3. **Tweet Generation Issues**
   - Use `--dry-run` to test without posting
   - Check Twitter API credentials
   - Review history with `--show-history`

## Getting Help

- Check `docs/preset_manager.md` for detailed system documentation
- Review test outputs for detailed error messages
- Use `--list-presets` to verify available locations
- Contact the development team for additional support
