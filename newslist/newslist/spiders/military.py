from newslist.items import NewslistItem
from newslist.loaders import NewsLoader

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MilitarySpider(CrawlSpider):
    name = 'military'
    allowed_domains = ['china.com']
    start_urls = ['http://military.china.com/']

    rules = (
        Rule(LinkExtractor(restrict_css='#js-info-flow .item_list li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css='ul.top_header_channel li')),
    )

    @staticmethod
    def parse_item(response):
        loader = NewsLoader(item=NewslistItem(), response=response)
        loader.add_css('title', 'h1.article_title::text')
        loader.add_value('url', response.url)
        loader.add_css('text', '.article_content p::text')
        loader.add_css('datetime', '.article_info .time::text', re='(\d+-\d+-\d+\s\d+:\d+:\d+)')
        loader.add_css('source', '.article_info .source::text', re='来源：(.*)')
        loader.load_item()
        loader.add_value('website', '中华网')
        yield loader.load_item()
