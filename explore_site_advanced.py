import asyncio
import random
import json
from playwright.async_api import async_playwright

async def main(url, name, ua):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent=ua,
            viewport={'width': 1280, 'height': 720},
        )
        page = await context.new_page()
        
        print(f"[{name}] Navigating to {url}...")
        try:
            await page.goto(url, wait_until="load", timeout=90000)
            await asyncio.sleep(10)
            
            title = await page.title()
            print(f"[{name}] Title: {title}")
            
            content = await page.content()
            if "Access Denied" in content or "Just a moment" in content:
                print(f"[{name}] Blocked with UA: {ua}")
            else:
                print(f"[{name}] SUCCESS with UA: {ua}")
                with open(f"{name}_success.html", "w") as f:
                    f.write(content)
            
        except Exception as e:
            print(f"[{name}] Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    name = sys.argv[2]
    # Try Safari on Mac
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
    asyncio.run(main(url, name, ua))
