import json
from database.db import SessionLocal
from database.models import CyberLaw

db = SessionLocal()

with open("cyber_laws.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    law = CyberLaw(
        act_name=item["chapter"],
        section=item["section"],
        title=item["section_name"],
        description=item["description"],
        punishment=item["punishment"]
    )
    db.add(law)

db.commit()
db.close()
