"""
Email Test Script using MailerSend
"""
import os
from mailersend import emails
import json

def read_env_file(path):
    """Read environment variables directly from file."""
    env_vars = {}
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Split on first = only
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove inline comments (anything after #)
                        if '#' in value:
                            value = value.split('#')[0].strip()
                        env_vars[key] = value
    except Exception as e:
        print(f"Error reading env file: {e}")
    return env_vars

def test_email():
    print("\n=== Environment Debug Info ===")
    
    # Load environment variables
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(os.path.dirname(script_dir), 'config', '.env')
    print(f"\n1. Loading .env from: {env_path}")
    print(f"File exists: {os.path.exists(env_path)}")
    print(f"Absolute path: {os.path.abspath(env_path)}")
    
    # Print raw file contents for debugging
    print("\n2. Raw .env file contents:")
    try:
        with open(env_path, 'r') as f:
            print(f.read())
    except Exception as e:
        print(f"Error reading .env file: {e}")
    
    print("\n3. Loading environment variables directly...")
    env_vars = read_env_file(env_path)
    
    # Get configuration
    from_email = env_vars.get('FROM_EMAIL')
    to_email = env_vars.get('TO_EMAIL')
    api_key = env_vars.get('MAILERSEND_API_KEY')

    print("\n=== Configuration ===")
    print(f"FROM_EMAIL: {from_email}")
    print(f"TO_EMAIL: {to_email}")
    print(f"MAILERSEND_API_KEY: {'[HIDDEN]' if api_key else 'Not set'}")
    
    # Print all loaded values
    print("\nLoaded .env values:")
    for key, value in sorted(env_vars.items()):
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
        mail_body = {
            "from": mail_from,
            "to": recipients,
            "subject": "Test Email from MailerSend",
            "text": "This is a test email sent using MailerSend.",
            "html": "<p>This is a test email sent using MailerSend.</p>"
        }
        
        print("Email data:", json.dumps(mail_body, indent=2))
        response = mailer.send(mail_body)
        
        print("\nAPI Response:", response)
        if isinstance(response, str):
            try:
                response_data = json.loads(response)
                if response_data.get('status', '') == 'success':
                    print("\nSuccess! Email sent successfully.")
                    print(f"Response data: {json.dumps(response_data, indent=2)}")
                else:
                    print(f"\nError: Failed to send email.")
                    print(f"Response: {json.dumps(response_data, indent=2)}")
            except json.JSONDecodeError:
                print(f"\nError: Unexpected response format")
                print(f"Response: {response}")
        else:
            # Handle response object
            if hasattr(response, 'status_code'):
                if response.status_code == 202:
                    print("\nSuccess! Email sent successfully.")
                    print(f"Message ID: {response.headers.get('x-message-id')}")
                else:
                    print(f"\nError: Failed to send email. Status code: {response.status_code}")
                    print(f"Response: {response.text}")
            else:
                print(f"\nError: Unexpected response type: {type(response)}")
                print(f"Response: {response}")
            
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        if hasattr(e, '__dict__'):
            print(f"Error details: {e.__dict__}")

if __name__ == "__main__":
    test_email()
