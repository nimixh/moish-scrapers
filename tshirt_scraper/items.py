import scrapy

class TshirtItem(scrapy.Item):
    id = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    scraped_at = scrapy.Field()
    product = scrapy.Field()
    design = scrapy.Field()
    context = scrapy.Field()
    images = scrapy.Field()
    engagement = scrapy.Field()
    image_urls = scrapy.Field()
    images_downloaded = scrapy.Field()
