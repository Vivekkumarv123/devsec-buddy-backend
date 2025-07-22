import requests

def check_clickjacking(url):
    result = {
        "vulnerable": False,
        "details": ""
    }

    try:
        response = requests.get(url, timeout=10)
        x_frame = response.headers.get("X-Frame-Options", "").lower()
        csp = response.headers.get("Content-Security-Policy", "").lower()

        if "deny" in x_frame or "sameorigin" in x_frame:
            result["vulnerable"] = False
            result["details"] = f"Protected by X-Frame-Options: {x_frame}"
        elif "frame-ancestors" in csp:
            result["vulnerable"] = False
            result["details"] = f"Protected by CSP: {csp}"
        else:
            result["vulnerable"] = True
            result["details"] = "Missing clickjacking protection headers."

    except Exception as e:
        result["vulnerable"] = None
        result["details"] = f"Error while checking: {str(e)}"

    return result
