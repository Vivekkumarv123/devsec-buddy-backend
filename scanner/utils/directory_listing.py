import requests

def check_directory_listing(url):
    result = {
        "enabled": False,
        "details": ""
    }

    try:
        if not url.endswith("/"):
            url += "/"

        response = requests.get(url, timeout=10)

        directory_keywords = [
            "Index of /",
            "<title>Index of",
            "Directory listing for",
            "Parent Directory"
        ]

        for keyword in directory_keywords:
            if keyword.lower() in response.text.lower():
                result["enabled"] = True
                result["details"] = f"Directory listing is enabled. Found keyword: '{keyword}'"
                return result

        result["details"] = "Directory listing not detected."

    except Exception as e:
        result["enabled"] = None
        result["details"] = f"Error checking directory listing: {str(e)}"

    return result
