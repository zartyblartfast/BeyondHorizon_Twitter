# BeyondHorizon Twitter Project Architecture

## Overview

BeyondHorizon Twitter is a companion project to [beyondhorizoncalc.com](https://beyondhorizoncalc.com), designed to automatically showcase remarkable long line of sight views on Earth through Twitter/X posts. This project is part of a larger ecosystem that includes:

1. **BeyondHorizonCalc Website**: The main platform that calculates and visualizes long line of sight views, considering Earth's curvature effects.
2. **BeyondHorizonCalc-Function**: An Azure Functions project providing API access to the curvature calculations.
3. **BeyondHorizon Twitter**: This project, which automatically posts preset views to Twitter/X.

## System Architecture

### Data Flow

1. **Preset Data Source**
   - Preset views are stored in JSON format in the BeyondHorizonCalc repository
   - Accessed via GitHub URL: `raw.githubusercontent.com/.../presets.json`
   - New presets added to the website automatically become available for tweeting

2. **Core Components**
   - LocationManager: Fetches and manages preset location data from GitHub
   - PresetManager: Handles preset rotation and tweet history
   - TweetDB: SQLite database for tracking tweet history
   - TwitterClient: Manages Twitter API interactions

### Key Features

1. **Preset Management**
   - Automatic fetching of preset data from GitHub
   - Smart rotation through presets to avoid repetition
   - Support for random preset selection

2. **Tweet Generation**
   - Automatic formatting of tweet content with location details
   - Image URL handling for diagrams and visualizations
   - Preview capability for testing

3. **History Tracking**
   - SQLite database for recording tweet history
   - Tracks successful and failed tweet attempts
   - Prevents duplicate posts

## Dependencies and Hosting

### Core Dependencies
1. **Tweepy (≥4.14.0)**
   - Python library for Twitter/X API integration
   - Handles authentication and tweet posting
   - Supports media uploads and rate limiting

2. **Python-dotenv (≥1.0.0)**
   - Environment variable management
   - Secure credential handling

3. **Requests (≥2.31.0)**
   - HTTP client for fetching preset data
   - Used by LocationManager for GitHub integration

4. **Schedule (≥1.2.0)**
   - Task scheduling library
   - Manages tweet timing

### Hosting and Deployment
1. **PythonAnywhere**
   - Hosts the production instance
   - Provides scheduled task execution
   - Handles environment configuration
   - Offers reliable uptime monitoring

### External Services
1. **GitHub**
   - Hosts preset data in JSON format
   - Provides raw file access for LocationManager
   - Enables easy preset updates

2. **Twitter/X Platform**
   - API v2 for tweet posting
   - Media handling capabilities
   - Rate limiting considerations (3-minute minimum between tweets)

## Component Details

### LocationManager
- Fetches preset data from GitHub repository
- Caches data with automatic refresh (every 6 hours)
- Provides random location selection
- Formats location data for tweeting

### PresetManager
- Manages the rotation through preset locations
- Tracks tweet history in SQLite database
- Ensures even distribution of tweets across all presets

### Tweet Generation
- Creates engaging tweet content with:
  - Location names and heights
  - Distance between points
  - Refraction factor used
  - Link to website
  - Relevant diagrams/images

## Usage Patterns

1. **Regular Tweet Posting**
   ```bash
   python src/tweet_manager.py
   ```
   - Selects next preset in sequence
   - Generates and posts tweet
   - Records in history

2. **Testing and Preview**
   ```bash
   python src/tweet_manager.py --dry-run
   ```
   - Shows tweet content without posting
   - Useful for content verification

3. **Preset Management**
   ```bash
   python src/tweet_manager.py --list-presets
   python src/tweet_manager.py --show-history
   ```
   - Tools for monitoring and management

## Documentation

For detailed project information, please refer to:
- [Quickstart Guide](quickstart.md)
- [Preset Manager Documentation](preset_manager.md)
- [Azure Function Setup](azure_function_setup.md)

## Configuration

1. **Environment Variables**
   - Twitter API credentials
   - Environment selection (development/production)
   - Debug settings

2. **Database**
   - Separate databases for development and production
   - Automatic creation and initialization

## Future Considerations

1. **Potential Enhancements**
   - Advanced scheduling capabilities
   - Additional social media platform integration
   - Enhanced analytics and reporting

2. **Maintenance**
   - Regular monitoring of Twitter API changes
   - Database maintenance and optimization
   - Preset data updates

## Integration Points

1. **BeyondHorizonCalc Website**
   - Preset data synchronization
   - Image asset access
   - Website links in tweets

2. **Twitter/X Platform**
   - API authentication
   - Tweet posting
   - Media handling
