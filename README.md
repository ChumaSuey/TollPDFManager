# Toll PDF Manager

A Python application for managing and verifying toll PDF documents with AI assistance and Excel export.

## Features

- **Archive Space**: Browse and manage PDF files naturally sorted.
- **PDF Viewer**: Zoomable viewer with smart navigation (Page & File).
- **AI Analysis**: Extracts toll amounts using Google Gemini AI.
- **Verification**: Calculus pane for manual review and correction.
- **Data Export**: Saves verified data to `Peajes 2026 Calculo.xlsx`.

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

      ```
      GEMINI_API_KEY=your_key_here
      ```

## Usage

- Run `python main.py` to start the application.
- Use **"Analyze with AI"** to check a page.
- Use **"Save & Next"** to log data and move forward.
