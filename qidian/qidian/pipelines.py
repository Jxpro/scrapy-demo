# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import traceback

from scrapy.pipelines.images import ImagesPipeline


class QidianPipeline:
    file = None

    def open_spider(self, spider):
        self.file = open('./data.json', 'w')
        self.file.write('[\n')

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.file.write(line)
        return item


class ImgPipeline(ImagesPipeline):
   def file_path(self, request, response=None, info=None, *, item=None):
       # print('----------------------------------------------------')
       # print(f'{item["title"]}\'s file_path method was called from {traceback.extract_stack()[-2]}')
       # print(f'{item["title"]}\'s file_path method was called from {traceback.extract_stack()[-3]}')
       # print(f'{item["title"]}\'s file_path method was called from {traceback.extract_stack()[-4]}')
       # print(f'{item["title"]}\'s file_path method was called from {traceback.extract_stack()[-5]}')
       # print(f'{item["title"]}\'s file_path method was called from {traceback.extract_stack()[-6]}')
       # print('----------------------------------------------------')
       request.meta['title']=item['title']
       return f'full/{item["title"]}.jpg'

   def thumb_path(self, request, thumb_id, response=None, info=None):
       # print('****************************************************')
       # print(f'{thumb_id}/{request.meta["title"]}\'s thumb_path method was called from {traceback.extract_stack()[-2]}')
       # print(f'{thumb_id}/{request.meta["title"]}\'s thumb_path method was called from {traceback.extract_stack()[-3]}')
       # print(f'{thumb_id}/{request.meta["title"]}\'s thumb_path method was called from {traceback.extract_stack()[-4]}')
       # print(f'{thumb_id}/{request.meta["title"]}\'s thumb_path method was called from {traceback.extract_stack()[-5]}')
       # print(f'{thumb_id}/{request.meta["title"]}\'s thumb_path method was called from {traceback.extract_stack()[-6]}')
       # print('****************************************************')
       return f'thumbs/{thumb_id}/{request.meta["title"]}.jpg'