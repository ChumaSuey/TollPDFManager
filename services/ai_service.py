import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class TollAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None

        if self.api_key:
            # Debug: Print masked key to verify what is loaded
            masked = (
                f"{self.api_key[:4]}...{self.api_key[-4:]}"
                if len(self.api_key) > 8
                else "****"
            )
            print(f"AI Service loaded Key: {masked}")

            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to initialize GenAI Client: {e}")
        else:
            print("Warning: GEMINI_API_KEY not found in environment.")

    def analyze_page(self, image_data):
        """
        Analyzes a PDF page image to extract toll data using Gemini.

        Args:
            image_data: PIL Image object of the PDF page.

        Returns:
            dict: Extracted data (list of tolls, total amount).
        """
        if not self.client:
            return {"error": "API Key missing or Client init failed", "tolls": []}

        try:
            prompt = """
            Analyze this image of a toll report.
            Identify all toll amounts found on the page.
            Group the tolls by their amount.
            
            Return ONLY a JSON response with this structure:
            {
                "tolls": [
                    {"amount": 5.50, "quantity": 2},
                    {"amount": 3.00, "quantity": 5}
                ]
            }
            Do not include markdown formatting (```json), just the raw JSON string.
            If no tolls are found, return {"tolls": []}.
            """

            # New SDK call structure
            # model='gemini-2.0-flash'
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents=[prompt, image_data]
            )

            text = response.text.strip()

            # Clean up potential markdown code blocks
            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "")

            data = json.loads(text)

            # Calculate total locally
            tolls = data.get("tolls", [])
            total = sum(t.get("amount", 0) * t.get("quantity", 0) for t in tolls)

            return {"tolls": tolls, "total_calculated": total}

        except Exception as e:
            print(f"AI Analysis failed: {e}")
            return {"error": str(e), "tolls": []}

    def verify_calculation(self, extracted_data, user_total):
        """
        Compares AI extracted total with user provided total.
        """
        ai_total = extracted_data.get("total_calculated", 0.0)
        match = abs(ai_total - user_total) < 0.01
        return {"match": match, "difference": ai_total - user_total}
