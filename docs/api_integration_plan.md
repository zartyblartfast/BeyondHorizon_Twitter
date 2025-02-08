# Beyond Horizon API Integration Plan

## Current Setup Understanding

### Local Azure Functions Development
- **Location**: `c:/Users/clive/VSC/BeyondHorizonCalc-API/api/calculate`
- **Runtime**: Python Azure Functions
- **Local Endpoint**: `http://localhost:7071/api/calculate`
- **Authentication**: Anonymous (development only)
- **Storage**: Azure Storage Emulator

### Calculation Methods
1. **Local Python Calculations** (Current Twitter Bot)
   - Direct mathematical calculations in `curvature_calculator.py`
   - No API dependency
   - Input validation matches API limits

2. **Local Azure Function** (BeyondHorizonCalc-API)
   - Same calculations via HTTP API
   - Used by Flutter app in "API mode"
   - Runs locally for development

## Integration Plan

### Phase 1: Local API Testing (In Progress)

### ✅ Completed Steps

1. **Environment Setup**
   ```bash
   # Created requirements-api.txt with dependencies
   azure-functions
   azure-functions-worker
   python-dotenv>=1.0.0
   requests>=2.31.0
   ```

2. **Configuration**
   - Added Azure Functions settings to `config/.env`:
     ```bash
     AZURE_FUNCTION_URL=http://localhost:7071
     AZURE_FUNCTION_KEY=
     ```
   - Verified Azure Functions Core Tools installation (`func --version`)

3. **Test Client Implementation**
   - Created `src/api_test_client.py` for API testing
   - Implemented comparison between API and local calculations
   - Discovered API parameter naming conventions (camelCase)
   - Documented request/response formats

4. **Initial Testing**
   - Successfully connected to local API
   - Verified input validation
   - Compared calculation results
   - Found minor differences in precision and field naming

### 🔄 Current Status
1. **API Connection**: Working
2. **Parameter Format**: 
   - Request: camelCase (e.g., `observerHeight`)
   - Response: snake_case (e.g., `hidden_height`)
3. **Calculation Comparison**:
   - Most values match within acceptable precision
   - Some field names differ between API and local calculator

### 📝 Key Findings
1. **API Parameter Requirements**:
   ```json
   {
       "observerHeight": float,    // meters/feet
       "distance": float,          // km/miles
       "targetHeight": float,      // meters/feet (optional)
       "refractionFactor": float,  // default 1.07
       "isMetric": boolean        // unit control
   }
   ```

2. **Validation Limits**:
   - Observer height: 2.0m - 9000m
   - Distance: 5km - 600km
   - Target height: 0m - 9000m
   - Refraction: 1.00 - 1.25

3. **Response Format Differences**:
   - API provides additional fields (e.g., `perspective_scaled_height`)
   - Different field naming convention
   - Slight variations in numerical precision

### 🔜 Next Steps
1. **Code Updates**:
   - [ ] Align local calculator field names with API
   - [ ] Add API error handling to Twitter bot
   - [ ] Create unified calculation interface

2. **Testing**:
   - [ ] Edge case validation
   - [ ] Unit conversion verification
   - [ ] Error handling scenarios

3. **Documentation**:
   - [ ] Update API integration guide
   - [ ] Document field mapping between local/API
   - [ ] Add troubleshooting section

### Phase 2: Production API Setup
1. **Azure Resource Creation**
   - Create Azure Function App
   - Set up Azure Storage Account
   - Configure deployment credentials

2. **API Security**
   - Generate API keys
   - Set up proper authentication
   - Configure CORS if needed
   - Update anonymous access settings

3. **Environment Configuration**
   - Create production environment variables
   - Set up key vault for sensitive data
   - Configure logging and monitoring

4. **Code Deployment**
   - Deploy calculation code to Azure
   - Update API endpoint URLs
   - Verify production environment variables

### Phase 3: Production Testing
1. **API Verification**
   - Test production API endpoints
   - Verify authentication
   - Check rate limiting
   - Monitor performance

2. **Twitter Bot Integration**
   - Update configuration for production API
   - Implement proper error handling
   - Add retry logic for API failures
   - Test with production endpoints

3. **Monitoring Setup**
   - Configure Azure monitoring
   - Set up alerts
   - Monitor API usage and costs

## Implementation Notes

### API Response Format
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

### Input Validation Limits
```python
MIN_OBSERVER_HEIGHT = 2.0    # meters
MAX_OBSERVER_HEIGHT = 9000.0 # meters
MIN_DISTANCE = 5.0          # kilometers
MAX_DISTANCE = 600.0        # kilometers
MAX_TARGET_HEIGHT = 9000.0  # meters
```

### Required Environment Variables
1. **Development**
   ```
   AZURE_FUNCTION_URL=http://localhost:7071
   AZURE_FUNCTION_KEY=
   ```

2. **Production**
   ```
   AZURE_FUNCTION_URL=https://your-function-app.azurewebsites.net
   AZURE_FUNCTION_KEY=your-function-key
   ```

## Next Steps
1. Start local Azure Function for testing
2. Add API client to Twitter bot
3. Test with local API
4. Plan Azure resource requirements
5. Begin production API setup

## Questions to Address
1. Expected API request volume?
2. Budget constraints for Azure resources?
3. Required uptime/SLA?
4. Monitoring requirements?
5. Backup calculation strategy if API is unavailable?
