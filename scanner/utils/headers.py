# headers.py

import requests

SECURITY_HEADERS = {
    "Content-Security-Policy": "high",
    "Strict-Transport-Security": "high",
    "X-Content-Type-Options": "medium",
    "X-Frame-Options": "medium",
    "X-XSS-Protection": "medium",
    "Referrer-Policy": "low",
    "Permissions-Policy": "low"
}

def check_security_headers(url):
    try:
        response = requests.get(url, timeout=10)
        present = []
        missing = []

        for header, severity in SECURITY_HEADERS.items():
            if header in response.headers:
                present.append(header)
            else:
                missing.append(header)

        return {
            "status_code": response.status_code,
            "present": present,
            "missing": missing,
            "severity": "medium" if missing else "safe"
        }
    except Exception as e:
        return {
            "error": f"Header check failed: {str(e)}",
            "severity": "critical"
        }
