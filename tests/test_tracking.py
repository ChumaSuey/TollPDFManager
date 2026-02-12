import os
import unittest
import pandas as pd
from services.data_service import DataService

class TestTrackingLogic(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/test_export"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        
        # Configure DataService to use this dir temporarily
        # DataService uses config.json, but get_processed_tolls takes a folder_path argument
        # However, get_excel_path logic uses config first. 
        # But get_excel_path(folder_path) prioritizes config > argument > cwd. 
        # Wait, the code says:
        # base_folder = config.get("export_folder", folder_path)
        # fast check:
        # if config has export_folder, it uses it.
        # This makes testing hard if config exists.
        # We should patch load_config or ensure we pass a folder that overrides?
        # Actually line 36: base_folder = config.get("export_folder", folder_path)
        # If "export_folder" is in config, it returns that, ignoring folder_path if unrelated?
        # No, dict.get(key, default). If key exists, it returns value. 
        # So if config has export_folder, folder_path arg is IGNORED.
        # That's a potential bug or design choice in DataService.import json
        
        # unique filename to avoid conflict
        from datetime import datetime
        self.current_year = datetime.now().year
        self.filename = f"Peajes {self.current_year} Calculo.xlsx"
        self.excel_path = os.path.join(self.test_dir, self.filename)
        
        # We need to bypass config for this test.
        # Best way is to mock load_config.
        self.original_load_config = DataService.load_config
        DataService.load_config = lambda: {} # Return empty config
        
    def tearDown(self):
        DataService.load_config = self.original_load_config
        if os.path.exists(self.excel_path):
            os.remove(self.excel_path)
        if os.path.exists(self.test_dir):
            try:
                os.rmdir(self.test_dir)
            except:
                pass

    def test_get_processed_tolls_empty(self):
        # No excel file
        processed = DataService.get_processed_tolls(self.test_dir)
        self.assertEqual(processed, set())

    def test_get_processed_tolls_with_data(self):
        # Create excel with data
        df = pd.DataFrame({
            "PDF Name": ["file1.pdf", "file2.pdf", "file1.pdf"], # Duplicates shouldn't matter for set
            "Amount": [10, 20, 10]
        })
        
        with pd.ExcelWriter(self.excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Detalle", index=False)
            
        processed = DataService.get_processed_tolls(self.test_dir)
        self.assertIn("file1.pdf", processed)
        self.assertIn("file2.pdf", processed)
        self.assertEqual(len(processed), 2)

    def test_get_processed_tolls_no_detalle_sheet(self):
        # modify sheet name
        df = pd.DataFrame({"PDF Name": ["file1.pdf"]})
        with pd.ExcelWriter(self.excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False)
            
        processed = DataService.get_processed_tolls(self.test_dir)
        self.assertEqual(processed, set())

if __name__ == '__main__':
    unittest.main()
