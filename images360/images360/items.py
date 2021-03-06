# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'images'

    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    thumb = scrapy.Field()
