from peewee import *
from app.database import db

class Users(Model):
    id = UUIDField(primary_key=True)
    username = CharField(unique=True, null=False)
    password = CharField(null=False)
    is_admin = BooleanField(null=False)

    class Meta:
        database = db
        table_name="users"