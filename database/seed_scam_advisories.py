import json
from database.db import SessionLocal
from database.models import ScamAdvisory

db = SessionLocal()

with open("scam_advisories.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    record = ScamAdvisory(
        scam_name=item["scam_name"],
        modus_operandi=item["modus_operandi"],
        police_advice=item["police_advice"]
    )
    db.add(record)

db.commit()
db.close()

