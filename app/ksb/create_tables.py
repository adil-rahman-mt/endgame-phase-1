from app.database import db
from app.ksb.models import KSB

db.connect()
db.create_tables([KSB])
print("KSBs table has been created successfully!")
db.close()