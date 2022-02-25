import re

from itemloaders.processors import Join, Compose
from newslist.items import NewslistItem
from newslist.loaders import NewsLoader
from parsel.utils import extract_regex
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MilitarySpider(CrawlSpider):
    name = 'military'
    allowed_domains = ['china.com']
    start_urls = ['http://military.china.com/']

    rules = (
        Rule(LinkExtractor(restrict_css='#js-info-flow .item_list li'), callback='parse_item', follow=True),
        # news yz edu
        # Rule(LinkExtractor(restrict_css='#js-info-flow .lists_start .listItem'), callback='parse_item', follow=True),
        # # military
        # Rule(LinkExtractor(restrict_css='#js-newsTab .newsTab-list .listItem'), callback='parse_item', follow=True),
        # # finance ent
        # Rule(LinkExtractor(restrict_css='#newsTab .news-tab-cnt .item-phototext'), callback='parse_item', follow=True),
        # # game
        # Rule(LinkExtractor(restrict_css='#js-main .newsDefList .listItem'), callback='parse_item', follow=True),  # law
        Rule(LinkExtractor(restrict_css='ul.top_header_channel li')),
    )

    def parse_item(self, response):
        loader = NewsLoader(item=NewslistItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_value('website', '中华网')
        loader.add_value('collection', re.search(r'//(.*?).china', response.url).group(1))
        loader.add_css('title', 'h1.article_title::text')
        loader.add_css('text', '.article_content p::text')
        loader.add_css('datetime', '.article_info .time::text', re='(\d+-\d+-\d+\s\d+:\d+:\d+)')
        loader.add_css('source', '.article_info .source *::text', re='(.*)')
        print('-----------------------------------------------------')
        selector = response.css('.article_info .source *::text')
        texts = selector.extract()
        processor = Compose(Join(), lambda s: s.strip())
        print(selector)
        print(texts)
        print(processor(texts))
        print(extract_regex('来源：(.*)', processor(texts)))
        print('-----------------------------------------------------')
        # match re.search(r'//(.*?).china', response.url).group(1):
        #     case 'ent':
        #         self.repair(loader)
        #         print('-----------------------------------------------------')
        #         print(loader.load_item())
        #         print('-----------------------------------------------------')
        yield loader.load_item()

    @staticmethod
    def repair(loader):
        loader.add_css('title', '#chan_newsTitle::text')
        loader.add_css('text', '#chan_newsDetail *::text')
        loader.add_css('datetime', '#chan_newsInfo ::text', re='(\d+-\d+-\d+\s\d+:\d+:\d+)')
        loader.add_css('source', '#chan_newsInfo .chan_newsInfo_source *::text')
