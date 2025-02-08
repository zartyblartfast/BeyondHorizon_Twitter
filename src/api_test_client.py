"""
Test client for local Azure Functions API integration.
"""
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config/.env")

def test_api_connection(observer_height: float = 4808, 
                       distance: float = 100, 
                       target_height: float = 2000,
                       refraction_factor: float = 1.07,
                       is_metric: bool = True) -> dict:
    """
    Test connection to local Azure Functions API.
    Uses Mont Blanc example by default.
    """
    # Get API URL from environment or use default local URL
    api_url = os.getenv("AZURE_FUNCTION_URL", "http://localhost:7071")
    endpoint = f"{api_url}/api/calculate"
    
    # Prepare request payload - match API's expected camelCase format
    payload = {
        "observerHeight": observer_height,
        "distance": distance,
        "targetHeight": target_height,
        "refractionFactor": refraction_factor,
        "isMetric": is_metric
    }
    
    try:
        # Make API request
        response = requests.post(endpoint, json=payload)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse and return results
        return response.json()
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Is the Azure Functions host running?")
        print(f"Attempted to connect to: {endpoint}")
        return None
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text}")
        return None
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def compare_with_local_calc():
    """Compare API results with local calculator results."""
    from curvature_calculator import CurvatureCalculator
    
    # Test parameters (Mont Blanc example)
    params = {
        "observer_height": 4808,  # meters
        "distance": 100,          # kilometers
        "target_height": 2000,    # meters
        "refraction_factor": 1.07
    }
    
    print("\nTesting calculations...")
    print("----------------------")
    print(f"Parameters:")
    print(f"Observer Height: {params['observer_height']}m")
    print(f"Distance: {params['distance']}km")
    print(f"Target Height: {params['target_height']}m")
    print(f"Refraction: {params['refraction_factor']}")
    
    # Get API results
    print("\nAPI Results:")
    api_results = test_api_connection(**params)
    if api_results:
        print(json.dumps(api_results, indent=2))
    
    # Get local results
    print("\nLocal Calculator Results:")
    local_calc = CurvatureCalculator()
    local_results = local_calc.calculate_visibility(
        h1=params['observer_height'],
        L0=params['distance'],
        XZ=params['target_height'],
        refraction_factor=params['refraction_factor']
    )
    print(json.dumps(local_results, indent=2))
    
    # Compare results if we have both
    if api_results:
        print("\nComparison:")
        print("------------")
        for key in local_results:
            if key in api_results:
                api_val = api_results[key]
                local_val = local_results[key]
                diff = abs(float(api_val) - float(local_val)) if isinstance(api_val, (int, float)) else 0
                match = "✓" if diff < 0.001 else "✗"
                print(f"{key}: {match} API={api_val}, Local={local_val}, Diff={diff:.6f}")

if __name__ == "__main__":
    compare_with_local_calc()
