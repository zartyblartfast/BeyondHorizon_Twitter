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

4. **Test Tweet Generation (Dry Run)**
   ```bash
   # Show tweet preview without posting (using default preset)
   python src/test_tweet.py --dry-run

   # Test with specific preset location
   python src/test_tweet.py --dry-run --preset "Mount Everest to Kanchenjunga"

   # List all available presets
   python src/test_tweet.py --list-presets

   # Test with custom refraction factor
   python src/test_tweet.py --dry-run --preset "K2 to Broad Peak" --refraction 1.15
   ```

## Project Structure

```
BeyondHorizon_Twitter/
├── config/
│   └── .env               # Environment variables (not in git)
├── docs/
│   ├── quick_setup.md    # This guide
│   └── batch_testing.md  # Detailed testing documentation
├── src/
│   ├── curvature_calculator.py    # Core calculation engine
│   ├── location_manager.py        # Location data management
│   ├── test_api_comparison.py     # API vs local comparison
│   └── test_single_location.py    # Single location API test
└── requirements.txt          # Python dependencies
```

## Recent Updates

### Calculation Engine
- Implemented core curvature calculations in `curvature_calculator.py`
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
  - Single location testing (`test_single_location.py`)
  - Batch comparison testing (`test_api_comparison.py`)
- Added CSV output for detailed comparisons
- See `docs/batch_testing.md` for detailed testing instructions

## Current Status

1. **Working Features**
   - Local curvature calculations
   - API integration
   - Batch testing framework
   - CSV comparison output

2. **Under Verification**
   - Calculation accuracy (comparing API vs local results)
   - Real-world validation needed for:
     - Hidden height calculations
     - Visible height predictions
     - Perspective scaling factors

3. **Next Steps**
   - Validate calculations against real-world observations
   - Resolve discrepancies between API and local calculations
   - Add automated regression testing
   - Implement command-line arguments for testing tools

## Troubleshooting

1. **API Connection Issues**
   - Verify Azure Function URL and key in `.env`
   - Check Azure Function status
   - Review error messages in test output

2. **Calculation Discrepancies**
   - Check test output for detailed comparisons
   - Focus on specific fields showing differences
   - Compare with real-world observations when possible

## Getting Help

- Check the documentation in the `docs/` directory
- Review test outputs for detailed error messages
- Consult the Azure Function logs for API issues
- Contact the development team for additional support
