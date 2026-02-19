import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        print("Navigating to ASOS...")
        try:
            await page.goto("https://www.asos.com/men/tops/t-shirts-vests/cat/?cid=7616", wait_until="load", timeout=60000)
            await asyncio.sleep(5)
            
            # Extract product links
            data = await page.evaluate('''() => {
                const links = Array.from(document.querySelectorAll('a'))
                                   .map(a => a.href)
                                   .filter(href => href.includes('/prd/'));
                return { links: [...new Set(links)] };
            }''')
            print(f"Found {len(data['links'])} products.")
            with open("asos_links.json", "w") as f:
                json.dump(data, f)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    import os
    os.environ["DISPLAY"] = ":99"
    asyncio.run(main())
