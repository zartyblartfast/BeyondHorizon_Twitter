# Beyond Horizon Twitter AI Agent

## Project Overview
An AI-powered Twitter bot that automates the sharing of fascinating Long Line of Sight (LoS) views from around the world. This project aims to build an engaged community around remarkable viewpoints, encouraging users to discover, verify, and contribute new LoS locations using our web-based calculation tool.

## Project Goals
1. Share verified LoS views with accurate calculations
2. Build an engaged community of LoS enthusiasts
3. Encourage discovery of new LoS locations
4. Maintain a curated database of verified viewpoints
5. Recognize community contributions

## Technical Architecture

### Core Technologies
- Python-based implementation
- Twitter/X API via Tweepy for social media interaction
- Azure Functions-based LoS Calculation API
- GitHub-based image storage
- PythonAnywhere for hosting

### Data Sources
1. **Preset Locations**
   - Source: BeyondHorizonCalc GitHub repository
   - Data: presets.json with location pairs and images
   - Calculations (✓ Completed):
     * Distance to Horizon
     * Horizon Dip Angle
     * Hidden Height
     * Visible Height

2. **Calculation Engine**
   - Local implementation (✓ Complete)
   - Local Azure Functions API (✓ Testing)
   - Production Azure Functions API (Pending)
   - Automatic fallback system (✓ Complete)

3. **Image System**
   - GitHub repository storage (Partial)
   - Image URLs in presets.json
   - Attribution system defined
   - Format: JPG (Twitter-compatible)

## Current Phase: Calculation Integration

### Immediate Priorities
1. **Tweet Enhancement**
   - Add calculation results to tweets
   - Test with local calculator
   - Verify format with dry runs
   - Document final format

2. **Production API Setup**
   - Configure production endpoint
   - Implement authentication
   - Test connection
   - Verify fallback system

3. **Image Completion**
   - Complete preset image integration
   - Test with calculations
   - Verify attribution

### Implementation Plan
1. **Tweet Format Update**
   ```
   From [Observer] ([Height]m) in [Country] to [Target] ([Height]m) in [Country]
   Distance: [Distance]km
   Refraction: [Level]([Value])
   Hidden Height: [h2]km
   Dip Angle: [dip_angle]°
   [Attribution if images present]
   Try your own calculations at https://beyondhorizoncalc.com
   #LongLineOfSight #BeyondHorizon
   ```

2. **API Integration**
   - Local testing complete
   - Production setup pending
   - Fallback mechanism ready

3. **Image Support**
   - Structure defined
   - Partial implementation
   - Attribution system ready

## Technical Requirements

### Current Dependencies
- tweepy>=4.14.0 (Twitter API)
- python-dotenv>=1.0.0 (Environment)
- requests>=2.31.0 (HTTP)
- azure-functions>=1.14.0 (API)

### Environment Configuration
```bash
# Twitter API
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=

# Azure Functions API
AZURE_FUNCTION_URL=
AZURE_FUNCTION_KEY=
```

## Success Metrics
1. Calculation accuracy
2. Tweet readability
3. Image integration
4. API reliability
5. System stability

## Current Status
- Basic Tweet System ✓ Complete
- Local Calculations ✓ Complete
- Local API Testing ✓ Complete
- Production API ⏳ Pending
- Image System 🔄 Partial

## Next Steps
1. Implement calculation results in tweets
2. Set up production API connection
3. Complete image integration
4. Update documentation
