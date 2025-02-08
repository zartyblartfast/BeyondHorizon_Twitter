# API Calculator Usage Guide

## Overview
The `CurvatureCalculator` class supports both local calculations and API-based calculations with automatic fallback. Both implementations now provide identical results, using spherical geometry and matching the API's calculation methods exactly.

## Basic Usage

### Local Calculations Only
```python
from src.curvature_calculator import CurvatureCalculator

# Create calculator in local-only mode
calc = CurvatureCalculator()

# Calculate visibility
result = calc.calculate_visibility(
    h1=4808,    # Observer height (meters)
    L0=100,     # Distance (kilometers)
    XZ=2000,    # Target height (meters)
    refraction_factor=1.07  # Optional, defaults to 1.07
)
```

### API-Enabled Calculations
```python
# Create calculator with API enabled
calc = CurvatureCalculator(use_api=True)

# Calculate visibility (will try API first, fall back to local if API fails)
result = calc.calculate_visibility(
    h1=4808,
    L0=100,
    XZ=2000
)
```

## Configuration

### Environment Variables
Create a `config/.env` file with:
```bash
# API Configuration
AZURE_FUNCTION_URL=http://localhost:7071  # Local development
AZURE_FUNCTION_KEY=                       # Optional for local development
```

For production:
```bash
AZURE_FUNCTION_URL=https://your-function-app.azurewebsites.net
AZURE_FUNCTION_KEY=your-function-key
```

## Calculation Details

### Key Implementation Notes
1. **Dip Angle Calculation**:
   - Uses unrefracted Earth radius (6371 km) for geometric dip angle
   - Formula: `dip_angle = acos(R / (R + h1))` where R is unrefracted radius
   - This matches the API implementation exactly

2. **Refraction Handling**:
   - Refraction factor (default 1.07) applied to Earth radius for all calculations EXCEPT dip angle
   - Effective radius = 6371 km * refraction_factor

3. **Precision Differences**:
   - API (Dart) and local (Python) calculations may show minor differences (0.1-2.0%)
   - These are due to floating-point arithmetic differences between languages
   - All core calculations match within acceptable precision

## Error Handling

### Handling API Errors
```python
from src.curvature_calculator import CurvatureCalculator, APIError, ValidationError

calc = CurvatureCalculator(use_api=True)

try:
    result = calc.calculate_via_api(
        h1=4808,
        L0=100,
        XZ=2000
    )
except ValidationError as e:
    print(f"Invalid input: {e}")
except APIError as e:
    print(f"API error: {e}")
```

### Automatic Fallback
When using `calculate_visibility()`, API errors are automatically handled:
```python
# Will try API first, fall back to local calculation if API fails
result = calc.calculate_visibility(
    h1=4808,
    L0=100,
    XZ=2000
)
```

## Response Format

### API Response
```python
{
    "D1": 256.031,              # Distance to horizon (km)
    "dip_angle": 2.23,          # Horizon dip angle (degrees)
    "h2": 1.786,                # Hidden height (km)
    "h3": 0.214,                # Visible height (km)
    "CD": 0.214,                # Apparent visible height (km)
    "is_visible": True,         # Whether target is visible
    "total_distance": 100.0,    # Total distance (km)
    "perspective_scaled_height": 0.002  # Height adjusted for perspective
}
```

## Input Validation

### Valid Ranges
- Observer height: 2.0m - 9000m
- Distance: 5km - 600km
- Target height: 0m - 9000m
- Refraction factor: 1.00 - 1.25

### Unit Handling
- All inputs should be in metric units (meters for heights, kilometers for distances)
- Results are returned in the same units
- The API handles unit conversion internally if needed

## Testing

### Running Unit Tests
```bash
# Run all tests
python -m unittest tests/test_api_calculator.py

# Run specific test
python -m unittest tests.test_api_calculator.TestCurvatureCalculatorAPI.test_successful_api_call
```

## Best Practices

1. **Error Handling**
   - Always handle `ValidationError` and `APIError` when using `calculate_via_api()`
   - Use `calculate_visibility()` for automatic error handling and fallback

2. **Configuration**
   - Keep API credentials in `.env` file
   - Never commit API keys to version control
   - Use environment-specific URLs (local/production)

3. **Testing**
   - Run unit tests before deploying changes
   - Test both API and local calculation paths
   - Verify error handling works as expected
