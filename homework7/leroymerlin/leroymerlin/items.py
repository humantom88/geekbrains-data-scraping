# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.loader.processors import TakeFirst, MapCompose
import scrapy
import re

def cleaner_price(value):
    price_string = re.sub('[^\d]', '', value)
    return int(price_string)

class LeroymerlinItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    parameters = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field(input_processor=TakeFirst(), output_processor=MapCompose(cleaner_price))
