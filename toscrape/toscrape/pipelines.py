# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from scrapy.exceptions import DropItem


class TextPipeline:
    def __init__(self):
        self.limit = 50

    # 可直接返回dict
    def process_item(self, item, spider):
        if text := item['text']:
            if len(text) > self.limit:
                # raise DropItem('Missing Text')
                item['text'] = text[0:self.limit].rstrip() + '...'
            return item
        else:
            raise DropItem('Missing Text')


class MongoPipeline:
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.client = None
        self.db = None
        self.count = 0

    @classmethod
    def from_crawler(cls, crawler):
        # print('--------------------------------------------------')
        # print(str(crawler.settings))
        # print(type(crawler.settings))
        # print('--------------------------------------------------')
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert_one(dict(item))
        # self.count += 1
        # spider.logger.debug(self.count)
        # print('-------------------------------------------')
        # print(item.__class__.__name__)
        # print(item.__class__)
        # print('-------------------------------------------')
        return item

    def close_spider(self, spider):
        self.client.close()
