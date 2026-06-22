import os
import json
import google.generativeai as genai


API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )
else:
    model = None


def classify_merchants(merchants):

    # Gemini not configured
    if not model:
        return None

    if not merchants:
        return {}

    prompt = f"""
Assign exactly ONE category to each merchant.

Allowed Categories:

Food
Shopping
Travel
Transport
Utilities
Cash Withdrawal
Entertainment
Other

Return ONLY valid JSON.

Example:

{{
    "Swiggy": "Food",
    "Amazon": "Shopping",
    "Uber": "Transport"
}}

Merchants:

{merchants}
"""

    try:

        response = model.generate_content(
            prompt
        )

        text = response.text.strip()

        # Remove markdown code blocks if Gemini adds them
        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        return json.loads(text)

    except Exception as e:

        print(
            f"Gemini categorization failed: {e}"
        )

        return None