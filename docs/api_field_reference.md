# BeyondHorizonCalc API Field Reference

## Field Name Mapping

### Input Fields
| API Field Name    | App Field Name | Description                | Units      |
|------------------|----------------|----------------------------|------------|
| observerHeight   | h1            | Height of observer         | meters/feet|
| distance         | L0            | Line of sight distance     | km/miles   |
| targetHeight     | XZ            | Height of target (optional)| meters/feet|
| refractionFactor | refraction    | Atmospheric refraction     | ratio      |
| isMetric         | units         | Use metric units if true   | boolean    |

### Response Fields
| API Field Name           | App Field Name | Description                    | Units      |
|-------------------------|----------------|--------------------------------|------------|
| D1                      | D1            | Distance to horizon            | km/miles   |
| dip_angle               | dip           | Horizon dip angle              | degrees    |
| h2                      | XC            | Hidden height                  | meters/feet|
| h3                      | h3            | Visible height                 | meters/feet|
| CD                      | CD            | Apparent visible height        | meters/feet|
| is_visible              | visible       | Target visibility status       | boolean    |

## Input Field Specifications

### Required Fields
- Observer Height (h1)
  - Range: 2 to 9,000 meters
  - API field: observerHeight

- Distance (L0)
  - Range: 5 to 600 kilometers
  - API field: distance

- Refraction Factor
  - Range: 1.00 to 1.25
  - API field: refractionFactor
  - Preset values:
    - None: 1.00
    - Low: 1.02
    - Below Average: 1.04
    - Average: 1.07 (default)
    - Above Average: 1.10
    - High: 1.15
    - Very High: 1.20
    - Extremely High: 1.25

### Optional Fields
- Target Height (XZ)
  - Range: 0 to 9,000 meters
  - API field: targetHeight

### Unit Conversion
- When isMetric is false:
  - Heights: meters to feet (× 3.28084)
  - Distances: kilometers to miles (× 0.621371)

## Notes
- API uses camelCase for request fields
- API response uses snake_case
- App uses short-form variable names from original calculations
- All numerical values use float type
