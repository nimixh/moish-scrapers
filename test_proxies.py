import requests

proxies_list = [
    "http://144.126.155.60:3128",
    "http://20.211.60.173:80",
    "http://103.170.153.11:8080",
]

for proxy in proxies_list:
    try:
        print(f"Testing {proxy}...")
        r = requests.get("https://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
        print(f"Success! IP: {r.json()}")
    except Exception as e:
        print(f"Failed: {e}")

