"""
Gmail SMTP Connection Test Script
This script tests Gmail SMTP connection with verbose debugging enabled.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

def test_smtp_connection():
    # Load environment variables
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(os.path.dirname(script_dir), 'config', '.env')
    print(f"\nDebug: Looking for .env file at: {env_path}")
    load_dotenv(env_path)

    # Get credentials from environment
    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')
    app_password = os.getenv('EMAIL_PASSWORD')

    # Print debug info (without showing the full password)
    print("\nConfiguration:")
    print(f"From Email: {from_email}")
    print(f"To Email: {to_email}")
    print(f"App Password Set: {'Yes' if app_password else 'No'}")
    print(f"App Password Length: {len(app_password) if app_password else 0}")

    # Create a simple test message
    msg = MIMEMultipart()
    msg['Subject'] = 'SMTP Test Email'
    msg['From'] = from_email
    msg['To'] = to_email
    msg.attach(MIMEText('This is a test email to verify SMTP connection.', 'plain'))

    # Gmail SMTP settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        print("\nStarting SMTP connection test...")
        print(f"1. Creating SMTP connection to {smtp_server}:{smtp_port}")
        
        # Enable debug mode
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.set_debuglevel(2)  # Enable verbose debugging
        
        print("\n2. Starting TLS...")
        smtp.starttls()
        
        print("\n3. Attempting login...")
        smtp.login(from_email, app_password)
        
        print("\n4. Sending test email...")
        smtp.send_message(msg)
        
        print("\nSuccess! SMTP connection and authentication working correctly.")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        if hasattr(e, 'smtp_code'):
            print(f"SMTP Code: {e.smtp_code}")
        if hasattr(e, 'smtp_error'):
            print(f"SMTP Error: {e.smtp_error}")
    finally:
        try:
            print("\nClosing SMTP connection...")
            smtp.quit()
        except:
            pass

if __name__ == "__main__":
    test_smtp_connection()
