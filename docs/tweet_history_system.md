# Tweet History Database Specification

## Overview
Track all tweets posted by the BeyondHorizon system, including scheduled presets and future post types. This allows for history tracking, error monitoring, and preventing duplicate posts.

## Database Schema

### Post Types Table
```sql
CREATE TABLE post_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL UNIQUE,
    description TEXT
);
```

Initial post types:
```sql
INSERT INTO post_types (type_name, description) VALUES
('scheduled_preset', 'Regular scheduled posts from preset locations');
```

### Tweet History Table
```sql
CREATE TABLE tweet_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_type_id INTEGER NOT NULL,
    preset_name TEXT,  -- NULL for non-preset posts
    tweet_id TEXT NOT NULL,
    tweet_text TEXT NOT NULL,
    posted_at TIMESTAMP NOT NULL,
    status TEXT NOT NULL,
    error_message TEXT,
    FOREIGN KEY (post_type_id) REFERENCES post_types(id)
);
```

## Implementation Details

### 1. Database Setup
- Location: `data/tweet_history_{env}.db` where env is 'dev' or 'prod'
- Add `data/*.db` to `.gitignore`
- Create initialization script in `src/db_init.py`

### 2. Core Classes

#### PresetManager Class (`src/preset_manager.py`)
Handles preset selection and tweet recording:
```python
class PresetManager:
    def __init__(self, db_path):
        self.db = TweetDB(db_path)
        self.location_manager = LocationManager()

    def get_next_preset(self, dry_run=False):
        """Get the next preset to post, considering history. 
        If dry_run=True, returns next preset without affecting sequence"""
        
    def record_tweet_result(self, preset_name, tweet_id, tweet_text, success=True, error_message=None):
        """Record the result of a tweet attempt. Not called during dry runs."""
```

Note: Dry runs will display the tweet content and selected preset but won't record anything to the database, keeping the history clean for actual posts only.

#### ReportManager Class (`src/report_manager.py`)
Handles report generation and email notifications:
```python
class ReportManager:
    def __init__(self, db_path):
        self.db = TweetDB(db_path)

    def generate_history_table(self, days=7):
        """Generate formatted table of recent tweet history"""
        
    def send_email_report(self, recipient_email):
        """Send email with formatted history table"""
```

#### TweetDB Class (`src/tweet_db.py`)
Low-level database operations:
```python
class TweetDB:
    def __init__(self, db_path):
        self.db_path = db_path
        
    def record_tweet(self, preset_name, tweet_id, tweet_text, status='success', error_message=None):
        """Record a tweet in the history database"""
        
    def get_last_preset(self):
        """Get the name of the last successfully posted preset"""
        
    def execute_query(self, query, params=None):
        """Execute a database query and return results"""
```

### 3. Test Tweet Script Integration
Update `src/test_tweet.py`:
```python
def main():
    preset_manager = PresetManager(get_db_path())
    report_manager = ReportManager(get_db_path())
    
    # Get next preset or use specified one
    if args.preset:
        location = find_preset_by_name(locations, args.preset)
    else:
        location = preset_manager.get_next_preset()
    
    # Post tweet
    try:
        tweet_id = twitter_client.post_tweet(tweet_content, image_urls)
        preset_manager.record_tweet_result(
            preset_name=location['name'],
            tweet_id=tweet_id,
            tweet_text=tweet_content,
            success=bool(tweet_id)
        )
    except Exception as e:
        preset_manager.record_tweet_result(
            preset_name=location['name'],
            tweet_id=None,
            tweet_text=tweet_content,
            success=False,
            error_message=str(e)
        )
```

### 4. Automated Tweet Scheduling

#### ScheduledTweetRunner (`src/scheduled_tweet_runner.py`)
Manages automated tweet posting with configurable intervals and random delays:

```python
class ScheduledTweetRunner:
    """Wrapper script for automated tweet management with configurable intervals"""
    
    def should_post_today(self):
        """Check if enough days have passed since last tweet"""
        
    def random_wait(self):
        """Add random delay before posting to create natural timing"""
```

Configuration (in `.env`):
```bash
# Number of days between tweets (default: 3, max: 14)
SCHEDULED_DAYS_INTERVAL=3

# Maximum random wait in minutes before posting (default: 10, max: 15)
SCHEDULED_RANDOM_MINUTES=10
```

Features:
- Configurable posting interval (1-14 days)
- Random wait period before posting (1-15 minutes)
- Dry run mode for testing
- Detailed logging of all actions
- Safety checks for environment variables

Example log output:
```
=== Starting scheduled tweet runner ===
Using production environment
Last tweet was 3 days and 2 hours ago
Waiting for 3 days between tweets
Adding random wait of 5 minutes and 30 seconds
Running tweet manager...
=== Tweet manager completed successfully ===
```

#### PythonAnywhere Deployment
Schedule the runner to check daily:
```bash
python3 /home/BeyondHorizon/BeyondHorizon_Twitter/src/scheduled_tweet_runner.py
```

The script will:
1. Check if enough days have passed since last tweet
2. If ready to post:
   - Add random wait time
   - Post tweet with images
   - Record in history database
3. If not ready:
   - Log status and exit

### 5. Email Reporting
Reports will include:
- Formatted ASCII table using PrettyTable
- Recent tweet history (last 7 days by default)
- Status of each tweet
- Links to posted tweets
- Error messages if any

Sample email format:
```
BeyondHorizon Tweet History Report
Generated: 2025-02-08 21:27

Recent Tweet History:
+------------------+----------------------+---------+----------------------------------------+-------------+
| Date             | Preset               | Status  | Tweet URL                             | Error       |
+------------------+----------------------+---------+----------------------------------------+-------------+
| 2025-02-08 21:20 | K2 to Broad Peak    | success | https://twitter.com/user/status/12345 |             |
| 2025-02-04 21:15 | Everest to Kangchen | success | https://twitter.com/user/status/12344 |             |
| 2025-01-31 21:10 | Pic de Finstrelles  | error   |                                       | API timeout |
+------------------+----------------------+---------+----------------------------------------+-------------+
```

### 6. Environment Setup
```python
def get_db_path():
    """Get database path based on environment"""
    env = os.getenv('ENVIRONMENT', 'development')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_name = f"tweet_history_{env}.db"
    return os.path.join(base_dir, 'data', db_name)
```

## Viewing Database Contents

To view the current contents of the tweet history database:

```bash
# View both tables (post_types and tweet_history)
python src/view_db.py

# For development database (default)
python src/view_db.py test

# For production database
python src/view_db.py prod
```

This will display a nicely formatted table showing:
- All tweet records with their status
- Post types and descriptions
- Total row counts for each table

Example output:
```
=== tweet_history Table ===
+----+--------------+-----------------------------------+----------+--------------+---------------------+---------+---------------+
| id | post_type_id | preset_name                       | tweet_id | tweet_text   | posted_at           | status  | error_message |
+----+--------------+-----------------------------------+----------+--------------+---------------------+---------+---------------+
| 1  | 1            | Pic de Finstrelles to Pic Gaspard | 123456   | Test tweet 1 | 2025-02-08 21:45:23 | success | None          |
+----+--------------+-----------------------------------+----------+--------------+---------------------+---------+---------------+
Total rows: 1
```

The database viewer uses PrettyTable for formatting and shows:
- Tweet IDs and status
- Preset names and post times
- Error messages if any tweets failed
- Row counts for each table

## Next Steps
1. Implement database initialization script
2. Create core classes (PresetManager, ReportManager, TweetDB)
3. Add PrettyTable to requirements.txt
4. Set up email configuration in PythonAnywhere
5. Test locally before deploying
6. Add email credentials to .env file

# Preset Manager Documentation

## Overview
The Preset Manager system handles the selection and tracking of location presets for the BeyondHorizon Twitter bot. It ensures each location is tweeted in a fair rotation and maintains a history of all tweet attempts.

## Components

### 1. PresetManager Class
Located in `src/preset_manager.py`, this class manages:
- Selection of the next preset to tweet
- Recording tweet results
- Finding specific presets by name

Key methods:
```python
get_next_preset(dry_run=False)  # Get next preset considering history
record_tweet_result(...)        # Record tweet attempt results
find_preset_by_name(name)       # Find specific preset by name
```

### 2. TweetDB Class
Located in `src/tweet_db.py`, this class handles:
- Database creation and schema management
- Tweet history recording
- Query execution

Tables:
1. `post_types`:
   - `id`: INTEGER PRIMARY KEY
   - `type_name`: TEXT NOT NULL UNIQUE
   - `description`: TEXT

2. `tweet_history`:
   - `id`: INTEGER PRIMARY KEY
   - `post_type_id`: INTEGER
   - `preset_name`: TEXT NOT NULL
   - `tweet_id`: TEXT
   - `tweet_text`: TEXT
   - `posted_at`: DATETIME
   - `status`: TEXT
   - `error_message`: TEXT

### 3. ReportManager Class
Located in `src/report_manager.py`, this class provides:
- Formatted history tables
- Email-ready reports
- History filtering and analysis

## Testing Tools

### test_tweet_v2.py
Command line options:
```bash
--dry-run          # Show tweet content without posting
--test-record      # Record dry run to database (testing only)
--list-presets     # List all available presets
--show-history     # Show recent tweet history
--clear-history    # Clear all tweet history (testing only)
--preset NAME      # Use specific preset
--random           # Use random preset
```

### test_managers.py
Dedicated test script that verifies:
- PresetManager functionality
- ReportManager formatting
- Database operations

## Preset Selection Logic

1. **First Run**:
   - If no history exists, starts with first preset

2. **Normal Operation**:
   - Checks for presets not used in last 30 days
   - Selects first unused preset from list
   - If all presets used, starts with least recently used

3. **History Tracking**:
   - Records successful and failed attempts
   - Stores tweet IDs and error messages
   - Maintains timestamps for rotation logic

## Database Files

- Development: `data/tweet_history_development.db`
- Production: `data/tweet_history_production.db`
- Test: `data/tweet_history_test.db`

Environment is determined by the `ENVIRONMENT` variable (defaults to 'development').

## Usage Examples

1. Post next preset in sequence:
```bash
python src/test_tweet_v2.py
```

2. Test with specific preset:
```bash
python src/test_tweet_v2.py --dry-run --preset "K2 to Broad Peak"
```

3. View tweet history:
```bash
python src/test_tweet_v2.py --show-history
```

4. Run all tests:
```bash
python src/test_managers.py
```

## Implementation Notes

1. **Database Creation**:
   - Tables created automatically if they don't exist
   - Default post type "scheduled_preset" added on creation

2. **Error Handling**:
   - Failed tweets are recorded but don't affect rotation
   - Errors include full error messages for debugging

3. **Testing Features**:
   - Dry run mode for testing without posting
   - Test database can be cleared for fresh starts
   - Random selection available for testing
