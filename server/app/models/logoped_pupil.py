from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import Base

class LogopedPupil(Base):
    __tablename__ = "logoped_pupil"

    logoped_id = Column(Integer, ForeignKey("logoped.id"), primary_key=True)
    pupil_id = Column(Integer, ForeignKey("pupil.id"), primary_key=True)