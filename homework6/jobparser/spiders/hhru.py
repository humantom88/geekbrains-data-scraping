# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse        #Для подсказок объекта response
from jobparser.items import JobparserItem   #Подключаем класс из items

class HhruSpider(scrapy.Spider):
    name = 'hhru'                           #Имя паука
    allowed_domains = ['hh.ru']             #Домен в рамках которого работаем

    #Стартовая ссылка (точка входа)
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=python&showClusters=true']

    def parse(self, response:HtmlResponse):     #С этого метода все и начинается (в response - первый ответ)
        #Ищем ссылку для перехода на следующую страницу
        next_page = response.css('a.HH-Pager-Controls-Next.HH-Pager-Control::attr(href)').extract_first()

        #Ищем на полученной странице ссылки на вакансии
        vacansy_links = response.css('div.vacancy-serp div.vacancy-serp-item a.HH-LinkModifier::attr(href)').extract()
        for link in vacansy_links:          #Перебираем ссылки
            yield response.follow(link, callback=self.vacansy_parse)        #Переходим по каждой ссылке и обрабатываем ответ методом vacansy_parse

        yield response.follow(next_page, callback=self.parse)               #Переходим по ссылке на следующую страницу и возвращаемся к началу метода parse



    def vacansy_parse(self, response:HtmlResponse):                         #Здесь обрабатываем информацию по вакансии
        name_job = response.xpath('//h1/text()').extract_first()            #Получаем наименование вакансии
        salary_job = response.css('p.vacancy-salary span::text').extract()  #Получаем зарплату в виде списка отдельных блоков
        yield JobparserItem(name=name_job, salary=salary_job)               #Передаем данные в item для создания структуры json






