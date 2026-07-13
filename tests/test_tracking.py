import os
import unittest
from unittest.mock import patch
import pandas as pd
from services.data_service import DataService

class TestTrackingLogic(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/test_export"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        from datetime import datetime
        self.current_year = datetime.now().year
        self.filename = f"Peajes {self.current_year} Calculo.xlsx"
        self.excel_path = os.path.join(self.test_dir, self.filename)

    def tearDown(self):
        if os.path.exists(self.excel_path):
            os.remove(self.excel_path)
        if os.path.exists(self.test_dir):
            try:
                os.rmdir(self.test_dir)
            except Exception:
                pass

    @patch("services.data_service.DataService.load_config", return_value={})
    def test_get_processed_tolls_empty(self, mock_cfg):
        processed = DataService.get_processed_tolls(self.test_dir)
        self.assertEqual(processed, set())

    @patch("services.data_service.DataService.load_config", return_value={})
    def test_get_processed_tolls_with_data(self, mock_cfg):
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

    @patch("services.data_service.DataService.load_config", return_value={})
    def test_get_processed_tolls_no_detalle_sheet(self, mock_cfg):
        # modify sheet name
        df = pd.DataFrame({"PDF Name": ["file1.pdf"]})
        with pd.ExcelWriter(self.excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False)
            
        processed = DataService.get_processed_tolls(self.test_dir)
        self.assertEqual(processed, set())

if __name__ == '__main__':
    unittest.main()
