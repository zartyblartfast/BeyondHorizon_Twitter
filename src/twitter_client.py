"""
Twitter integration module for posting Long Line of Sight tweets.
"""
import os
import io
import requests
from typing import Optional, List
import tweepy
from dotenv import load_dotenv
from pathlib import Path
import datetime
import time

class TwitterClient:
    def __init__(self):
        """Initialize Twitter client with API credentials from environment variables."""
        # Get the project root directory (parent of src)
        project_root = Path(__file__).parent.parent
        env_path = project_root / 'config' / '.env'
        
        # Load environment variables from .env file
        load_dotenv(env_path)
        
        # Get Twitter credentials
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("Twitter API credentials not found in environment variables")
        
        # Initialize Twitter client with v2 API
        self.client = tweepy.Client(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )
        
        # Track last tweet time for rate limiting
        self.last_tweet_time = None

    def _check_rate_limit(self):
        """Check if we need to wait before tweeting again"""
        if self.last_tweet_time:
            elapsed = datetime.datetime.now() - self.last_tweet_time
            if elapsed.total_seconds() < 180:  # 3 minutes
                wait_time = 180 - elapsed.total_seconds()
                print(f"\nRate limit: Waiting {wait_time:.0f} seconds before posting...")
                time.sleep(wait_time)

    def post_tweet(self, content: str, image_urls: List[str] = None) -> Optional[str]:
        """
        Post a tweet with content and optional images.
        
        Args:
            content (str): The tweet content to post
            image_urls (list): Optional list of image URLs to attach
            
        Returns:
            Optional[str]: The ID of the posted tweet if successful, None otherwise
        """
        try:
            # Check rate limit
            self._check_rate_limit()
            
            # If we have images, upload them first
            media_ids = []
            if image_urls:
                auth = tweepy.OAuth1UserHandler(
                    self.api_key, self.api_secret,
                    self.access_token, self.access_token_secret
                )
                api = tweepy.API(auth)
                
                for url in image_urls[:4]:  # Twitter allows max 4 images
                    # Download image to temporary file
                    response = requests.get(url)
                    if response.status_code == 200:
                        # Upload to Twitter
                        media = api.media_upload(filename=None, file=io.BytesIO(response.content))
                        media_ids.append(media.media_id)

            # Post tweet with media if we have any
            response = self.client.create_tweet(
                text=content,
                media_ids=media_ids if media_ids else None
            )
            
            # Update last tweet time
            self.last_tweet_time = datetime.datetime.now()
            
            return str(response.data['id'])
        except Exception as e:
            print(f"\nError posting tweet: {str(e)}")
            if "429" in str(e):
                print("Too Many Requests - Please wait a few minutes before trying again")
            return None
