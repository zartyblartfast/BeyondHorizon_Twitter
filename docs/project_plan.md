# Beyond Horizon Twitter AI Agent

## Project Overview
An AI-powered Twitter bot that automates the sharing of fascinating Long Line of Sight (LoS) views from around the world. This project aims to build an engaged community around remarkable viewpoints, encouraging users to discover, verify, and contribute new LoS locations using our web-based calculation tool at [website_url].

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
- Google Maps API for visualization (Phase 2)
- PythonAnywhere for hosting

### Data Sources
1. **Preset Locations**
   - Source: BeyondHorizonCalc GitHub repository
   - Data: presets.json with location pairs
   - Required calculations:
     * Distance to Horizon
     * Horizon Dip Angle
     * Hidden Height
     * Visible Height

2. **Calculation Engine**
   - Azure Functions API for dynamic calculations
   - Fallback to pre-calculated results for presets

## Development Phases

### Phase 1: Core Infrastructure and Data Management

#### Objective
Establish foundational data management and calculation system for meaningful LoS content.

#### Implementation Details
1. **Data Source Integration**
   - GitHub repository connection
   - Preset location data parsing
   - Data validation and error handling

2. **Results Integration**
   - Pre-calculate results for preset locations
   - Store extended preset data
   - Design data structure for calculations

3. **Tweet Content Structure**
   - Location information formatting
   - Calculation result presentation
   - Refraction level display

4. **Azure Functions Integration**
   - API endpoint setup
   - Authentication implementation
   - Response handling
   - Fallback mechanisms

### Phase 2: Enhanced Content and Visualization

#### Objective
Enhance tweets with professional visual content and relevant historical/scientific context.

#### Implementation Details
1. **Visual Content Integration**
   - Google Maps static image showing LoS path
   - Target location photographs
   - Image caching and management
   - Proper attribution for images

2. **Content Enhancement**
   - Historical records and achievements
   - Scientific context and calculations
   - Link to web calculator for custom experiments
   - Community contribution highlights

3. **Professional Presentation**
   - Clean, technical format
   - Relevant links and citations
   - Contributor attribution
   - Web tool integration

### Phase 3: Community Engagement and Automation

#### Objective
Build an active community while maintaining reliable automated posting.

#### Implementation Details
1. **Community Management**
   - Contribution verification system
   - Attribution tracking
   - Contributor recognition in posts
   - Community guidelines

2. **Data Structure Enhancement**
   - Update presets.json schema:
     ```json
     {
       "id": "unique_identifier",
       "contributor": {
         "name": "Display Name",
         "twitter": "@handle",
         "date_added": "YYYY-MM-DD"
       },
       "locations": {
         // existing location data
       },
       "verification": {
         "status": "verified",
         "method": "calculation/photograph/historical",
         "date": "YYYY-MM-DD"
       }
     }
     ```

3. **Engagement Strategy**
   - Call for new locations
   - Recognition of contributors
   - Regular website promotion
   - Custom calculation encouragement
   - Community success stories

4. **Scheduling System**
   - Strategic posting times
   - Content mix (presets vs. new discoveries)
   - Contributor highlight rotation
   - Seasonal considerations

### Phase 4: Analytics and Community Growth

#### Objective
Track engagement and optimize community growth.

#### Implementation Details
1. **Analytics System**
   - Community growth metrics
   - Contribution tracking
   - Engagement analysis
   - Website traffic correlation

2. **Growth Optimization**
   - Content timing optimization
   - Contribution incentives
   - Community recognition programs
   - Cross-platform promotion

## Tweet Content Structure
1. **Core Technical Data**
   - Location details and heights
   - Distance and calculations
   - Refraction conditions

2. **Engagement Elements**
   - Maps and photographs
   - Link to web calculator
   - Contributor attribution (if applicable)
   - Call for new discoveries

3. **Website Integration**
   - Custom calculation promotion
   - Preset database access
   - Contribution guidelines
   - Community recognition

## Success Criteria
1. Accurate LoS calculations
2. Growing contributor base
3. Regular new location submissions
4. Active community engagement
5. Quality of contributed locations

## Technical Requirements
1. Python 3.8+
2. Required packages:
   - tweepy>=4.14.0
   - python-dotenv>=1.0.0
   - requests>=2.31.0
   - schedule>=1.2.0
3. API Keys:
   - Twitter API (OAuth 1.0a)
   - Azure Functions
   - Google Maps (Phase 2)

## Security Considerations
1. Secure API key management
2. Rate limiting compliance
3. Error handling and logging
4. Backup systems for API failures

## Maintenance Plan
1. Regular data updates
2. Contribution verification
3. Community management
4. Attribution accuracy
