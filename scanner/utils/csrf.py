# csrf.py

import requests
import re

def check_csrf_token_presence(url):
    try:
        res = requests.get(url, timeout=10, headers={"User-Agent": "DevSecBuddyScanner"})
        html = res.text

        # Look for hidden input fields with CSRF-ish names
        token_names = [
            "csrfmiddlewaretoken",
            "_csrf",
            "csrf_token",
            "__RequestVerificationToken"
        ]

        token_found = False
        tokens_detected = []

        for token in token_names:
            pattern = rf'<input[^>]+name=["\']{token}["\']'
            if re.search(pattern, html, re.IGNORECASE):
                token_found = True
                tokens_detected.append(token)

        if token_found:
            return {
                "status": "protected",
                "tokens_detected": tokens_detected,
                "severity": "low"
            }
        else:
            return {
                "status": "no_token_found",
                "recommendation": "Implement CSRF tokens in forms and APIs.",
                "severity": "medium"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "severity": "unknown"
        }

def check_csrf_exploitability(
    url,
    method="POST",
    data=None,
    headers=None,
    cookies=None
):
    try:
        headers = headers or {"User-Agent": "DevSecBuddyScanner"}
        cookies = cookies or {}

        # Send forged request without CSRF token
        response = requests.request(
            method=method,
            url=url,
            data=data,
            headers=headers,
            cookies=cookies,
            allow_redirects=False,
            timeout=10
        )

        status = response.status_code
        body = response.text.lower()

        # Very naive way to guess if CSRF succeeded
        if status in [200, 302, 201] and not any(x in body for x in ["csrf", "token required", "forbidden", "unauthorized"]):
            return {
                "status": "vulnerable",
                "message": "Endpoint allowed state-changing request without CSRF protection.",
                "severity": "high",
                "response_snippet": body[:300]
            }
        else:
            return {
                "status": "protected",
                "message": "CSRF protection appears to be in place.",
                "severity": "low"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "severity": "unknown"
        }