from sqlalchemy import Column, Integer, String
from app.models.base import Base

class TaskType(Base):
    __tablename__ = "task_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)