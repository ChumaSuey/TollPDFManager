import unittest
import os
import json
from services.data_service import DataService

class TestFlagPersistence(unittest.TestCase):
    def setUp(self):
        self.flags_file = "flags.json"
        # Cleanup before
        if os.path.exists(self.flags_file):
            os.remove(self.flags_file)

    def tearDown(self):
        # Cleanup after
        if os.path.exists(self.flags_file):
            os.remove(self.flags_file)

    def test_save_and_load(self):
        flags = {"c:\\path\\to\\file1.pdf", "c:\\path\\to\\file2.pdf"}
        
        # Save
        result = DataService.save_flags(flags)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.flags_file))
        
        # Load
        loaded_flags = DataService.load_flags()
        self.assertEqual(loaded_flags, flags)

    def test_load_empty(self):
        # Load without file
        loaded_flags = DataService.load_flags()
        self.assertEqual(loaded_flags, set())

    def test_overwrite(self):
        # Save initial
        DataService.save_flags({"file1"})
        
        # Save new set (simulating toggle remove)
        DataService.save_flags(set())
        
        loaded = DataService.load_flags()
        self.assertEqual(loaded, set())

if __name__ == '__main__':
    unittest.main()
