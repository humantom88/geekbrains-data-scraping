# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class JobparserPipeline:                            #Класс для обработки item'a
    def __init__(self):                             #Конструктор, где инициализируем подключение к СУБД
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacansy_hh_scrapy


    def process_item(self, item, spider):           #Метод, куда прилетает сформированный item
        if spider.name == 'hhru':                 #Зесь можно сделать обработку item в зависимости от имени паука
            self.process_hh_item(item, spider.name)
        if spider.name == 'sjru':                 #Зесь можно сделать обработку item в зависимости от имени паука
            collection = self.mongo_base[spider.name]   #Выбираем коллекцию по имени паука
            collection.insert_one(item)                 #Добавляем в базу данных
        return item

    def process_hh_item(self, item, collection_name):
        #   * Наименование вакансии
        #   * Зарплата от
        #   * Зарплата до
        #   * Ссылку на саму вакансию
        #   * Сайт откуда собрана вакансия
        collection = self.mongo_base[collection_name]  # Выбираем коллекцию по имени паука
        vacancy = {
            'name': item.name,
            'salary_from': None,
            'salary_to': None,
            'currency': None,
            'link': None,
            'source_site': None
        }
        collection.insert_one(vacancy)  # Добавляем в базу данных

    def get_hh_salary_from(self, item):
        if len(item) < 2:
            return None

        if len(item) <= 5:
            return int(item[1].replace(' ',''))

    def get_hh_salary_to(self, item):
        if len(item) < 2:
            return None

        if len(item) > 5:
            return int(item[3].replace(' ', ''))

    def get_hh_currency(self, item):
        if len(item) < 2:
            return None

        if len(item) > 5:
            return int(item[5].replace(' ', ''))
