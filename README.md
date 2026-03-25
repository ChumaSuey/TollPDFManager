# Toll PDF Manager

A Python application for managing and verifying toll PDF documents with AI assistance and Excel export.

## Features

- **Archive Space**: Browse and manage PDF files naturally sorted.
- **PDF Viewer**: Zoomable viewer with smart navigation (Page & File).
- **AI Analysis**: Extracts toll amounts using Google Gemini AI.
- **Verification**: Calculus pane for manual review and correction.
- **Data Export**: Saves verified data to `Peajes [Year] Calculo.xlsx` with professional formatting (Sequential numbering, Title headers, and a separate Detail sheet).

## Setup

1. **Install Python 3.10+**
2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure API Key**:
    - Get a Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/).
    - Create a file named `.env` in this folder.
    - Add the line:

      ```text
      GEMINI_API_KEY=your_key_here
      ```

## 🏗️ Build

To create a standalone executable:

1. **Install PyInstaller**: `pip install pyinstaller`
2. **Build**: `pyinstaller TollPDFManager.spec`
3. The executable will be generated in the `dist/` folder.

## Usage

- Run `python main.py` to start the application.
- Use **"Analyze with AI"** to check a page.
- Use **"Save & Next"** to log data and move forward.

## ⌨️ Keyboard Shortcuts

For a complete list of keyboard shortcuts and productivity tips, see [KEYBINDS.md](file:///c:/Users/luism/PycharmProjects/TollPDFManager/KEYBINDS.md).

## 📁 Project Structure

- `gui/`: Application interface components.
- `services/`: Core logic and AI integration.
- `utils/`: Common utility functions.
- `scripts/`: Auxiliary maintenance and debug scripts (e.g., `debug_models.py`).
- `tests/`: Automated test suite.
