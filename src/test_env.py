import os
from dotenv import load_dotenv

print("1. Testing direct file read:")
try:
    with open('config/.env', 'r') as f:
        content = f.read()
        print(content)
        # Check if PA_API_TOKEN is in the content
        print("\nIs PA_API_TOKEN in file?", 'PA_API_TOKEN' in content)
except Exception as e:
    print(f"Error reading file: {str(e)}")

print("\n2. Testing dotenv load:")
try:
    # Get absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(os.path.dirname(script_dir), 'config', '.env')
    print(f"Env path: {env_path}")
    print(f"File exists: {os.path.exists(env_path)}")
    
    result = load_dotenv(env_path)
    print(f"load_dotenv result: {result}")
    
    token = os.getenv('PA_API_TOKEN')
    print(f"Token from dotenv: {token}")
    
    # Print all environment variables that start with PA_
    print("\nAll PA_ environment variables:")
    for key, value in os.environ.items():
        if key.startswith('PA_'):
            print(f"{key}: {value}")
except Exception as e:
    print(f"Error loading dotenv: {str(e)}")

print("\n3. Testing direct environ:")
print(f"Token from environ: {os.environ.get('PA_API_TOKEN')}")
