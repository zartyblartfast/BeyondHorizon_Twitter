"""Wrapper script for scheduled tweet management"""
import os
import sys
import time
import random
import logging
import subprocess
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Set up logging to stdout only
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Load environment variables from config/.env
config_path = os.path.join(parent_dir, 'config', '.env')
if os.path.exists(config_path):
    load_dotenv(config_path)
    logging.info(f"Loaded environment from {config_path}")
else:
    logging.warning(f"No .env file found at {config_path}")

from src.tweet_db import TweetDB

# Constants for safety limits
MIN_DAYS_INTERVAL = 0  # Allow 0 for testing purposes
MAX_DAYS_INTERVAL = 14
DEFAULT_DAYS_INTERVAL = 3

MIN_RANDOM_MINUTES = 1
MAX_RANDOM_MINUTES = 15
DEFAULT_RANDOM_MINUTES = 10

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
        logging.info(f"{var_name} set to {value}")
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
    hours_since_last_tweet = int((datetime.now() - last_tweet_date).total_seconds() / 3600)
    
    days_interval = get_safe_int_env(
        'SCHEDULED_DAYS_INTERVAL', 
        DEFAULT_DAYS_INTERVAL,
        MIN_DAYS_INTERVAL,
        MAX_DAYS_INTERVAL
    )
    
    if days_interval == 0:
        logging.warning("TEST MODE: Days interval is 0 - allowing multiple posts per day")
        return True
    
    logging.info(f"Last tweet was {days_since_last_tweet} days and {hours_since_last_tweet % 24} hours ago")
    logging.info(f"Waiting for {days_interval} days between tweets")
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
    wait_mins = seconds // 60
    wait_secs = seconds % 60
    
    logging.info(f"Waiting for {wait_mins}m {wait_secs}s before posting...")
    time.sleep(seconds)

def main():
    """Main function to manage scheduled tweet posting"""
    try:
        logging.info("=== Starting scheduled tweet runner ===")
        
        # Initialize database
        env = os.getenv('ENVIRONMENT', 'development')
        db_name = f"tweet_history_{env}.db"  # Match tweet_manager.py naming
        db_path = os.path.join(parent_dir, 'data', db_name)
        
        # Ensure data directory exists with correct permissions
        data_dir = os.path.dirname(db_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, mode=0o755)
            logging.info(f"Created data directory: {data_dir}")
            
        if not os.path.exists(db_path):
            logging.info(f"Database will be created at: {db_path}")
            
        logging.info(f"Using {env} environment with database: {db_path}")
        db = TweetDB(db_path)
        
        # Check if we should post today
        if not should_post_today(db):
            logging.info("Skipping - not enough time has passed since last tweet")
            return
            
        # Random wait before posting
        logging.info("=== Enough time has passed - preparing to post ===")
        random_wait()
        
        # Run the tweet manager
        tweet_manager_path = os.path.join(parent_dir, 'src', 'tweet_manager.py')
        if not os.path.exists(tweet_manager_path):
            logging.error(f"Tweet manager not found: {tweet_manager_path}")
            return
            
        logging.info("Running tweet manager...")
        # Set DRY_RUN in environment if specified
        dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'
        if dry_run:
            logging.info("DRY RUN mode enabled - tweet will not be posted")
            os.environ['DRY_RUN'] = 'true'
            
        # Use subprocess instead of os.system to better handle environment
        env_copy = os.environ.copy()  # Copy current environment
        env_copy['PYTHONPATH'] = parent_dir  # Ensure imports work
        
        result = subprocess.run(
            [sys.executable, tweet_manager_path],
            env=env_copy,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            logging.info("=== Tweet manager completed successfully ===")
            if result.stdout:
                logging.info("Output:\n" + result.stdout)
        else:
            logging.error(f"Tweet manager failed with exit code: {result.returncode}")
            if result.stderr:
                logging.error("Error output:\n" + result.stderr)
            if result.stdout:
                logging.info("Standard output:\n" + result.stdout)
            
    except Exception as e:
        logging.error(f"Error in scheduled tweet runner: {str(e)}", exc_info=True)

if __name__ == '__main__':
    main()
