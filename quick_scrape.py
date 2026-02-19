import asyncio
import json
from curl_cffi import requests
from datetime import datetime

async def scrape_teepublic():
    proxy = "http://abqimktx-rotate:q6neqerkmvn6@p.webshare.io:80"
    base_url = "https://www.teepublic.com"
    r = requests.get(base_url + "/t-shirts?sort=popular", proxy=proxy, impersonate="chrome")
    import re
    links = re.findall(r'href="(/t-shirt/.*?)"', r.text)
    links = [base_url + l for l in set(links)]
    count = 0
    for url in links[:20]:
        try:
            r = requests.get(url, proxy=proxy, impersonate="chrome", timeout=10)
            if r.status_code == 200:
                match = re.search(r'dataLayer\.push\((\{.*?\})\)', r.text)
                if match:
                    raw_data = json.loads(match.group(1))
                    data = {'title': raw_data.get('design__design_title'), 'source': 'teepublic', 'url': url}
                    with open("teepublic_quick.jsonl", "a") as f:
                        f.write(json.dumps(data) + "\n")
                    count += 1
        except: pass
    print(f"TeePublic: {count}")

async def main():
    await scrape_teepublic()

if __name__ == "__main__":
    asyncio.run(main())
