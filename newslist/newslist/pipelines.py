# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

import pymongo
from scrapy.exceptions import DropItem


class MongoPipeline:
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.client = None
        self.db = None
        self.collections = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        collection = item.pop('collection')
        data = dict(item)
        if not (datalist := self.collections.get(collection, [])):
            self.collections.update({collection: datalist})
        datalist.append(data)
        return item

    def close_spider(self, spider):
        # print(self.collections)
        for collection in self.collections:
            prefix = time.strftime("%Y_%m_%d_%H_%M_%S_", time.gmtime())
            self.db[prefix + collection].insert_many(self.collections[collection])
        self.client.close()


class FilterPipeline:
    @staticmethod
    def process_item(item, spider):
        if len(dict(item)) != 7:
            raise DropItem('Missing filed')
        return item
