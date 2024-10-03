from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

class MongoDBHandler:

    def __init__(self):
        super().__init__()
        self.DB_URL = os.environ['LOCAL_URL']
        self.client = MongoClient(self.DB_URL)

    def get_database(self, DB=os.environ['DATABASE']):
        """
        :param DB: Your mongodb database, default is local
        """
        db = self.client[DB]
        return db
