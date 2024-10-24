import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(override=True)
class MySQLHandler:

    def __init__(self, database, driver='mysql'):
        self.username = os.environ['BACKEND_MYSQL_USER']
        self.password = os.environ['BACKEND_MYSQL_SECRET_KEY']
        self.host = os.environ['BACKEND_MYSQL_HOST']
        self.port = os.environ['BACKEND_MYSQL_PORT']
        self.database = database
        db_url = f'{driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
        self.engine = create_engine(db_url, echo=False)

    def df_to_sql(self, df, table_name, if_exists='replace'):
        """Writes a pandas DataFrame to a MySQL table."""
        try:
            if not self.table_exists(table_name):
                df.to_sql(table_name, con=self.engine, if_exists=if_exists, index=False)
                print(f"DataFrame written to {table_name} table successfully")
            else:
                print(f"Table {table_name} already exists. Skipping DataFrame insertion.")
        except SQLAlchemyError as e:
            print(f"Error writing DataFrame to SQL: {e}")

    def table_exists(self, table_name):
        """Check if a table exists in the database."""
        query = text(f"""
        SELECT COUNT(*)
        FROM {self.database}.{table_name}
        """)
        with self.engine.connect() as connection:
            result = connection.execute(query).scalar()
        return result > 0

    # Method to run raw SQL queries
    def run_query(self, query):
        return pd.read_sql(query, self.engine)