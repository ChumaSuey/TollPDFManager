# Toll PDF Manager - Detailed Walkthrough

This guide explains how to use the application effectively for your daily workflow.

## 🌟 Core Features

### 1. Navigation (Viewer)

- **Smart Scroll**: Clicking "Next >" at the end of a document automatically loads the *next PDF file* in the folder.
- **Zoom**: Use the **🔍-** / **🔍+** buttons or `Ctrl + MouseWheel` to inspect stamps closely.
- **Reset**: Click **"1:1"** to instantly restore default 100% zoom. Zoom level is remembered as you browse.

### 2. The Calculator (Right Pane)

This is your command center. It offers three ways to work:

#### A. AI Assisted (Fastest) ⚡

1. Click **"✨ Analyze with AI"**.
2. The AI reads the page and lists found stamps in the table.
3. The **"Page Total (Calculated)"** updates automatically.
4. If it looks correct, just click **"Save & Next"**.

#### B. Manual Correction (Precision) 🛠️

If the AI makes a mistake or misses a stamp:

- **Add**: Type `Amount` and `Qty` in the Manual Entry box and click **"Add"**.
- **Edit**: Select a row in the list -> Click **"Edit Selected"** -> Update values -> Click **"Update"**.
- **Delete**: Select a row and click **"Delete Selected"**.
- **Clear**: Click **"Clear All"** to wipe the current page's data.

#### C. Manual Override (The "Boss" Mode) 👑

If the list calculation is slightly off but you know the real total:

- Type the correct amount in the **"Verified Value (Manual)"** box.
- **Priority Rule**: When you save, the system *always* prefers your "Verified Value" over the calculated one.

### 3. Safety Features 🛡️

- **Read-Only Total**: You cannot accidentally type over the calculated total. Use the Override box instead.
- **Auto-Clear**: When you switch pages, the calculator wipes itself clean. You never have to worry about saving the previous page's data to the wrong page.
- **Flag for Review**: See a weird page? Click **"Flag for Review"**.
  - It signals the file with a **🚩** icon in the file list.
  - **Persistence**: Flags are saved automatically, so you can come back to them later even after restarting the app.
  - Click **"Unflag"** to remove it once resolved.

## 💾 Data Saving

- Clicking **"Save & Next"** saves the current page's total to Excel.
- **Dynamic Filename**: The app automatically saves to `Peajes [Current Year] Calculo.xlsx` (e.g., `Peajes 2026 Calculo.xlsx`). It handles the year change automatically!
- **Professional Formatting**:
  - **Calculo (Summary)**: A clean summary sheet with a Title row and columns for "Numero de Peajes" (auto-incremented) and "Total en BS".
  - **Detalle (Record)**: A background sheet that preserves the PDF Name, Page Number, and Timestamp for every entry to ensure full traceability.

## 🚀 Pro Tips

- **Speed Run**: If the AI is consistently right, you can just spam **Analyze** -> **Save & Next** -> **Analyze** -> **Save & Next**.
- **Shortcuts**:
  - `Left/Right Arrow`: Prev/Next Page.
  - `Ctrl + Wheel`: Zoom.
  - `Ctrl + Wheel`: Zoom.
  - `Ctrl + H`: Toggle Highlight (Yellow marker).
  - **Calculator Shortcuts**:
    - **Double-Click**: Inline edit (Amount/Qty).
    - `Enter`: Save entry (Inline or Manual).
    - `Esc`: Cancel editing / Clear inputs.
    - `Delete`: Remove selected item.

### 4. Highlight Function 📌

The **highlight** function serves as an internal marker for you to know where to start or track your progress within the toll list.

- **How to use**: Select a PDF and click the **📌 Highlight Item** button, or press `Ctrl + H`.
- **Effect**: The selected item in the "Archive Space" list will be highlighted with a soft yellow background.
- **Toggle**: Click **📍 Unhighlight** or press `Ctrl + H` again to remove the marker.

### 5. Processed Tracking ✅

The app automatically tracks which files have been saved to the Excel export.

- **Visual Indicator**: Files that have been processed will appear with a **Green Checkmark (✅)** in the file list.
- **Automatic Update**: When you click "Save & Next", the current file is immediately marked as processed.
- **Persistence**: This status is read directly from your Excel file, so it remembers your progress even if you restart the app.
