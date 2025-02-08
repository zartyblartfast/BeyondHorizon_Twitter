import json
import requests
import pandas as pd
import os
import urllib.parse
# from tabulate import tabulate
from location_manager import LocationManager
from curvature_calculator import CurvatureCalculator
from dotenv import load_dotenv
import datetime
import time

# Load environment variables
load_dotenv('config/.env')

def get_api_result(observer_height, distance, target_height, refraction_factor):
    """Get result from Azure Function API"""
    url = os.getenv('AZURE_FUNCTION_URL')
    # URL decode the function key
    function_key = urllib.parse.unquote(os.getenv('AZURE_FUNCTION_KEY'))
    params = {"code": function_key}
    data = {
        "observerHeight": observer_height,
        "targetHeight": target_height,
        "distance": distance,
        "refractionFactor": refraction_factor,
        "isMetric": True
    }
    
    try:
        print("\nAPI Request:", flush=True)
        print(f"URL: {url}/api/calculate", flush=True)
        print("Data:", flush=True)
        print(json.dumps(data, indent=2), flush=True)
        time.sleep(0.1)  # Small delay to ensure output is flushed
        
        full_url = f"{url}/api/calculate"
        response = requests.post(full_url, params=params, json=data)
        response.raise_for_status()  # Raise exception for bad status codes
        result = response.json()
        
        print("\nAPI Response:", flush=True)
        print(f"Status Code: {response.status_code}", flush=True)
        print("Headers:", flush=True)
        print(json.dumps(dict(response.headers), indent=2), flush=True)
        print("Body:", flush=True)
        print(json.dumps(result, indent=2), flush=True)
        time.sleep(0.1)  # Small delay to ensure output is flushed
        return result
    except Exception as e:
        print(f"\nAPI Request failed for:", flush=True)
        print(f"URL: {url}", flush=True)
        print(f"Data: {json.dumps(data, indent=2)}", flush=True)
        print(f"Error: {str(e)}", flush=True)
        if hasattr(e, 'response'):
            print(f"Status Code: {e.response.status_code}", flush=True)
            print(f"Response Text: {e.response.text}", flush=True)
        raise

def get_local_result(observer_height, distance, target_height, refraction_factor):
    """Get result from local calculator"""
    calculator = CurvatureCalculator()
    result = calculator.calculate_visibility(
        h1=observer_height,
        L0=distance,
        XZ=target_height,
        refraction_factor=refraction_factor
    )
    # Format to match API response structure
    return {
        "hidden_height": round(result["h2"], 3),
        "horizon_distance": round(result["D1"], 3),
        "total_distance": round(result["total_distance"], 3),
        "dip_angle": round(result["dip_angle"], 3),
        "is_metric": True,
        "visible_target_height": round(result.get("h3", 0), 3),
        "apparent_visible_height": round(result.get("CD", 0), 3),
        "perspective_scaled_height": round(result.get("perspective_scaled_height", 0), 3),
        "target_visible": result.get("is_visible", False)
    }

def compare_results(api_result, local_result):
    """Compare API and local results"""
    differences = {}
    
    # Define fields to compare with their rounding precision
    fields_to_compare = {
        "hidden_height": 3,
        "horizon_distance": 3,
        "total_distance": 3,
        "dip_angle": 3,
        "visible_target_height": 3,
        "apparent_visible_height": 3,
        "perspective_scaled_height": 3,
        "target_visible": None  # Boolean, no rounding needed
    }
    
    for field, precision in fields_to_compare.items():
        api_value = api_result.get(field)
        local_value = local_result.get(field)
        
        if api_value is None:
            differences[field] = ("MISSING", local_value)
            continue
        if local_value is None:
            differences[field] = (api_value, "MISSING")
            continue
        
        # Compare numeric values with rounding
        if precision is not None:
            try:
                api_val = round(float(api_value), precision)
                local_val = round(float(local_value), precision)
                if abs(api_val - local_val) > 0.001:  # Allow small floating point differences
                    differences[field] = (api_val, local_val)
            except (TypeError, ValueError):
                differences[field] = (api_value, local_value)
        # Compare non-numeric values directly
        elif api_value != local_value:
            differences[field] = (api_value, local_value)
    
    return differences

def main():
    """Main function to test API and local calculations"""
    # Create output directory if it doesn't exist
    os.makedirs("test_results/batch_comparisons", exist_ok=True)
    
    # Load locations from GitHub
    location_manager = LocationManager()
    location_manager.load_locations()
    locations = location_manager.locations['presets']
    print(f"\nLoaded {len(locations)} locations from GitHub", flush=True)
    
    # Prepare results for CSV - store each test case
    test_cases = []
    
    # Test each location
    for location in locations:
        print(f"\nTesting {location['name']}:", flush=True)
        print(f"  Observer Height: {location['observerHeight']}m", flush=True)
        print(f"  Target Height: {location['targetHeight']}m", flush=True)
        print(f"  Distance: {location['distance']}km", flush=True)
        print(f"  Refraction: {location['refractionFactor']}", flush=True)
        
        try:
            # Get results
            api_result = get_api_result(
                location["observerHeight"],
                location["distance"],
                location["targetHeight"],
                location["refractionFactor"]
            )
            time.sleep(1)  # Add a small delay between API calls
            
            # Print API result for debugging
            print("\n  API Result:", flush=True)
            for key, value in api_result.items():
                print(f"    {key}: {value}", flush=True)
            
            local_result = get_local_result(
                location["observerHeight"],
                location["distance"],
                location["targetHeight"],
                location["refractionFactor"]
            )
            
            # Print local result for debugging
            print("\n  Local Result:", flush=True)
            for key, value in local_result.items():
                print(f"    {key}: {value}", flush=True)
            
            # Compare and print differences
            differences = compare_results(api_result, local_result)
            if differences:
                print("\n  Differences found:", flush=True)
                for field, (api_val, local_val) in differences.items():
                    print(f"    {field}:", flush=True)
                    print(f"      API:   {api_val}", flush=True)
                    print(f"      Local: {local_val}", flush=True)
            else:
                print("\n  Results match exactly!", flush=True)
            
            # Store test case results
            test_case = {
                "Measurement": [
                    "Location",
                    "Observer Height",
                    "Target Height",
                    "Total Distance",
                    "Horizon Distance",
                    "Hidden Height",
                    "Visible Height",
                    "Apparent Height",
                    "Target Visible?",
                    "Dip Angle"
                ],
                "API Result": [
                    location["name"],
                    location["observerHeight"],
                    location["targetHeight"],
                    api_result["total_distance"],
                    api_result["horizon_distance"],
                    api_result["hidden_height"],
                    api_result["visible_target_height"],
                    api_result["apparent_visible_height"],
                    api_result["target_visible"],
                    api_result["dip_angle"]
                ],
                "Local Result": [
                    location["name"],
                    location["observerHeight"],
                    location["targetHeight"],
                    local_result["total_distance"],
                    local_result["horizon_distance"],
                    local_result["hidden_height"],
                    local_result["visible_target_height"],
                    local_result["apparent_visible_height"],
                    local_result["target_visible"],
                    local_result["dip_angle"]
                ],
                "Units": [
                    "-",
                    "meters",
                    "meters",
                    "kilometers",
                    "kilometers",
                    "meters",
                    "meters",
                    "meters",
                    "-",
                    "degrees"
                ],
                "Notes": [
                    "Test Location",
                    "Height of observer",
                    "Height of target",
                    "Total distance between points",
                    "Distance to horizon",
                    "Height hidden by Earth's curve",
                    "Height visible above horizon",
                    "Height considering refraction",
                    "Is target visible?",
                    "Angle to horizon"
                ]
            }
            test_cases.append(test_case)
                
        except Exception as e:
            print(f"\n  Error: {str(e)}", flush=True)
            if hasattr(e, 'response'):
                print(f"  Response Status: {e.response.status_code}", flush=True)
                print(f"  Response Text: {e.response.text}", flush=True)
    
    # Save results to CSV
    if test_cases:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for idx, test_case in enumerate(test_cases):
            csv_path = f"test_results/batch_comparisons/comparison_{idx+1}_{timestamp}.csv"
            pd.DataFrame(test_case).to_csv(csv_path, index=False)
            print(f"\nResults for {test_case['API Result'][0]} saved to: {csv_path}", flush=True)

if __name__ == "__main__":
    main()
