from peewee import *
from app.database import db
from app.models.coins import Coins
from app.models.duties import Duties

class CoinDuties(Model):
    id = UUIDField(primary_key=True)
    coin_id = ForeignKeyField(Coins, on_delete='Cascade', on_update='Cascade', backref='coin_duties')
    duty_id = ForeignKeyField(Duties, on_delete='Cascade', on_update='Cascade', backref='coin_duties')

    class Meta:
        database = db
        table_name="coin_duties"
        indexes = (
            (('coin_id', 'duty_id'), True),
        )