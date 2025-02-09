"""
SMTP Connection Test Script for PythonAnywhere
This script tests SMTP connection using PythonAnywhere's mail server.
"""
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

def test_smtp_connection():
    print("\n=== Environment Debug Info ===")
    
    # Check raw env variables before loading .env
    print("\n1. Before loading .env:")
    email_vars = {k: v for k, v in os.environ.items() if 'EMAIL' in k.upper()}
    print(f"Email-related env vars: {email_vars}")
    
    # Load environment variables
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(os.path.dirname(script_dir), 'config', '.env')
    print(f"\n2. Loading .env from: {env_path}")
    print(f"File exists: {os.path.exists(env_path)}")
    
    load_dotenv(env_path)
    
    # Check env variables after loading .env
    print("\n3. After loading .env:")
    email_vars = {k: v for k, v in os.environ.items() if 'EMAIL' in k.upper()}
    print(f"Email-related env vars: {email_vars}")
    
    # Get credentials from environment
    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')
    app_password = os.getenv('EMAIL_PASSWORD')

    print("\n=== Configuration ===")
    print(f"FROM_EMAIL: {from_email}")
    print(f"TO_EMAIL: {to_email}")
    print(f"EMAIL_PASSWORD set: {'Yes' if app_password else 'No'}")
    if app_password:
        print(f"EMAIL_PASSWORD length: {len(app_password)}")

    # Create a simple test message
    msg = MIMEMultipart()
    msg['Subject'] = 'PythonAnywhere SMTP Test Email'
    msg['From'] = from_email
    msg['To'] = to_email
    msg.attach(MIMEText('This is a test email using PythonAnywhere\'s SMTP server.', 'plain'))

    # PythonAnywhere SMTP settings
    smtp_server = "smtp.pythonanywhere.com"
    smtp_port = 587

    try:
        print("\n=== SMTP Connection Test ===")
        print(f"1. Connecting to {smtp_server}:{smtp_port}")
        
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.set_debuglevel(1)  # Reduced debug level
        
        print("2. Starting TLS...")
        smtp.starttls(context=ssl.create_default_context())
        
        print("3. Attempting login...")
        if not app_password:
            raise ValueError("EMAIL_PASSWORD not found in .env file")
        
        smtp.login(from_email, app_password)
        print("Login successful!")
        
        print("4. Sending test email...")
        smtp.send_message(msg)
        print("Email sent successfully!")
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\nAuthentication Error: {str(e)}")
        print("This usually means:")
        print("1. The password is incorrect")
        print("2. Make sure you're using your Yahoo account password (not an app password)")
        
    except ValueError as e:
        print(f"\nConfiguration Error: {str(e)}")
        
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
