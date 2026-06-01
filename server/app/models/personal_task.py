from sqlalchemy import Column, Integer, String
from app.models.base import Base

class PersonalTaskCard(Base):
    __tablename__ = "personal_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    media = Column(String, nullable=False)
    description = Column(String, nullable=True)
    answer_type = Column(Integer, nullable=False)