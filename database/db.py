from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "postgresql://postgres:lekshmihr%4013@localhost:5432/cybot_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
