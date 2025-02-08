import os
import json
import requests
import urllib.parse
from dotenv import load_dotenv
import datetime
import pandas as pd
from curvature_calculator import CurvatureCalculator  # Assuming this is where CurvatureCalculator is defined

# Load environment variables
load_dotenv('config/.env')

def test_single_location():
    """Test a single location with minimal output"""
    # Test data for Pic de Finstrelles to Pic Gaspard
    data = {
        "observerHeight": 2826,
        "targetHeight": 3883,
        "distance": 443,
        "refractionFactor": 1.2,
        "isMetric": True
    }
    
    # Also test with local calculator
    calculator = CurvatureCalculator()
    local_result = calculator.calculate_visibility(
        h1=data["observerHeight"],
        L0=data["distance"],
        XZ=data["targetHeight"],
        refraction_factor=data["refractionFactor"]
    )
    
    print("\nLocal Calculator Result:")
    print(json.dumps(local_result, indent=2))
    
    url = os.getenv('AZURE_FUNCTION_URL') + "/api/calculate"
    function_key = urllib.parse.unquote(os.getenv('AZURE_FUNCTION_KEY'))
    params = {"code": function_key}
    
    print("\nMaking API request:")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    # Make request
    response = requests.post(url, params=params, json=data)
    
    print(f"\nResponse Status: {response.status_code}")
    print("\nResponse Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    
    print("\nResponse Text:")
    print(response.text)
    
    if response.ok:
        try:
            result = response.json()
            print("\nParsed Response:")
            print(json.dumps(result, indent=2))
        except json.JSONDecodeError as e:
            print("\nFailed to parse JSON:", str(e))

def main():
    """Test a single location (Fort Niagara to Toronto) and save detailed comparison"""
    # Create output directory if it doesn't exist
    os.makedirs("test_results/single_location", exist_ok=True)
    
    # Test parameters for Fort Niagara to Toronto
    observer_height = 2  # meters (height at Fort Niagara State Park)
    target_height = 533  # meters (CN Tower height)
    distance = 51       # kilometers (approximate distance across Lake Ontario)
    refraction = 0.13   # standard refraction factor
    
    try:
        # Get results from both calculations
        api_result = get_api_result(observer_height, distance, target_height, refraction)
        local_result = get_local_result(observer_height, distance, target_height, refraction)
        
        # Create comparison data
        comparison_data = {
            "Measurement": [
                "Observer Height", "Target Height", "Total Distance",
                "Horizon Distance", "Hidden Height", "Visible Height",
                "Apparent Height", "Target Visible?", "Dip Angle"
            ],
            "API Result": [
                observer_height, target_height, distance,
                api_result["horizon_distance"], api_result["hidden_height"],
                api_result["visible_target_height"], api_result["apparent_height"],
                api_result["target_visible"], api_result["dip_angle"]
            ],
            "Local Result": [
                observer_height, target_height, distance,
                local_result["horizon_distance"], local_result["hidden_height"],
                local_result["visible_target_height"], local_result["apparent_height"],
                local_result["target_visible"], local_result["dip_angle"]
            ],
            "Units": [
                "meters", "meters", "kilometers",
                "kilometers", "meters", "meters",
                "meters", "-", "degrees"
            ],
            "Notes": [
                "Standing at Fort Niagara State Park",
                "Height of CN Tower",
                "Distance across Lake Ontario",
                "How far until horizon drops away",
                "How much of target is hidden by Earth's curve",
                "How much of target is visible above horizon",
                "How tall the target appears considering atmospheric effects",
                "Can you see the CN Tower?",
                "How much you need to look down to see horizon"
            ]
        }
        
        # Save to CSV
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"test_results/single_location/niagara_toronto_{timestamp}.csv"
        pd.DataFrame(comparison_data).to_csv(csv_path, index=False)
        print(f"\nDetailed comparison saved to: {csv_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response Status: {e.response.status_code}")
            print(f"Response Text: {e.response.text}")

def get_api_result(observer_height, distance, target_height, refraction):
    # This function is not implemented in the provided code
    pass

def get_local_result(observer_height, distance, target_height, refraction):
    # This function is not implemented in the provided code
    pass

if __name__ == "__main__":
    test_single_location()
    main()
