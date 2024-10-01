from pymongo import MongoClient
import os
import json
from scripts.logger.logger import Log
import uuid
import bson
from bson.binary import Binary, UuidRepresentation
import pandas as pd
import warnings
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

class MongoDBHandler:

    def __init__(self):
        super().__init__()
        self.DB_URL = os.environ['MONGODB_URL']
        self.client = MongoClient(self.DB_URL)

    def get_database(self, DB=os.environ['DATABASE']):
        """
        :param DB: Your mongodb database, default is local
        """
        db = self.client[DB]
        return db

if __name__ == '__main__':

    mongodb_handler = MongoDBHandler()
    db = mongodb_handler.get_database()
    col = db[os.environ['NEWS_COLLECTION']]
    test_data = col.aggregate([{'$sample': {'size': 100}}])
    test_data_list = list(test_data)
