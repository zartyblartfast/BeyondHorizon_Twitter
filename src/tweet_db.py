"""SQLite database interface for tweet history tracking"""
import sqlite3
import os
from datetime import datetime

class TweetDB:
    def __init__(self, db_path):
        """Initialize database connection"""
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Create database and tables if they don't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
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

    def record_tweet(self, preset_name, tweet_id, tweet_text, status='success', error_message=None):
        """Insert a new tweet record into the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tweet_history 
                (post_type_id, preset_name, tweet_id, tweet_text, posted_at, status, error_message)
                VALUES 
                (1, ?, ?, ?, datetime('now'), ?, ?)
            """, (preset_name, tweet_id, tweet_text, status, error_message))
            conn.commit()

    def get_last_preset(self):
        """Get the most recently posted preset name"""
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
            return result[0] if result else None

    def execute_query(self, query, params=None):
        """Execute any SQL query and return results"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
