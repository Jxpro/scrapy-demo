import re

from newslist.items import NewslistItem
from newslist.loaders import NewsLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MilitarySpider(CrawlSpider):
    name = 'military'
    allowed_domains = ['china.com']
    start_urls = ['http://military.china.com/']

    rules = (
        Rule(LinkExtractor(restrict_css='#js-info-flow .item_list li'), callback='parse', follow=True),
        # news yz edu
        Rule(LinkExtractor(restrict_css='#js-info-flow .lists_start .listItem'), callback='parse', follow=True),
        # # military
        Rule(LinkExtractor(restrict_css='#js-newsTab .newsTab-list .listItem'), callback='parse', follow=True),
        # # finance ent
        # 下面这两条rule的测试重复又复杂，暂时不测了
        # Rule(LinkExtractor(restrict_css='#newsTab .news-tab-cnt .item-phototext'), callback='parse_item', follow=True),
        # # game
        # Rule(LinkExtractor(restrict_css='#js-main .newsDefList .listItem'), callback='parse_item', follow=True),  # law
        Rule(LinkExtractor(restrict_css='ul.top_header_channel li')),
    )

    def parse(self, response, **kwargs):
        collection = re.search(r'//(.*?).china', response.url).group(1)
        loader = NewsLoader(item=NewslistItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_value('collection', collection)
        loader.add_value('website', '中华网')
        self.load_diff_attr(collection, loader, response)
        yield loader.load_item()

    @staticmethod
    def load_diff_attr(collection, loader, response):
        match collection:
            case 'ent':
                loader.add_css('title', '#chan_newsTitle::text')
                loader.add_css('text', '#chan_newsDetail *::text')
                loader.add_css('datetime', '#chan_newsInfo *::text', re='(\d+-\d+-\d+\s\d+:\d+:\d+)')
                if response.css('.chan_newsInfo_source .source *::text'):
                    loader.add_css('source', '.chan_newsInfo_source .source *::text')
                elif response.css('#chan_newsInfo .chan_newsInfo_source *::text'):
                    loader.add_css('source', '#chan_newsInfo .chan_newsInfo_source *::text')
                else:
                    loader.add_css('source', '#chan_newsInfo .chan_newsInfo_author *::text')
            case 'military':
                loader.add_css('title', '.article-main-title::text')
                loader.add_css('text', '#chan_newsDetail *::text')
                loader.add_css('datetime', '.time-source .time::text')
                source = response.css('.time-source .source::text')
                loader.add_value('source', source.extract_first() if source else '未注明来源')
            case 'finance' | 'jiu':
                loader.add_css('title', '.arti-title::text')
                loader.add_css('text', '#js-main .arti-detail *::text')
                loader.add_css('datetime', '#js-main .time::text')
                loader.add_css('source', '.arti-info .source::text', re='来源：(.*)')
            case _:
                loader.add_css('title', 'h1.article_title::text')
                loader.add_css('text', '.article_content p::text')
                loader.add_css('datetime', '.article_info .time::text')
                selector = response.css('.article_info .source *::text')
                texts = ''.join(selector.extract())
                try:
                    loader.add_value('source', re.search('来源：(.*)', texts).group(1).strip())
                except AttributeError:
                    loader.add_value('source', '未注明来源')
                # print('-----------------------------------------------------')
                # selector = response.css('.article_info .source *::text')
                # texts = selector.extract()
                # processor = Compose(Join(), lambda s: s.strip())
                # print(selector)
                # print(texts)
                # print(processor(texts))
                # print(extract_regex('来源：(.*)', processor(texts)))
                # print('-----------------------------------------------------')
