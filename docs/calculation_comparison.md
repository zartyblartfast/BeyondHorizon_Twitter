# Beyond Horizon API Implementation Analysis

## Test Case: K2 to Broad Peak
Input Parameters:
- Observer Height (h1): 8611m (K2)
- Target Height (XZ): 8051m (Broad Peak)
- Distance (L0): 207.891 km
- Refraction Factor: 1.07

## Core Mathematical Calculations

### 1. Distance to Horizon
Both implementations use the correct formula:
```python
d1 = sqrt(2 * h1 * R)  # R is effective radius with refraction
```

### 2. Hidden Height Calculation
Both use similar formulas:
```python
l2 = distance_meters - d1_m
BOX_fraction = l2 / C          # C = 2πR
BOX_angle = 2π * BOX_fraction  # This is correct! Converts fraction to radians
OC = R / cos(BOX_angle)
h2 = OC - R
```

The 2π multiplication is mathematically correct because:
1. BOX_fraction = l2 / (2πR)  # Fraction of Earth's circumference
2. BOX_angle = 2π * (l2 / (2πR)) = l2/R  # Actual angle in radians

### 3. Visible Height
Both use:
```python
h3 = max(0, XZ - h2)
```

### 4. Apparent Height
API (Incorrect):
```python
angle = (L0 * 1000) / R  # WRONG: Uses total distance
CD = h3 * cos(angle)
```

Should be:
```python
angle = l2 / R  # Use distance beyond horizon
CD = h3 * cos(angle)
```

## Calculation Differences

### 1. Distance to Horizon (d1)
Both implementations use identical formulas:
```python
R = EARTH_RADIUS * refraction_factor
d1 = sqrt(2 * h1 * R)
```

No differences in this calculation.

### 2. Hidden Height (h2)
Both use the same sequence of calculations but with one critical difference:

Local (Correct):
```python
l2 = distance_meters - d1
BOX_fraction = l2 / (2 * π * R)
BOX_angle = BOX_fraction  # Angle in radians
OC = R / cos(BOX_angle)
h2 = OC - R
```

API (Incorrect):
```python
l2 = distance_meters - d1
BOX_fraction = l2 / (2 * π * R)
BOX_angle = 2 * π * BOX_fraction  # DIFFERENCE: Extra 2π multiplication
OC = R / cos(BOX_angle)
h2 = OC - R
```

Difference: API multiplies BOX_fraction by 2π, which is incorrect. This effectively doubles the angle used in the cosine calculation.

### 3. Visible Height (h3)
Both implementations use identical formulas:
```python
h3 = max(0, XZ - h2)
```

No formula difference, but API uses incorrect h2 value from previous calculation.

### 4. Apparent Height (CD)

Local (Correct):
```python
l2 = distance_meters - d1  # Distance beyond horizon
angle = l2 / R  # Uses distance beyond horizon
CD = h3 * cos(angle)
```

API (Incorrect):
```python
angle = (L0 * 1000) / R  # DIFFERENCE: Uses total distance
CD = h3 * cos(angle)
```

Difference: API uses total distance (L0) for angle calculation instead of distance beyond horizon (l2).

### 5. Perspective Height

Both use same basic formula but with different inputs:

Local (Correct):
```python
perspective_height = CD / distance_meters  # Uses correct CD value
```

API (Incorrect):
```python
perspective_height = CD / (L0 * 1000)  # Uses incorrect CD value
```

No formula difference, but API uses incorrect CD value from previous calculation.

## Impact on Test Case Results

For K2 to Broad Peak:

1. Hidden Height (h2):
   - API: 3594.4m
   - Error: Too large due to doubled angle in BOX_angle calculation

2. Visible Height (h3):
   - API: 4456.6m
   - Error: Incorrect due to using wrong h2 value

3. Apparent Height (CD):
   - API: Incorrect
   - Error: Uses wrong distance in angle calculation (L0 instead of l2)

4. Perspective Height:
   - API: Incorrect
   - Error: Uses incorrect CD value from previous calculation

## Critical Issues

### 1. Geometric Error in Apparent Height
The API uses the wrong distance for angle calculation:
- Uses total distance (L0) instead of distance beyond horizon (l2)
- This is a fundamental geometric error
- Results in incorrect apparent height regardless of units

### 2. Unit Handling Issues
These compound the geometric errors:
1. Distance conversions:
   - Inconsistent handling of km vs m
   - Affects l2 calculation
   - Cascades through hidden height calculation

2. Input validation:
   - No clear unit specifications
   - No validation of unit consistency

### 3. Combined Effects
For K2 to Broad Peak test case:
1. Hidden Height = 3594.4m
   - Formula is correct
   - Value is wrong due to incorrect l2 from unit issues

2. Visible Height = 4456.6m
   - Formula is correct
   - Value is wrong due to incorrect hidden height

3. Apparent Height
   - Formula is wrong (uses L0 instead of l2)
   - Also affected by unit issues
   - Double error from both geometric and unit problems

## Required Fixes

### 1. Fix Geometric Error
```python
# In calculate_visibility
l2 = distance_meters - d1_m
angle = l2 / R  # Use correct distance for angle
```

### 2. Fix Unit Handling
```python
def calculate_hidden_height(self, L0_km: float, d1_m: float, R_m: float):
    # Ensure consistent units
    distance_meters = L0_km * 1000
    l2 = distance_meters - d1_m
```

### 3. Add Validation
```python
def validate_inputs(self, h1: float, L0: float, XZ: float):
    # Add unit validation
    if L0 > 1000:
        raise ValidationError("Distance appears to be in meters, expected kilometers")
```

## API Correction Specification

### Overview
Two critical changes are required in the API implementation to match the correct local calculations:

1. Remove the 2π multiplication in the hidden height calculation
2. Use distance beyond horizon (l2) instead of total distance (L0) for apparent height angle calculation

### Required Changes

#### 1. Hidden Height Calculation Fix
```python
# Current API code
l2 = distance_meters - d1
BOX_fraction = l2 / (2 * π * R)
BOX_angle = 2 * π * BOX_fraction  # INCORRECT: Extra 2π multiplication
OC = R / cos(BOX_angle)
h2 = OC - R

# Change to:
l2 = distance_meters - d1
BOX_fraction = l2 / (2 * π * R)
BOX_angle = BOX_fraction  # CORRECTED: Remove 2π multiplication
OC = R / cos(BOX_angle)
h2 = OC - R
```

#### 2. Apparent Height Calculation Fix
```python
# Current API code
angle = (L0 * 1000) / R  # INCORRECT: Uses total distance
CD = h3 * cos(angle)

# Change to:
l2 = distance_meters - d1  # Ensure l2 is calculated or passed from hidden height calculation
angle = l2 / R  # CORRECTED: Use distance beyond horizon
CD = h3 * cos(angle)
```

### Implementation Notes

1. Hidden Height Change:
   - Location: In the hidden height calculation function
   - Impact: Will produce smaller, correct hidden height values
   - Dependencies: No other changes required for this fix

2. Apparent Height Change:
   - Location: In the visibility calculation function
   - Impact: Will produce correct apparent height values
   - Dependencies: Requires l2 value from hidden height calculation
   - Note: Ensure l2 is available in this scope

### Expected Results After Changes
For K2 to Broad Peak test case:
1. Hidden Height (h2): Will be significantly smaller than current 3594.4m
2. Visible Height (h3): Will be larger than current 4456.6m due to correct h2
3. Apparent Height (CD): Will use correct angle calculation
4. Perspective Height: Will be correct due to proper CD value

### Validation Steps
1. Compare API results with local implementation using test case:
   - Observer Height (h1): 8611m
   - Target Height (XZ): 8051m
   - Distance (L0): 207.891 km
   - Refraction Factor: 1.07

2. Verify each calculation step:
   - Hidden height matches local implementation
   - Visible height is correct based on new hidden height
   - Apparent height uses correct distance for angle
   - Perspective height matches local implementation

## Next Steps
1. Update the API's apparent height calculation to use distance beyond horizon (l2) instead of total distance (L0):
```python
# Current API code
angle = (L0 * 1000) / R  # Uses total distance

# Should be changed to
l2 = distance_meters - d1  # Distance beyond horizon
angle = l2 / R  # Use distance beyond horizon
```

## Actual Code Differences

After reviewing both implementations, there is only one concrete difference in the code:

1. In the apparent height calculation:
   - Local uses distance beyond horizon (l2) for the angle calculation
   - API uses total distance (L0) for the angle calculation

All other calculations (hidden height, visible height, perspective scaling) use identical formulas in both implementations.