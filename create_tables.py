from database import db
from models import Coins

db.connect()
db.create_tables([Coins])
print("Database tables created!")
db.close()