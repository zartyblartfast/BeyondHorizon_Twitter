from api_client import test_api, CurvatureApiClient
from location_manager import LocationManager
import os
from dotenv import load_dotenv

def check_configuration():
    """Check if Azure Functions configuration is properly set"""
    load_dotenv("config/.env")
    
    config_status = {
        "url": os.getenv("AZURE_FUNCTION_URL", "http://localhost:7071"),
        "key": os.getenv("AZURE_FUNCTION_KEY", "not_set"),
        "using_local": False
    }
    
    if config_status["url"] == "http://localhost:7071":
        config_status["using_local"] = True
    
    return config_status

def main():
    print("\nTesting Beyond Horizon Calculator API Integration")
    print("==============================================\n")
    
    # Step 1: Check configuration
    print("Step 1: Checking Configuration")
    print("-----------------------------")
    config = check_configuration()
    print(f"API URL: {config['url']}")
    print(f"API Key: {'configured' if config['key'] != 'not_set' else 'not configured'}")
    if config["using_local"]:
        print("⚠️  Using local development server (http://localhost:7071)")
        print("   Make sure the Azure Functions API is running locally")
    print()
    
    # Step 2: Test API connectivity
    print("Step 2: Testing API Connectivity")
    print("--------------------------------")
    if test_api():
        print("✓ API test successful!")
    else:
        print("✗ API test failed!")
        return
    
    # Step 3: Load a test location
    print("\nStep 3: Loading Test Location")
    print("----------------------------")
    try:
        manager = LocationManager()
        location = manager.get_test_tweet(index=0)  # Get first location
        print("✓ Successfully loaded test location")
        print(f"\nLocation Tweet Format:\n{location}")
    except Exception as e:
        print(f"✗ Failed to load test location: {str(e)}")
        return

if __name__ == "__main__":
    main()
