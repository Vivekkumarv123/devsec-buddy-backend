import requests

def check_security_headers(url):
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        expected_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Referrer-Policy",
            "Permissions-Policy"
        ]

        missing = []
        for header in expected_headers:
            if header not in headers:
                missing.append(header)

        return {
            "status_code": response.status_code,
            "missing": missing,
            "present": [h for h in expected_headers if h in headers]
        }
    except Exception as e:
        return { "error": str(e) }
