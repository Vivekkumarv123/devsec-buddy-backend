# main.py

import json
import sys
from utils.headers import check_security_headers
from utils.xss import check_xss
from utils.sql_injection import check_sql_injection
from utils.csrf import check_csrf_token_presence, check_csrf_exploitability
from utils.redirect import check_open_redirect
from utils.clickjacking import check_clickjacking
from utils.subdomain_takeover import check_subdomain_takeover
from utils.directory_listing import check_directory_listing
from utils.gemini_helper import get_gemini_remediation

def run_scan(url, profile="basic", method="GET", data=None, headers=None, cookies=None):
    results = {}

    # Normalize method to uppercase
    method = method.upper()

    # BASIC PROFILE SCANS
    results["security_headers"] = check_security_headers(url)
    results["clickjacking"] = check_clickjacking(url)

    # STANDARD PROFILE SCANS
    if profile in ["standard", "deep"]:
        results["xss"] = check_xss(url)
        results["sql_injection"] = check_sql_injection(url)
        results["open_redirect"] = check_open_redirect(url)
        results["directory_listing"] = check_directory_listing(url)

        # CSRF dual scan
        results["csrf"] = {
            "presence": check_csrf_token_presence(url),
            "exploitability": check_csrf_exploitability(
                url=url,
                method=method,
                data=data,
                headers=headers,
                cookies=cookies
            )
        }

    # DEEP PROFILE EXTRAS
    if profile == "deep":
        results["subdomain_takeover"] = check_subdomain_takeover(url)

    return results


if __name__ == "__main__":
    try:
        input_data = json.loads(sys.stdin.read())
        url = input_data.get("url")
        profile = input_data.get("profile", "basic")
        method = input_data.get("method", "POST")
        data = input_data.get("data")
        headers = input_data.get("headers")
        cookies = input_data.get("cookies")

        scan_results = run_scan(url, profile, method, data, headers, cookies)
        gemini_response = get_gemini_remediation(scan_results)
        final_output = {
            "scan_results": scan_results,
            "gemini_remediation": gemini_response
        }
        print(json.dumps(final_output, indent=2))

    except Exception as e:
        print(json.dumps({
            "error": str(e),
            "status": "scan_failed"
        }))
