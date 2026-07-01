from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ARRAY
from datetime import datetime

Base = declarative_base()

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True)
    resume_text = Column(String)
    jd_text = Column(String)
    keyword_score = Column(Float)
    semantic_score = Column(Float)
    missing_skills = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.utcnow)
    role_type = Column(String, default="general")
    