from peewee import *
from database import db

class Coins(Model):
    id = UUIDField(primary_key=True)
    name = CharField(unique=True, null=False)

    class Meta:
        database = db
        table_name="coins"