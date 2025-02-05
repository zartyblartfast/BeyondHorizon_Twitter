"""
Twitter integration module for posting Long Line of Sight tweets.
"""
import os
from typing import Optional
import tweepy
from dotenv import load_dotenv
from pathlib import Path

class TwitterClient:
    def __init__(self):
        """Initialize Twitter client with API credentials from environment variables."""
        # Get the project root directory (parent of src)
        project_root = Path(__file__).parent.parent
        env_path = project_root / 'config' / '.env'
        
        # Load environment variables from .env file
        load_dotenv(env_path)
        
        # Get Twitter credentials
        api_key = os.getenv('TWITTER_API_KEY')
        api_secret = os.getenv('TWITTER_API_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        if not all([api_key, api_secret, access_token, access_token_secret]):
            raise ValueError("Twitter API credentials not found in environment variables")
        
        # Initialize Twitter client with v2 API
        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

    def post_tweet(self, content: str) -> Optional[str]:
        """
        Post a tweet with the given content using Twitter API v2.
        
        Args:
            content (str): The tweet content to post
            
        Returns:
            Optional[str]: The ID of the posted tweet if successful, None otherwise
        """
        try:
            response = self.client.create_tweet(text=content)
            return str(response.data['id'])
        except Exception as e:
            print(f"Error posting tweet: {str(e)}")
            return None
