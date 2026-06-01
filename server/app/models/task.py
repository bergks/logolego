from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(Integer, ForeignKey("task_types.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    type = relationship("TaskType", lazy="joined")