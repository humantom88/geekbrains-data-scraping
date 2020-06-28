# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstagramSpider(scrapy.Spider):
    # атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'stepan_scientist'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    usernames_to_parse = ['humantom88', 'slava_popova']  # Пользователь, у которого собираем посты. Можно указать список

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    posts_hash = 'eddbde960fed6bde675388aac39a3657'  # hash для получения данных по постах с главной страницы
    user_followers_hash = 'c76146de99bb02f6415203be841dd25a'
    user_subscriptions_hash = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response: HtmlResponse):  # Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)  # csrf token забираем из html
        yield scrapy.FormRequest(  # заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.login_user,
            formdata={
                'username': self.insta_login,
                'enc_password': self.insta_pwd
            },
            headers={
                'X-CSRFToken': csrf_token
            }
        )

    def login_user(self, response: HtmlResponse):
        j_body = json.loads(response.text)

        if j_body['authenticated']:  # Проверяем ответ после авторизации
            for username in self.usernames_to_parse:
                yield response.follow(
                    # Переходим на желаемую страницу пользователя. Сделать цикл для кол-ва пользователей больше двух
                    f'/{username}',
                    callback=self.parse_userdata,
                    cb_kwargs={'username': username}
                )

    def parse_userdata(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)  # Получаем id пользователя

        variables = {
            "id": user_id,
            "include_reel": True,
            "fetch_mutual": False,
            "first": 50
        }

        # Followers

        user_followers_url = f'{self.graphql_url}query_hash={self.user_followers_hash}&{urlencode(variables)}'
        yield response.follow(
            user_followers_url,
            callback=self.parse_user_info,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': variables,
                'followed_by': True
            }
        )

        # Subscriptions

        user_subscriptions_url = f'{self.graphql_url}query_hash={self.user_subscriptions_hash}&{urlencode(variables)}'
        yield response.follow(
            user_subscriptions_url,
            callback=self.parse_user_info,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': variables
            }
        )

    def parse_user_info(self, response: HtmlResponse, username, user_id, variables, followed_by=False):
        data = json.loads(response.text)

        page_info = data.get('data').get('user').get('edge_followed_by' if followed_by else 'edge_follow')

        if page_info is None:
            return

        page_info = page_info.get('page_info') if page_info is not None else None

        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']

            user_followers_url = f'{self.graphql_url}query_hash={self.user_followers_hash}&{urlencode(variables)}'

            yield response.follow(
                user_followers_url,
                callback=self.parse_user_info,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id,
                    'variables': variables
                }
            )

        users = data.get('data').get('user').get('edge_followed_by' if followed_by else 'edge_follow').get('edges')  # Сами подписчики
        for user in users:  # Перебираем подписчиков, собираем данные
            item = InstaparserItem(
                user_id=user.get('node').get('id'),
                user_name = user.get('node').get('username'),
                full_name = user.get('node').get('full_name'),
                photo = user.get('node').get('profile_pic_url'),
                is_followed_by = user_id if followed_by else None,
                follows = None if followed_by else user_id
            )

            yield item

    # Получаем токен для авторизации

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
