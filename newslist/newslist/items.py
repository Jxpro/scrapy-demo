# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class NewslistItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = Field()
    text = Field()
    datetime = Field()
    source = Field()
    url = Field()
    website = Field()
    collection = Field()


class CollectionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    collection = Field()
    data = Field()
