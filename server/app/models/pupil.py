from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Pupil(Base):
    __tablename__ = "pupil"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)