from parsers.news_parser import NewsParser
from datetime import datetime
from abc import ABC

DOMAIN_URL = 'https://m.lenta.ru'
SEARCH_URL = f'{DOMAIN_URL}/search/v2/process'

# Не получается сделать парсинг новостей Lenta.ru через xpath
# на клиенте - react, который загружает только пустой контейнер для отображения новостей
# сами новости загружаются отдельным GET запросом к api и возвращаются в формате JSON


class LentaParser(NewsParser, ABC):
    def __init__(self, query_string):
        super().__init__(url=SEARCH_URL,
                         header=None,
                         params={
                             'query': query_string,
                             'from': 0,
                             'size': 100,
                             'sort': 2,
                             'title_only': 0,
                             'domain': 1
                         })

    def get_news_pages(self, pages_range):
        total_news = []
        for page_number in pages_range:
            self.params['from'] = page_number * self.params['size']
            self.fetch_data()
            total_news += self.get_news()

        return total_news

    # Extension methods

    def get_nodes_list(self):
        result = self.response.json()['matches']
        return result

    def get_page_link(self, page_number):
        pass

    def get_source_from_node(self, node):
        return None

    def get_title_from_node(self, node):
        return node['title']

    def get_link_from_node(self, node):
        return node['url']

    def get_publish_date_from_node(self, node):
        timestamp = node['pubdate']
        return datetime.fromtimestamp(timestamp) if timestamp else None