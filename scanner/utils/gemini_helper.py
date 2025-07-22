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
You are a professional application security analyst.

A website security scan has produced the following results:

{formatted_report}

---

🎯 Your task:
1. Explain **what each issue means** in simple terms.
2. Suggest **clear remediation or mitigation steps**.
3. Provide **severity rating** (Low/Medium/High/Critical).
4. Use **bullet points** or markdown formatting for clarity.
"""

        response = model.generate_content(prompt)

        if response.text:
            return response.text.strip()
        else:
            return "⚠️ Gemini returned an empty response. Please try again."

    except Exception as e:
        return f"❌ Gemini analysis failed: {str(e)}"
