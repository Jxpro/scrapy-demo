from rssspider.items import RssspiderItem
from scrapy.spiders import XMLFeedSpider


class RsstestSpider(XMLFeedSpider):
    name = 'rsstest'
    allowed_domains = ['blog.sina.com.cn']
    start_urls = ['http://blog.sina.com.cn/rss/1246151574.xml']
    iterator = 'iternodes'  # you can change this; see the docs
    itertag = 'item'  # change it accordingly

    def parse_node(self, response, selector):
        item = RssspiderItem()
        item['title'] = selector.css('title::text').extract()
        item['link'] = selector.css('link::text').get()
        item['all_elem'] = selector.xpath('/*').get()
        return item
