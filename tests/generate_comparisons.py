"""
Generate comparison data between API and local calculations.
"""
import json
import csv
import os
from pathlib import Path
import sys

# Add API project to path
api_project = Path(__file__).parent.parent.parent / "BeyondHorizonCalc-Function"
sys.path.append(str(api_project))

from calculate import CurvatureCalculator
from calculate.calculation_tracer import TracedCalculator

# Constants
TEST_RESULTS_DIR = Path(__file__).parent.parent / "test_results"
BATCH_COMP_DIR = TEST_RESULTS_DIR / "batch_comparisons"

def ensure_directories():
    """Ensure output directories exist."""
    TEST_RESULTS_DIR.mkdir(exist_ok=True)
    BATCH_COMP_DIR.mkdir(exist_ok=True)

def save_test_case(name: str, inputs: dict, api_result: dict, local_result: dict):
    """Save test case results and traces."""
    # Save traces as CSV
    with open(BATCH_COMP_DIR / f"{name}_api_trace.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Step', 'Description', 'Formula', 'Inputs', 'Result'])
        for step in api_result['trace'].steps:
            writer.writerow([
                step.step_number,
                step.description,
                step.formula,
                json.dumps(step.inputs),
                step.result
            ])
            
    with open(BATCH_COMP_DIR / f"{name}_local_trace.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Step', 'Description', 'Formula', 'Inputs', 'Result'])
        for step in local_result['trace'].steps:
            writer.writerow([
                step.step_number,
                step.description,
                step.formula,
                json.dumps(step.inputs),
                step.result
            ])
            
    # Save comparison summary
    with open(BATCH_COMP_DIR / f"{name}_comparison.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Metric', 'API Value', 'Local Value', 'Difference'])
        
        # Input parameters
        writer.writerow(['', '', '', ''])
        writer.writerow(['Inputs:', '', '', ''])
        writer.writerow(['Observer Height (h1)', inputs['h1'], inputs['h1'], 0])
        writer.writerow(['Distance (L0)', inputs['L0'], inputs['L0'], 0])
        writer.writerow(['Refraction Factor', inputs['refraction_factor'], inputs['refraction_factor'], 0])
        writer.writerow(['Target Height - optional (XZ)', inputs['XZ'], inputs['XZ'], 0])
        
        # Results
        writer.writerow(['', '', '', ''])
        writer.writerow(['Results:', '', '', ''])
        
        # Map the internal keys to their display labels
        metric_labels = {
            'D1': 'Distance to Horizon (D1)',
            'dip_angle': 'Horizon Dip Angle',
            'h2': 'Hidden Height (h2, XC)',
            'h3': 'Visible Height (h3)',
            'CD': 'Apparent Visible Height (CD)',
            'perspective_scaled_height': 'Perspective Scaled Apparent Visible Height'
        }
        
        metrics = ['D1', 'dip_angle', 'h2', 'h3', 'CD', 'perspective_scaled_height']
        for metric in metrics:
            api_val = api_result[metric]
            local_val = local_result[metric]
            diff = abs(api_val - local_val)
            writer.writerow([metric_labels[metric], api_val, local_val, diff])
        
        # Add visibility result
        writer.writerow(['Target Visible', 
                        'Yes' if api_result['is_visible'] else 'No',
                        'Yes' if local_result['is_visible'] else 'No',
                        'Match' if api_result['is_visible'] == local_result['is_visible'] else 'MISMATCH'])

def generate_test_data():
    """Generate test data for various scenarios."""
    ensure_directories()
    
    test_cases = [
        # Standard cases
        {
            "name": "mont_blanc",
            "h1": 375,    # Geneva altitude
            "L0": 70,     # Distance to Mont Blanc
            "XZ": 4808,   # Mont Blanc height
            "refraction_factor": 1.07
        },
        {
            "name": "sea_level_observation",
            "h1": 2,      # Minimum height
            "L0": 10,     # Short distance
            "XZ": 100,    # Small target
            "refraction_factor": 1.07
        },
        {
            "name": "high_altitude",
            "h1": 5000,   # High observer
            "L0": 200,    # Long distance
            "XZ": 6000,   # High target
            "refraction_factor": 1.07
        },
        # Edge cases
        {
            "name": "minimum_values",
            "h1": 2,      # Minimum height
            "L0": 5,      # Minimum distance
            "XZ": 0,      # Minimum target
            "refraction_factor": 1.00    # No refraction
        },
        {
            "name": "maximum_values",
            "h1": 9000,   # Maximum height
            "L0": 600,    # Maximum distance
            "XZ": 9000,   # Maximum target
            "refraction_factor": 1.25    # Maximum refraction
        },
        {
            "name": "near_horizon",
            "h1": 100,    # Observer near horizon
            "L0": 35.7,   # Distance near horizon
            "XZ": 100,    # Target near horizon
            "refraction_factor": 1.07
        },
        {
            "name": "just_visible",
            "h1": 1000,   # Standard height
            "L0": 150,    # Medium distance
            "XZ": 2000,   # Medium target
            "refraction_factor": 1.07
        }
    ]
    
    # Initialize calculators
    api_calc = CurvatureCalculator()
    local_calc = TracedCalculator()
    
    # Generate results
    results = []
    for case in test_cases:
        print(f"Processing {case['name']}...")
        
        # Calculate with both implementations
        api_result = api_calc.calculate_visibility(
            h1=case["h1"],
            L0=case["L0"],
            XZ=case["XZ"],
            refraction_factor=case["refraction_factor"]
        )
        
        local_result = local_calc.calculate_visibility(
            h1=case["h1"],
            L0=case["L0"],
            XZ=case["XZ"],
            refraction_factor=case["refraction_factor"]
        )
        
        # Save traces
        save_test_case(case['name'], case, api_result, local_result)
        
        # Save combined results
        results.append({
            "name": case["name"],
            "inputs": {
                "h1": case["h1"],
                "L0": case["L0"],
                "XZ": case["XZ"],
                "refraction_factor": case["refraction_factor"]
            },
            "api_result": {k: v for k, v in api_result.items() if k != "trace"},
            "local_result": {k: v for k, v in local_result.items() if k != "trace"}
        })
    
    # Save combined results
    with open(TEST_RESULTS_DIR / "test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nTest data generation complete!")
    print(f"Results saved to: {TEST_RESULTS_DIR}")

if __name__ == "__main__":
    generate_test_data()
