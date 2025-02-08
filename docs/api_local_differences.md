# Beyond Horizon Calculation Comparison

## Document Purpose
This document outlines the verified differences between the local calculator implementation and the Azure Functions API implementation.

## Implementation Differences

### 1. Unit Conversion in Hidden Height Calculation
The API and local calculator handle distance unit conversion differently:

```python
# API Implementation (calculate_hidden_height)
if distance_meters < 1000:  # If distance is in km
    distance_meters = distance_meters * 1000

# Local Implementation (calculate_hidden_height)
distance_meters = L0 * 1000  # Always converts km to m
```

### 2. Response Units
The API returns values in different units compared to the local calculator:

```python
# API returns heights in kilometers
{
    "h2": round(h2, 3),  # in km
    "h3": round(h3, 3),  # in km
    "CD": round(CD, 3)   # in km
}

# Local calculator works in meters
```

## Testing Infrastructure

### 1. Calculation Tracing
The API implementation includes detailed tracing via the `CalculationTrace` class:
```python
class CalculationTrace:
    def add_step(self, description: str, formula: str, inputs: Dict[str, float], result: float):
        # Records each calculation step with:
        # - Description of the step
        # - Formula used
        # - Input values
        # - Result
        # - Timestamp
```

### 2. Test Cases
Standard test case using Mont Blanc scenario:
```python
# Mont Blanc viewpoint test case
h1 = 4808   # Observer height (Mont Blanc) in meters
L0 = 100    # Distance in kilometers
XZ = 2000   # Target height in meters
```

Additional validation test cases:
- Invalid observer height (h1 < H1_MIN)
- Invalid distance (L0 > L0_MAX)
- Invalid target height (XZ > XZ_MAX)
- Invalid refraction factor (RF > RF_MAX)

### 3. Trace Comparison
The `compare_traces` method identifies calculation differences:
```python
def compare_traces(self, other: 'CalculationTrace', tolerance: float = 1e-6) -> List[str]:
    # Compares two calculation traces and identifies:
    # - Missing calculation steps
    # - Different results
    # - Input differences
    # Returns list of discrepancies found
```

## Impact
These unit handling differences can lead to calculation discrepancies between the API and local implementations. The local calculator's implementation is considered correct.

## Next Steps
1. Run Mont Blanc test case through both implementations with tracing enabled
2. Compare traces to identify exact calculation differences
3. Verify mathematical formulas in both implementations
4. Document any additional differences found through testing
