# Beyond Horizon Calculation Specification

This document specifies the core calculations used in the Beyond Horizon API. These calculations have been tested and verified to match the calculations used in beyondHorizonCalc.com.

## Core Constants

- Earth Radius (R): 6,371,000 meters
- Default Refraction Factor: 1.07 (standard atmospheric conditions)
- Effective Radius: R * refraction_factor

## Input Parameters

1. **Observer Height (h1)**
   - Units: meters
   - Valid range: 2m to 9,000m

2. **Distance (L0)**
   - Units: kilometers
   - Valid range: 5km to 600km

3. **Target Height (XZ)**
   - Units: meters
   - Valid range: 0m to 9,000m
   - Optional parameter

4. **Refraction Factor**
   - Dimensionless ratio
   - Valid range: 1.00 to 1.25
   - Default: 1.07

## Core Calculations

### 1. Distance to Horizon
```python
R = EARTH_RADIUS * refraction_factor
d1 = math.sqrt(2 * h1 * R)  # Result in meters
D1 = d1 / 1000  # Convert to kilometers
```

### 2. Hidden Height
```python
distance_meters = L0 * 1000
C = 2 * math.pi * R  # Earth's circumference

l2 = distance_meters - d1
BOX_fraction = l2 / C
BOX_angle = 2 * math.pi * BOX_fraction
OC = R / math.cos(BOX_angle)
h2 = OC - R  # Hidden height in meters
```

### 3. Visible Height
```python
h3 = max(0, XZ - h2)  # Visible height in meters
```

### 4. Apparent Height
```python
angle = (L0 * 1000) / R  # Using total distance in meters
CD = h3 * math.cos(angle)  # Apparent height in meters
```

### 5. Perspective Scaling
```python
perspective_scaled = CD / (L0 * 1000)  # Ratio of apparent height to distance
perspective_scaled = max(0, perspective_scaled)
```

### 6. Dip Angle
```python
ratio = R / (R + h1)
dip_angle = math.degrees(math.acos(ratio))  # Degrees
```

## Implementation Notes

1. All internal calculations use meters for consistency
2. Angles are calculated in radians and converted to degrees only for output
3. The API includes detailed calculation tracing for debugging and verification
4. These calculations have been verified to match beyondHorizonCalc.com's results

## API Response Format

```json
{
    "D1": 123.456,              // Distance to horizon (km)
    "hidden_height": 789.012,   // Hidden height (m)
    "visible_target_height": 345.678,  // Visible height (m)
    "CD": 234.567,              // Apparent height (m)
    "dip_angle": 1.234,         // Horizon dip angle (degrees)
    "perspective_scaled_height": 0.001234,  // Height/distance ratio
    "is_visible": true,         // Target visibility status
    "total_distance": 100.0     // Total distance (km)
}
```
