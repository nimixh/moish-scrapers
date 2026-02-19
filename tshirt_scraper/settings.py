BOT_NAME = 'tshirt_scraper'
SPIDER_MODULES = ['tshirt_scraper.spiders']
NEWSPIDER_MODULE = 'tshirt_scraper.spiders'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": False,
}

PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 90000

IMAGES_STORE = 'images'
ITEM_PIPELINES = {
   'scrapy.pipelines.images.ImagesPipeline': 1,
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
