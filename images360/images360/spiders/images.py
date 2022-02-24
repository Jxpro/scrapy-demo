import json
from urllib.parse import urlencode

import scrapy
from images360.items import ImageItem


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        data = {'ch': 'wallpaper'}
        base_url = 'https://images.so.com/zjl?'
        with open('item_length.log', 'w') as _:
            pass

        for page_num in range(self.settings.get('MAX_PAGE')):
            data['sn'] = page_num * 30
            url = base_url + urlencode(data)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        result = json.loads(response.text)
        with open('item_length.log', 'a') as f:
            f.write(str(len(result.get('list'))) + '\n')
            # f.write(response.url)
        for image in result.get('list'):
            item = ImageItem()
            item['id'] = image.get('id')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('title')
            item['thumb'] = image.get('qhimg_thumb')
            # print('item:', item)
            yield item
