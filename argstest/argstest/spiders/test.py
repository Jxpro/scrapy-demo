import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],meta={'meta_data':'meta_value'},cb_kwargs={'cb_key':'cb_value_test'})

    def parse(self, response, **kwargs):
        print('-----------------------------------------')
        print(response.meta['meta_data'])
        print(kwargs['cb_key'])
        print(response.cb_kwargs['cb_key'])
        print(response.request.cb_kwargs['cb_key'])
        print('-----------------------------------------')
