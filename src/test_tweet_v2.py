"""Test tweet generation and posting with database tracking"""
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
    env = os.getenv('ENVIRONMENT', 'development')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_name = f"tweet_history_{env}.db"
    return os.path.join(base_dir, 'data', db_name)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Test tweet generation and posting with various parameters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
            Examples:
              # Dry run with next preset in sequence
              python test_tweet_v2.py --dry-run
              
              # Post specific preset
              python test_tweet_v2.py --preset "Mount Everest to Kanchenjunga"
              
              # List all available presets
              python test_tweet_v2.py --list-presets
              
              # Show recent tweet history
              python test_tweet_v2.py --show-history
              
              # Test with custom refraction (Note: Requires Azure Functions API)
              python test_tweet_v2.py --dry-run --preset "K2 to Broad Peak" --refraction 1.15
        ''')
    )
    
    # Test control arguments
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show tweet content without posting')
    parser.add_argument('--list-presets', action='store_true',
                       help='List all available presets and exit')
    parser.add_argument('--show-history', action='store_true',
                       help='Show recent tweet history and exit')
    parser.add_argument('--test-record', action='store_true',
                       help='Record dry run to database (for testing only)')
    parser.add_argument('--clear-history', action='store_true',
                       help='Clear all tweet history (for testing only)')
    
    # Content selection arguments
    parser.add_argument('--preset', 
                       help='Name of preset to use (default: next in sequence)')
    parser.add_argument('--random', action='store_true',
                       help='Use a random preset')
    
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
        
    # Post the tweet
    print("\nPosting tweet...")
    try:
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

if __name__ == "__main__":
    main()
