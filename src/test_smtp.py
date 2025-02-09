"""
Email Test Script using MailerSend
"""
import os
from mailersend import emails
from dotenv import load_dotenv, dotenv_values

def test_email():
    print("\n=== Environment Debug Info ===")
    
    # Load environment variables
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(os.path.dirname(script_dir), 'config', '.env')
    print(f"\n1. Loading .env from: {env_path}")
    print(f"File exists: {os.path.exists(env_path)}")
    
    # Print raw file contents for debugging
    print("\n2. Raw .env file contents:")
    try:
        with open(env_path, 'r') as f:
            print(f.read())
    except Exception as e:
        print(f"Error reading .env file: {e}")
    
    print("\n3. Loading environment variables...")
    # Try both methods of loading env vars
    config = dotenv_values(env_path)
    load_dotenv(env_path)
    
    # Get configuration (try both env and config)
    from_email = os.getenv('FROM_EMAIL') or config.get('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL') or config.get('TO_EMAIL')
    api_key = os.getenv('MAILERSEND_API_KEY') or config.get('MAILERSEND_API_KEY')

    print("\n=== Configuration ===")
    print(f"FROM_EMAIL: {from_email}")
    print(f"TO_EMAIL: {to_email}")
    print(f"MAILERSEND_API_KEY: {'[HIDDEN]' if api_key else 'Not set'}")
    
    # Print all loaded values from .env
    print("\nLoaded .env values:")
    for key, value in config.items():
        if 'KEY' in key or 'TOKEN' in key or 'SECRET' in key:
            print(f"{key}: [HIDDEN]")
        else:
            print(f"{key}: {value}")

    if not all([from_email, to_email, api_key]):
        print("\nError: Missing required environment variables.")
        print("Make sure FROM_EMAIL, TO_EMAIL, and MAILERSEND_API_KEY are set in .env")
        return

    try:
        print("\n=== Sending Email ===")
        print("1. Setting up MailerSend client...")
        
        # Initialize mailer object
        mailer = emails.NewEmail(api_key)

        # Prepare email data
        recipients = [{"email": to_email}]
        mail_from = {
            "email": from_email,
            "name": "BeyondHorizon Bot"
        }

        print("2. Sending email...")
        # Send email
        response = mailer.send({
            "from": mail_from,
            "to": recipients,
            "subject": "Test Email from MailerSend",
            "text": "This is a test email sent using MailerSend.",
            "html": "<p>This is a test email sent using MailerSend.</p>"
        })

        if response.status_code == 202:
            print("\nSuccess! Email sent successfully.")
            print(f"Message ID: {response.headers.get('x-message-id')}")
        else:
            print(f"\nError: Failed to send email. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    test_email()
