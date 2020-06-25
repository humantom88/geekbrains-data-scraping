# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.loader.processors import TakeFirst, MapCompose
import scrapy

class LeroymerlinItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    parameters = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field(output_processor=TakeFirst())
