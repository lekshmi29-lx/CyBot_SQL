from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CyberLaw(Base):
    __tablename__ = "cyber_laws"

    id = Column(Integer, primary_key=True)
    act_name = Column(String)
    section = Column(String)
    title = Column(String)
    description = Column(Text)
    punishment = Column(Text)

class ScamAdvisory(Base):
    __tablename__ = "scam_advisories"

    id = Column(Integer, primary_key=True)
    scam_name = Column(String)
    modus_operandi = Column(Text)
    police_advice = Column(Text)

class ReportingProcedure(Base):
    __tablename__ = "reporting_procedures"

    id = Column(Integer, primary_key=True)
    crime_type = Column(String)
    procedure = Column(Text)
    contact = Column(String)

class CyberCell(Base):
    __tablename__ = "cyber_cells"

    id = Column(Integer, primary_key=True)
    district = Column(String)
    station_name = Column(String)
    phone = Column(String)
    email = Column(String)

class LegalGuidance(Base):
    __tablename__ = "legal_guidance"

    id = Column(Integer, primary_key=True)
    crime_type = Column(String, nullable=False)
    applicable_laws = Column(Text)   # stored as joined string
    punishment = Column(Text)
    jurisdiction = Column(String)
