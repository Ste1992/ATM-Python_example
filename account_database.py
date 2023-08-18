import pymongo
from pymongo import MongoClient


class LoginDatabase:

    def __init__(self):
        self.client = None
        self.user_collection = None

    def init_db(self):
        self.client = MongoClient('mongodb://localhost:27017')
        db = self.client.bank
        self.user_collection = db.users

    def close_db(self):
        self.user_collection.close()
