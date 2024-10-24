import os

from scripts.db.mysqldb import MySQLHandler
from scripts.db.mongodb import MongoDBHandler
import pandas as pd

class Mongodb2Mysql:

    def __init__(self):
        self.db_handler = MySQLHandler(database='caesars_reporting_system')
        self.category_map = {}
        self.factor_map = {}

    # Function to insert categories into MySQL
    def insert_categories(self, data):
        categories = ['Macroeconomics', 'Industry', 'Debt and Financing', 'Operational Performance']
        category_df = pd.DataFrame({'category_name': categories})
        self.db_handler.df_to_sql(category_df, 'altdata_categories', if_exists='replace')

        # Update category_map for later use
        for category in categories:
            category_id = self.get_category_id(category)
            self.category_map[category] = category_id

    # Function to insert factors into MySQL
    def insert_factors(self, data):
        factors_list = []
        for company in data:
            for category, factors in company.items():
                if category in ['Company_Name', '_id']:  # Skip non-factor keys
                    continue
                category_id = self.category_map[category]  # Use the cached category_id
                for factor_name in factors.keys():
                    if factor_name not in self.factor_map:
                        factors_list.append({'factor_name': factor_name, 'category_id': category_id})

        factors_df = pd.DataFrame(factors_list)
        factors_df = factors_df.drop_duplicates()
        self.db_handler.df_to_sql(factors_df, 'altdata_factors', if_exists='append')

        # Update factor_map for later use
        for factor in factors_list:
            factor_id = self.get_factor_id(factor['factor_name'])
            self.factor_map[factor['factor_name']] = factor_id

    # Function to insert company factor importance scores into MySQL
    def insert_company_scores(self, data):
        scores_list = []
        for company in data:
            company_name = company['Company_Name']
            for category, factors in company.items():
                if category in ['Company_Name', '_id']:  # Skip non-factor keys
                    continue
                category_id = self.category_map[category]
                for factor_name, score in factors.items():
                    factor_id = self.factor_map[factor_name]
                    scores_list.append({
                        'company_name': company_name,
                        'category_id': category_id,
                        'factor_id': factor_id,
                        'importance_score': score
                    })
        comp_info = self.db_handler.run_query("SELECT * FROM caesars_reporting_system.company_information;")[['company_id', 'company_name']]
        scores_df = pd.DataFrame(scores_list)
        df_merge = scores_df.merge(comp_info, how='left', on='company_name')[['company_id', 'category_id', 'factor_id', 'importance_score']]
        self.db_handler.df_to_sql(df_merge, 'altdata_company_factor_importance', if_exists='append')

    # Helper function to retrieve category ID from MySQL
    def get_category_id(self, category_name):
        query = f""" SELECT id FROM altdata_categories WHERE category_name = "{category_name}" """
        result = self.db_handler.run_query(query)
        return result['id'].iloc[0] if not result.empty else None

    # Helper function to retrieve factor ID from MySQL
    def get_factor_id(self, factor_name):
        query = f"""SELECT id FROM altdata_factors WHERE factor_name = "{factor_name}" """
        result = self.db_handler.run_query(query)
        return result['id'].iloc[0] if not result.empty else None


    @staticmethod
    def get_nosql_data():

        mongodbhandler = MongoDBHandler()
        db = mongodbhandler.get_database(os.environ['DATABASE'])
        col = db['Company_Importance']
        data = col.find()
        return list(data)



if __name__ == '__main__':

    mysqlhandler = MySQLHandler('caesars_reporting_system')
    mongodb2mysql = Mongodb2Mysql()
    data = mongodb2mysql.get_nosql_data()
    mongodb2mysql.insert_categories(data)
    mongodb2mysql.insert_factors(data)
    mongodb2mysql.insert_company_scores(data)