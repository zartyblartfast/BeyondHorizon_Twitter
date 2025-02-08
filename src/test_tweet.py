from location_manager import LocationManager
from twitter_client import TwitterClient
import json
import logging
import argparse
import textwrap
import random

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

def find_preset_by_name(locations, name=None):
    """Find a preset by its name or get the first preset if no name provided"""
    presets = locations['presets']
    preset_names = [p['name'] for p in presets]
    print(f"\nAvailable presets:")
    for i, preset_name in enumerate(preset_names, 1):
        print(f"{i}. {preset_name}")
    
    # If no name provided, use first preset
    if name is None:
        first_preset = presets[0]
        print(f"\nUsing first preset: {first_preset['name']}")
        return first_preset
    
    # Otherwise find by name
    print(f"\nLooking for preset: {name}")
    for preset in presets:
        if preset['name'] == name:
            print("\nFound preset!")
            return preset
    return None

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Test tweet generation and posting with various parameters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
            Examples:
              # Dry run with first preset
              python test_tweet.py --dry-run
              
              # Post specific preset
              python test_tweet.py --preset "Mount Everest to Kanchenjunga"
              
              # List all available presets
              python test_tweet.py --list-presets
              
              # Test with custom refraction (Note: Requires Azure Functions API)
              python test_tweet.py --dry-run --preset "K2 to Broad Peak" --refraction 1.15
              
            Note:
              The --refraction parameter is prepared for future integration with the
              Azure Functions calculation API. Currently, it only affects the display
              value and does not recalculate visibility conditions.
        ''')
    )
    
    # Test control arguments
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show tweet content without posting')
    parser.add_argument('--list-presets', action='store_true',
                       help='List all available presets and exit')
    
    # Content selection arguments
    parser.add_argument('--preset', 
                       help='Name of preset to use (default: first preset)')
    parser.add_argument('--random', action='store_true',
                       help='Use a random preset')
    
    # Tweet customization arguments
    parser.add_argument('--refraction', type=float,
                       help='Override refraction value (e.g., 1.15). Note: Requires Azure Functions API for full functionality')
    parser.add_argument('--no-images', action='store_true',
                       help='Skip image attachments')
    parser.add_argument('--format', choices=['normal', 'compact', 'detailed'],
                       default='normal',
                       help='Tweet format style (default: normal)')
    
    args = parser.parse_args()

    # Initialize managers
    location_manager = LocationManager()
    twitter_client = TwitterClient()
    
    # Get all locations
    locations = location_manager.get_all_locations()
    
    # Handle --list-presets
    if args.list_presets:
        print("\nAvailable presets:")
        for i, preset in enumerate(locations['presets'], 1):
            print(f"{i}. {preset['name']}")
            print(f"   Distance: {preset['distance']}km")
            print(f"   Countries: {preset['details']['location']['observer']['country']} → "
                  f"{preset['details']['location']['target']['country']}\n")
        return
    
    # Select preset based on arguments
    if args.random:
        location = random.choice(locations['presets'])
        print(f"\nRandomly selected preset: {location['name']}")
    elif args.preset:
        print(f"DEBUG: args.preset value: {args.preset}")
        print(f"DEBUG: Type of args.preset: {type(args.preset)}")
        location = find_preset_by_name(locations, args.preset)
        if not location:
            print(f"Could not find preset: {args.preset}")
            return
    else:
        location = locations['presets'][0]
        print(f"\nUsing first preset: {location['name']}")
    
    # Apply any overrides
    if args.refraction:
        print("\nNote: Refraction override is currently for display only.")
        print("Full recalculation will be available when Azure Functions API is implemented.")
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
        return
        
    # Post the tweet
    print("\nPosting tweet...")
    tweet_id = twitter_client.post_tweet(tweet_content, image_urls)
    
    if tweet_id:
        print("\nTweet Posted Successfully!")
        print(f"Tweet URL: https://twitter.com/user/status/{tweet_id}")
    else:
        print("\nFailed to post tweet.")

if __name__ == "__main__":
    main()
