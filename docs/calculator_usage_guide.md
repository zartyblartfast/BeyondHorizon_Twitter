# Calculator Usage Guide

## Overview
The `CurvatureCalculator` class provides a unified interface for Earth curvature calculations, supporting both local calculations and API-based calculations with automatic fallback. For details about the calculations and API deployment, see:
- [Calculation Specification](calculation_specification.md)
- [API Deployment Guide](api_calculator_deployment.md)

## Basic Usage

### Local Calculations
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

3. **Input Units**
   - Always provide heights in meters
   - Always provide distances in kilometers
   - Results will be returned in the same units

## Batch Testing

### Overview
The project includes tools to verify that local calculations match the API results exactly. This is crucial for maintaining calculation consistency across all platforms.

### Running Tests

1. **Test All Presets**
   ```bash
   python src/test_api_comparison.py
   ```
   This runs calculations for all preset locations using both local and API methods, highlighting any discrepancies.

2. **Test Single Location**
   ```bash
   python src/test_single_location.py
   ```
   Tests a specific location (default: Fort Niagara to Toronto) with detailed API response analysis.

### Test Results
Results are stored in the `test_results` directory:
```
test_results/
├── batch_comparisons/    # Full batch test results
└── single_location/     # Individual location tests
```

### Common Issues
1. **API Connection**
   - Verify Azure Function URL and key in `.env`
   - Check if the Azure Function is running

2. **Calculation Differences**
   - The script highlights differences between API and local results
   - Differences should be investigated as they indicate potential bugs

3. **Dependencies**
   - Ensure all packages are installed: `pip install requests pandas python-dotenv tabulate`
