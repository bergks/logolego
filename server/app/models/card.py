from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Card(Base):
    __tablename__ = "card"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(Integer, ForeignKey("task_types.id"), nullable=False)
    content_id = Column(Integer, nullable=False)  # без FK, полиморфная связь

    type = relationship("TaskType", lazy="joined")