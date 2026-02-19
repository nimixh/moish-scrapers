from curl_cffi import requests

try:
    print("Attempting to fetch Threadless with curl_cffi...")
    response = requests.get("https://www.threadless.com/designs", impersonate="chrome")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success! First 500 chars of content:")
        print(response.text[:500])
    else:
        print(f"Blocked or other error: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
