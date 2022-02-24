from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose
from scrapy.spiders import CrawlSpider, Rule


class MilitarySpider(CrawlSpider):
    name = 'military'
    allowed_domains = ['china.com']
    start_urls = ['http://military.china.com/']
    count = 0
    urls = []
    url_set = []

    rules = (
        # Rule(LinkExtractor(restrict_css='#js-info-flow .item_list li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css='ul.top_header_channel li'), callback='parse_item', follow=False),
    )

    def __del__(self):
        print(self.urls)
        print(self.count)
        print(len(self.url_set))

    def parse_item(self, response):
        self.count += 1
        self.urls.append(response.url)
        self.url_set.append(response.url)
        print(self.count, "=======> ", response.url)


class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())
