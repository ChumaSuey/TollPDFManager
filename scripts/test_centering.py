import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from services.data_service import DataService

def test_excel_centering():
    test_folder = os.getcwd()
    current_year = datetime.now().year
    expected_filename = f"Peajes {current_year} Calculo.xlsx"
    file_path = os.path.join(test_folder, expected_filename)
    
    # Remove existing if any
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed existing {expected_filename}")

    # Test Case: Create and verify
    data = {
        "PDF Name": "centering_test.pdf",
        "Page Number": 1,
        "Total Amount": "3000.00"
    }
    print("Saving entry with centering...")
    success, msg = DataService.save_toll_entry(test_folder, data)
    print(f"Result: {success}, {msg}")

    if os.path.exists(file_path):
        print(f"Success: {expected_filename} created with centered text logic.")
    else:
        print(f"Failure: {expected_filename} Not found.")

if __name__ == "__main__":
    test_excel_centering()
