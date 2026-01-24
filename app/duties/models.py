from peewee import *
from app.database import db

class Duties(Model):
    id = UUIDField(primary_key=True)
    name = CharField(unique=True, null=False)
    description = CharField(unique=True, null=False)

    class Meta:
        database = db
        table_name="duties"