import requests

def check_xss(url):
    try:
        test_param = "<script>alert('xss')</script>"
        test_url = f"{url}?q={test_param}"

        response = requests.get(test_url, timeout=5)

        if test_param in response.text:
            return "vulnerable"
        else:
            return "safe"
    except Exception as e:
        return f"error: {str(e)}"
