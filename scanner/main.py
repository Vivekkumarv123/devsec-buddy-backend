import os
import sys
import json

# Ensure "utils" is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.headers import check_security_headers
from utils.xss import check_xss
from utils.sql_injection import check_sql_injection

def main():
    if len(sys.argv) != 2:
        print(json.dumps({'error': 'URL argument required'}))
        return

    url = sys.argv[1]

    result = {
        'url': url,
        'headers': check_security_headers(url),
        'xss': check_xss(url),
        'sql_injection': check_sql_injection(url),
    }

    print(json.dumps(result))

if __name__ == '__main__':
    main()
