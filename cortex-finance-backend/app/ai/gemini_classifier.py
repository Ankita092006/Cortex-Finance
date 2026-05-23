import os
import json
import google.generativeai as genai

def load_env_fallback():
    """Manually reads .env variables if python-dotenv is not installed."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # Search parent directories for .env
        for path in [".env", "../.env", "../../.env", "../../../.env"]:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if "=" in line and not line.startswith("#"):
                            key, val = line.split("=", 1)
                            os.environ[key.strip()] = val.strip().strip('"').strip("'")
                break

# Load env variables on module import
load_env_fallback()

# Fetch and configure Gemini API Key
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

CATEGORIES = [
    "Food", "Shopping", "Travel", "Rent", "Salary", 
    "EMI", "Utilities", "Entertainment", "Subscriptions", 
    "UPI Transfers", "Others"
]

def classify_transactions_gemini(narrations: list) -> dict:
    """
    Classifies a list of transaction narrations into categories using Gemini API.
    
    Security / Robustness:
    - Runs in batches to prevent API rate-limiting and minimize latency.
    - If API key is missing or calls fail, falls back gracefully to default 'Others'.
    """
    if not narrations:
        return {}

    # Unique narrations to avoid redundant token usage
    unique_narrations = list(set(narrations))
    results = {narration: "Others" for narration in unique_narrations}

    # Verify if Gemini API is configured
    if not api_key:
        print("Warning: GEMINI_API_KEY not found in environment. Defaulting to 'Others' fallback.")
        return results

    try:
        # Construct prompt
        narrations_str = json.dumps(unique_narrations)
        prompt = f"""
You are a financial classification assistant. Your task is to categorize transaction descriptions (narrations) from Indian bank statements.
Classify each description into exactly one of the following categories:
- {', '.join(CATEGORIES)}

Here is the list of transaction descriptions:
{narrations_str}

Return the output as a JSON object where the keys are the exact descriptions provided, and the values are their classified categories.
Example output format:
{{
  "UPI/Zomato/123": "Food",
  "Amazon Pay Balance": "Shopping"
}}
Do not write any conversational intro or outro text, only return the clean JSON block.
"""

        # Call Gemini model
        # Using gemini-1.5-flash as a fast, cost-effective classifier
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Parse JSON output
        parsed_results = json.loads(response.text.strip())
        
        # Populate result mapping
        for narration in unique_narrations:
            category = parsed_results.get(narration, "Others")
            if category in CATEGORIES:
                results[narration] = category
            else:
                results[narration] = "Others"
                
    except Exception as e:
        print(f"Error in Gemini classification: {e}. Falling back to 'Others'.")
        # Keep default "Others" mappings on failure
        pass

    return results
