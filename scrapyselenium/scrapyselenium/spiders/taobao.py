from urllib.parse import quote

import scrapy
from scrapy import Request
from scrapyselenium.items import ProductItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    base_url = 'https://s.taobao.com/search?q='
    error_times = 0

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(self.settings.get('MAX_PAGE')):
                url = self.base_url + quote(keyword)
                yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response, **kwargs):
        # page_num = response.css('#mainsrp-pager .active span::text').extract()
        # page = response.css('#mainsrp-pager .active').extract()
        products = response.css('#mainsrp-itemlist .items .item')
        for product in products:
            if 'item-ad' in product.css('::attr("class")'):
                continue
            item = ProductItem()
            item['price'] = ''.join(product.css('.price *::text').extract()).strip()
            item['title'] = ''.join(product.css('.title a::text').extract()).strip()
            item['shop'] = product.css('.shop .dsrs+span::text').extract_first()
            item['image'] = product.css('.img::attr("src")').extract_first()
            item['deal'] = product.css('.deal-cnt::text').extract_first()
            item['location'] = product.css('.location::text').extract_first()
            if item['image'] == '//g.alicdn.com/s.gif':
                self.error_times += 1
                self.logger.debug('-------------------------------------------------------------------')
                self.logger.debug('image_url fetch error, time : %d' % self.error_times)
                self.logger.debug('-------------------------------------------------------------------')
            yield item
