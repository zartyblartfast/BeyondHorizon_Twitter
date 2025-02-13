import unittest
import os
import sys
import sqlite3
import tempfile
from unittest.mock import MagicMock, patch

# Add src directory to path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from preset_manager import PresetManager
from location_manager import LocationManager
from tweet_db import TweetDB

class TestPresetManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Sample presets data with hidden and visible presets
        self.sample_presets = {
            'presets': [
                {
                    'name': 'Preset1',
                    'isHidden': False,
                    'description': 'Visible preset 1'
                },
                {
                    'name': 'Preset2',
                    'isHidden': True,
                    'description': 'Hidden preset'
                },
                {
                    'name': 'Preset3',
                    'isHidden': False,
                    'description': 'Visible preset 2'
                },
                {
                    'name': 'Preset4',
                    'description': 'Preset without isHidden flag'
                }
            ]
        }
        
    def tearDown(self):
        """Clean up test fixtures"""
        os.close(self.db_fd)
        try:
            os.unlink(self.db_path)
        except:
            pass
        
    def test_hidden_presets_are_filtered(self):
        """Test that hidden presets are not returned by get_next_preset"""
        # Create PresetManager instance with real data
        preset_manager = PresetManager(self.db_path)
        
        # Get next preset using real location manager
        next_preset = preset_manager.get_next_preset()
        print("\n=== Testing hidden presets are filtered ===")
        print(f"Selected preset details:")
        print(f"  Name: {next_preset['name']}")
        print(f"  Description: {next_preset.get('description', 'No description')}")
        print(f"  Hidden: {next_preset.get('isHidden', False)}")
        print("=========================================")
        
        # Verify it's not hidden
        self.assertFalse(next_preset.get('isHidden', False))
        
    def test_preset_rotation_excludes_hidden(self):
        """Test that preset rotation works correctly while excluding hidden presets"""
        # Create PresetManager instance with real data
        preset_manager = PresetManager(self.db_path)
        
        # Get all presets in sequence using real location manager
        first_preset = preset_manager.get_next_preset()
        
        # Record it as used
        preset_manager.record_tweet_result(
            preset_name=first_preset['name'],
            tweet_id='123',
            tweet_text='Test tweet'
        )
        
        # Get next preset
        second_preset = preset_manager.get_next_preset()
        
        print("\n=== Testing preset rotation ===")
        print("First selected preset details:")
        print(f"  Name: {first_preset['name']}")
        print(f"  Description: {first_preset.get('description', 'No description')}")
        print(f"  Hidden: {first_preset.get('isHidden', False)}")
        print("\nSecond selected preset details:")
        print(f"  Name: {second_preset['name']}")
        print(f"  Description: {second_preset.get('description', 'No description')}")
        print(f"  Hidden: {second_preset.get('isHidden', False)}")
        print("==============================")
        
        # Verify we got different presets and neither is hidden
        self.assertNotEqual(first_preset['name'], second_preset['name'])
        self.assertFalse(first_preset.get('isHidden', False))
        self.assertFalse(second_preset.get('isHidden', False))
        
    def test_missing_ishidden_flag(self):
        """Test that presets without isHidden flag are treated as visible"""
        # Create PresetManager instance
        preset_manager = PresetManager(self.db_path)
        
        # Create test data with a preset missing the isHidden flag
        test_presets = {
            'presets': [
                {
                    'name': 'PresetWithoutFlag',
                    'description': 'No isHidden flag'
                }
            ]
        }
        
        # Mock the location manager
        preset_manager.location_manager.get_all_locations = MagicMock(return_value=test_presets)
        
        # Get next preset
        next_preset = preset_manager.get_next_preset()
        print("\n=== Testing preset without isHidden flag ===")
        print(f"Selected preset details:")
        print(f"  Name: {next_preset['name']}")
        print(f"  Description: {next_preset.get('description', 'No description')}")
        print(f"  Hidden: {next_preset.get('isHidden', False)}")
        print("=========================================")
        
        # Verify we got the preset without the flag
        self.assertEqual(next_preset['name'], 'PresetWithoutFlag')

if __name__ == '__main__':
    unittest.main()
