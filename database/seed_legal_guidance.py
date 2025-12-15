import json
from database.db import SessionLocal
from database.models import LegalGuidance

db = SessionLocal()

with open("legal_guidance.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    applicable_laws_text = " | ".join(item.get("applicable_laws", []))

    record = LegalGuidance(
        crime_type=item["crime_type"],
        applicable_laws=applicable_laws_text,
        punishment=item.get("punishment"),
        jurisdiction=item.get("jurisdiction")
    )
    db.add(record)

db.commit()
db.close()


