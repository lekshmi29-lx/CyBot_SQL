import json
from database.db import SessionLocal
from database.models import ReportingProcedure

db = SessionLocal()

with open("reporting_procedures.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    record = ReportingProcedure(
        crime_type=item["crime_type"],
        procedure=item["procedure"],
        contact=item["contact_detail"]
    )
    db.add(record)

db.commit()
db.close()


