from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

rules = {
    'universal': (
        Rule(LinkExtractor(restrict_css='#js-info-flow .item_list li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css='ul.top_header_channel li')),
    )
}
