from curl_cffi import requests

proxy = "http://abqimktx-rotate:q6neqerkmvn6@p.webshare.io:80"

try:
    print("Testing Redbubble with curl_cffi + proxy...")
    r = requests.get(
        "https://www.redbubble.com/shop/t-shirts", 
        proxy=proxy,
        impersonate="chrome",
        timeout=15
    )
    print(f"Redbubble Status: {r.status_code}")
    if r.status_code == 200:
        print("Success!")
    else:
        print(f"Failed: {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
