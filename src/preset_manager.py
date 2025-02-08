"""Manages preset selection and tweet recording"""
from location_manager import LocationManager
from tweet_db import TweetDB
import datetime

class PresetManager:
    def __init__(self, db_path):
        """Initialize with database path"""
        self.db = TweetDB(db_path)
        self.location_manager = LocationManager()
        
    def get_next_preset(self, dry_run=False):
        """Get the next preset to post, considering history"""
        all_presets = self.location_manager.get_all_locations()['presets']
        
        # Get recent history (last 30 days)
        query = """
            SELECT preset_name 
            FROM tweet_history 
            WHERE posted_at >= datetime('now', '-30 days')
            AND status = 'success'
            ORDER BY posted_at DESC
        """
        used_presets = [row[0] for row in self.db.execute_query(query)]
        
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
        result = self.db.execute_query(query)
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
        self.db.record_tweet(
            preset_name=preset_name,
            tweet_id=tweet_id or 'none',
            tweet_text=tweet_text,
            status=status,
            error_message=error_message
        )
        
    def find_preset_by_name(self, name):
        """Find a specific preset by name"""
        all_presets = self.location_manager.get_all_locations()['presets']
        for preset in all_presets:
            if preset['name'] == name:
                return preset
        return None
