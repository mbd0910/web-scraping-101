from typing import Iterable

import scrapy
from scrapy import Request


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["zalando.co.uk"]
    start_urls = ["https://zalando.co.uk"]

    def start_requests(self) -> Iterable[Request]:
        urls = []
        for p in range(1, 429):
            urls.append(f'https://www.zalando.co.uk/men/?p={p}')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        pass

    def parse(self, response):
        pass
