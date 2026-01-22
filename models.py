from peewee import *
from database import db

class Coins(Model):
    id = UUIDField()
    name = CharField()

    class Meta:
        database = db
        table_name="coins"