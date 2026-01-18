import os
import pandas as pd
from datetime import datetime

# EXCEL_FILENAME removed, generating dynamically
    
class DataService:
    @staticmethod
    def save_toll_entry(folder_path, data):
        """
        Saves a toll entry to the Excel file in the specified folder.
        Creates the file if it doesn't exist.
        The filename contains the current year (e.g., "Peajes 2026 Calculo.xlsx").
        
        Args:
            folder_path (str): Directory to save the Excel file.
            data (dict): Dictionary containing row data (PDF Name, Page, Amount, etc.)
        """
        current_year = datetime.now().year
        filename = f"Peajes {current_year} Calculo.xlsx"
        file_path = os.path.join(folder_path, filename)
        
        # Add timestamp
        data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Convert single dict to DataFrame
        df_new = pd.DataFrame([data])
        
        try:
            if os.path.exists(file_path):
                # Append to existing
                # mode='a' for append, needs logic to handle headers if file is empty
                # Simplest robust way with pandas: load, concat, save
                # Or use openpyxl engine with mode='a'
                
                # Reading existing to ensure schema match and append
                with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    # Find last row
                    try:
                        writer.book['Sheet1']
                        start_row = writer.book['Sheet1'].max_row
                        header = False
                    except KeyError:
                        start_row = 0
                        header = True
                        
                    df_new.to_excel(writer, index=False, header=header, startrow=start_row)
            else:
                # Create new
                df_new.to_excel(file_path, index=False)
                
            return True, f"Saved to {filename}"
            
        except Exception as e:
            print(f"Error saving to Excel: {e}")
            return False, str(e)
