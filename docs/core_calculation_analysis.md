# Beyond Horizon Core Calculation Analysis

## 1. Fundamental Concepts

### Earth Model
- Earth is modeled as a sphere with radius (R) = 6,371,000 meters
- Atmospheric refraction affects how light travels through the atmosphere
- Refraction is modeled by increasing the effective Earth radius
- Default refraction factor = 1.07 (standard atmospheric conditions)

### Key Physical Concepts
1. **Geometric Line of Sight**
   - Light travels in straight lines in a uniform medium
   - Earth's curvature blocks distant objects
   - Atmospheric refraction bends light slightly downward

2. **Atmospheric Refraction**
   - Light bends towards denser air (downward near Earth's surface)
   - Effect modeled by increasing Earth's apparent radius
   - Refraction factor typically between 1.00-1.25
   - Standard value of 1.07 represents average conditions

3. **Perspective Effects**
   - Objects appear smaller with distance
   - Angular size decreases linearly with distance
   - Apparent height affected by viewing angle

## 2. Core Variables

### Input Parameters
1. **Observer Height (h1)**
   - Physical height of observer above sea level
   - Units: meters
   - Valid range: 2m to 9000m
   - Affects horizon distance and dip angle

2. **Target Height (XZ)**
   - Physical height of target above sea level
   - Units: meters
   - Valid range: 0m to 9000m
   - Used to calculate visibility

3. **Total Distance (L0)**
   - Distance between observer and target
   - Units: kilometers
   - Valid range: 5km to 600km
   - Critical for hidden height calculation

4. **Refraction Factor**
   - Multiplier for effective Earth radius
   - Dimensionless ratio
   - Valid range: 1.00 to 1.25
   - Default: 1.07

### Intermediate Variables
1. **Effective Radius (R)**
   - R = EARTH_RADIUS * refraction_factor
   - Units: meters
   - Accounts for atmospheric refraction
   - Used in all spherical geometry calculations

2. **Earth Circumference (C)**
   - C = 2 * π * R
   - Units: meters
   - Used to calculate angular fractions
   - Depends on effective radius

3. **Distance to Horizon (d1)**
   - Units: meters (D1 in kilometers)
   - Based on observer height
   - Key reference point for visibility

4. **Beyond Horizon Distance (l2)**
   - l2 = distance_meters - d1
   - Units: meters
   - Portion of path beyond horizon
   - Used in hidden height calculation

### Output Variables
1. **Hidden Height (h2)**
   - Height hidden by Earth's curvature
   - Units: meters
   - Key determinant of visibility
   - Based on spherical geometry

2. **Visible Height (h3)**
   - Portion of target above hidden height
   - Units: meters
   - h3 = max(0, XZ - h2)
   - Determines if target is visible

3. **Apparent Height (CD)**
   - Visible height adjusted for viewing angle
   - Units: meters
   - Accounts for spherical geometry
   - Used in perspective calculation

4. **Perspective Scaled Height**
   - Ratio of apparent height to distance
   - Dimensionless
   - Represents visual scale
   - Used for display purposes

[To be continued with detailed calculation analysis...]
