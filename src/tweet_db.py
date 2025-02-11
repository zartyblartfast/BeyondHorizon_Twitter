"""SQLite database interface for tweet history tracking"""
import sqlite3
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TweetDB:
    def __init__(self, db_path):
        """Initialize database connection"""
        logger.info(f"Initializing TweetDB with path: {db_path}")
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Create database and tables if they don't exist"""
        try:
            logger.info(f"Creating data directory: {os.path.dirname(self.db_path)}")
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            logger.info("Connecting to database and creating tables...")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create post_types table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS post_types (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type_name TEXT NOT NULL UNIQUE,
                        description TEXT
                    )
                """)
                
                # Create tweet_history table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tweet_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        post_type_id INTEGER NOT NULL,
                        preset_name TEXT,
                        tweet_id TEXT NOT NULL,
                        tweet_text TEXT NOT NULL,
                        posted_at TIMESTAMP NOT NULL,
                        status TEXT NOT NULL,
                        error_message TEXT,
                        FOREIGN KEY (post_type_id) REFERENCES post_types(id)
                    )
                """)
                
                # Insert default post type if not exists
                cursor.execute("""
                    INSERT OR IGNORE INTO post_types (type_name, description)
                    VALUES ('scheduled_preset', 'Regular scheduled posts from preset locations')
                """)
                
                conn.commit()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise

    def record_tweet(self, preset_name, tweet_id, tweet_text, status='success', error_message=None):
        """Insert a new tweet record into the database"""
        logger.info(f"Recording tweet - Preset: {preset_name}, Status: {status}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO tweet_history 
                    (post_type_id, preset_name, tweet_id, tweet_text, posted_at, status, error_message)
                    VALUES 
                    (1, ?, ?, ?, datetime('now'), ?, ?)
                """, (preset_name, tweet_id, tweet_text, status, error_message))
                conn.commit()
            logger.info("Tweet recorded successfully")
        except Exception as e:
            logger.error(f"Error recording tweet: {str(e)}")
            raise

    def get_last_preset(self):
        """Get the most recently posted preset name"""
        logger.info("Retrieving last preset name")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT preset_name 
                    FROM tweet_history 
                    WHERE status = 'success' 
                    ORDER BY posted_at DESC 
                    LIMIT 1
                """)
                result = cursor.fetchone()
                logger.info("Last preset name retrieved successfully")
                return result[0] if result else None
        except Exception as e:
            logger.error(f"Error retrieving last preset name: {str(e)}")
            raise

    def execute_query(self, query, params=None):
        """Execute any SQL query and return results"""
        logger.info(f"Executing query: {query}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                result = cursor.fetchall()
                logger.info("Query executed successfully")
                return result
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
