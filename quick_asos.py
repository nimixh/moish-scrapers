import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15")
        page = await context.new_page()
        await page.goto("https://www.asos.com/men/tops/t-shirts-vests/cat/?cid=7616", wait_until="load")
        links = await page.evaluate('''() => Array.from(document.querySelectorAll('a')).map(a => a.href).filter(h => h.includes('/prd/'))''')
        count = 0
        for url in list(set(links))[:20]:
            p_page = await context.new_page()
            try:
                await p_page.goto(url, wait_until="load", timeout=30000)
                title = await p_page.title()
                if "ASOS" in title:
                    with open("asos_quick.jsonl", "a") as f:
                        f.write(json.dumps({'title': title, 'source': 'asos', 'url': url}) + "\n")
                    count += 1
            except: pass
            finally: await p_page.close()
        await browser.close()
    print(f"ASOS: {count}")

if __name__ == "__main__":
    import os
    os.environ["DISPLAY"] = ":99"
    asyncio.run(main())
