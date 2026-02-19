import asyncio
import random
from playwright.async_api import async_playwright
from playwright_stealth import stealth

async def main(url, name):
    async with async_playwright() as p:
        # Using a realistic user agent and viewport
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            device_scale_factor=1,
        )
        page = await context.new_page()
        
        # Apply stealth
        stealth(page)
        
        print(f"Navigating to {url}...")
        try:
            # Add some random delay before navigation
            await asyncio.sleep(random.uniform(1, 3))
            await page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Wait for potential CF challenge
            print("Waiting for page to settle...")
            for i in range(20):
                await asyncio.sleep(2)
                content = await page.content()
                if "Performing security verification" not in content and "challenge-platform" not in content:
                    print(f"[{name}] Likely cleared CF or not present.")
                    break
                print(f"[{name}] Still seeing challenge... {i}")
                
            # Take screenshot and save HTML
            await page.screenshot(path=f"{name}_screenshot.png")
            content = await page.content()
            with open(f"{name}_rendered.html", "w") as f:
                f.write(content)
            print(f"[{name}] Saved content and screenshot.")
            
        except Exception as e:
            print(f"[{name}] Error: {e}")
        finally:
            await browser.close()

async def run_all():
    tasks = [
        main("https://www.threadless.com/shop/@lousydrawingsforgoodpeople/design/wisdom", "threadless"),
        main("https://www.teepublic.com/t-shirt/5123456-example", "teepublic"),
        main("https://www.redbubble.com/i/t-shirt/Example-by-Artist/12345678.ASOSL", "redbubble")
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run_all())
