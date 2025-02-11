"""Manages preset selection and tweet recording"""
from location_manager import LocationManager
from tweet_db import TweetDB
import datetime
import logging

logger = logging.getLogger(__name__)

class PresetManager:
    def __init__(self, db_path):
        """Initialize with database path"""
        logger.info(f"Initializing PresetManager with database: {db_path}")
        self.db = TweetDB(db_path)
        self.location_manager = LocationManager()
        
    def get_next_preset(self, dry_run=False):
        """Get the next preset to post, considering history"""
        all_presets = self.location_manager.get_all_locations()['presets']
        
        # Get all successful tweets in order of most recent first
        query = """
            SELECT preset_name 
            FROM tweet_history 
            WHERE status = 'success'
            ORDER BY posted_at DESC
        """
        logger.info("Executing query to retrieve successful tweets")
        try:
            used_presets = [row[0] for row in self.db.execute_query(query)]
            logger.info("Successfully retrieved successful tweets")
        except Exception as e:
            logger.error(f"Failed to retrieve successful tweets: {str(e)}")
            return None
        
        # Find first preset not in recent history
        for preset in all_presets:
            if preset['name'] not in used_presets:
                return preset
                
        # If all presets used, start over with least recently used
        query = """
            SELECT preset_name 
            FROM tweet_history 
            WHERE status = 'success'
            ORDER BY posted_at ASC 
            LIMIT 1
        """
        logger.info("Executing query to retrieve oldest successful tweet")
        try:
            result = self.db.execute_query(query)
            logger.info("Successfully retrieved oldest successful tweet")
        except Exception as e:
            logger.error(f"Failed to retrieve oldest successful tweet: {str(e)}")
            return None
        
        oldest_preset = result[0][0] if result else None
        
        # Find the preset after the oldest one
        if oldest_preset:
            for i, preset in enumerate(all_presets):
                if preset['name'] == oldest_preset:
                    return all_presets[(i + 1) % len(all_presets)]
        
        # If no history at all, start from beginning
        return all_presets[0]
    
    def record_tweet_result(self, preset_name, tweet_id, tweet_text, success=True, error_message=None):
        """Record the result of a tweet attempt"""
        status = 'success' if success else 'error'
        logger.info(f"Recording tweet result - Preset: {preset_name}, Status: {status}")
        try:
            self.db.record_tweet(
                preset_name=preset_name,
                tweet_id=tweet_id or 'none',
                tweet_text=tweet_text,
                status=status,
                error_message=error_message
            )
            logger.info("Successfully recorded tweet to database")
        except Exception as e:
            logger.error(f"Failed to record tweet to database: {str(e)}")
        
    def find_preset_by_name(self, name):
        """Find a specific preset by name"""
        all_presets = self.location_manager.get_all_locations()['presets']
        for preset in all_presets:
            if preset['name'] == name:
                return preset
        return None
