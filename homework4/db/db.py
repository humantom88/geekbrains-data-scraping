from pymongo import MongoClient, errors
import zlib

client = MongoClient('localhost', 27017)
db = client['news_db']
news_db = db.news


def make_hash(any_dict):
    return zlib.adler32(bytes(repr(any_dict), 'utf-8'))


def save_news_to_db(news_list):
    for article in news_list:
        article_hash = make_hash(article)
        article["_id"] = article_hash

        try:
            news_db.insert_one(article)
        except errors.DuplicateKeyError:
            print("Duplicate found for article: ", article)
            pass

