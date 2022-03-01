import hashlib
import re

from qidian.items import QidianItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.python import to_bytes


class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['qidian.com']
    start_urls = ['https://www.qidian.com/finish/']

    rules = (
        Rule(LinkExtractor(restrict_css='.lbf-pagination-item-list li'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        for novel in response.css('#book-img-text li'):
            # loader 必须传response对象，不能是selector
            # loader = NovelLoader(item=QidianItem(),response=response)
            # loader.add_css('title','.book-mid-info h2 a::text')
            # loader.add_css('author','.book-mid-info .author *::text')
            # loader.add_css('tags','.book-mid-info .author *::text')
            # loader.add_css('intro','.book-mid-info .intro::text')
            # loader.add_css('images_url','.book-mid-info h2 a::text')
            item = QidianItem()
            info = re.findall(r'(.*?)\|', ''.join(novel.css('.book-mid-info .author *::text').extract()).strip())
            item['title'] = novel.css('.book-mid-info h2 a::text').extract_first()
            item['author'] = info[0]
            item['tags'] = info[1]
            item['intro'] = novel.css('.book-mid-info .intro::text').extract_first().strip()
            item['image_urls'] = ['https:' + novel.css('.book-img-box img::attr(src)').extract_first()]
            item['path_name'] = hashlib.sha1(to_bytes(item['image_urls'][0])).hexdigest()
            yield item
