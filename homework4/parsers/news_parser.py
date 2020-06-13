import requests
from lxml import html
from abc import ABC, abstractmethod
from db.db import save_news_to_db

DEFAULT_HEADER = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, \
like Gecko) Chrome/83.0.4103.97 Safari/537.36'


class NewsParser(ABC):
    u"""Абстрактный класс парсера новостей"""

    def __init__(self, url, header, params):
        self.url = url
        self.params = params
        self.header = header if header else {
            'User-Agent': DEFAULT_HEADER,
            'Cache-Control': 'private, no-cache, no-store'
        }
        self.response = None
        self.dom = None

    def fetch_data(self, url=None):
        if self.url is None and url is None:
            raise Exception("No 'url' parameter provided during initialization")

        if url is not None:
            self.url = url
            self.response = requests.get(url=self.url, headers=self.header)
            return

        self.response = requests.get(url=self.url, headers=self.header, params=self.params)

    def get_dom(self):
        if self.response is None:
            raise Exception("You need to fetch_data first")
        self.dom = html.fromstring(self.response.text)
        return self.dom

    def get_news(self):
        nodes_list = self.get_nodes_list()

        news = []
        for node in nodes_list:
            article = {
                'link': self.get_link_from_node(node),
                'source': self.get_source_from_node(node),
                'title': self.get_title_from_node(node),
                'published_at': self.get_publish_date_from_node(node)
            }
            news.append(article)

        return news

    @staticmethod
    def save_news_to_db(news_list):
        save_news_to_db(news_list)

    @abstractmethod
    def get_page_link(self, page_number):
        pass

    @abstractmethod
    def get_nodes_list(self):
        pass

    @abstractmethod
    def get_source_from_node(self, node):
        pass

    @abstractmethod
    def get_title_from_node(self, node):
        pass

    @abstractmethod
    def get_link_from_node(self, node):
        pass

    @abstractmethod
    def get_publish_date_from_node(self, node):
        pass
