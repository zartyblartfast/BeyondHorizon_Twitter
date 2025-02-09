import os
from dotenv import load_dotenv

print("1. Testing direct file read:")
try:
    with open('config/.env', 'r') as f:
        print(f.read())
except Exception as e:
    print(f"Error reading file: {str(e)}")

print("\n2. Testing dotenv load:")
try:
    load_dotenv('config/.env')
    token = os.getenv('PA_API_TOKEN')
    print(f"Token from dotenv: {token}")
except Exception as e:
    print(f"Error loading dotenv: {str(e)}")

print("\n3. Testing direct environ:")
print(f"Token from environ: {os.environ.get('PA_API_TOKEN')}")
