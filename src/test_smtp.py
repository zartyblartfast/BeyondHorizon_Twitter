"""
Email Test Script using PythonAnywhere API
This script tests sending email using PythonAnywhere's API.
"""
import os
import requests
from dotenv import load_dotenv

def test_email():
    print("\n=== Environment Debug Info ===")
    
    # Load environment variables
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(os.path.dirname(script_dir), 'config', '.env')
    print(f"\n1. Loading .env from: {env_path}")
    print(f"File exists: {os.path.exists(env_path)}")
    
    load_dotenv(env_path)
    
    # Get configuration
    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')
    pa_token = os.getenv('PA_API_TOKEN')

    print("\n=== Configuration ===")
    print(f"FROM_EMAIL: {from_email}")
    print(f"TO_EMAIL: {to_email}")
    print(f"PA_API_TOKEN set: {'Yes' if pa_token else 'No'}")

    if not all([from_email, to_email, pa_token]):
        print("\nError: Missing required environment variables.")
        print("Make sure FROM_EMAIL, TO_EMAIL, and PA_API_TOKEN are set in .env")
        return

    # PythonAnywhere API endpoint
    api_url = "https://www.pythonanywhere.com/api/v0/user/{username}/emails/"
    username = "BeyondHorizon"  # Your PythonAnywhere username

    # Headers for authentication
    headers = {'Authorization': f'Token {pa_token}'}

    # Email content
    data = {
        'subject': 'Test Email via PythonAnywhere API',
        'to': to_email,
        'from': from_email,
        'text': 'This is a test email sent using the PythonAnywhere API.'
    }

    try:
        print("\n=== Sending Email ===")
        print("1. Making API request...")
        
        response = requests.post(
            api_url.format(username=username),
            headers=headers,
            json=data
        )
        
        if response.status_code == 201:
            print("\nSuccess! Email sent successfully.")
        else:
            print(f"\nError: API request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    test_email()
