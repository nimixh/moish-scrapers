from curl_cffi import requests

proxy = "http://abqimktx-rotate:q6neqerkmvn6@p.webshare.io:80"

try:
    print("Testing Myntra with curl_cffi + proxy...")
    r = requests.get(
        "https://www.myntra.com/men-tshirts", 
        proxy=proxy,
        impersonate="chrome",
        timeout=15
    )
    print(f"Myntra Status: {r.status_code}")
    if r.status_code == 200:
        print("Success!")
except Exception as e:
    print(f"Error: {e}")
