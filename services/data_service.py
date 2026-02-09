import json
import os
from datetime import datetime

import pandas as pd

# EXCEL_FILENAME removed, generating dynamically
CONFIG_FILE = "config.json"


class DataService:
    @staticmethod
    def load_config():
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        return {}

    @staticmethod
    def save_config(config):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    @staticmethod
    def get_excel_path(folder_path=None):
        config = DataService.load_config()
        # Priority: Config > Argument > current dir
        base_folder = config.get("export_folder", folder_path)
        if not base_folder:
            base_folder = os.getcwd()

        current_year = datetime.now().year
        filename = f"Peajes {current_year} Calculo.xlsx"
        return os.path.join(base_folder, filename), filename

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
            folder_path (str): Default directory if no export folder is configured.
            data (dict): Dictionary containing row data (PDF Name, Page, Amount, etc.)
        """
        file_path, filename = DataService.get_excel_path(folder_path)
        current_year = datetime.now().year

        # Add timestamp
        data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Ensure Total Amount is a number (float)
        # It might come in as a string with formatting (e.g. from the UI entry)
        try:
            val = data.get("Total Amount", 0)
            if isinstance(val, str):
                # Clean up any currency symbols or commas just in case
                val = val.replace("$", "").replace(",", "")
            data["Total Amount"] = float(val)
        except (ValueError, TypeError):
            data["Total Amount"] = 0.0

        try:
            # 1. Determine next sequence number
            next_num = 1
            if os.path.exists(file_path):
                try:
                    df_calc = pd.read_excel(file_path, sheet_name="Calculo", skiprows=1)
                    if not df_calc.empty:
                        last_num = df_calc.iloc[:, 0].max()
                        if pd.notna(last_num):
                            next_num = int(last_num) + 1
                except Exception:
                    next_num = 1

            # 2. Prepare data for Detalle sheet
            # Add sequential 'No.' as the first column
            detail_data = {"No.": next_num}
            detail_data.update(data)
            df_detail_new = pd.DataFrame([detail_data])

            # 3. Prepare data for Calculo sheet
            df_summary_new = pd.DataFrame(
                {
                    "Numero de Peajes": [next_num],
                    "Total en BS": [data.get("Total Amount", 0)],
                }
            )

            # 4. Write to Excel
            if os.path.exists(file_path):
                with pd.ExcelWriter(
                    file_path, mode="a", engine="openpyxl", if_sheet_exists="overlay"
                ) as writer:
                    # Write Summary (Calculo)
                    start_row_summary = 0
                    try:
                        writer.book["Calculo"]
                        start_row_summary = writer.book["Calculo"].max_row
                        df_summary_new.to_excel(
                            writer,
                            sheet_name="Calculo",
                            index=False,
                            header=False,
                            startrow=start_row_summary,
                        )
                    except KeyError:
                        # Create sheet if it somehow disappeared but file exists
                        title_df = pd.DataFrame([[f"Calculo peajes {current_year}"]])
                        title_df.to_excel(
                            writer, sheet_name="Calculo", index=False, header=False
                        )
                        df_summary_new.to_excel(
                            writer,
                            sheet_name="Calculo",
                            index=False,
                            header=True,
                            startrow=1,
                        )

                    # Write Detalle (Detalle)
                    start_row_detail = 0
                    try:
                        writer.book["Detalle"]
                        start_row_detail = writer.book["Detalle"].max_row
                        df_detail_new.to_excel(
                            writer,
                            sheet_name="Detalle",
                            index=False,
                            header=False,
                            startrow=start_row_detail,
                        )
                    except KeyError:
                        df_detail_new.to_excel(
                            writer, sheet_name="Detalle", index=False, header=True
                        )

                    # Apply styling (Centering and Borders)
                    from openpyxl.styles import Alignment, Border, Side
                    thin_border = Border(
                        left=Side(style="thin"),
                        right=Side(style="thin"),
                        top=Side(style="thin"),
                        bottom=Side(style="thin"),
                    )

                    # Style Calculo sheet (headers on row 2)
                    ws_calc = writer.book["Calculo"]
                    for row in ws_calc.iter_rows(min_row=2):
                        for cell in row:
                            cell.alignment = Alignment(horizontal="center")
                            cell.border = thin_border

                    # Style Detalle sheet (headers on row 1)
                    ws_detail = writer.book["Detalle"]
                    for row in ws_detail.iter_rows(min_row=1):
                        for cell in row:
                            cell.alignment = Alignment(horizontal="center")
                            cell.border = thin_border
            else:
                # Create new file
                with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                    # Title row
                    title_df = pd.DataFrame([[f"Calculo peajes {current_year}"]])
                    title_df.to_excel(
                        writer, sheet_name="Calculo", index=False, header=False
                    )

                    # Summary
                    df_summary_new.to_excel(
                        writer,
                        sheet_name="Calculo",
                        index=False,
                        header=True,
                        startrow=1,
                    )

                    # Detail
                    df_detail_new.to_excel(
                        writer, sheet_name="Detalle", index=False, header=True
                    )

                    # Apply styling (Centering and Borders)
                    from openpyxl.styles import Alignment, Border, Side
                    thin_border = Border(
                        left=Side(style="thin"),
                        right=Side(style="thin"),
                        top=Side(style="thin"),
                        bottom=Side(style="thin"),
                    )

                    # Style Calculo sheet
                    ws_calc = writer.book["Calculo"]
                    for row in ws_calc.iter_rows(min_row=2):  # Header and data
                        for cell in row:
                            cell.alignment = Alignment(horizontal="center")
                            cell.border = thin_border

                    # Style Detalle sheet
                    ws_detail = writer.book["Detalle"]
                    for row in ws_detail.iter_rows(min_row=1):  # Header and data
                        for cell in row:
                            cell.alignment = Alignment(horizontal="center")
                            cell.border = thin_border

            return True, f"Saved to {filename}"

        except Exception as e:
            import traceback

            traceback.print_exc()
            print(f"Error saving to Excel: {e}")
            return False, str(e)
