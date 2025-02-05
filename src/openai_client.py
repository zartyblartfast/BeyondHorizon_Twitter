"""
OpenAI integration module for generating tweet content about Long Line of Sight views.
"""
import os
from typing import Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

class OpenAIClient:
    def __init__(self):
        """Initialize OpenAI client with API key from environment variables."""
        # Get the project root directory (parent of src)
        project_root = Path(__file__).parent.parent
        env_path = project_root / 'config' / '.env'
        
        # Load environment variables from .env file
        load_dotenv(env_path)
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)

    def generate_tweet_content(self, location_data: Dict[str, str]) -> str:
        """
        Generate a tweet about a Long Line of Sight view using GPT-4.
        
        Args:
            location_data (Dict[str, str]): Dictionary containing location information
                Required keys: 'observer_location', 'target_location', 'distance'
                Optional keys: 'elevation_gain', 'weather_conditions'
        
        Returns:
            str: Generated tweet content
        """
        try:
            # Construct the prompt for GPT-4
            prompt = self._construct_prompt(location_data)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable guide sharing fascinating information about long-distance views and geographic features. Keep responses within Twitter's character limit."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,  # Limit to ensure we stay within Twitter's character limit
                temperature=0.7  # Balance between creativity and consistency
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating tweet content: {str(e)}")
            return None

    def _construct_prompt(self, location_data: Dict[str, str]) -> str:
        """
        Construct a prompt for GPT-4 based on location data.
        
        Args:
            location_data (Dict[str, str]): Dictionary containing location information
        
        Returns:
            str: Constructed prompt
        """
        base_prompt = f"Create an engaging tweet about the long-distance view from {location_data['observer_location']} to {location_data['target_location']}, which are {location_data['distance']} apart."
        
        # Add optional information if available
        if 'elevation_gain' in location_data:
            base_prompt += f" The elevation difference is {location_data['elevation_gain']}."
        
        if 'weather_conditions' in location_data:
            base_prompt += f" Typical viewing conditions: {location_data['weather_conditions']}."
        
        base_prompt += " Include relevant hashtags. Keep the tweet engaging and informative while staying within character limit."
        
        return base_prompt
