from pymongo import MongoClient, errors
from pprint import pprint
import zlib

client = MongoClient('localhost', 27017)
db = client['mails_db']
mails_db = db.mails


def make_hash(item):
    return zlib.adler32(bytes(repr(item), 'utf-8'))


def save_mails_to_db(mails_list):
    for mail in mails_list:
        mail_hash = make_hash(mail)
        mail["_id"] = mail_hash

        try:
            mails_db.insert_one(mail)
        except errors.DuplicateKeyError:
            print("Duplicate found for mail: ", mail)
            pass
