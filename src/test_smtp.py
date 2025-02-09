"""
Email Test Script using MailerSend
"""
import os
from mailersend import emails
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
    api_key = os.getenv('MAILERSEND_API_KEY')

    print("\n=== Configuration ===")
    print(f"FROM_EMAIL: {from_email}")
    print(f"TO_EMAIL: {to_email}")
    print(f"MAILERSEND_API_KEY set: {'Yes' if api_key else 'No'}")

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
