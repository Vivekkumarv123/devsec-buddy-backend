import re
from urllib.parse import urlparse


def check_open_redirect(url):
    """
    Detects potential open redirect vulnerabilities by checking:
    - URLs that redirect to external domains based on user input (e.g., ?next=http://evil.com)
    - Dangerous query parameters like 'redirect', 'next', 'url', 'continue'
    """

    parsed_url = urlparse(url)
    query = parsed_url.query.lower()

    # Regex pattern to detect redirect params pointing to external domains
    redirect_patterns = [
        r'(redirect|url|next|continue)=(http|https)%3A%2F%2F',   # encoded URLs
        r'(redirect|url|next|continue)=(http|https):\/\/',       # plain URLs
        r'(redirect|url|next|continue)=\/\/'                     # protocol-relative
    ]

    for pattern in redirect_patterns:
        if re.search(pattern, query):
            return {
                "vulnerability": "Open Redirect",
                "severity": "High",
                "description": f"Possible open redirect found in query: '{pattern}'",
                "recommendation": "Avoid using unvalidated redirect URLs in parameters like 'next', 'redirect', or 'url'. Always validate redirect domains."
            }

    return None
