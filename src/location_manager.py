import json
import random
import logging
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Configure logging with a cleaner format
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # Only show the message, no timestamps or levels
)
logger = logging.getLogger(__name__)

class LocationManager:
    def __init__(self):
        self.url = "https://raw.githubusercontent.com/zartyblartfast/BeyondHorizonCalc/main/assets/info/presets.json"
        self.locations = None
        self.last_update = None

    def load_locations(self):
        """Load locations from GitHub"""
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            self.locations = response.json()
            self.last_update = datetime.now()
            logger.info(f"Loaded {len(self.locations['presets'])} locations from GitHub")
        except Exception as e:
            logger.error(f"Failed to load locations: {str(e)}")
            raise

    def get_random_location(self):
        """Get a random location for tweeting"""
        if not self.locations or self.needs_refresh():
            self.load_locations()
        return random.choice(self.locations['presets'])

    def needs_refresh(self, hours=6):
        """Check if we should refresh the data"""
        if not self.last_update:
            return True
        return datetime.now() - self.last_update > timedelta(hours=hours)

    def format_refraction(self, refraction):
        """Format refraction factor using app's fixed levels"""
        if refraction == 1.00:
            return f"None({refraction:.2f})"
        elif refraction == 1.02:
            return f"Low({refraction:.2f})"
        elif refraction == 1.04:
            return f"Below Avg({refraction:.2f})"
        elif refraction == 1.07:
            return f"Avg({refraction:.2f})"
        elif refraction == 1.10:
            return f"Above Avg({refraction:.2f})"
        elif refraction == 1.15:
            return f"High({refraction:.2f})"
        elif refraction == 1.20:
            return f"Very High({refraction:.2f})"
        elif refraction == 1.25:
            return f"Extremely High({refraction:.2f})"
        else:
            # For any non-standard value, round to nearest standard level
            levels = [1.00, 1.02, 1.04, 1.07, 1.10, 1.15, 1.20, 1.25]
            labels = ["None", "Low", "Below Avg", "Avg", "Above Avg", "High", "Very High", "Extremely High"]
            closest = min(levels, key=lambda x: abs(x - refraction))
            idx = levels.index(closest)
            return f"{labels[idx]}({refraction:.2f})"

    def format_tweet(self, location):
        """Format location data into a tweet"""
        # Get observer and target info
        observer = location['details']['location']['observer']
        target = location['details']['location']['target']
        
        # Format the tweet content
        tweet_lines = [
            f"{observer['name']} ({location['observerHeight']}m) → {target['name']} ({location['targetHeight']}m)",
            f"🌍 {observer['country']} to {target['country']} | 📏 {location['distance']}km",
            f"🌤️ Refraction: {self.format_refraction(location['refractionFactor'])}",
            f"Full details & calculations: https://beyondhorizoncalc.com",
            "#LongLineOfSight #BeyondHorizon"
        ]
        
        # Add attribution if present
        if location['details'].get('attribution'):
            tweet_lines.append(f"📸 {location['details']['attribution']}")
        
        return "\n".join(tweet_lines)

    def force_refresh(self):
        """Force a refresh of the location data"""
        self.locations = None
        self.last_update = None
        self.load_locations()

    def get_test_tweet(self, index=0):
        """Generate a test tweet from a location by index"""
        if not self.locations:
            self.load_locations()
        # Force refresh to get latest data
        self.force_refresh()
        
        # Get location by index, wrapping around if needed
        locations = self.locations['presets']
        if not locations:
            return "No locations available for testing"
        
        index = index % len(locations)
        location = locations[index]
        
        # Debug: Print full location data
        logger.info("Full location data structure:")
        logger.info(json.dumps(location, indent=2))
        
        return self.format_tweet(location)

    def get_all_locations(self):
        """Get all locations"""
        if not self.locations or self.needs_refresh():
            self.load_locations()
        return self.locations

    def get_image_urls(self, location):
        """Get list of non-null image URLs from location"""
        image_urls = []
        for i in range(1, 5):  # Check imageURL_1 through imageURL_4
            url = location['details'].get(f'imageURL_{i}')
            if url:  # Only add non-null URLs
                image_urls.append(url)
        return image_urls
