import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Mobile User Agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
        )
        page = await context.new_page()
        print("Navigating to product page with Mobile UA...")
        await page.goto("https://www.threadless.com/shop/@lousydrawingsforgoodpeople/design/wisdom")
        
        for i in range(15):
            await page.wait_for_timeout(2000)
            content = await page.content()
            if "Performing security verification" not in content:
                print("CF Cleared!")
                break
            print(f"Waiting... {i}")
        
        content = await page.content()
        with open("threadless_product_mobile.html", "w") as f:
            f.write(content)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
