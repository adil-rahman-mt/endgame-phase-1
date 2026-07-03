from peewee import *
from app.database import db

class Coins(Model):
    id = UUIDField(primary_key=True)
    name = CharField(unique=True, null=False)
    completed = BooleanField(null=True, constraints=[SQL("DEFAULT FALSE")])

    class Meta:
        database = db
        table_name="coins"