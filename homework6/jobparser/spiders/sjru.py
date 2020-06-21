# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse        # Для подсказок объекта response
from jobparser.items import JobparserItem   # Подключаем класс из items

class SjruSpider(scrapy.Spider):
    name = 'sjru'                           # Имя паука
    allowed_domains = ['superjob.ru']       # Домен в рамках которого работаем

    # Стартовая ссылка (точка входа)
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=javascript']

    def parse(self, response:HtmlResponse):     # С этого метода все и начинается (в response - первый ответ)
        # Ищем ссылку для перехода на следующую страницу
        next_page = response.css('a.icMQ_._1_Cht._3ze9n.f-test-button-dalshe.f-test-link-Dalshe::attr(href)').extract_first()

        # Ищем на полученной странице ссылки на вакансии

        vacancy_links = response.css('a.icMQ_._6AfZ9._2JivQ._1UJAN::attr(href)').extract()
        for link in vacancy_links:          # Перебираем ссылки
            yield response.follow(link, callback=self.vacansy_parse)        # Переходим по каждой ссылке и обрабатываем ответ методом vacansy_parse

        yield response.follow(next_page, callback=self.parse)               # Переходим по ссылке на следующую страницу и возвращаемся к началу метода parse



    def vacansy_parse(self, response:HtmlResponse):                         # Здесь обрабатываем информацию по вакансии
        name_job = response.xpath('//h1/text()').extract_first()            # Получаем наименование вакансии
        salary_job = response.css('div._3MVeX span._1OuF_.ZON4b span._3mfro._2Wp8I.PlM3e._2JVkc::text').extract()     # Получаем зарплату в виде списка отдельных блоков
        link = response.url
        source_link = response.css('a.icMQ_._2JivQ::attr(href)').extract_first()
        yield JobparserItem(name=name_job, salary=salary_job, link=link, source_link=source_link)   # Передаем данные в item для создания структуры json






