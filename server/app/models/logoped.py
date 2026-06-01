from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Logoped(Base):
    __tablename__ = "logoped"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)