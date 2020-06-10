import requests
import re
from pprint import pprint
from bs4 import BeautifulSoup
from db import save_vacancies_to_db


main_url = 'http://vologda.hh.ru'
search_url = '/search/vacancy'

params = {
    'clusters': 'true',
    'enable_snippets': 'true',
    'text': 'Javascript',
    'schedule': 'remote',
    'from': 'cluster_schedule',
    'showClusters': 'false'
}

url_address = f'{main_url}{search_url}'

headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

response = requests.get(url_address, params=params, headers=headers)
soup = BeautifulSoup(response.text, features='html.parser')
button = soup.find('a', attrs={'class': 'HH-Pager-Controls-Next'})


def get_site_url(node):
    site_node = node.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'})

    return f"{main_url}{site_node['href']}" if site_node is not None else None


def get_vacancy(node):
    vacancy_node = node.find('a', attrs={'class': 'bloko-link HH-LinkModifier'})

    if vacancy_node is not None:
        return vacancy_node.getText(), vacancy_node['href']

    return None, None


def get_salaries(node):
    salaries_node = node.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})

    if salaries_node is not None:
        salary_text = salaries_node.getText()
        salary_text_without_utf_spaces = salary_text.replace('\xa0', '')
        currency = re.sub(r'[\d\-.\s]', '', salary_text_without_utf_spaces)[-3:]

        prefix = salary_text_without_utf_spaces[0:2]

        if prefix.lower() == 'от':
            amount = re.sub(r'[^\d\s]', '', salary_text_without_utf_spaces[3:].strip())
            amounts = [int(amount), None, currency]
        elif prefix.lower() == 'до':
            amount = re.sub(r'[^\d\s]', '', salary_text_without_utf_spaces[3:].strip())
            amounts = [None, int(amount), currency]
        else:
            amounts_text = re.sub(r'[^\d\-]', '', salary_text_without_utf_spaces)
            amounts = [int(amount) for amount in amounts_text.split('-')]
            amounts.append(currency)

        return amounts

    return [None, None, None]


def get_vacancy_from_node(node):
    if node is None:
        return None

    salaries = get_salaries(node)
    vacancy = get_vacancy(node)

    result = {
        'vacancy_name': vacancy[0],
        'url': vacancy[1],
        'site': get_site_url(node),
        'currency': None,
        'salary_min': None,
        'salary_max': None
    }

    if len(salaries) > 0:
        result['salary_min'] = salaries[0] if len(salaries) > 0 else None
        if len(salaries) == 3:
            result['salary_max'] = salaries[1] if len(salaries) > 0 else None

        result['currency'] = salaries[2]
    else:
        result['salary_max'] = None
        result['currency'] = None

    if result is None or (
        result['vacancy_name'] is None and
        result['url'] is None and
        result['site'] is None and
        result['salary_min'] is None and
        result['currency'] is None and
            result['salary_max'] is None):
        return None

    return result


def get_vacancy_list(vacancy_nodes):
    if vacancy_nodes is None:
        return []

    result = [get_vacancy_from_node(node) for node in vacancy_nodes if node is not None]

    return [vacancy for vacancy in result if vacancy is not None]


def get_dirty_vacancies(soup_node):
    vacancy_tags_list = soup_node.find('div', attrs={'class': 'vacancy-serp'})
    return vacancy_tags_list.children


vacancies = []
while button is not None:
    next_url = button.attrs['href']
    dirty_vacancies_list = get_dirty_vacancies(soup)
    vacancies_list = get_vacancy_list(dirty_vacancies_list)
    vacancies = vacancies + vacancies_list
    response = requests.get(f'{main_url}{next_url}', headers=headers)
    soup = BeautifulSoup(response.text, features='html.parser')
    button = soup.find('a', attrs={'class': 'HH-Pager-Controls-Next'})


save_vacancies_to_db(vacancies)
