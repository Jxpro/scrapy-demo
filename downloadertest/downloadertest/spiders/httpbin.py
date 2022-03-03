import scrapy


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/cookies/set/number/123456789', 'http://httpbin.org/cookies']

    def start_requests(self):
        self.logger.debug('start_requests method')
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
            # yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={'cookiejar': 1})

    # 在setting里设置 REDIRECT_ENABLED = False
    def parse(self, response, **kwargs):
        print('----------------------------------------------')
        self.logger.debug(response.text)
        # self.logger.debug('cookiejar: ' + str(response.meta['cookiejar']))
        print('----------------------------------------------')
        # yield scrapy.Request(url='http://httpbin.org/cookies', callback=self.parse, dont_filter=True)
        # yield scrapy.Request(url='http://httpbin.org/cookies', callback=self.parse,
        #                      dont_filter=True, meta={'cookiejar': 1})
        # yield scrapy.Request(url='http://httpbin.org/cookies', callback=self.parse,
        #                      dont_filter=True, meta={'cookiejar': 2})
        # self.logger.debug(self.crawler.stats.inc_value('httpbin'))
        # self.logger.debug('stats'+str(self.crawler.stats.spider_stats))
        # self.logger.debug(self.crawler.stats.inc_value('httpbin'))
