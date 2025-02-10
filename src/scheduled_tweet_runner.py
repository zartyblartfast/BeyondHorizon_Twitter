"""Wrapper script for scheduled tweet management"""
import os
import sys
import time
import random
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Load environment variables from config/.env
config_path = os.path.join(parent_dir, 'config', '.env')
if os.path.exists(config_path):
    load_dotenv(config_path)
    logging.info(f"Loaded environment from {config_path}")
else:
    logging.warning(f"No .env file found at {config_path}")

from src.tweet_db import TweetDB

# Constants for safety limits
MIN_DAYS_INTERVAL = 1
MAX_DAYS_INTERVAL = 14
DEFAULT_DAYS_INTERVAL = 3

MIN_RANDOM_MINUTES = 1
MAX_RANDOM_MINUTES = 15
DEFAULT_RANDOM_MINUTES = 10

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_safe_int_env(var_name: str, default: int, min_val: int, max_val: int) -> int:
    """Get an environment variable with safety bounds"""
    try:
        value = int(os.getenv(var_name, str(default)))
        if value < min_val:
            logging.warning(f"{var_name} value {value} below minimum, using {min_val}")
            return min_val
        if value > max_val:
            logging.warning(f"{var_name} value {value} above maximum, using {max_val}")
            return max_val
        return value
    except (ValueError, TypeError) as e:
        logging.warning(f"Invalid {var_name} value, using default {default}: {str(e)}")
        return default

def should_post_today(db: TweetDB) -> bool:
    """Check if enough days have passed since last tweet"""
    query = "SELECT posted_at FROM tweet_history ORDER BY posted_at DESC LIMIT 1"
    result = db.execute_query(query)
    
    if not result:
        logging.info("No previous tweets found, ok to post")
        return True
        
    # Result is a tuple, not a dictionary
    last_tweet_date = datetime.strptime(result[0][0], '%Y-%m-%d %H:%M:%S')
    days_since_last_tweet = (datetime.now() - last_tweet_date).days
    
    days_interval = get_safe_int_env(
        'SCHEDULED_DAYS_INTERVAL', 
        DEFAULT_DAYS_INTERVAL,
        MIN_DAYS_INTERVAL,
        MAX_DAYS_INTERVAL
    )
    
    logging.info(f"Days since last tweet: {days_since_last_tweet} (interval: {days_interval})")
    return days_since_last_tweet >= days_interval

def random_wait():
    """Wait for a random period within configured minutes"""
    # Use shorter wait time if in dry run mode
    dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'
    if dry_run:
        max_minutes = 1  # Only wait up to 1 minute in dry run mode
        logging.info("DRY RUN mode - using shortened wait time (1 minute max)")
    else:
        max_minutes = get_safe_int_env(
            'SCHEDULED_RANDOM_MINUTES',
            DEFAULT_RANDOM_MINUTES,
            MIN_RANDOM_MINUTES,
            MAX_RANDOM_MINUTES
        )
    
    seconds = random.randint(0, max_minutes * 60)
    logging.info(f"Waiting {seconds} seconds (max {max_minutes} minutes) before posting")
    time.sleep(seconds)

def main():
    """Main function to manage scheduled tweet posting"""
    try:
        # Initialize database
        env = os.getenv('ENVIRONMENT', 'development')
        db_path = os.path.join(parent_dir, 'data', 
                              'tweet_history_test.db' if env == 'development' else 'tweet_history_prod.db')
        
        if not os.path.exists(db_path):
            logging.error(f"Database not found: {db_path}")
            return
            
        logging.info(f"Using database: {db_path}")
        db = TweetDB(db_path)
        
        # Check if we should post today
        if not should_post_today(db):
            logging.info("Not enough days since last tweet, skipping")
            return
            
        # Random wait before posting
        random_wait()
        
        # Run the tweet manager
        tweet_manager_path = os.path.join(parent_dir, 'src', 'tweet_manager.py')
        if not os.path.exists(tweet_manager_path):
            logging.error(f"Tweet manager not found: {tweet_manager_path}")
            return
            
        logging.info("Running tweet manager")
        # Set DRY_RUN in environment if specified
        dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'
        if dry_run:
            logging.info("DRY RUN mode enabled - tweet will not be posted")
            os.environ['DRY_RUN'] = 'true'
            
        result = os.system(f'python {tweet_manager_path}')
        
        if result == 0:
            logging.info("Tweet manager completed successfully")
        else:
            logging.error(f"Tweet manager failed with exit code: {result}")
            
    except Exception as e:
        logging.error(f"Error in scheduled tweet runner: {str(e)}", exc_info=True)

if __name__ == '__main__':
    main()
