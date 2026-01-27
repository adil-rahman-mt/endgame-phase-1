from app.database import db
from coin_duties.models import CoinDuties

db.connect()
db.create_tables([CoinDuties])
print("Coin_duties table has been created successfully!")
db.close()