"""
Simple test script to verify Azure Functions LoS Calculator API functionality.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from calculator_client import CalculatorClient, CalculationInput

def main():
    # Load environment variables from config/.env
    env_path = Path(__file__).parent.parent / 'config' / '.env'
    print(f"\nLooking for .env at: {env_path}")
    print(f"File exists: {env_path.exists()}")
    
    load_dotenv(env_path)
    
    # Debug: Check if variables are loaded
    azure_url = os.getenv('AZURE_FUNCTION_URL')
    azure_key = os.getenv('AZURE_FUNCTION_KEY')
    print(f"\nAzure Function URL found: {'Yes' if azure_url else 'No'}")
    print(f"Azure Function Key found: {'Yes' if azure_key else 'No'}")
    
    # Create calculator client
    calculator = CalculatorClient()
    
    # Test data (using Pic de Finstrelles to Pic Gaspard as example)
    test_input = CalculationInput(
        observer_height=2826,  # Pic de Finstrelles height (meters)
        distance=443,         # Distance (kilometers)
        refraction=1.20,      # Very High refraction
        target_height=3883    # Pic Gaspard height (meters)
    )
    
    print("\nTesting LoS Calculator API...")
    print("-" * 50)
    print(f"Observer Height: {test_input.observer_height}m")
    print(f"Target Height: {test_input.target_height}m")
    print(f"Distance: {test_input.distance}km")
    print(f"Refraction: {test_input.refraction}")
    print("-" * 50)
    
    try:
        # Make API call
        results = calculator.calculate(test_input)
        
        # Print formatted results
        print("\nCalculation Results:")
        print("=" * 50)
        print(calculator.format_results(results, with_target=True))
        print("=" * 50)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPlease check:")
        print("1. AZURE_FUNCTION_URL is set in .env")
        print("2. AZURE_FUNCTION_KEY is set in .env")
        print("3. Azure Function is running and accessible")

if __name__ == "__main__":
    main()
