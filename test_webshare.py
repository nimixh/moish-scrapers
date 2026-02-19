import requests

proxy = "http://abqimktx-rotate:q6neqerkmvn6@p.webshare.io:80"
proxies = {"http": proxy, "https": proxy}

try:
    print("Testing Webshare proxy...")
    r = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10)
    print(f"Proxy IP: {r.json()}")
    
    # Test on a blocked site
    print("Testing on Redbubble...")
    r = requests.get("https://www.redbubble.com/shop/t-shirts", proxies=proxies, timeout=10, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"})
    print(f"Redbubble Status: {r.status_code}")
except Exception as e:
    print(f"Error: {e}")
