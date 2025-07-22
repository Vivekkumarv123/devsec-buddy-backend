import requests
import socket

CLOUD_PROVIDERS_SIGNATURES = {
    "github.io": "There isn't a GitHub Pages site here.",
    "herokuapp.com": "No such app",
    "amazonaws.com": "NoSuchBucket",
    "bitbucket.io": "Repository not found",
    "ghost.io": "The thing you were looking for is no longer here",
    "tumblr.com": "There's nothing here.",
    "wordpress.com": "Do you want to register"
}

def check_subdomain_takeover(url):
    result = {
        "vulnerable": False,
        "details": ""
    }

    try:
        domain = url.replace("http://", "").replace("https://", "").split("/")[0]

        ip = socket.gethostbyname(domain)
        response = requests.get(url, timeout=10)

        for provider, signature in CLOUD_PROVIDERS_SIGNATURES.items():
            if provider in domain and signature.lower() in response.text.lower():
                result["vulnerable"] = True
                result["details"] = f"Potential subdomain takeover via {provider} – signature found."
                return result

        result["details"] = "No known takeover signatures found."

    except socket.gaierror:
        result["vulnerable"] = True
        result["details"] = "DNS resolution failed. Potential dangling CNAME record."

    except Exception as e:
        result["vulnerable"] = None
        result["details"] = f"Error while checking: {str(e)}"

    return result
