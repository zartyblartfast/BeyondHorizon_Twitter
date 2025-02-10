# BeyondHorizonCalc Azure Function Setup

## Overview
The BeyondHorizonCalc-Function project provides API access to the core curvature calculations used by the BeyondHorizon ecosystem. This guide covers both development and production setup.

## Development Environment

### Prerequisites
- Azure Functions Core Tools (`func --version` to verify)
- Python 3.8 or higher
- Azure Storage Emulator
- Visual Studio Code with Azure Functions extension (recommended)

### Local Setup
- **Location**: `c:/Users/clive/VSC/BeyondHorizonCalc-Function`
- **Runtime**: Python Azure Functions
- **Local Endpoint**: `http://localhost:7071/api/calculate`
- **Authentication**: Anonymous (development only)

### Environment Variables
```bash
# Development (.env)
AZURE_FUNCTION_URL=http://localhost:7071
AZURE_FUNCTION_KEY=
```

## API Specification

For detailed field mappings and naming conventions, see [API Field Reference](api_field_reference.md).

### Request Format
```json
{
    "observerHeight": float,    // meters/feet
    "distance": float,          // km/miles
    "targetHeight": float,      // meters/feet (optional)
    "refractionFactor": float,  // default 1.07
    "isMetric": boolean        // unit control
}
```

### Validation Limits
```python
MIN_OBSERVER_HEIGHT = 2.0    # meters
MAX_OBSERVER_HEIGHT = 9000.0 # meters
MIN_DISTANCE = 5.0          # kilometers
MAX_DISTANCE = 600.0        # kilometers
MAX_TARGET_HEIGHT = 9000.0  # meters
```

### Response Format
```json
{
  "D1": 256.031,        // Distance to horizon (km)
  "dip_angle": 2.225,   // Horizon dip angle (degrees)
  "h2": 733.529,        // Hidden height (m)
  "h3": 1266.471,       // Visible height (m) - if target provided
  "CD": 1266.334,       // Apparent visible height (m) - if target provided
  "is_visible": true    // Whether target is visible
}
```

## Production Setup

### Azure Resources Required
1. **Function App**
   - Python runtime
   - Consumption plan (or dedicated if needed)
   - Application Insights enabled

2. **Storage Account**
   - General purpose v2
   - Standard performance tier
   - LRS replication (or higher if needed)

### Configuration Steps
1. Create Azure Function App
   - Choose Python runtime
   - Set up deployment credentials
   - Configure application settings

2. Security Setup
   - Generate API keys
   - Configure authentication
   - Set up CORS if needed

3. Environment Configuration
   ```bash
   # Production
   AZURE_FUNCTION_URL=https://your-function-app.azurewebsites.net
   AZURE_FUNCTION_KEY=your-function-key
   ```

4. Monitoring
   - Configure Azure Application Insights
   - Set up alerts
   - Monitor API usage and costs

## Testing

### Local Testing
1. Start local Azure Function:
   ```bash
   func start
   ```
2. Use tools like Postman or curl to test endpoints
3. Verify input validation
4. Test error handling

### Production Testing
1. Verify API endpoints
2. Test authentication
3. Check rate limiting
4. Monitor performance metrics

## Maintenance

### Regular Tasks
1. Monitor Azure costs
2. Review Application Insights logs
3. Update dependencies
4. Check for Azure Functions runtime updates

### Troubleshooting
1. Check Application Insights for errors
2. Verify environment variables
3. Review CORS settings if applicable
4. Check Azure Function logs
