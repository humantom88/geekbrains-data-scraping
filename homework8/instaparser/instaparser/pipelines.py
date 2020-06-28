# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient, errors

class InstaparserPipeline:
    def __init__(self):                             # Конструктор, где инициализируем подключение к СУБД
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instagram

    def write_to_db(self, item, collection_name):
        collection = self.mongo_base[collection_name]  # Выбираем коллекцию по имени паука
        try:
            collection.insert_one(item)  # Добавляем в базу данных
        except errors.DuplicateKeyError:
            print("Duplicate found for vacancy: ", item)
            pass

    def process_item(self, item, spider):
        user = {
            'user_id': item['user_id'],
            'user_name': item['user_name'],
            'full_name': item['full_name'],
            'photo': item['photo'],
            'is_followed_by': item['is_followed_by'],
            'follows': item['follows']
        }

        self.write_to_db(user, 'instagram_users')

        return item