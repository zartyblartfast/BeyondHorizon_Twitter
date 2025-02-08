import json
import requests
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/.env')

def test_api():
    url = os.getenv('AZURE_FUNCTION_URL') + "/api/calculate"
    function_key = urllib.parse.unquote(os.getenv('AZURE_FUNCTION_KEY'))
    params = {"code": function_key}
    
    # Test data
    data = {
        "observerHeight": 2,
        "distance": 10,
        "targetHeight": 100,
        "refractionFactor": 1.07,
        "isMetric": True
    }
    
    print("\nAPI Request:")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, params=params, json=data)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.ok:
            result = response.json()
            print("\nParsed Response:")
            print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_api()
