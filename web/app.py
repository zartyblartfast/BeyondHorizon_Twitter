"""BeyondHorizon Twitter Dashboard"""
from flask import Flask, render_template
import os
import sys
import psutil
import sqlite3
from datetime import datetime
import traceback

# Add parent directory to path so we can import from src
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(f"Adding to path: {parent_dir}")
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

app = Flask(__name__)

def get_db_path():
    """Get database path based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if env == 'development':
        db_path = os.path.join(base_dir, 'data', 'tweet_history_test.db')
    elif env == 'production':
        db_path = os.path.join(base_dir, 'data', 'tweet_history_production.db')
    else:
        db_path = os.path.join(base_dir, 'data', 'tweet_history_test.db')
    print(f"Using database: {db_path}")
    print(f"Database exists: {os.path.exists(db_path)}")
    return db_path

def get_tweets():
    """Get tweets directly using SQLite"""
    db_path = get_db_path()
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return []
        
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Get column names first
        cur.execute("PRAGMA table_info(tweet_history)")
        columns = [col[1] for col in cur.fetchall()]
        print(f"Columns: {columns}")
        
        # Get the data
        query = """
            SELECT 
                tweet_history.id,
                tweet_history.post_type_id,
                tweet_history.preset_name,
                tweet_history.tweet_id,
                tweet_history.tweet_text,
                tweet_history.posted_at,
                tweet_history.status,
                tweet_history.error_message,
                post_types.type_name
            FROM tweet_history
            LEFT JOIN post_types ON tweet_history.post_type_id = post_types.id
            ORDER BY posted_at DESC
            LIMIT 50
        """
        print(f"Executing query: {query}")
        cur.execute(query)
        rows = cur.fetchall()
        print(f"Found {len(rows)} rows")
        
        # Convert to dictionaries
        tweets = []
        for row in rows:
            tweet = {
                'id': row[0],
                'post_type_id': row[1],
                'preset_name': row[2],
                'tweet_id': row[3],
                'tweet_text': row[4],
                'posted_at': row[5],
                'status': row[6],
                'error_message': row[7],
                'type_name': row[8]
            }
            tweets.append(tweet)
            
        return tweets
    except Exception as e:
        print(f"Database error: {str(e)}")
        print(traceback.format_exc())
        return []
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/')
def dashboard():
    """Display main dashboard"""
    try:
        # Get tweet history
        tweets = get_tweets()
        print(f"Retrieved {len(tweets)} tweets")
        
        # Get system info
        system_info = {
            'python_version': sys.version.split()[0],
            'flask_env': os.getenv('FLASK_ENV', 'development'),
            'memory_usage': f"{psutil.Process().memory_info().rss / 1024 / 1024:.1f}MB",
            'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'db_path': get_db_path()
        }
        
        return render_template('dashboard.html', 
                             tweets=tweets, 
                             system_info=system_info)
    except Exception as e:
        print("Error in dashboard:")
        print(traceback.format_exc())
        return f"Error: {str(e)}<br><pre>{traceback.format_exc()}</pre>", 500

if __name__ == '__main__':
    app.run(debug=True)
