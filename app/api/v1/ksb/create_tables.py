from app.database import db
from app.api.v1.ksb.models import KSB

db.connect()
db.create_tables([KSB])
print("KSB table has been created successfully!")
db.close()