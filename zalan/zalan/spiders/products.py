import scrapy


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["zalando.co.uk"]
    start_urls = ["https://zalando.co.uk"]

    def parse(self, response):
        pass
