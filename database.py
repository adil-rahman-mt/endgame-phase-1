from peewee import PostgresqlDatabase
import os
from dotenv import load_dotenv

load_dotenv()

db = PostgresqlDatabase(os.getenv('DB_NAME'),
                           host=os.getenv('DB_HOST'),
                           user=os.getenv('DB_USERNAME'),
                           password=os.getenv('DB_PASSWORD'),
                           port=25060,
                           autoconnect=False)