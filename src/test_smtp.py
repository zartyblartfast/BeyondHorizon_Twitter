"""
Email Test Script using PythonAnywhere's mail module
"""
import os
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

    print("\n=== Configuration ===")
    print(f"FROM_EMAIL: {from_email}")
    print(f"TO_EMAIL: {to_email}")

    if not all([from_email, to_email]):
        print("\nError: Missing required environment variables.")
        print("Make sure FROM_EMAIL and TO_EMAIL are set in .env")
        return

    try:
        print("\n=== Sending Email ===")
        print("1. Importing mail module...")
        
        # Import PythonAnywhere's mail module
        from pythonanywhere.mail import Mailer
        
        print("2. Creating mailer...")
        mailer = Mailer()
        
        print("3. Sending email...")
        mailer.send(
            to_email,
            subject="Test Email from PythonAnywhere",
            text="This is a test email sent using PythonAnywhere's mail module.",
            from_email=from_email
        )
        
        print("\nSuccess! Email sent successfully.")
            
    except ImportError:
        print("\nError: Could not import pythonanywhere.mail module.")
        print("This script must be run on PythonAnywhere's servers.")
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    test_email()
