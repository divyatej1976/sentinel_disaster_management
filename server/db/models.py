from sqlalchemy import Column, Integer, String, Float, DateTime
from server.db.database import Base, engine
import datetime

class AssessmentRecord(Base):
    __tablename__ = "assessment_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    hazard = Column(String, index=True)
    risk_level = Column(String)
    final_probability = Column(Float)
    template = Column(String, nullable=True)
    result_json = Column(String)

# Initialize database
Base.metadata.create_all(bind=engine)
