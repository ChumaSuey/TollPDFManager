from google import genai
import os
from dotenv import load_dotenv

# Load .env from project root (2 levels up from scripts/debug)
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(root_dir, '.env'))

api_key = os.getenv("GEMINI_API_KEY")
print(f"Key loaded: {api_key[:5]}...")

try:
    client = genai.Client(api_key=api_key)
    print("Listing models...")
    # The new SDK might have a different way to list, but let's try standard iteration
    # or client.models.list()
    
    # Check if models.list exists or we need to access via http
    # Documentation for google-genai is sparse in training data, but follows resource patterns
    
    pager = client.models.list() 
    with open("models_list.txt", "w") as f:
        for model in pager:
            print(f"Model Name: {model.name}")
            f.write(f"{model.name}\n")
        
except Exception as e:
    print(f"Error: {e}")
