from app.database import db
from app.models import Coins, Duties, KSB, CoinDuties, KsbDuties, Users

def create_tables():
    db.connect()
    db.create_tables([Coins, Duties, KSB, CoinDuties, KsbDuties, Users])
    db.close()

if __name__ == "__main__":
    create_tables()
