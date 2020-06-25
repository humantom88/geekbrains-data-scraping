# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient, errors

import scrapy
from scrapy.pipelines.images import ImagesPipeline


class DataBasePipeline:
    def __init__(self):                             # Конструктор, где инициализируем подключение к СУБД
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.lm_scrapy

    def write_to_db(self, item, collection_name):
        collection = self.mongo_base[collection_name]  # Выбираем коллекцию по имени паука
        try:
            collection.insert_one(item)  # Добавляем в базу данных
        except errors.DuplicateKeyError:
            print("Duplicate found for vacancy: ", item)
            pass

    def process_item(self, item, spider):
        product = {
            'name': item['name'].extract_first(),
            'photos': item['photos'],
            'parameters': self.extract_parameters(item),
            'link': item['link'],
            'price': item['price'].extract_first()
        }

        self.write_to_db(product, 'leroymerlin')

        return item

    def extract_parameters(self, item):
        parameters = item['parameters']
        return [{
            f"{parameter.xpath('.//dt/text()').get()}": parameter.xpath('.//dd/text()').get()
        } for parameter in parameters]

class LeroymerlinPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img.get(), meta=item)  # Скачиваем фото и передает item через meta
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


