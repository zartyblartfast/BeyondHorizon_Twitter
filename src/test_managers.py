"""Test script for PresetManager and ReportManager functionality"""
import os
import sys
from preset_manager import PresetManager
from report_manager import ReportManager
import datetime

def get_test_db_path():
    """Get path for test database"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'data', 'tweet_history_test.db')

def test_preset_manager():
    """Test PresetManager functionality"""
    print("\n=== Testing PresetManager ===")
    
    # Initialize with test database
    db_path = get_test_db_path()
    if os.path.exists(db_path):
        os.remove(db_path)  # Start fresh
    
    preset_manager = PresetManager(db_path)
    
    # Test 1: Get first preset (when no history)
    print("\nTest 1: Get first preset (no history)")
    preset = preset_manager.get_next_preset()
    print(f"Got preset: {preset['name']}")
    
    # Test 2: Record a successful tweet
    print("\nTest 2: Record successful tweet")
    preset_manager.record_tweet_result(
        preset_name=preset['name'],
        tweet_id="123456",
        tweet_text="Test tweet 1",
        success=True
    )
    print("Recorded successful tweet")
    
    # Test 3: Get next preset (should be different)
    print("\nTest 3: Get next preset")
    next_preset = preset_manager.get_next_preset()
    print(f"Got next preset: {next_preset['name']}")
    assert next_preset['name'] != preset['name'], "Next preset should be different"
    
    # Test 4: Record a failed tweet
    print("\nTest 4: Record failed tweet")
    preset_manager.record_tweet_result(
        preset_name=next_preset['name'],
        tweet_id=None,
        tweet_text="Test tweet 2",
        success=False,
        error_message="Test error"
    )
    print("Recorded failed tweet")
    
    # Test 5: Find preset by name
    print("\nTest 5: Find preset by name")
    found_preset = preset_manager.find_preset_by_name(preset['name'])
    assert found_preset is not None, f"Should find preset {preset['name']}"
    print(f"Found preset: {found_preset['name']}")
    
    return preset_manager

def test_report_manager(preset_manager):
    """Test ReportManager functionality"""
    print("\n=== Testing ReportManager ===")
    
    report_manager = ReportManager(get_test_db_path())
    
    # Test 1: Generate history table
    print("\nTest 1: Generate history table")
    table = report_manager.generate_history_table()
    print("\nHistory Table:")
    print(table)
    
    # Test 2: Generate full report
    print("\nTest 2: Generate full report")
    report = report_manager.generate_report()
    print("\nFull Report:")
    print(report)
    
    # Test 3: Test email report (simulation)
    print("\nTest 3: Test email report")
    report_manager.send_email_report("test@example.com")

def main():
    try:
        # Run PresetManager tests
        preset_manager = test_preset_manager()
        
        # Run ReportManager tests
        test_report_manager(preset_manager)
        
        print("\n=== All tests completed successfully! ===")
        
    except AssertionError as e:
        print(f"\nTest failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
