from curl_cffi import requests

try:
    print("Testing Redbubble with curl_cffi...")
    # Use a real browser-like request
    r = requests.get(
        "https://www.redbubble.com/shop/t-shirts", 
        impersonate="chrome",
        headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }
    )
    print(f"Status: {r.status_code}")
    with open("redbubble_test.html", "w") as f:
        f.write(r.text)
except Exception as e:
    print(f"Error: {e}")
