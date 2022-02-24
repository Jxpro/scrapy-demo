from itemloaders.processors import TakeFirst, Compose, Join
from scrapy.loader import ItemLoader


class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())
