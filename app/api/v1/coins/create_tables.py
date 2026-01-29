from app.database import db
from app.api.v1.coins.models import Coins

db.connect()
db.create_tables([Coins])
print("Coins table has been created successfully!")
db.close()