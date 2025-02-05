from location_manager import LocationManager
from twitter_client import TwitterClient

def main():
    # Initialize managers
    location_manager = LocationManager()
    twitter_client = TwitterClient()
    
    # Get and format tweet
    location_manager.get_all_locations()
    test_tweet = location_manager.get_test_tweet()
    
    print("\nTweet Content to be Posted:")
    print("-" * 50)
    print(test_tweet)
    print("-" * 50)
    
    # Post the tweet
    tweet_id = twitter_client.post_tweet(test_tweet)
    
    if tweet_id:
        print("\nTweet Posted Successfully!")
        print(f"Tweet URL: https://twitter.com/user/status/{tweet_id}")
    else:
        print("\nFailed to post tweet.")

if __name__ == "__main__":
    location_manager = LocationManager()
    twitter_client = TwitterClient()

    # Try second location (index 1)
    tweet_content = location_manager.get_test_tweet(1)
    
    print("\nTweet Content to be Posted:")
    print("-" * 50)
    print(tweet_content)
    print("-" * 50)

    try:
        tweet_id = twitter_client.post_tweet(tweet_content)
        if tweet_id:
            print(f"\nTweet Posted Successfully!")
            print(f"Tweet URL: https://twitter.com/user/status/{tweet_id}")
        else:
            print("\nFailed to post tweet.")
    except Exception as e:
        print(f"\nError posting tweet: {str(e)}")
        print("\nFailed to post tweet.")
