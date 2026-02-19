import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Intercept GraphQL requests
        async def handle_request(request):
            if "graphql" in request.url:
                print(f"GraphQL Request: {request.url}")
                # print(f"Post Data: {request.post_data}")
        
        async def handle_response(response):
            if "graphql" in response.url:
                try:
                    data = await response.json()
                    # Look for product search results
                    if 'data' in data:
                        with open("redbubble_graphql_sample.json", "w") as f:
                            json.dump(data, f, indent=2)
                        print("Saved GraphQL response sample!")
                except:
                    pass

        page.on("request", handle_request)
        page.on("response", handle_response)

        print("Navigating to Redbubble...")
        try:
            await page.goto("https://www.redbubble.com/shop/t-shirts", wait_until="load", timeout=90000)
            await asyncio.sleep(20) # Give time for CF and GraphQL
            await page.screenshot(path="redbubble_intercept_screenshot.png")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    import os
    os.environ["DISPLAY"] = ":99"
    asyncio.run(main())
