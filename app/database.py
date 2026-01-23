import os
from dotenv import load_dotenv
from playhouse.db_url import connect

load_dotenv()

db = connect(os.environ.get('DB_URL'))