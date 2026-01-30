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
        Format:
        Row 1: Calculo peajes [Year]
        Row 2: Numero de Peajes | Total en BS
        Following rows: Sequential numbering | Amount
        
        Args:
            folder_path (str): Directory to save the Excel file.
            data (dict): Dictionary containing row data (PDF Name, Page, Amount, etc.)
        """
        current_year = datetime.now().year
        filename = f"Peajes {current_year} Calculo.xlsx"
        file_path = os.path.join(folder_path, filename)
        
        # Add timestamp
        data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Prepare detail data
            df_detail_new = pd.DataFrame([data])
            
            # Prepare summary data (Calculo sheet)
            # We need to know the next sequence number
            next_num = 1
            
            if os.path.exists(file_path):
                # Load existing to find next number and append detail
                with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    # Handle Summary Sheet (Calculo)
                    try:
                        df_summary_existing = pd.read_excel(file_path, sheet_name='Calculo', skiprows=1)
                        if not df_summary_existing.empty:
                            last_num = df_summary_existing.iloc[:, 0].max()
                            if pd.notna(last_num):
                                next_num = int(last_num) + 1
                    except Exception:
                        next_num = 1
                    
                    df_summary_new = pd.DataFrame({
                        "Numero de Peajes": [next_num],
                        "Total en BS": [data.get("Total Amount", 0)]
                    })
                    
                    # Write summary
                    # If it's a new sheet or file, we need the title
                    start_row_summary = 0
                    try:
                        writer.book['Calculo']
                        start_row_summary = writer.book['Calculo'].max_row
                        df_summary_new.to_excel(writer, sheet_name='Calculo', index=False, header=False, startrow=start_row_summary)
                    except KeyError:
                        # Create sheet with title
                        title_df = pd.DataFrame([[f"Calculo peajes {current_year}"]])
                        title_df.to_excel(writer, sheet_name='Calculo', index=False, header=False)
                        df_summary_new.to_excel(writer, sheet_name='Calculo', index=False, header=True, startrow=1)

                    # Apply centering to Calculo sheet
                    from openpyxl.styles import Alignment
                    ws = writer.book['Calculo']
                    for row in ws.iter_rows():
                        for cell in row:
                            cell.alignment = Alignment(horizontal='center')

                    # Handle Detail Sheet (Detalle)
                    start_row_detail = 0
                    try:
                        writer.book['Detalle']
                        start_row_detail = writer.book['Detalle'].max_row
                        df_detail_new.to_excel(writer, sheet_name='Detalle', index=False, header=False, startrow=start_row_detail)
                    except KeyError:
                        df_detail_new.to_excel(writer, sheet_name='Detalle', index=False, header=True)
            else:
                # Create new file
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    # Title row
                    title_df = pd.DataFrame([[f"Calculo peajes {current_year}"]])
                    title_df.to_excel(writer, sheet_name='Calculo', index=False, header=False)
                    
                    # Summary headers and first row
                    df_summary_new = pd.DataFrame({
                        "Numero de Peajes": [1],
                        "Total en BS": [data.get("Total Amount", 0)]
                    })
                    df_summary_new.to_excel(writer, sheet_name='Calculo', index=False, header=True, startrow=1)
                    
                    # Apply centering to Calculo sheet
                    from openpyxl.styles import Alignment
                    ws = writer.book['Calculo']
                    for row in ws.iter_rows():
                        for cell in row:
                            cell.alignment = Alignment(horizontal='center')
                    
                    # Detail sheet
                    df_detail_new.to_excel(writer, sheet_name='Detalle', index=False, header=True)
                
            return True, f"Saved to {filename}"
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error saving to Excel: {e}")
            return False, str(e)
