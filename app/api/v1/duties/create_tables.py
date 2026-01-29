from app.database import db
from app.api.v1.duties.models import Duties

db.connect()
db.create_tables([Duties])
print("Duties table has been created successfully!")
db.close()