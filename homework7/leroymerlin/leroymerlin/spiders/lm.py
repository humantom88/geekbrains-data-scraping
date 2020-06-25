import scrapy
from scrapy.http import HtmlResponse        # Для подсказок объекта response
from leroymerlin.items import LeroymerlinItem   # Подключаем класс из items

class LmSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']
    # Стартовая ссылка (точка входа)
    start_urls = ['https://leroymerlin.ru/search/?q=%D0%B4%D0%B8%D0%B2%D0%B0%D0%BD&suggest=true']

    def parse(self, response):
        # Ищем ссылку для перехода на следующую страницу
        next_page = response.css('a.paginator-button.next-paginator-button::attr(href)').extract_first()

        # Ищем на полученной странице ссылки на товары
        goods_links = response.css('a.black-link.product-name-inner::attr(href)').extract()
        for link in goods_links:  # Перебираем ссылки
            yield response.follow(link, callback=self.item_parse)  # Переходим по каждой ссылке и обрабатываем ответ методом vacansy_parse

        yield response.follow(next_page,
                              callback=self.parse)  # Переходим по ссылке на следующую страницу и возвращаемся к началу метода parse

    def item_parse(self, response:HtmlResponse):
        name = response.xpath('//h1[@itemprop="name"]/text()')         # Получаем наименование товара
        photos = response.xpath('//img[@itemprop="image"]/@src')       # Все фото
        parameters = response.xpath('//div[@class="def-list__group"]') # Параметры товара в объявлении
        link = response.url                                            # Ссылка
        price = response.xpath('//span[@slot="price"]/text()')         # Цена
        yield LeroymerlinItem(
            name=name,
            photos=photos,
            parameters=parameters,
            link=link,
            price=price
        )
