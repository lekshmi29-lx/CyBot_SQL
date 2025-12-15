from database.db import engine
from database.models import Base

if __name__ == "__main__":
    print("Creating tables in PostgreSQL...")
    Base.metadata.create_all(engine)
    print("✅ Tables created successfully")
