# Beyond Horizon Calculator API

## Deployment Status 
The Beyond Horizon Calculator API is successfully deployed and operational.

## API Endpoint
Base URL: `https://beyondhorizoncalc.azurewebsites.net/api/calculate`

## Authentication
- Function-level authentication using function key
- Key must be included as `code` parameter in URL
- Example: `https://beyondhorizoncalc.azurewebsites.net/api/calculate?code=YOUR_FUNCTION_KEY`

## Project Structure
```
BeyondHorizonCalc-Function/
├── calculate/
│   ├── __init__.py      # Main calculator logic and HTTP trigger
│   └── function.json    # HTTP trigger configuration
├── host.json            # Function app configuration
├── local.settings.json  # Local development settings
└── requirements.txt     # Project dependencies (azure-functions)
```

## API Usage

For detailed information about the calculations performed by the API, see [Calculation Specification](calculation_specification.md).

### Request Format
```json
{
    "observerHeight": 2,      // meters (2-9000)
    "distance": 10,           // kilometers (5-600)
    "targetHeight": 100,      // meters (0-9000)
    "refractionFactor": 1.07, // optional (1.00-1.25)
    "isMetric": true         // optional
}
```

### Response Format
```json
{
    "D1": 5.222,                    // Distance to horizon (km)
    "hidden_height": 1.834,         // Hidden height (m)
    "visible_target_height": 98.166, // Visible height (m)
    "CD": 98.123,                   // Apparent height (m)
    "dip_angle": 0.045,             // Horizon dip angle (degrees)
    "perspective_scaled_height": 0.009812, // Height/distance ratio
    "is_visible": true,             // Target visibility status
    "total_distance": 10.0,         // Total distance (km)
    "trace": {                      // Optional calculation trace
        "steps": [
            {
                "description": "Initial parameters",
                "formula": "N/A",
                "inputs": {...},
                "result": 0.0
            },
            // Additional calculation steps...
        ]
    }
}
```

The `trace` field provides detailed step-by-step calculation information, useful for debugging and verification. Each step includes the formula used, input values, and the result.

## Configuration Settings
1. Azure Function App:
   - Runtime: Python
   - Version: 3.9
   - HTTP Version: 2.0
   - Functions Extension Version: ~4

2. Authentication:
   - App Service Authentication: OFF
   - Function-level Authentication: ON (requires function key)

## Error Handling
The API returns appropriate HTTP status codes:
- 200: Successful calculation
- 400: Invalid input (with error message)
- 401: Missing or invalid function key
- 500: Internal server error

## Testing
- Use Postman for API testing
- Save the function URL and key for Twitter bot configuration
- Test edge cases within these ranges:
  - Observer height: 2-9000 meters
  - Distance: 5-600 kilometers
  - Target height: 0-9000 meters
  - Refraction factor: 1.00-1.25

## Maintenance Notes
1. Function Key Management:
   - Access keys via Azure Portal: Functions > calculate > Function Keys
   - Or via VS Code: Azure Extension > Function App > Functions > calculate > Copy Function Url

2. Deployment:
   - Deploy via VS Code Azure Extension
   - Right-click Function App > "Deploy to Function App..."
   - Select BeyondHorizonCalc-Function directory

3. Monitoring:
   - Check logs in Azure Portal under "Monitor"
   - Use Application Insights for detailed telemetry

## Security Considerations
1. Never commit function keys to source control
2. Store keys securely in Twitter bot configuration
3. Monitor API usage through Azure Portal
4. Consider implementing rate limiting if needed

## Next Steps
1. Integrate with Twitter bot:
   - Add function URL and key to bot configuration
   - Implement error handling for API responses
   - Test integration thoroughly

2. Consider future enhancements:
   - Add caching for frequent calculations
   - Implement batch calculation endpoint
   - Add detailed logging for usage analytics
