import scrapy
from scrapy.crawler import CrawlerProcess
from tshirt_scraper.spiders.thesouledstore import TheSouledStoreSpider

class SingleTSSSpider(TheSouledStoreSpider):
    name = "single_tss"
    start_urls = ["https://www.thesouledstore.com/product/stranger-things-upside-down-spray-men-oversized-tshirt?gte=1"]

    async def parse_listing(self, response):
        # Skip listing, go straight to product
        return await self.parse_product(response)

process = CrawlerProcess(settings={
    "DOWNLOAD_HANDLERS": {
        "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    },
    "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": False},
    "FEEDS": {"single_tss.jsonl": {"format": "jsonlines"}},
})

process.crawl(SingleTSSSpider)
process.start()
