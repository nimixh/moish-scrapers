import scrapy
from tshirt_scraper.items import TshirtItem
from datetime import datetime
import json

class TheSouledStoreSpider(scrapy.Spider):
    name = "thesouledstore"
    allowed_domains = ["thesouledstore.com"]
    start_urls = ["https://www.thesouledstore.com/men/t-shirts?page=1"]

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
            # Scroll to load more
            for _ in range(3):
                await page.mouse.wheel(0, 2000)
                await page.wait_for_timeout(2000)

            links = await page.evaluate('''() => {
                const links = Array.from(document.querySelectorAll('a'))
                                   .map(a => a.href)
                                   .filter(href => href.includes('/product/'));
                return [...new Set(links)];
            }''')
            
            self.logger.info(f"Found {len(links)} links on page {response.url}")
            
            for link in links:
                yield scrapy.Request(
                    link,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                    },
                    callback=self.parse_product
                )
            
            # Pagination
            current_page = int(response.url.split('page=')[-1])
            if current_page < 10: # Get up to 10 pages
                next_page = f"https://www.thesouledstore.com/men/t-shirts?page={current_page + 1}"
                yield scrapy.Request(
                    next_page,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                    },
                    callback=self.parse_listing
                )
        finally:
            await page.close()

    async def parse_product(self, response):
        page = response.meta.get("playwright_page")
        if not page: return
        try:
            await page.wait_for_timeout(3000)
            data = await page.evaluate('''() => {
                const results = {};
                results.title = document.querySelector('h1')?.innerText;
                results.price = document.querySelector('.offerPrice')?.innerText || 
                                document.querySelector('.offer')?.innerText;
                results.description = document.querySelector('.product-details-content')?.innerText || 
                                      document.querySelector('.accordiontabs')?.innerText;
                results.images = Array.from(document.querySelectorAll('img'))
                                    .map(img => img.src)
                                    .filter(src => src.includes('catalog/product') && src.includes('w=480'));
                results.artist = document.querySelector('.artist-details-content')?.innerText;
                results.tags = Array.from(document.querySelectorAll('.tags-list a')).map(a => a.innerText);
                return results;
            }''')
            
            if not data or not data.get('title'): return

            item = TshirtItem()
            item['id'] = response.url.split('/')[-1].split('?')[0]
            item['source'] = 'thesouledstore'
            item['url'] = response.url
            item['scraped_at'] = datetime.utcnow().isoformat()
            item['product'] = {
                'title': data.get('title'),
                'brand': 'The Souled Store',
                'artist': data.get('artist'),
                'garment_type': 't-shirt',
                'price': data.get('price'),
                'currency': 'INR',
            }
            item['design'] = {
                'description': data.get('description', ''),
                'tags': data.get('tags', []),
            }
            imgs = data.get('images', [])
            item['images'] = {'primary': imgs[0] if imgs else None, 'all': imgs}
            item['image_urls'] = imgs[:2]
            yield item
        finally:
            await page.close()
