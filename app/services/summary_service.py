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


def generate_summary(summary_data):

    # Gemini not configured
    if not model:
        return None

    prompt = f"""
Generate ONLY valid JSON.

Required fields:

{{
    "total_spend_inr": number,
    "total_spend_usd": number,
    "top_merchants": object,
    "anomaly_count": number,
    "narrative": string,
    "risk_level": string
}}

Risk Level must be:

low
medium
high

Input Data:

{summary_data}
"""

    try:

        response = model.generate_content(
            prompt
        )

        text = response.text.strip()

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
            f"Gemini summary failed: {e}"
        )

        return None