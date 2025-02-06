from location_manager import LocationManager
from twitter_client import TwitterClient
import json
import logging
import argparse
import textwrap

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
    """Show a clean preview of the tweet content and images"""
    print("\n" + "="*70)
    print("TWEET PREVIEW".center(70))
    print("="*70 + "\n")
    
    print("TEXT CONTENT:")
    print("-"*70)
    print(textwrap.fill(tweet_content.strip(), width=70))
    print("-"*70 + "\n")
    
    if image_urls:
        print("IMAGES TO ATTACH:")
        print("-"*70)
        for i, url in enumerate(image_urls, 1):
            print(f"Image {i}:")
            print(wrap_url(url))
            print()
    else:
        print("No images to attach")
    
    print("="*70)

def find_preset_by_name(locations, name):
    """Find a preset by its name"""
    logger.info(f"Looking for preset: {name}")
    logger.info(f"Available presets: {[p['name'] for p in locations['presets']]}")
    
    for preset in locations['presets']:
        if preset['name'] == "Pic de Finstrelles to Pic Gaspard":
            logger.info("Found preset! Details:")
            logger.info(json.dumps(preset['details'], indent=2))
            return preset
    return None

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test tweet generation and posting')
    parser.add_argument('--dry-run', action='store_true', help='Show tweet content without posting')
    args = parser.parse_args()

    # Initialize managers
    location_manager = LocationManager()
    twitter_client = TwitterClient()
    
    # Get all locations and find Finstrelles-Gaspard preset
    locations = location_manager.get_all_locations()
    location = find_preset_by_name(locations, "Pic de Finstrelles to Pic Gaspard")
    
    if not location:
        print("Could not find Finstrelles-Gaspard preset!")
        return
        
    tweet_content = location_manager.format_tweet(location)
    image_urls = location_manager.get_image_urls(location)
    
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
