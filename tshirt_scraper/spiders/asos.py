import scrapy
from tshirt_scraper.items import TshirtItem
from datetime import datetime
import json

class AsosSpider(scrapy.Spider):
    name = "asos"
    allowed_domains = ["asos.com"]
    start_urls = ["https://www.asos.com/men/tops/t-shirts-vests/cat/?cid=7616"]

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
        await page.wait_for_timeout(10000)
        
        links = await page.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('a'))
                               .map(a => a.href)
                               .filter(href => href.includes('/prd/'));
            return [...new Set(links)];
        }''')
        
        await page.close()
        
        for link in links[:100]:
            yield scrapy.Request(
                link,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                },
                callback=self.parse_product
            )

    async def parse_product(self, response):
        page = response.meta["playwright_page"]
        await page.wait_for_timeout(5000)
        
        data = await page.evaluate('''() => {
            const results = {};
            results.title = document.querySelector('h1')?.innerText;
            results.price = document.querySelector('[data-testid="current-price"]')?.innerText;
            results.description = document.querySelector('#productDescription')?.innerText;
            results.brand = document.querySelector('.product-brand-description')?.innerText;
            
            results.images = Array.from(document.querySelectorAll('img'))
                                .map(img => img.src)
                                .filter(src => src.includes('images.asos-media.com/products/'));
            
            return results;
        }''')
        
        item = TshirtItem()
        item['id'] = response.url.split('/')[-1].split('#')[0]
        item['source'] = 'asos'
        item['url'] = response.url
        item['scraped_at'] = datetime.utcnow().isoformat()
        
        item['product'] = {
            'title': data.get('title'),
            'brand': data.get('brand') or 'ASOS',
            'garment_type': 't-shirt',
            'price': data.get('price'),
            'currency': 'GBP',
        }
        
        item['design'] = {
            'description': data.get('description'),
            'tags': [],
        }
        
        item['images'] = {
            'primary': data.get('images')[0] if data.get('images') else None,
            'all': data.get('images')
        }
        
        item['image_urls'] = data.get('images')[:2]
        
        await page.close()
        yield item
