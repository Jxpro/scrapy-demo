import scrapy

from toscrape.items import QuotesItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response, **kwargs):
        # print('------------------------------------------------')
        # print(response.text)
        # print('------------------------------------------------')
        # print(response.headers)
        # print('------------------------------------------------')
        # print(response.body)
        # print('------------------------------------------------')
        # print(response.css('*'))
        # print('------------------------------------------------')
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuotesItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item

        next_page = response.css('.pager .next a::attr(href)').extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url=url, callback=self.parse)
