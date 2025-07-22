import google.generativeai as genai
import os
from typing import Union

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("❌ GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini Pro model
model = genai.GenerativeModel("gemini-2.0-flash")

def get_gemini_remediation(scan_report: Union[dict, str]) -> str:
    try:
        if isinstance(scan_report, dict):
            formatted_report = f"```json\n{scan_report}\n```"
        else:
            formatted_report = scan_report  # fallback if already string

        prompt = f"""
You are an expert security analyst.

A website scan report is given below:

{formatted_report}

---
🎯 Your job:
Give a ** short summary** of issues (2-3 line per issue) with:
- 🔧 **Simple Fix** (two line)
- 🛑 **Severity** (Low/Medium/High/Critical)

Use bullet points (•). No long explanations. No repetition. Limit output to max 20-25 lines if possible.
"""

        response = model.generate_content(prompt)

        return response.text.strip() if response.text else "⚠️ Gemini returned an empty response."

    except Exception as e:
        return f"❌ Gemini analysis failed: {str(e)}"
