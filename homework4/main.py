from parsers.mail import MailRuParser
from parsers.yandex import YandexParser
from parsers.lenta import LentaParser
from db.db import save_news_to_db

query_string = 'наука'

# https://news.mail.ru/
mail_ru_parser = MailRuParser(query_string)
mail_ru_parser.fetch_data()
mail_ru_news_from_page = mail_ru_parser.get_news()
mail_ru_news_from_api = mail_ru_parser.get_news_from_pages_range(range(2, 12))

# https://yandex.ru/news/

yandex_parser = YandexParser(query_string)
yandex_parser.fetch_data()
yandex_news = yandex_parser.get_news_pages(3)

# lenta.ru

lenta_parser = LentaParser(query_string)
lenta_parser.fetch_data()
lenta_news = lenta_parser.get_news_pages(range(0, 2))

result_news = mail_ru_news_from_page + mail_ru_news_from_api + yandex_news + lenta_news

save_news_to_db(result_news)
