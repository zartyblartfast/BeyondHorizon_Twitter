# SQLite Handy Commands

## PythonAnywhere Path
Replace `/path/to/db` with: `/home/zartyblartfast/BeyondHorizon_Twitter/data/tweet_history_production.db`

## View Commands
```sql
-- View table schema
sqlite3 /path/to/db ".schema tweet_history"

-- View all rows
sqlite3 /path/to/db "SELECT * FROM tweet_history;"

-- View specific columns
sqlite3 /path/to/db "SELECT id, preset_name, tweet_id, posted_at FROM tweet_history;"
```

## Delete Commands
```sql
-- Delete by ID
sqlite3 /path/to/db "DELETE FROM tweet_history WHERE id=5;"

-- Delete by tweet_id
sqlite3 /path/to/db "DELETE FROM tweet_history WHERE tweet_id='1234567890';"
```

## Filter Commands
```sql
-- View recent tweets
sqlite3 /path/to/db "SELECT * FROM tweet_history ORDER BY posted_at DESC LIMIT 5;"

-- View tweets by status
sqlite3 /path/to/db "SELECT * FROM tweet_history WHERE status='success';"

-- View tweets for specific preset
sqlite3 /path/to/db "SELECT * FROM tweet_history WHERE preset_name='PresetName';"
```
