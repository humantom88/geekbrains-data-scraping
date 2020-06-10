from pymongo import MongoClient, errors
from pprint import pprint
import zlib

client = MongoClient('localhost', 27017)
db = client['vacancies_db']
vacancies_db = db.vacancies


def make_hash(object):
    return zlib.adler32(bytes(repr(object), 'utf-8'))


def save_vacancies_to_db(vacancies_list):
    for vacancy in vacancies_list:
        vacancy_hash = make_hash(vacancy)
        vacancy["_id"] = vacancy_hash

        try:
            vacancies_db.insert_one(vacancy)
        except errors.DuplicateKeyError:
            print("Duplicate found for vacancy: ", vacancy)
            pass


def print_vacancies_with_salary_higher_than(salary):
    for vacancy in vacancies_db.find({'salary_min': {'$gt': salary}}):
        pprint(vacancy)


print_vacancies_with_salary_higher_than(200000)