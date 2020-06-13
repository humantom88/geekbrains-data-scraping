from abc import ABC
from parsers.news_parser import NewsParser
from datetime import datetime

DOMAIN_URL = 'https://news.mail.ru'
SEARCH_URL = f'{DOMAIN_URL}/search'
API_URL = f'{DOMAIN_URL}//najax/search'


class MailRuParser(NewsParser, ABC):
    def __init__(self, query_string):
        super().__init__(url=SEARCH_URL,
                         header=None,
                         params={
                             'q': query_string
                         })

    def get_news_from_pages_range(self, pages_range):
        total_news = []
        for page_number in pages_range:
            self.fetch_data(self.get_page_link(page_number))
            total_news += self.get_api_news()

        return total_news

    def get_api_news(self):
        data = self.response.json()
        news_list = []
        for item in data['data']['items']:
            article = {
                'link': f'{DOMAIN_URL}{item["url"]}',
                'source': item['source']['name'],
                'title': item['title'],
                'published_at': datetime.fromisoformat(item['published']['rfc3339'])
            }
            news_list.append(article)

        return news_list

    # Extension methods

    def get_nodes_list(self):
        dom = self.get_dom()
        return dom.xpath("//div[@class='paging js-module']//div[@class='paging__content js-pgng_cont']/\
        div[@class='newsitem newsitem_height_fixed js-ago-wrapper js-pgng_item']")

    def get_page_link(self, page_number):
        return f'{API_URL}/?q={self.params["q"]}&page={page_number}'

    def get_source_from_node(self, node):
        return node.xpath(".//span[@class='newsitem__param'][1]/text()")[0]

    def get_title_from_node(self, node):
        return node.xpath("./span[@class='cell']/a/@href")[0]

    def get_link_from_node(self, node):
        return node.xpath("./span[@class='cell']/a/span/text()")[0]

    def get_publish_date_from_node(self, node):
        published_at_string = node.xpath(".//div[@class='newsitem__params']/span[@class='newsitem__param js-ago']/@datetime")[0]
        return datetime.fromisoformat(published_at_string) if published_at_string is not None else None
