import requests

def check_sql_injection(url):
    try:
        payload = "' OR '1'='1"
        test_url = f"{url}?id={payload}"

        response = requests.get(test_url, timeout=5)

        indicators = ["sql", "mysql", "syntax", "error", "warning", "database"]
        if any(word in response.text.lower() for word in indicators):
            return "vulnerable"
        else:
            return "safe"
    except Exception as e:
        return f"error: {str(e)}"
