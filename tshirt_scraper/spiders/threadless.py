import scrapy
import json
from datetime import datetime
from tshirt_scraper.items import TshirtItem

class ThreadlessSpider(scrapy.Spider):
    name = "threadless"
    allowed_domains = ["threadless.com"]
    start_urls = ["https://www.threadless.com/shop/apparel/t-shirt"]

    custom_settings = {
        'PLAYWRIGHT_LAUNCH_OPTIONS': {'headless': False}, # Using xvfb
    }

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
        # Wait for potential CF
        await page.wait_for_timeout(10000)
        
        # Extract product links
        links = await page.eval_on_selector_all("a", "nodes => nodes.map(n => n.href)")
        product_links = [link for link in links if "/design/" in link][:100]
        
        await page.close()
        
        for link in product_links:
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
        
        try:
            # Basic extraction using Playwright evaluate for better reliability
            data = await page.evaluate('''() => {
                const title = document.querySelector('h1')?.innerText || document.querySelector('.productPicker-design')?.innerText;
                const artist = document.querySelector('.productPicker-artistName')?.innerText;
                const description = document.querySelector('.product-description')?.innerText;
                const tags = Array.from(document.querySelectorAll('.tags-list a')).map(a => a.innerText);
                const primaryImg = document.querySelector('#design-image img')?.src;
                const price = document.querySelector('.product-price')?.innerText;
                
                return { title, artist, description, tags, primaryImg, price };
            }''')
            
            # Filtering pass: Drop records where description word count < 30
            desc = data.get('description', '')
            if len(desc.split()) < 30:
                self.logger.info(f"Skipping {response.url} due to short description.")
                await page.close()
                return

            item = TshirtItem()
            item['id'] = response.url.split('/')[-1]
            item['source'] = 'threadless'
            item['url'] = response.url
            item['scraped_at'] = datetime.utcnow().isoformat()
            
            item['product'] = {
                'title': data.get('title'),
                'brand': 'Threadless Artist Shop',
                'artist': data.get('artist'),
                'garment_type': 't-shirt',
                'price': data.get('price'),
                'currency': 'USD',
            }
            
            item['design'] = {
                'description': desc,
                'tags': data.get('tags'),
            }
            
            item['images'] = {
                'primary': data.get('primaryImg'),
            }
            
            item['image_urls'] = [data.get('primaryImg')] if data.get('primaryImg') else []
            
            yield item
            
        except Exception as e:
            self.logger.error(f"Error parsing {response.url}: {e}")
        finally:
            await page.close()
