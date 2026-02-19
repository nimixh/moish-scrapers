import cloudscraper

scraper = cloudscraper.create_scraper()
try:
    print("Attempting to fetch Threadless with cloudscraper...")
    response = scraper.get("https://www.threadless.com/designs")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success! First 500 chars of content:")
        print(response.text[:500])
    else:
        print("Blocked or other error.")
except Exception as e:
    print(f"Error: {e}")
