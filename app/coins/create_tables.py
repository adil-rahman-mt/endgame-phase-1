from app.database import db
from app.coins.models import Coins

db.connect()
db.create_tables([Coins])
print("Coins table has been created successfully!")
db.close()