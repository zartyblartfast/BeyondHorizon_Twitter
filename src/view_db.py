"""View contents of the tweet history database"""
import sqlite3
import os
from prettytable import PrettyTable

def get_db_path(env='test'):
    """Get database path"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'data', f'tweet_history_{env}.db')

def view_table(cursor, table_name):
    """Display contents of a table"""
    print(f"\n=== {table_name} Table ===")
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Create table
    table = PrettyTable()
    table.field_names = columns
    table.align = "l"
    
    # Get data
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    for row in rows:
        table.add_row(row)
    
    print(table)
    print(f"Total rows: {len(rows)}\n")

def main():
    db_path = get_db_path()
    if not os.path.exists(db_path):
        print(f"Database not found at: {db_path}")
        return
        
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # View post_types table
        view_table(cursor, "post_types")
        
        # View tweet_history table
        view_table(cursor, "tweet_history")

if __name__ == "__main__":
    main()
