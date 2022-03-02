import scrapy


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,cookies={'cookie': 'test:cookies_spider'})

    def parse(self, response, **kwargs):
        self.logger.debug(response.text)
