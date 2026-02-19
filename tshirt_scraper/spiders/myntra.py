import scrapy
from tshirt_scraper.items import TshirtItem
from datetime import datetime
import json

class MyntraSpider(scrapy.Spider):
    name = "myntra"
    allowed_domains = ["myntra.com"]
    start_urls = ["https://www.myntra.com/men-tshirts"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                },
                callback=self.parse_listing
            )

    async def parse_listing(self, response):
        page = response.meta["playwright_page"]
        try:
            # Simulate human scroll to load items
            for i in range(5):
                await page.mouse.wheel(0, 1000)
                await page.wait_for_timeout(2000)
            
            links = await page.evaluate('''() => {
                const links = Array.from(document.querySelectorAll('a'))
                                   .map(a => a.href)
                                   .filter(href => href.includes('/tshirts/') || href.includes('myntra.com/'));
                // Filter specifically for product links
                return [...new Set(links)].filter(h => /\/\d+\/buy$/.test(h) || h.includes('/prd/'));
            }''')
            
            if not links:
                # Try generic link extraction
                links = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('.product-base a')).map(a => a.href);
                }''')

            self.logger.info(f"Found {len(links)} links on Myntra")
            for link in links[:100]:
                yield scrapy.Request(
                    link,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                    },
                    callback=self.parse_product
                )
        finally:
            await page.close()

    async def parse_product(self, response):
        page = response.meta.get("playwright_page")
        if not page: return
        try:
            await page.wait_for_timeout(5000)
            data = await page.evaluate('''() => {
                const results = {};
                results.title = document.querySelector('.pdp-title')?.innerText;
                results.name = document.querySelector('.pdp-name')?.innerText;
                results.price = document.querySelector('.pdp-price strong')?.innerText;
                results.description = document.querySelector('.pdp-product-description-content')?.innerText;
                results.images = Array.from(document.querySelectorAll('.pdp-image-container img')).map(img => img.src);
                return results;
            }''')
            
            if not data or not data.get('title'):
                return

            item = TshirtItem()
            item['id'] = response.url.split('/')[-2]
            item['source'] = 'myntra'
            item['url'] = response.url
            item['scraped_at'] = datetime.utcnow().isoformat()
            item['product'] = {
                'title': f"{data.get('title')} {data.get('name')}",
                'brand': data.get('title'),
                'garment_type': 't-shirt',
                'price': data.get('price'),
                'currency': 'INR',
            }
            item['design'] = {
                'description': data.get('description', ''),
                'tags': [],
            }
            item['images'] = {
                'primary': data.get('images')[0] if data.get('images') else None,
                'all': data.get('images')
            }
            item['image_urls'] = data.get('images')[:2]
            yield item
        finally:
            await page.close()
