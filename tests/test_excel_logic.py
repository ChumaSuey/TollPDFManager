import os
import sys
import json
import unittest
from datetime import datetime
import pandas as pd

# Add project root to path
sys.path.append(os.getcwd())

from services.data_service import DataService

class TestExcelLogic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_folder = os.path.join(os.getcwd(), "tests", "data")
        if not os.path.exists(cls.test_folder):
            os.makedirs(cls.test_folder)
        cls.config_backup = "config.json.bak"
        if os.path.exists("config.json"):
            os.rename("config.json", cls.config_backup)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.config_backup):
            if os.path.exists("config.json"):
                os.remove("config.json")
            os.rename(cls.config_backup, "config.json")

    def test_01_config_persistence(self):
        """Test that configuration is saved and loaded correctly."""
        test_config = {"export_folder": self.test_folder}
        DataService.save_config(test_config)
        loaded = DataService.load_config()
        self.assertEqual(loaded["export_folder"], self.test_folder)

    def test_02_excel_generation_and_centering(self):
        """Test Excel creation, dual sheets, sequential numbering, and centering."""
        current_year = datetime.now().year
        expected_filename = f"Peajes {current_year} Calculo.xlsx"
        file_path = os.path.join(self.test_folder, expected_filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)

        # First entry
        data1 = {"PDF Name": "test1.pdf", "Page Number": 1, "Total Amount": 100.0}
        success1, _ = DataService.save_toll_entry(self.test_folder, data1)
        self.assertTrue(success1)

        # Second entry
        data2 = {"PDF Name": "test2.pdf", "Page Number": 1, "Total Amount": 200.0}
        success2, _ = DataService.save_toll_entry(self.test_folder, data2)
        self.assertTrue(success2)

        self.assertTrue(os.path.exists(file_path))
        
        # Verify content using pandas
        df_summary = pd.read_excel(file_path, sheet_name='Calculo', skiprows=1)
        self.assertEqual(len(df_summary), 2)
        self.assertEqual(int(df_summary.iloc[1, 0]), 2) # Check sequential numbering
        self.assertEqual(df_summary.iloc[1, 1], 200.0)

        # Check detail sheet
        df_detail = pd.read_excel(file_path, sheet_name='Detalle')
        self.assertEqual(len(df_detail), 2)
        self.assertEqual(df_detail.iloc[1]['PDF Name'], "test2.pdf")

if __name__ == "__main__":
    unittest.main()
