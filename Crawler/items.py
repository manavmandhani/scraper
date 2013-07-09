# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst

class CrawlerItem(Item):
    #Restaurant details to be scraped
    name = Field(
        input_processor = MapCompose(unicode.strip),
        output_processor = Join()
)
    categories = Field()
    address = Field(
        output_processor = Join()
)
    number = Field()
    rating = Field()
    price_range = Field(
        output_processor = Join()
)
    hours = Field()
    url = Field()
    #attributes = Field()

