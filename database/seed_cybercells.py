import json
from database.db import SessionLocal
from database.models import CyberCell

db = SessionLocal()

with open("cybercells.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    record = CyberCell(
        district=item["district"],
        station_name=item["station_name"],
        phone=item["phone_number"],
        email=item["email"]
    )
    db.add(record)

db.commit()
db.close()


