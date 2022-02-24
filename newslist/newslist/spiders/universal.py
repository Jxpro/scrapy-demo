from newslist.rules import rules
from newslist.utlis import get_config
from scrapy.spiders import CrawlSpider

from newslist.items import NewslistItem
from newslist.loaders import NewsLoader

class UniversalSpider(CrawlSpider):
    name = 'universal'

    def __init__(self, name, *a, **kw):
        config = get_config(name)
        self.config = config
        self.rules = rules.get(config.get('rules'))
        self.start_urls = config.get('start_urls')
        self.allowed_domains = config.get('allowed_domains')
        CrawlSpider.__init__(self, *a, **kw)

    def parse_item(self, response):
        item = self.config.get('item')
        if item:
            cls = eval(item.get('class'))()
            loader = eval(item.get('loader'))(cls, response=response)
            for key, value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'css':
                        loader.add_css(key, *extractor.get('args'), re=extractor.get('re', None))
                    if extractor.get('method') == 'value':
                        loader.add_value(key, *extractor.get('args'), re=extractor.get('re', None))
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *extractor.get('args')))
            yield loader.load_item()
