"""
BeyondHorizon Tweet Manager

This script manages the automated tweeting system for BeyondHorizon:
- Posts tweets with preset content and images
- Manages tweet history in a SQLite database
- Sends email reports after each tweet
- Provides testing and dry-run capabilities

Usage:
    Regular tweet posting:
    python tweet_manager.py

    Test without posting:
    python tweet_manager.py --dry-run

    Just send email report:
    python tweet_manager.py --email-report

    List available presets:
    python tweet_manager.py --list-presets

    Show tweet history:
    python tweet_manager.py --show-history

Environment Variables Required:
    - Twitter API credentials in .env
    - Email settings in .env
"""
from location_manager import LocationManager
from twitter_client import TwitterClient
from preset_manager import PresetManager
from report_manager import ReportManager
import json
import logging
import argparse
import textwrap
import random
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Configure logging with a cleaner format
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # Only show the message, no timestamps or levels
)
logger = logging.getLogger(__name__)

def wrap_url(url, width=70):
    """Wrap a long URL for display"""
    return '\n'.join(textwrap.wrap(url, width=width))

def preview_tweet(tweet_content, image_urls=None):
    """Display a preview of the tweet content"""
    print("\nTEXT CONTENT:")
    print("-" * 70)
    # Use sys.stdout.buffer.write to handle Unicode characters
    import sys
    sys.stdout.buffer.write(textwrap.fill(tweet_content.strip(), width=70).encode('utf-8'))
    sys.stdout.buffer.write(b'\n')
    
    if image_urls:
        print("\nIMAGE URLS:")
        print("-" * 70)
        for url in image_urls:
            print(url)

def get_db_path():
    """Get database path based on environment"""
    load_dotenv()
    env = os.getenv('ENVIRONMENT', 'development')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_name = f"tweet_history_{env}.db"
    return os.path.join(base_dir, 'data', db_name)

def send_email_report(report_content):
    """Send an email with the tweet history report."""
    # Get absolute path to .env file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(os.path.dirname(script_dir), 'config', '.env')
    print(f"\nDebug: Script directory: {script_dir}")
    print(f"Debug: Looking for .env file at: {env_path}")
    print(f"Debug: .env file exists: {os.path.exists(env_path)}")
    
    # Load environment variables
    load_dotenv(env_path)
    
    # Get email configuration from environment
    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    
    # Debug logging
    print("\nDebug: Environment variables:")
    print(f"FROM_EMAIL: {from_email}")
    print(f"TO_EMAIL: {to_email}")
    print(f"SENDGRID_API_KEY: {'Set' if sendgrid_api_key else 'Not set'}")
    print(f"PYTHONANYWHERE_SITE: {'Set' if 'PYTHONANYWHERE_SITE' in os.environ else 'Not set'}")
    
    # Create email subject
    subject = f'BeyondHorizon Tweet Report - {datetime.now().strftime("%Y-%m-%d %H:%M")}'
    
    # Convert the report to HTML format
    html_content = f"""
    <html>
        <head>
            <style>
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h2>BeyondHorizon Tweet History Report</h2>
            <pre>{report_content}</pre>
        </body>
    </html>
    """
    
    try:
        # For local testing, just print the email
        if 'PYTHONANYWHERE_SITE' not in os.environ:
            print("\nEmail would be sent with following content:")
            print(f"From: {from_email}")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print("\nContent:")
            print(html_content)
        else:
            # On PythonAnywhere, use SendGrid API
            try:
                import requests
                
                # SendGrid API endpoint
                url = 'https://api.sendgrid.com/v3/mail/send'
                headers = {
                    'Authorization': f'Bearer {sendgrid_api_key}',
                    'Content-Type': 'application/json'
                }
                
                # Prepare email data
                data = {
                    'personalizations': [{
                        'to': [{'email': to_email}]
                    }],
                    'from': {'email': from_email},
                    'subject': subject,
                    'content': [{
                        'type': 'text/html',
                        'value': html_content
                    }]
                }
                
                print("\nDebug: Sending email via SendGrid API...")
                response = requests.post(url, headers=headers, json=data)
                print(f"SendGrid response status: {response.status_code}")
                
                if response.status_code >= 400:
                    print(f"SendGrid response text: {response.text}")
                    raise Exception(f"SendGrid API returned {response.status_code}")
                else:
                    print("Email sent successfully via SendGrid")
                    
            except ImportError as e:
                print(f"\nError importing requests: {str(e)}")
                raise
            except Exception as e:
                print(f"\nError sending via SendGrid: {str(e)}")
                raise
            
        print("\nEmail report handled successfully")
    except Exception as e:
        print(f"\nError handling email report: {str(e)}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='BeyondHorizon Tweet Manager - Posts tweets, manages history, and sends reports'
    )
    
    # Operation modes
    mode_group = parser.add_argument_group('Operation Modes')
    mode_group.add_argument('--dry-run', action='store_true', 
                          help='Show tweet content without posting')
    mode_group.add_argument('--email-report', action='store_true',
                          help='Just send the email report without posting')
    mode_group.add_argument('--list-presets', action='store_true',
                          help='List all available presets and exit')
    mode_group.add_argument('--show-history', action='store_true',
                          help='Show recent tweet history and exit')
    
    # Content selection
    content_group = parser.add_argument_group('Content Selection')
    content_group.add_argument('--preset', 
                             help='Use specific preset instead of next in sequence')
    content_group.add_argument('--random', action='store_true',
                             help='Use random preset')
    
    # Testing and maintenance
    test_group = parser.add_argument_group('Testing and Maintenance')
    test_group.add_argument('--test-record', action='store_true',
                          help='Record dry run to database (for testing only)')
    test_group.add_argument('--clear-history', action='store_true',
                          help='Clear all tweet history (for testing only)')
    
    # Tweet customization arguments
    parser.add_argument('--refraction', type=float,
                       help='Override refraction value (e.g., 1.15)')
    parser.add_argument('--no-images', action='store_true',
                       help='Skip image attachments')
    parser.add_argument('--format', choices=['normal', 'compact', 'detailed'],
                       default='normal',
                       help='Tweet format style (default: normal)')
    
    args = parser.parse_args()

    # Initialize managers
    location_manager = LocationManager()
    twitter_client = TwitterClient()
    preset_manager = PresetManager(get_db_path())
    report_manager = ReportManager(get_db_path())
    
    # Clear history if requested
    if args.clear_history:
        db_path = get_db_path()
        if os.path.exists(db_path):
            # Close any existing connections
            preset_manager = None
            report_manager = None
            import gc
            gc.collect()  # Force garbage collection to close connections
            
            try:
                os.remove(db_path)
                print(f"\nCleared tweet history database: {db_path}")
            except Exception as e:
                print(f"\nError clearing database: {str(e)}")
        else:
            print("\nNo history database found to clear")
        return
        
    # Show history if requested
    if args.show_history:
        print(report_manager.generate_report())
        return
    
    # Just show email report if requested
    if args.email_report:
        print("\nGenerating email report...")
        report = report_manager.generate_report()
        print("\nAttempting to send email report...")
        send_email_report(report)
        return
    
    # Get all locations for listing
    locations = location_manager.get_all_locations()
    
    # Handle --list-presets
    if args.list_presets:
        print("\nAvailable presets:")
        for i, preset in enumerate(locations['presets'], 1):
            print(f"{i}. {preset['name']}")
            print(f"   Distance: {preset['distance']}km")
            print(f"   Countries: {preset['details']['location']['observer']['country']} to "
                  f"{preset['details']['location']['target']['country']}\n")
        return
    
    # Select preset based on arguments
    if args.random:
        location = random.choice(locations['presets'])
        print(f"\nRandomly selected preset: {location['name']}")
    elif args.preset:
        location = preset_manager.find_preset_by_name(args.preset)
        if not location:
            print(f"Could not find preset: {args.preset}")
            return
    else:
        location = preset_manager.get_next_preset(dry_run=args.dry_run)
        print(f"\nNext preset in sequence: {location['name']}")
    
    # Apply any overrides
    if args.refraction:
        print("\nNote: Refraction override is currently for display only.")
        location['refractionFactor'] = args.refraction
        print(f"Overriding refraction factor to: {args.refraction}")
    
    # Format tweet based on style
    tweet_content = location_manager.format_tweet(location)
    
    # Get images unless --no-images is specified
    image_urls = None if args.no_images else location_manager.get_image_urls(location)
    
    # Show preview
    preview_tweet(tweet_content, image_urls)
    
    if args.dry_run:
        print("\nDRY RUN - Tweet not posted")
        if args.test_record:
            print("\nTEST MODE - Recording to database")
            preset_manager.record_tweet_result(
                preset_name=location['name'],
                tweet_id='dry-run-test',
                tweet_text=tweet_content,
                success=True
            )
            print("Recorded test entry to database")
        return
        
    try:
        # Post the tweet
        print("\nPosting tweet...")
        tweet_id = twitter_client.post_tweet(tweet_content, image_urls)
        if tweet_id:
            # Record successful tweet
            preset_manager.record_tweet_result(
                preset_name=location['name'],
                tweet_id=tweet_id,
                tweet_text=tweet_content,
                success=True
            )
            print("\nTweet Posted Successfully!")
            print(f"Tweet URL: https://twitter.com/user/status/{tweet_id}")
        else:
            # Record failed tweet
            preset_manager.record_tweet_result(
                preset_name=location['name'],
                tweet_id=None,
                tweet_text=tweet_content,
                success=False,
                error_message='No tweet ID returned'
            )
            print("\nFailed to post tweet.")
    except Exception as e:
        # Record error
        preset_manager.record_tweet_result(
            preset_name=location['name'],
            tweet_id=None,
            tweet_text=tweet_content,
            success=False,
            error_message=str(e)
        )
        print(f"\nError posting tweet: {str(e)}")

    # After successful tweet or dry run, send email report if not in test mode
    print("\nGenerating email report...")
    report = report_manager.generate_report()
    if not args.test_record:  # Don't send emails during testing
        print("\nAttempting to send email report...")
        send_email_report(report)

if __name__ == "__main__":
    main()
