"""
Test script for OpenAI and Twitter integration
"""
from openai_client import OpenAIClient
from twitter_client import TwitterClient

def test_tweet_generation_and_posting():
    """Test tweet generation and posting with sample data"""
    # Sample location data
    location_data = {
        'observer_location': 'Fort Niagara State Park, NY',
        'target_location': 'Toronto, Canada',
        'distance': '31 miles across Lake Ontario',
        'elevation_gain': '0 feet (both at lake level)',
        'weather_conditions': 'Best visibility on clear, cold winter days'
    }
    
    try:
        # Initialize clients
        openai_client = OpenAIClient()
        twitter_client = TwitterClient()
        
        # Generate tweet
        tweet_content = openai_client.generate_tweet_content(location_data)
        
        if tweet_content:
            print("\nGenerated Tweet:")
            print("-" * 50)
            print(tweet_content)
            print("-" * 50)
            print(f"Character count: {len(tweet_content)}")
            
            # Post to Twitter
            tweet_id = twitter_client.post_tweet(tweet_content)
            if tweet_id:
                print(f"\nSuccessfully posted tweet! ID: {tweet_id}")
            else:
                print("\nFailed to post tweet")
        else:
            print("Failed to generate tweet content")
            
    except Exception as e:
        print(f"Error during test: {str(e)}")

if __name__ == "__main__":
    test_tweet_generation_and_posting()
