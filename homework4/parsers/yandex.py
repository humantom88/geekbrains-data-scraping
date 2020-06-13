from parsers.news_parser import NewsParser
from abc import ABC

DOMAIN_URL = 'https://newssearch.yandex.ru'
SEARCH_URL = f'{DOMAIN_URL}/yandsearch'

# Яндекс беспощадно банит ( очень неудобно собирать с него новости


class YandexParser(NewsParser, ABC):
    def __init__(self, query_string):
        super().__init__(url=SEARCH_URL,
                         header=None,
                         params={
                             'text': query_string,
                             'rpt': 'nnews2',
                             'wiz_no_news': 1,
                             'rel': 'rel'
                         })

    def get_news_pages(self, number_of_pages):
        total_news = []

        self.fetch_data()
        total_news += self.get_news()
        next_page_link = self.get_page_link(None)

        if next_page_link is None:
            return total_news

        for i in range(0, number_of_pages):
            next_page_link = self.get_page_link(i)
            if next_page_link is not None:
                self.fetch_data(next_page_link)
                total_news += self.get_news()
            else:
                break

        return total_news

    # Extension methods

    def get_nodes_list(self):
        dom = self.get_dom()
        return dom.xpath("//ul[@class='search-list']/li")

    def get_page_link(self, page_number):
        dom = self.get_dom()
        link_node = dom.xpath("//div[@class='pager__content']//span[@class='pager__group'][last()]/a/@href")
        if link_node is not None and len(link_node) != 0:
            link_tail = link_node[0]
            return f'{DOMAIN_URL}{link_tail}'

        return None

    def get_source_from_node(self, node):
        return node.xpath(".//div[@class='document i-bem']//div[@class='document__provider-name']/text()")[0]

    def get_title_from_node(self, node):
        return node.xpath(".//div[@class='document i-bem']//h2[@class='document__head']//a/text()")[0]

    def get_link_from_node(self, node):
        return node.xpath(".//div[@class='document i-bem']//h2[@class='document__head']//a/@href")[0]

    def get_publish_date_from_node(self, node):
        return node.xpath(".//div[@class='document i-bem']//div[@class='document__time']/text()")[0]
