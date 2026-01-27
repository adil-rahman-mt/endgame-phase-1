from app.database import db
from app.ksb_duties.models import KsbDuties

db.connect()
db.create_tables([KsbDuties])
print("Ksb_duties table has been created successfully!")
db.close()