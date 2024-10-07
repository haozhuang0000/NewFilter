from pymongo import MongoClient
import os
import pandas as pd
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

    def insert_db(self, data, col_name, dbs_name='AIDF_NLP_Capstone'):

        if isinstance(data, pd.DataFrame):
            DB = self.get_database(DB=dbs_name)
            collection = DB[col_name]
            collection.insert_many(data.to_dict('records'))
        if isinstance(data, list):
            DB = self.get_database(DB=dbs_name)
            collection = DB[col_name]
            collection.insert_many(data)

if __name__ == '__main__':

    mongodb_handler = MongoDBHandler()
    db = mongodb_handler.get_database()
    col = db[os.environ['NEWS_COLLECTION']]
    print(col)
    top_items = col.find().sort("Storage_date", -1).limit(3)
    print(top_items)
    for item in top_items:
        print(item['Content'])
