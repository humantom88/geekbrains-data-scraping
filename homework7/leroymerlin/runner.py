from scrapy.crawler import CrawlerProcess           # Импортируем класс для создания процесса
from scrapy.settings import Settings                # Импортируем класс для настроек

from leroymerlin import settings                      # Наши настройки
from leroymerlin.spiders.lm import LmSpider         # Класс паука


if __name__ == '__main__':
    crawler_settings = Settings()                   # Создаем объект с настройками
    crawler_settings.setmodule(settings)            # Привязываем к нашим настройкам

    process = CrawlerProcess(settings=crawler_settings)     # Создаем объект процесса для работы
    process.crawl(LmSpider, search=['Диван', 'Кровать'])                # Добавляем нашего паука

    process.start()                                         # Пуск
