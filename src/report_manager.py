"""Manages report generation and email notifications"""
from tweet_db import TweetDB
from prettytable import PrettyTable
import datetime

class ReportManager:
    def __init__(self, db_path):
        """Initialize with database path"""
        self.db = TweetDB(db_path)
        
    def generate_history_table(self, days=7):
        """Generate formatted table of recent tweet history"""
        table = PrettyTable()
        table.field_names = ["Date", "Preset", "Status", "Tweet URL", "Error"]
        table.align = "l"  # Left align text
        
        # Get recent history from DB
        query = """
            SELECT posted_at, preset_name, status, tweet_id, error_message 
            FROM tweet_history 
            WHERE posted_at >= datetime('now', ?)
            ORDER BY posted_at DESC 
        """
        days_param = f'-{days} days'
        
        for row in self.db.execute_query(query, (days_param,)):
            date = datetime.datetime.fromisoformat(row[0]).strftime("%Y-%m-%d %H:%M")
            tweet_url = f"https://twitter.com/user/status/{row[3]}" if row[3] != 'none' else ''
            table.add_row([
                date,
                row[1],
                row[2],
                tweet_url,
                (row[4][:50] + '...') if row[4] and len(row[4]) > 50 else row[4] or ''
            ])
        
        return table.get_string()
        
    def generate_report(self, days=7):
        """Generate a complete report including history table"""
        history_table = self.generate_history_table(days)
        
        report = f"""
BeyondHorizon Tweet History Report
Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}

Recent Tweet History:
{history_table}
"""
        return report
        
    def send_email_report(self, recipient_email, days=7):
        """Send email with formatted history table"""
        # This is a placeholder for email sending functionality
        # We can implement this when email configuration is ready
        report = self.generate_report(days)
        print("Email would be sent to:", recipient_email)
        print("\nReport content:")
        print(report)
