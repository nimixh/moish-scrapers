import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15")
        page = await context.new_page()
        all_links = []
        for i in range(1, 6): # Get first 5 pages of 4 categories
            for cat in ['men/t-shirts', 'women/t-shirts', 'men/oversized-t-shirts', 'women/oversized-t-shirts']:
                url = f"https://www.thesouledstore.com/{cat}?page={i}"
                print(f"Fetching {url}")
                try:
                    await page.goto(url, wait_until="load")
                    await asyncio.sleep(3)
                    links = await page.evaluate('''() => Array.from(document.querySelectorAll('a')).map(a => a.href).filter(h => h.includes('/product/'))''')
                    all_links.extend(links)
                except: pass
        all_links = list(set(all_links))
        print(f"Found {len(all_links)} TSS links")
        with open('tss_links.json', 'w') as f:
            json.dump({'links': all_links}, f)
        await browser.close()

if __name__ == "__main__":
    import os
    os.environ["DISPLAY"] = ":99"
    asyncio.run(main())
