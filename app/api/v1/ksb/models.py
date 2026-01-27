from peewee import *
from app.database import db

class KSB(Model):
    id = UUIDField(primary_key=True)
    type = CharField(
            constraints=[
                Check("type IN ('Knowledge', 'Skill', 'Behaviour')")
            ]
        )
    name = CharField(unique=True, null=False)
    description = CharField(unique=True, null=False)

    class Meta:
        database = db
        table_name="ksbs"