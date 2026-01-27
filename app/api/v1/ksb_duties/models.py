from peewee import *
from app.database import db
from app.api.v1.duties.models import Duties
from app.api.v1.ksb.models import KSB

class KsbDuties(Model):
    id = UUIDField(primary_key=True)
    ksb_id = ForeignKeyField(KSB, on_delete='Cascade', on_update='Cascade', backref='ksb_duty')
    duty_id = ForeignKeyField(Duties, on_delete='Cascade', on_update='Cascade', backref='ksb_duty')

    class Meta:
        database = db
        table_name="ksb_duties"
        indexes = (
            (('duty_id', 'ksb_id'), True),
        )